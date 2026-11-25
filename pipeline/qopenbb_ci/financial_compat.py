"""Check a candidate modeling contract and exercised responses for the saved-output consumer."""

import argparse
import json
import subprocess
from pathlib import Path

from .financial_compat_cases import compare_cases
from .financial_compat_inputs import (
    EXPECTATIONS,
    POLICY,
    accepted_contracts,
    candidate_contracts,
    decode,
    digest,
    require,
)
from .financial_compat_replay import verify_source_export
from .financial_compat_structure import compare_structure

_NEXT_ACTION = (
    "Retain the adopted API and widget binding for existing dashboards, or review and "
    "explicitly adopt a versioned migration before promotion."
)


def evidence_record(
    candidate_dir: Path, consumer_file: Path, expectations_file: Path, cases: dict
) -> dict:
    """Bind observations to the contract and acceptance cases used for their exercise."""
    return {
        "format_version": 1,
        "candidate_manifest_sha256": digest(
            (candidate_dir / "manifest.json").read_bytes()
        ),
        "consumer_sha256": digest(consumer_file.read_bytes()),
        "expectations_sha256": digest(expectations_file.read_bytes()),
        "cases": cases,
    }


def assess(directory: Path, consumer: Path, evidence_file: Path) -> dict:
    report = {
        "decision": "blocked",
        "consumer_id": "workspace.saved-model-output",
        "widget_id": "qopenbb_saved_model_output",
        "operation_id": "readSavedWidgetOutput",
        "next_action": _NEXT_ACTION,
    }
    try:
        policy = decode(POLICY.read_bytes())
        accepted = accepted_contracts(policy)
        candidate = candidate_contracts(directory, consumer)
        report.update(
            adoption_revision=policy["adoption_revision"],
            provider_revision=accepted.revision,
            accepted_manifest_sha256=accepted.manifest_sha256,
            candidate_revision=candidate.revision,
            candidate_manifest_sha256=candidate.manifest_sha256,
        )
        expected = EXPECTATIONS.read_bytes()
        require(
            digest(expected) == policy["expectations_sha256"],
            "acceptance cases differ from reviewed digest",
        )
        evidence_bytes = evidence_file.read_bytes()
        record = decode(evidence_bytes)
        require(
            type(record["format_version"]) is int and record["format_version"] == 1,
            "unknown evidence format",
        )
        require(isinstance(record["cases"], dict), "invalid evidence cases")
        expected_pins = {
            "format_version": 1,
            "candidate_manifest_sha256": candidate.manifest_sha256,
            "consumer_sha256": candidate.consumer_sha256,
            "expectations_sha256": digest(expected),
        }
        for name, value in expected_pins.items():
            require(value == record[name], f"incorrect evidence binding: {name}")
        require(
            record.keys() == expected_pins.keys() | {"cases"}, "unknown evidence member"
        )
        report.update(
            evidence_sha256=digest(evidence_bytes),
            consumer_sha256=record["consumer_sha256"],
            expectations_sha256=record["expectations_sha256"],
        )
        findings = compare_structure(
            accepted.documents,
            candidate.documents,
            accepted.consumer,
            candidate.consumer,
        )
        findings += compare_cases(
            accepted.documents,
            candidate.documents,
            accepted.consumer,
            decode(expected),
            record["cases"],
        )
        if not findings:
            verify_source_export(candidate.revision, directory, consumer)
    except (
        subprocess.SubprocessError,
        OSError,
        KeyError,
        ValueError,
        TypeError,
        AttributeError,
        IndexError,
        RecursionError,
    ) as error:
        findings = [f"unknown: cannot verify compatibility ({error})"]
    report["findings"] = findings
    if not findings:
        report.update(decision="compatible", next_action=None)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-bundle", required=True, type=Path)
    parser.add_argument("--candidate-consumer", required=True, type=Path)
    parser.add_argument("--evidence", required=True, type=Path)
    args = parser.parse_args(argv)
    report = assess(args.candidate_bundle, args.candidate_consumer, args.evidence)
    print(json.dumps(report, sort_keys=True, allow_nan=False))
    return int(report["decision"] != "compatible")


if __name__ == "__main__":
    raise SystemExit(main())
