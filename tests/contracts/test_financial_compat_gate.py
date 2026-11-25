"""Exercise fail-closed promotion and source pinning at the public CLI."""

import hashlib
import json
import shutil

import pytest
from qopenbb_ci import financial_compat as gate
from qopenbb_ci.financial_compat_inputs import BUNDLE, CONSUMER, ROOT


@pytest.fixture
def candidate(tmp_path):
    bundle = tmp_path / "provider"
    shutil.copytree(ROOT / BUNDLE, bundle)
    consumer = tmp_path / "consumer.json"
    shutil.copyfile(ROOT / CONSUMER, consumer)
    return bundle, consumer


def run_gate(bundle, consumer, evidence, capsys):
    status = gate.main(
        [
            "--candidate-bundle",
            str(bundle),
            "--candidate-consumer",
            str(consumer),
            "--evidence",
            str(evidence),
        ]
    )
    return status, json.loads(capsys.readouterr().out)


def test_empty_cases_block_and_identify_saved_dashboard(candidate, tmp_path, capsys):
    bundle, consumer = candidate
    evidence = tmp_path / "responses.json"
    evidence.write_text(
        json.dumps(gate.evidence_record(bundle, consumer, gate.EXPECTATIONS, {}))
    )
    status, report = run_gate(bundle, consumer, evidence, capsys)
    assert status != 0 and report["decision"] == "blocked"
    assert report["consumer_id"] == "workspace.saved-model-output"
    assert report["widget_id"] == "qopenbb_saved_model_output"
    assert report["findings"] and report["next_action"]


def test_candidate_evidence_must_belong_to_exact_bytes(candidate, tmp_path, capsys):
    bundle, consumer = candidate
    evidence = tmp_path / "responses.json"
    record = gate.evidence_record(bundle, consumer, gate.EXPECTATIONS, {})
    record["candidate_manifest_sha256"] = "0" * 64
    evidence.write_text(json.dumps(record))
    status, report = run_gate(bundle, consumer, evidence, capsys)
    assert status != 0 and any(
        "candidate_manifest_sha256" in x for x in report["findings"]
    )


def test_extra_candidate_file_blocks_before_comparison(candidate, tmp_path, capsys):
    bundle, consumer = candidate
    (bundle / "unexpected.json").write_text("{}")
    status, report = run_gate(bundle, consumer, tmp_path / "missing.json", capsys)
    assert status != 0 and any("file set" in x for x in report["findings"])


def test_candidate_consumer_cannot_replace_pinned_consumer(candidate, tmp_path, capsys):
    bundle, consumer = candidate
    manifest = bundle / "manifest.json"
    changed = json.loads(consumer.read_bytes())
    changed["response"]["row_fields"][4]["semantic_id"] = "changed-unit"
    consumer.write_text(json.dumps(changed))
    provider = json.loads(manifest.read_bytes())
    provider["consumer_manifest_sha256"] = hashlib.sha256(
        consumer.read_bytes()
    ).hexdigest()
    manifest.write_text(json.dumps(provider))
    evidence = tmp_path / "responses.json"
    evidence.write_text(
        json.dumps(gate.evidence_record(bundle, consumer, gate.EXPECTATIONS, {}))
    )
    status, report = run_gate(bundle, consumer, evidence, capsys)
    assert status != 0 and any("semantic" in x.lower() for x in report["findings"])


def test_invalid_json_is_reported_without_a_traceback(candidate, tmp_path, capsys):
    bundle, consumer = candidate
    evidence = tmp_path / "responses.json"
    evidence.write_text('{"cases":{},"cases":{}}')
    status, report = run_gate(bundle, consumer, evidence, capsys)
    assert status != 0 and report["decision"] == "blocked"


def test_clean_comparison_cannot_promote_unreproducible_bytes(
    candidate, tmp_path, capsys, monkeypatch
):
    bundle, consumer = candidate
    catalog = bundle / "apps.json"
    catalog.write_bytes(catalog.read_bytes() + b"\n")
    manifest = bundle / "manifest.json"
    metadata = json.loads(manifest.read_bytes())
    metadata["files"]["apps.json"] = hashlib.sha256(catalog.read_bytes()).hexdigest()
    manifest.write_text(json.dumps(metadata))
    evidence = tmp_path / "responses.json"
    evidence.write_text(
        json.dumps(gate.evidence_record(bundle, consumer, gate.EXPECTATIONS, {}))
    )
    # Isolate the source attestation after compatible structural and response verdicts.
    monkeypatch.setattr(gate, "compare_structure", lambda *args: [])
    monkeypatch.setattr(gate, "compare_cases", lambda *args: [])
    status, report = run_gate(bundle, consumer, evidence, capsys)
    assert status != 0 and any(
        "does not reproduce" in finding for finding in report["findings"]
    )
