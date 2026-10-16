"""Ownership inventory and exclusions, independent of language measurements."""

import fnmatch
import json
import os
from pathlib import Path

from .changes import git_manifest, safe_path, validate_manifest


def matches(name: str, pattern: str) -> bool:
    return fnmatch.fnmatchcase(name, pattern) or (
        pattern.startswith("**/") and fnmatch.fnmatchcase(name, pattern[3:]))


def exclusion(repo: dict, name: str) -> dict | None:
    for item in repo["exclusions"]:
        if any(matches(name, pattern) for pattern in item["patterns"]):
            if not item.get("reason") or not item.get("source"):
                raise ValueError("exclusions require reason and source/generator")
            return item
    return None


def discover(root: Path, repo: dict) -> set[str]:
    def traversal_error(error: OSError) -> None:
        raise error

    found = set()
    for directory, dirs, files in os.walk(root, followlinks=False, onerror=traversal_error):
        relative = Path(directory).relative_to(root)
        dirs[:] = [name for name in sorted(dirs)
                   if not exclusion(repo, (relative / name).as_posix() + "/")]
        found.update((relative / name).as_posix() for name in files)
        for name in dirs:
            if (Path(directory) / name).is_symlink():
                raise ValueError(f"symlink directory requires explicit exclusion: {relative / name}")
    return found


def validate_config(config: dict, source_lock: dict) -> None:
    if config.get("metric") != "project-syntax-units-v1" or config.get("schema_version") != 1:
        raise ValueError("unsupported inventory schema or metric")
    if config.get("limits") != {"physical": 400, "logical": 300, "function": 50}:
        raise ValueError("inventory must enforce the approved 400/300/50 limits")
    ids = set()
    for repo in config["repositories"]:
        if repo["id"] in ids or repo["mode"] not in {"all", "changed"}:
            raise ValueError("duplicate repository identity or unsupported inventory mode")
        ids.add(repo["id"])
        if repo.get("source_lock_key"):
            locked = source_lock.get(repo["source_lock_key"], {})
            if any(repo.get(key) != locked.get(key) for key in ("repository", "revision")):
                raise ValueError(f"{repo['id']}: inventory differs from source lock")
        for item in repo["exclusions"]:
            if not item.get("reason") or not item.get("source") or not item.get("patterns"):
                raise ValueError("exclusions require patterns, reason and source/generator")


def owned(repo: dict, name: str) -> str:
    candidates = [owner for owner in repo["owners"]
                  if any(matches(name, pattern) for pattern in owner["include"])]
    mapped = [owner for owner in candidates if name in owner["files"]]
    if len(mapped) != 1:
        raise ValueError(f"{name}: unmapped or ambiguous production file; ownership review required")
    return mapped[0]["spec"]


def repository_scope(root: Path, repo: dict, manifest: dict | None,
                     revisions: tuple | None) -> tuple[dict, list[dict]]:
    if not root.is_dir():
        raise ValueError("repository root is missing or is not a directory")
    if repo["mode"] == "all":
        entries = [{"status": "M", "path": name} for name in sorted(discover(root, repo))]
        evidence = {"repository": repo["id"], "provenance": "maintained-tree"}
    else:
        if manifest is not None and revisions is not None:
            raise ValueError("choose a manifest or base/head, not both")
        if manifest is None and revisions is None:
            raise ValueError("explicit changed-file manifest or base/head required")
        supplied = manifest if manifest is not None else git_manifest(root, repo, *revisions)
        entries = validate_manifest(supplied, repo, root)
        evidence = {"repository": repo["id"], "base": supplied["base"], "head": supplied["head"],
                    "provenance": "manifest-declared" if manifest is not None else "git-verified"}
    return evidence, entries


def collect_repository(root: Path, repo: dict, entries: list[dict], report: dict) -> None:
    deleted = {entry["path"] for entry in entries if entry["status"] == "D"}
    renamed = {entry["old_path"] for entry in entries if entry["status"] == "R"}
    for owner in repo["owners"]:
        for name in owner["files"]:
            path = safe_path(root, name)
            if name not in deleted | renamed and not path.is_file():
                report["errors"].append(f"{repo['id']}:{name}: mapped file missing")
    for entry in entries:
        name = entry["path"]
        path = safe_path(root, name)
        if entry["status"] == "D":
            if path.exists():
                raise ValueError(f"deleted path still exists: {name}")
            report["deleted"].append({"repository": repo["id"], "path": name})
            continue
        excluded = exclusion(repo, name)
        if excluded:
            report["excluded"].append({"repository": repo["id"], "path": name, **excluded})
            continue
        try:
            owner = owned(repo, name)
        except ValueError as error:
            report["errors"].append(f"{repo['id']}:{error}")
            owner = None
        if not path.is_file():
            report["errors"].append(f"{repo['id']}:{name}: changed file missing")
            continue
        report["pending"].append({"repository": repo["id"], "path": name,
                                  "owner": owner, "absolute": path})


def collect(root: Path, changes: dict, repository_roots: dict, revisions: dict) -> dict:
    config = json.loads((root / ".kiro/complexity-budgets.json").read_text(encoding="utf-8-sig"))
    source_lock = root / "sources.lock.json"
    locked = json.loads(source_lock.read_text(encoding="utf-8")) if source_lock.exists() else {}
    validate_config(config, locked)
    report = {"limits": config["limits"], "scope": [], "exclusions": [], "excluded": [],
              "deleted": [], "pending": [], "errors": []}
    ids = {repo["id"] for repo in config["repositories"]}
    if (changes.keys() | repository_roots.keys() | revisions.keys()) - ids:
        raise ValueError("scope input names a repository outside inventory")
    for repo in config["repositories"]:
        location = Path(repository_roots.get(repo["id"], root / repo["root"])).resolve()
        report["exclusions"].extend({"repository": repo["id"], **item} for item in repo["exclusions"])
        try:
            evidence, entries = repository_scope(location, repo, changes.get(repo["id"]),
                                                 revisions.get(repo["id"]))
            report["scope"].append(evidence)
            collect_repository(location, repo, entries, report)
        except (ValueError, OSError, IndexError) as error:
            report["errors"].append(f"{repo['id']}: {error}")
    return report
