"""Validate QOpenBB artifacts using explicit paths and independent expected identity."""

import argparse
import json
from pathlib import Path

from qopenbb_ci import __version__
from qopenbb_ci.checks import evaluate, report

def parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command")
    check = commands.add_parser("check", help="Validate artifacts; never publish or promote")
    check.add_argument("--scope", required=True,
                       choices=("source", "manifest", "acceptance", "backup", "excel", "release"))
    check.add_argument("--input", required=True, type=Path)
    check.add_argument("--expected", type=Path)
    check.add_argument("--evidence", action="append", type=Path, default=[])
    check.add_argument("--report", required=True, type=Path)
    return parser


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON field")
        result[key] = value
    return result


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError("invalid JSON constant")))


def main() -> int:
    command_parser = parser()
    args = command_parser.parse_args()
    if args.command is None:
        command_parser.print_help()
        return 0
    if args.scope != "source" and args.expected is None:
        command_parser.error("--expected is required for this scope")
    try:
        result = evaluate(args.scope, read(args.input), read(args.expected) if args.expected else None,
                          [read(path) for path in args.evidence])
        code = 0 if result["valid"] else 1
    except (OSError, ValueError):
        result = report(args.scope, [{"path": "input", "code": "unreadable_or_invalid_json"}], False)
        code = 2
    try:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except OSError:
        print('{"valid": false, "issues": [{"path": "report", "code": "unwritable_report"}]}')
        return 2
    print(json.dumps(result))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
