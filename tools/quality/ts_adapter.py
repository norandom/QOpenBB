"""Pinned TypeScript subprocess boundary for project-syntax-units-v1."""

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXTENSIONS = {".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".mts", ".cts"}


def execute(arguments: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(arguments, cwd=ROOT, capture_output=True, text=True,
                          encoding="utf-8", check=False, timeout=60,
                          creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                          **kwargs)


def runtime() -> tuple[str, dict]:
    tools = json.loads((ROOT / "pipeline/tools.lock.json").read_text(encoding="utf-8"))
    expected_node = tools["tools"]["node"]["version"]
    probe = execute(["node", "--version"])
    if probe.returncode or probe.stdout.strip() != f"v{expected_node}":
        raise ValueError(f"TypeScript parser requires pinned Node {expected_node} on PATH")
    project = ROOT / "verification"
    expected_ts = json.loads((project / "package.json").read_text())["devDependencies"]["typescript"]
    actual_ts = json.loads((project / "node_modules/typescript/package.json").read_text())["version"]
    if actual_ts != expected_ts:
        raise ValueError(f"TypeScript parser requires pinned typescript {expected_ts}")
    return "node", {"node": expected_node, "typescript": actual_ts}


def integer(value, minimum: int = 0) -> bool:
    return type(value) is int and value >= minimum


def validate_records(rows, paths: list[str]) -> dict:
    if not isinstance(rows, list) or len(paths) != len(set(paths)):
        raise ValueError("TypeScript parser requires unique input paths and a JSON result array")
    found = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"path", "logical", "functions"}:
            raise ValueError("TypeScript parser record fields are invalid")
        name = row["path"]
        if not isinstance(name, str) or name not in paths or name in found:
            raise ValueError("TypeScript parser returned an unexpected or duplicate path")
        if not integer(row["logical"]) or not isinstance(row["functions"], list):
            raise ValueError("TypeScript parser logical count or functions array is invalid")
        for function in row["functions"]:
            if not isinstance(function, dict) or set(function) != {"name", "line", "column", "logical"}:
                raise ValueError("TypeScript parser function fields are invalid")
            if (not isinstance(function["name"], str) or not function["name"]
                    or not integer(function["logical"]) or not integer(function["line"], 1)
                    or not integer(function["column"], 1)):
                raise ValueError("TypeScript parser function name, count or position is invalid")
        found[name] = row
    if set(found) != set(paths):
        raise ValueError("TypeScript parser response does not match requested paths")
    return found


def measure_typescript(paths: list[str]) -> tuple[dict, dict]:
    try:
        node, versions = runtime()
        result = execute([node, str(ROOT / "tools/quality/syntax_units.ts")], input=json.dumps(paths))
        if result.returncode:
            raise ValueError(f"TypeScript parser failed (exit {result.returncode}): {result.stderr.strip()}")
        return validate_records(json.loads(result.stdout), paths), versions
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as error:
        raise ValueError(f"TypeScript parser unavailable or invalid response: {error}") from error
