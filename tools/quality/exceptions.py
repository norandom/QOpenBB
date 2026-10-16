"""Apply exact, reviewed size baselines without hiding additional growth."""

import json
import re
from datetime import date
from pathlib import Path, PurePosixPath


FIELDS = {"repository", "path", "metric", "baseline", "revision", "rationale", "review", "expires_on"}


def exact_path(value) -> bool:
    return (isinstance(value, str) and bool(value) and not PurePosixPath(value).is_absolute()
            and not any(symbol in value for symbol in "\\:*?[]")
            and all(part not in {"", ".", ".."} for part in value.split("/")))


def identity(entry: dict) -> tuple:
    function = entry.get("function", entry)
    return (entry["repository"], entry["path"], entry["metric"],
            *(function.get(key) for key in ("name", "line", "column")))


def validate_entry(entry, scope: dict, limits: dict) -> None:
    if not isinstance(entry, dict):
        raise ValueError("exception must be an object")
    expected = FIELDS | ({"function"} if entry.get("metric") == "function" else set())
    if set(entry) != expected or entry["metric"] not in limits:
        raise ValueError("exception fields or metric are invalid")
    if not exact_path(entry["path"]):
        raise ValueError("exception requires an exact repository-relative path")
    revision = entry["revision"]
    if (not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{40}", revision)
            or scope.get(entry["repository"]) != revision):
        raise ValueError("exception revision must match the measured fork head")
    if type(entry["baseline"]) is not int or entry["baseline"] <= limits[entry["metric"]]:
        raise ValueError("exception baseline must be an integer above the applicable cap")
    for key in ("rationale", "review"):
        if not isinstance(entry[key], str) or not entry[key].strip():
            raise ValueError(f"exception requires a {key}")
    if not isinstance(entry["expires_on"], str) or date.fromisoformat(entry["expires_on"]) < date.today():
        raise ValueError("exception expiry must be a current ISO date")
    if entry["metric"] == "function":
        function = entry["function"]
        if (not isinstance(function, dict) or set(function) != {"name", "line", "column"}
                or not isinstance(function["name"], str) or not function["name"]
                or any(type(function[key]) is not int or function[key] < 1 for key in ("line", "column"))):
            raise ValueError("function exception requires an exact name and one-based position")


def apply_exceptions(root: Path, report: dict) -> None:
    report["exceptions"] = []
    config = json.loads((root / ".kiro/complexity-budgets.json").read_text(encoding="utf-8-sig"))
    entries = config.get("exceptions", [])
    if not isinstance(entries, list):
        raise ValueError("exceptions must be an array")
    scope = {item["repository"]: item.get("head") for item in report["scope"]}
    reviewed = {}
    for entry in entries:
        validate_entry(entry, scope, report["limits"])
        key = identity(entry)
        if key in reviewed:
            raise ValueError("duplicate exception target")
        reviewed[key] = entry
    remaining = []
    for violation in report["violations"]:
        exception = reviewed.get(identity(violation))
        if exception and violation["actual"] <= exception["baseline"]:
            report["exceptions"].append({**violation, **exception})
        else:
            remaining.append(violation)
    report["violations"] = remaining
