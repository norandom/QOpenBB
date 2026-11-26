"""Select financial-modeling verification from two committed repository trees."""

import subprocess
from pathlib import Path

from .financial_compat_inputs import decode
from .financial_impact_documents import CONTRACT_DOCUMENTS, identities
from .financial_impact_manifest import MAP_PATH, Mapping, load_mapping, matches

_FALLBACK = (
    "tests/factors",
    "tests/contracts/test_modeling_adoption.py",
    "tests/contracts/test_modeling_impact_map.py",
    "tests/contracts/test_modeling_impact_gate.py",
    "tests/contracts/test_modeling_impact_run.py",
    "tests/contracts/test_financial_compat_gate.py",
    "tests/contracts/test_financial_compat_structure.py",
    "tests/delivery/test_data_image.py",
    "tests/delivery/test_prototype_compose.py",
)
_RELEVANT = (
    ".kiro/modeling-impact.toml",
    "contracts/modeling/**",
    "contracts/consumers/financial-modeling/**",
    "services/data-api/qopenbb_data/modeling/**",
    "pipeline/qopenbb_ci/financial_impact*.py",
    "pipeline/qopenbb_ci/modeling_*.py",
    "pipeline/qopenbb_ci/financial_compat*.py",
    "tests/factors/**",
    "tests/contracts/test_modeling_*.py",
    "tests/contracts/test_financial_compat*.py",
)


class Trees:
    def __init__(self, root: Path, base: str, head: str):
        self.root = root
        self.base = self.revision(base)
        self.head = self.revision(head)
        self.paths = self.list_paths(self.head)

    def git(self, *args: str) -> str:
        return subprocess.run(
            ["git", "--no-replace-objects", "-C", str(self.root), *args],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout.decode("utf-8", errors="surrogateescape")

    def revision(self, ref: str) -> str:
        if not ref:
            raise ValueError("empty Git revision")
        return self.git(
            "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}"
        ).strip()

    def list_paths(self, revision: str) -> set[str]:
        return set(
            self.git("ls-tree", "-r", "--name-only", "-z", revision).split("\0")
        ) - {""}

    def read(self, revision: str, path: str) -> str:
        return self.git("cat-file", "blob", f"{revision}:{path}")

    def changed_paths(self) -> set[str]:
        return set(
            self.git(
                "diff",
                "--name-only",
                "--no-renames",
                "--no-ext-diff",
                "-z",
                self.base,
                self.head,
                "--",
            ).split("\0")
        ) - {""}


def _document_changes(
    trees: Trees, paths: set[str], base_paths: set[str], gaps: set[str]
) -> tuple[set[str], set[str]]:
    changed = set()
    current = set()
    for path in sorted((paths | trees.paths) & CONTRACT_DOCUMENTS):
        try:
            before = (
                identities(path, decode(trees.read(trees.base, path).encode("utf-8")))
                if path in paths and path in base_paths
                else {}
            )
            after = (
                identities(path, decode(trees.read(trees.head, path).encode("utf-8")))
                if path in trees.paths
                else {}
            )
        except (KeyError, TypeError, ValueError, AttributeError):
            gaps.add(f"invalid contract identity document: {path}")
            continue
        current.update(after)
        if path in paths:
            changed.update(
                key
                for key in before.keys() | after.keys()
                if before.get(key) != after.get(key)
            )
    return changed, current


def _preserve_ownership(
    trees: Trees, mapping: list[Mapping], base_paths: set[str], gaps: set[str]
) -> None:
    if MAP_PATH not in base_paths:
        return
    base = load_mapping(base_paths, lambda path: trees.read(trees.base, path))
    for row in base:
        for identity in row.ids:
            if not any(candidate.preserves(identity, row) for candidate in mapping):
                gaps.add(f"removed mapping obligation: {identity}")


def _record(affected: dict, row: Mapping, row_ids: set[str]) -> None:
    for identity in row_ids:
        entry = affected.setdefault(
            identity, {"criteria": set(), "selectors": set(), "paths": set()}
        )
        entry["criteria"].update(row.criteria)
        entry["selectors"].update(row.selectors)
        entry["paths"].update(row.paths)


def _select(trees: Trees) -> dict:
    mapping = load_mapping(trees.paths, lambda path: trees.read(trees.head, path))
    paths = trees.changed_paths()
    gaps = set()
    affected_mappings: dict = {}
    base_paths = trees.list_paths(trees.base)
    if MAP_PATH in paths:
        _preserve_ownership(trees, mapping, base_paths, gaps)
    semantic_ids, current_ids = _document_changes(trees, paths, base_paths, gaps)
    changed_ids = set(semantic_ids)
    criteria: set[str] = set()
    selectors: set[str] = set()
    covered_paths = {MAP_PATH}
    mapped_ids = set()
    for row in mapping:
        test_paths = {selector.partition("::")[0] for selector in row.selectors}
        affected = {
            path for path in paths if path in test_paths or matches(path, row.paths)
        }
        covered_paths.update(affected)
        mapped_ids.update(row.ids)
        if affected or semantic_ids.intersection(row.ids) or MAP_PATH in paths:
            ids = (
                set(row.ids)
                if affected or MAP_PATH in paths
                else semantic_ids.intersection(row.ids)
            )
            _record(affected_mappings, row, ids)
            criteria.update(row.criteria)
            selectors.update(row.selectors)
        if affected - CONTRACT_DOCUMENTS:
            changed_ids.update(row.ids)
    gaps.update(
        f"unmapped contract identity: {identity}"
        for identity in (semantic_ids | current_ids) - mapped_ids
    )
    gaps.update(
        f"unmapped path: {path}"
        for path in paths - covered_paths
        if matches(path, _RELEVANT)
    )
    return _report(changed_ids, criteria, selectors, gaps, affected_mappings)


def _report(
    changed_ids: set[str],
    criteria: set[str],
    selectors: set[str],
    gaps: set[str],
    affected: dict,
) -> dict:
    return {
        "changed_ids": sorted(changed_ids),
        "criteria": sorted(criteria),
        "selectors": sorted(selectors.union(_FALLBACK) if gaps else selectors),
        "gaps": sorted(gaps),
        "affected_mappings": {
            identity: {key: sorted(values) for key, values in entry.items()}
            for identity, entry in sorted(affected.items())
        },
    }


def select(base: str, head: str, root: Path) -> dict:
    """Return change, verification and per-identity ownership. Gaps block acceptance."""
    try:
        return _select(Trees(root, base, head))
    except (OSError, subprocess.CalledProcessError):
        gap = "Git impact inputs unavailable"
    except ValueError as exc:
        gap = str(exc)
    return _report(set(), set(), set(), {gap}, {})
