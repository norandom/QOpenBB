"""Measure every maintained fork file at its verified locked source identity."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from qopenbb_ci.sources import identity
from tools.quality.changes import safe_path


def manifest(root: Path, repo: dict, lock: dict) -> dict:
    entry = lock[repo["source_lock_key"]]
    if repo["revision"] != entry["revision"] or repo["repository"] != entry["repository"]:
        raise ValueError("inventory source identity differs from lock")
    checkout = root / repo["root"]
    identity(checkout, entry)
    names = set()
    for owner in repo["owners"]:
        for name in owner["files"]:
            if not isinstance(name, str) or any(char in name for char in "*?[]"):
                raise ValueError("maintained files must be literal paths")
            path = safe_path(checkout, name)
            if not path.is_file():
                raise ValueError("maintained fork file is missing: " + name)
            names.add(name)
    if not names:
        raise ValueError("maintained fork file scope must not be empty")
    return {"repository": entry["repository"], "base": entry["revision"],
            "head": entry["revision"],
            "changes": [{"status": "M", "path": name} for name in sorted(names)]}


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--inventory", type=Path, default=Path(".kiro/complexity-budgets.json"))
    result.add_argument("--lock", type=Path, default=Path("sources.lock.json"))
    result.add_argument("--output", type=Path, default=Path("artifacts/quality.json"))
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        inventory = args.inventory.resolve()
        root = inventory.parent.parent
        # The existing checker resolves these two inputs from its root argument.
        if (inventory != root / ".kiro/complexity-budgets.json"
                or args.lock.resolve() != root / "sources.lock.json"):
            raise ValueError("checker requires canonical inventory and lock paths under one root")
        config = json.loads(inventory.read_text(encoding="utf-8-sig"))
        lock = json.loads(args.lock.read_text(encoding="utf-8"))
        repos = {repo["id"]: repo for repo in config["repositories"]}
        scopes = {name: manifest(root, repos[name], lock) for name in ("workspace", "data_api")}
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="qopenbb-quality-") as directory:
            command = [sys.executable, "-m", "tools.quality.complexity", "--check",
                       "--root", str(root), "--output", str(args.output)]
            for name, scope in scopes.items():
                path = Path(directory) / (name + ".json")
                path.write_text(json.dumps(scope) + "\n", encoding="utf-8")
                command += ["--changes", name + "=" + str(path)]
            return subprocess.run(command, check=False).returncode
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print(json.dumps({"valid": False, "error": type(error).__name__,
                          "detail": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
