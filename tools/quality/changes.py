"""Explicit changed-file manifests and verified Git snapshot inputs."""

import re
import subprocess
from pathlib import Path, PurePosixPath


def safe_path(root: Path, name: str) -> Path:
    if not isinstance(name, str) or not name or "\\" in name or ":" in name:
        raise ValueError(f"unsafe repository path: {name!r}")
    path = PurePosixPath(name)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in name.split("/")):
        raise ValueError(f"unsafe repository path: {name!r}")
    resolved = (root / name).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError(f"repository path escapes root: {name}")
    return resolved


def validate_manifest(value: dict, repo: dict, root: Path) -> list[dict]:
    if not isinstance(value, dict) or value.get("repository") != repo["repository"]:
        raise ValueError("changed-file repository identity does not match inventory")
    for key in ("base", "head"):
        if not isinstance(value.get(key), str) or not re.fullmatch(r"[0-9a-f]{40}", value[key]):
            raise ValueError(f"explicit full {key} revision required")
    if value["base"] != repo["revision"]:
        raise ValueError("changed-file base does not match inventory revision")
    if not isinstance(value.get("changes"), list):
        raise ValueError("explicit changes array required (empty is valid)")
    seen = set()
    for entry in value["changes"]:
        if not isinstance(entry, dict) or entry.get("status") not in {"A", "M", "D", "R", "C", "T"}:
            raise ValueError("unsupported changed-file status")
        name = entry.get("path")
        safe_path(root, name)
        if name in seen:
            raise ValueError(f"duplicate/conflicting changed path: {name}")
        seen.add(name)
        if entry["status"] in {"R", "C"}:
            safe_path(root, entry.get("old_path"))
            if entry["old_path"] == name:
                raise ValueError(f"rename/copy source equals destination: {name}")
    return value["changes"]


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True,
                            text=True, encoding="utf-8", errors="strict", check=False)
    if result.returncode:
        raise ValueError(f"Git scope validation failed: {result.stderr.strip()}")
    return result.stdout


def parse_diff(raw: str) -> list[dict]:
    fields = raw.rstrip("\0").split("\0") if raw else []
    changes = []
    position = 0
    while position < len(fields):
        status = fields[position][0]
        if status in {"R", "C"}:
            changes.append({"status": status, "old_path": fields[position + 1],
                            "path": fields[position + 2]})
            position += 3
        else:
            changes.append({"status": status, "path": fields[position + 1]})
            position += 2
    return changes


def git_manifest(root: Path, repo: dict, base: str, head: str) -> dict:
    # A clean worktree makes the measured bytes attributable to the declared head.
    if git(root, "remote", "get-url", "origin").strip() != repo["repository"]:
        raise ValueError("Git origin does not match inventory repository")
    if git(root, "rev-parse", "--show-toplevel").strip() != str(root.resolve()):
        raise ValueError("Git root does not match fork root")
    for revision in (base, head):
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            raise ValueError("explicit full base/head revisions required")
        if git(root, "rev-parse", "--verify", f"{revision}^{{commit}}").strip() != revision:
            raise ValueError("Git revision does not resolve to the declared commit")
    if git(root, "rev-parse", "HEAD").strip() != head:
        raise ValueError("Git HEAD differs from declared head")
    if git(root, "status", "--porcelain", "--untracked-files=all"):
        raise ValueError("Git scope requires a clean worktree; use an explicit manifest for working changes")
    return {"repository": repo["repository"], "base": base, "head": head,
            "changes": parse_diff(git(root, "diff", "--name-status", "-z", "-M", base, head, "--"))}
