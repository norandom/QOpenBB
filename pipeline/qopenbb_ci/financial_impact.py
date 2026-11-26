"""Run the modeling checks affected by a committed candidate and retain their evidence."""

import argparse
import json
import os
import re
import subprocess
import tempfile
from contextlib import contextmanager
from pathlib import Path

from .financial_compat import assess
from .financial_compat_inputs import CONSUMER, ROOT, decode, digest, require
from .financial_impact_map import select
from .financial_impact_run import run_checks
from .modeling_bundle import main as bundle_main
from .sources import identity

EXERCISE = (
    "tests/factors/test_financial_compat_cases.py"
    "::test_financial_compat_cli_writes_exercised_evidence"
)


def _git(*args: str) -> bytes:
    return subprocess.check_output(
        ["git", "--no-replace-objects", *args], cwd=ROOT, stderr=subprocess.PIPE
    )


def _revision(ref: str) -> str:
    return (
        _git("rev-parse", "--verify", "--end-of-options", ref + "^{commit}")
        .decode()
        .strip()
    )


def _verify_checkout(head: str) -> None:
    require(_revision("HEAD") == head, "checks require the selected candidate checkout")
    require(
        not _git("status", "--porcelain", "--untracked-files=normal"),
        "checks require a clean candidate checkout",
    )


def _counterparts(head: str) -> dict:
    lock = _git("show", f"{head}:sources.lock.json")
    sources = decode(lock)
    # Fork pins describe the inputs to integration. This source gate exercises no images.
    pins = {}
    for component in ("workspace", "data_api"):
        entry = sources[component]
        require(
            re.fullmatch(r"[0-9a-f]{40}", entry["revision"]), "invalid fork revision"
        )
        pins[component] = {key: entry[key] for key in ("repository", "revision")}
    return {
        "source_lock_sha256": digest(lock),
        "locked_sources": pins,
        "exercised_images": [],
    }


def _verify_forks(pins: dict) -> None:
    for component, path in (
        ("workspace", "vendor/workspace"),
        ("data_api", "vendor/data-api"),
    ):
        identity(ROOT / path, pins[component])


@contextmanager
def _case_environment(directory: Path, evidence: Path):
    values = {
        "QOPENBB_MODEL_COMPAT_BUNDLE": str(directory),
        "QOPENBB_MODEL_COMPAT_CONSUMER": str(ROOT / CONSUMER),
        "QOPENBB_MODEL_COMPAT_EVIDENCE": str(evidence),
    }
    previous = {name: os.environ.get(name) for name in values}
    os.environ.update(values)
    try:
        yield
    finally:
        for name, value in previous.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


def _exercise(head: str, selectors: list[str], output: Path, report: dict) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        bundle = Path(tmp) / "bundle"
        evidence = Path(tmp) / "saved-output.json"
        command = [
            "write",
            "--revision",
            head,
            "--output",
            str(bundle),
            "--consumer",
            str(ROOT / CONSUMER),
        ]
        if bundle_main(command):
            report["error"] = "could not export selected candidate"
        with _case_environment(bundle, evidence):
            report["checks"] = run_checks(sorted(set(selectors) | {EXERCISE}), ROOT)
        report["compatibility"] = assess(bundle, ROOT / CONSUMER, evidence)
        if evidence.exists():
            data = evidence.read_bytes()
            artifact = output.with_name(f"saved-output-{digest(data)}.json")
            artifact.write_bytes(data)
            report["saved_output_evidence"] = artifact.name


def evaluate(base: str, head: str, output: Path) -> dict:
    report = {"format_version": 1, "decision": "blocked"}
    try:
        base, head = _revision(base), _revision(head)
        report.update(base=base, head=head)
        _verify_checkout(head)
        try:
            report.update(_counterparts(head))
        except (ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
            report["error"] = f"unverified counterpart pins ({error})"
        selection = select(base, head, ROOT)
        report["selection"] = selection
        if not any(selection[key] for key in ("changed_ids", "selectors", "gaps")):
            if "error" not in report:
                report["decision"] = "unaffected"
            return report
        if "locked_sources" in report:
            try:
                _verify_forks(report["locked_sources"])
            except (OSError, ValueError, subprocess.SubprocessError) as error:
                report["error"] = f"unverified source checkout ({error})"
        _exercise(head, selection["selectors"], output, report)
        _verify_checkout(head)
        if "locked_sources" in report:
            _verify_forks(report["locked_sources"])
        if (
            "error" not in report
            and not selection["gaps"]
            and selection["selectors"]
            and report["checks"]["passed"]
            and report["compatibility"]["decision"] == "compatible"
        ):
            report["decision"] = "passed"
    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        subprocess.SubprocessError,
    ) as error:
        report["error"] = str(error)
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    report = evaluate(args.base, args.head, output)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(f"Modeling impact {report['decision']} ({output})")
    return int(report["decision"] == "blocked")


if __name__ == "__main__":
    raise SystemExit(main())
