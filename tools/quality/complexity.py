"""Inventory maintained files and enforce physical/Python/JavaScript/TypeScript size budgets.

Run from the repository root with ``python -m tools.quality.complexity``.
Use --python-only for an explicitly partial language report.
"""

import argparse
import json
import platform
import tokenize
from pathlib import Path

from .python_units import measure_python
from .scope import collect
from .exceptions import apply_exceptions
from .ts_adapter import EXTENSIONS, measure_typescript


ROOT = Path(__file__).resolve().parents[2]


def physical_lines(source: str) -> int:
    normalized = source.replace("\r\n", "\n").replace("\r", "\n")
    return normalized.count("\n") + int(bool(normalized) and not normalized.endswith("\n"))


def violations(item: dict, limits: dict) -> list[dict]:
    found = []
    identity = {key: item[key] for key in ("repository", "path") if key in item}
    for metric in ("physical", "logical"):
        if item.get(metric, 0) > limits[metric]:
            found.append({**identity, "metric": metric, "actual": item[metric],
                          "limit": limits[metric]})
    for function in item["functions"]:
        if function["logical"] > limits["function"]:
            found.append({**identity, **function, "metric": "function",
                          "actual": function["logical"], "limit": limits["function"]})
    return found


def measure_file(item: dict) -> dict:
    path = item["absolute"]
    if path.suffix == ".py":
        with tokenize.open(path) as stream:
            source = stream.read()
    else:
        source = path.read_text(encoding="utf-8-sig")
    measured = {key: value for key, value in item.items() if key != "absolute"}
    measured.update(physical=physical_lines(source), functions=[])
    if path.suffix == ".py":
        measured.update(measure_python(source, item["path"]))
    return measured


def inventory(root: Path = ROOT, *, changes: dict | None = None,
              repository_roots: dict | None = None, revisions: dict | None = None,
              python_only: bool = False) -> dict:
    report = {"metric": "project-syntax-units-v1", "files": [], "errors": [],
              "violations": [], "coverage": {"physical": "all maintained text files",
              "logical": ["python"], "mode": "python-only",
              "parser": f"CPython ast {platform.python_version()}",
              "combined_acceptance": "unverified; partial language scope"}}
    try:
        report.update(collect(root.resolve(), changes or {}, repository_roots or {}, revisions or {}))
        pending = report.pop("pending")
        for item in pending:
            try:
                report["files"].append(measure_file(item))
            except SyntaxError as error:
                report["errors"].append(f"{item['repository']}:{item['path']}:{error.lineno}: syntax: {error.msg}")
            except (OSError, UnicodeError, LookupError, ValueError) as error:
                report["errors"].append(f"{item['repository']}:{item['path']}: {error}")
        if not python_only:
            combine_languages(pending, report)
        report["violations"] = [entry for item in report["files"]
                                for entry in violations(item, report["limits"])]
        apply_exceptions(root, report)
    except (OSError, ValueError, KeyError, TypeError) as error:
        report["errors"].append(str(error))
    if not python_only:
        report["coverage"]["combined_acceptance"] = (
            "unverified" if report["errors"] else "failed" if report["violations"] else "passed")
    return report


def combine_languages(pending: list[dict], report: dict) -> None:
    selected = {(item["repository"], item["path"]): str(item["absolute"])
                for item in pending if item["absolute"].suffix in EXTENSIONS}
    report["coverage"].update(mode="combined", logical=["python", "javascript", "typescript"])
    try:
        measurements, versions = measure_typescript(list(selected.values()))
        report["coverage"]["parsers"] = {"python": platform.python_version(), **versions}
        for item in report["files"]:
            path = selected.get((item["repository"], item["path"]))
            if path is not None:
                item.update({key: measurements[path][key] for key in ("logical", "functions")})
    except ValueError as error:
        report["errors"].append(str(error))


def assignments(values: list[str]) -> dict:
    result = {}
    for value in values:
        key, separator, item = value.partition("=")
        if not separator or not key or not item or key in result:
            raise ValueError("scope arguments require unique repository=value assignments")
        result[key] = item
    return result


def arguments() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--changes", action="append", default=[], metavar="REPOSITORY=MANIFEST")
    parser.add_argument("--repository-root", action="append", default=[], metavar="REPOSITORY=PATH")
    parser.add_argument("--base", action="append", default=[], metavar="REPOSITORY=SHA")
    parser.add_argument("--head", action="append", default=[], metavar="REPOSITORY=SHA")
    parser.add_argument("--python-only", action="store_true", help="explicit partial language scope")
    parser.add_argument("--check", action="store_true", help="exit 1 for exceeded caps (scope errors always exit 2)")
    parser.add_argument("--output", type=Path)
    return parser


def main() -> int:
    parser = arguments()
    args = parser.parse_args()
    try:
        bases, heads = assignments(args.base), assignments(args.head)
        if bases.keys() != heads.keys():
            raise ValueError("each Git scope requires both base and head")
        changes = {key: json.loads(Path(value).read_text(encoding="utf-8-sig"))
                   for key, value in assignments(args.changes).items()}
        report = inventory(args.root, changes=changes,
                           repository_roots=assignments(args.repository_root),
                           revisions={key: (bases[key], heads[key]) for key in bases},
                           python_only=args.python_only)
    except (OSError, ValueError) as error:
        report = {"errors": [str(error)], "files": [], "violations": []}
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 2 if report["errors"] else int(args.check and bool(report["violations"]))


if __name__ == "__main__":
    raise SystemExit(main())
