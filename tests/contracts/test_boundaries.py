import copy
import json
import subprocess
import sys

import pytest

from conftest import ROOT
from qopenbb_ci.checks import evaluate
from qopenbb_ci.contracts import Acceptance, Backup, ExpectedContext, Image, Release
from qopenbb_ci.source_contract import SourceLock
from qopenbb_ci.schemas import MODELS, schema_text


@pytest.mark.parametrize("field,value", [("schema_version", True), ("exit_code", True),
                                         ("exit_code", "0"), ("status", "success"),
                                         ("timestamp", "2026-10-16T10:00:00"),
                                         ("timestamp", "2026-10-16T10:00:00+02:00"),
                                         ("requirements", ["REQ-12"]), ("extra", "private")])
def test_acceptance_types_are_closed(bundle, field, value):
    record = bundle["records"][0]
    record[field] = value
    assert not evaluate("acceptance", record, bundle["expected"], [])["valid"]


def test_pass_with_nonzero_exit_is_invalid(bundle):
    record = bundle["records"][0]
    record["exit_code"] = 1
    assert not evaluate("acceptance", record, bundle["expected"], [])["valid"]


@pytest.mark.parametrize("mutation", ["owner", "upstream", "branch", "candidate", "release", "image"])
def test_source_lock_rejects_provenance_or_acquisition_confusion(mutation):
    source = json.loads((ROOT / "sources.lock.json").read_text())
    if mutation == "owner":
        source["workspace"]["repository"] = "https://github.com/other/workspace.git"
    elif mutation == "upstream":
        source["data_api"]["upstream"] = "https://github.com/other/data.git"
    elif mutation == "branch":
        source["workspace"]["revision"] = "main"
    elif mutation == "candidate":
        source["data_api"]["candidate_release"]["revision"] = True
    elif mutation == "release":
        source["validated_release"] = "not-really-validated"
    else:
        source["images"]["identifiers"] = ["workspace:latest"]
    assert not evaluate("source", source, None, [])["valid"]


def test_current_api_candidate_does_not_replace_acquired_revision():
    payload = json.loads((ROOT / "sources.lock.json").read_text())
    lock = SourceLock.model_validate(payload)
    assert lock.data_api.revision == "7c9d4221bdf66965e3f6c7f4dc6ee848073e5ae2"
    assert lock.data_api.candidate_release.revision == "5a7517ae8bc74ecdcd1a549ed26df8ad131b02d0"


@pytest.mark.parametrize("mutation", ["fixture_context", "empty_context", "no_model", "no_agent",
                                      "stale_manifest", "unreferenced", "duplicate_record"])
def test_checkpoint_cannot_be_weakened_by_expected_selection(bundle, mutation):
    if mutation == "fixture_context":
        for check, record in zip(bundle["expected"]["required_checks"], bundle["records"]):
            check["evidence_class"] = record["evidence_class"] = "fixture"
    elif mutation == "empty_context":
        bundle["expected"]["required_checks"] = []
    elif mutation == "no_model":
        bundle["expected"]["identity"]["model"] = None
    elif mutation == "no_agent":
        del bundle["expected"]["identity"]["images"]["agent"]
    elif mutation == "stale_manifest":
        bundle["manifest"]["identity"]["run_id"] = "stale"
    elif mutation == "unreferenced":
        bundle["manifest"]["acceptance_refs"].pop()
    else:
        bundle["records"].append(copy.deepcopy(bundle["records"][-1]))
    report = evaluate("excel", bundle["manifest"], bundle["expected"], bundle["records"])
    assert not report["valid"]
    assert not report["runtime_accepted"]


def test_dashboard_checkpoint_does_not_require_agent(bundle):
    del bundle["manifest"]["identity"]["images"]["agent"]
    del bundle["expected"]["identity"]["images"]["agent"]
    assert evaluate("manifest", bundle["manifest"], bundle["expected"], [])["valid"]
    assert not evaluate("excel", bundle["manifest"], bundle["expected"], bundle["records"])["valid"]


def test_final_release_requires_distinct_complete_checks(bundle):
    bundle["manifest"]["status"] = "release"
    assert not evaluate("release", bundle["manifest"], bundle["expected"], bundle["records"])["valid"]
    bundle["records"][0]["requirements"] += ["4.1", "4.2"]
    bundle["expected"]["required_checks"][0]["requirements"] += ["4.1", "4.2"]
    for capability, requirements in (("linux", ["3.3", "9.4"]), ("recovery", ["8.2", "8.4"])):
        record = copy.deepcopy(bundle["records"][0])
        record.update(record_id=f"record-{capability}", capability=capability, requirements=requirements)
        bundle["records"].append(record)
        bundle["manifest"]["acceptance_refs"].append(record["record_id"])
        bundle["expected"]["required_checks"].append({
            "capability": capability, "requirements": requirements, "evidence_class": "live"})
    assert evaluate("release", bundle["manifest"], bundle["expected"], bundle["records"])["valid"]


@pytest.mark.parametrize("payload", ["{bad", '{"schema_version":2,"schema_version":2}', "NaN"])
def test_invalid_json_has_input_exit_and_sanitized_report(tmp_path, payload):
    path = tmp_path / "input.json"
    path.write_text(payload)
    report = tmp_path / "report.json"
    process = subprocess.run([sys.executable, "-m", "qopenbb_ci.cli", "check", "--scope", "source",
                              "--input", str(path), "--report", str(report)], capture_output=True)
    assert process.returncode == 2
    assert json.loads(report.read_text())["issues"] == [
        {"path": "input", "code": "unreadable_or_invalid_json"}]


def test_expected_context_required(tmp_path):
    process = subprocess.run([sys.executable, "-m", "qopenbb_ci.cli", "check", "--scope", "excel",
                              "--input", "absent.json", "--report", str(tmp_path / "report.json")],
                             capture_output=True, text=True)
    assert process.returncode == 2
    assert "--expected is required" in process.stderr


def test_models_export_closed_schemas():
    for model in (SourceLock, Release, Acceptance, Backup, ExpectedContext):
        schema = model.model_json_schema()
        assert schema["additionalProperties"] is False
        assert all(value.get("additionalProperties") is False for value in schema.get("$defs", {}).values())


def test_generated_schemas_match_authoritative_models():
    for name, model in MODELS.items():
        assert (ROOT / "schemas" / f"{name}.schema.json").read_text() == schema_text(model)


@pytest.mark.parametrize("category,key", [
    ("revisions", name) for name in ("qopenbb", "workspace", "data_api", "agent")
] + [("images", name) for name in ("workspace", "data-api", "agent")]
    + [("lock_hashes", name) for name in ("source", "tools", "dependencies")]
    + [("contract_hashes", name) for name in ("openapi", "widgets")])
def test_each_identity_component_is_bound_to_expected(bundle, category, key):
    identity = bundle["records"][-1]["identity"]
    if category == "images":
        identity[category][key]["digest"] = f"ghcr.io/example/{key}@sha256:" + "c" * 64
    else:
        identity[category][key] = "c" * 40 if category == "revisions" else "sha256:" + "c" * 64
    assert not evaluate("excel", bundle["manifest"], bundle["expected"], bundle["records"])["valid"]


@pytest.mark.parametrize("field,value", [("captured_at", "2026-10-16T12:00:00+02:00"),
                                         ("services_stopped", "true"),
                                         ("private_configuration_ref", "./.env"),
                                         ("restore_compatibility", ["different-format"])])
def test_backup_boundary_rejects_inconsistent_or_private_input(bundle, field, value):
    bundle["backup"][field] = value
    assert not evaluate("backup", bundle["backup"], bundle["expected"], [])["valid"]


def test_backup_checksum_is_required(bundle):
    bundle["backup"]["archive"]["sha256"] = "not-a-checksum"
    assert not evaluate("backup", bundle["backup"], bundle["expected"], [])["valid"]


def test_selected_excel_profile_requires_its_immutable_image(bundle):
    bundle["manifest"]["profiles"] = ["excel"]
    assert not evaluate("manifest", bundle["manifest"], bundle["expected"], [])["valid"]


def test_backup_archive_can_use_the_owned_backup_root(bundle):
    bundle["backup"]["archive"]["path"] = "backups/backup-1/workspace.tar"
    assert evaluate("backup", bundle["backup"], bundle["expected"], [])["valid"]


@pytest.mark.parametrize("status", ["passed", "failed", "skipped", "unverified"])
def test_report_preserves_acceptance_status_without_payload(bundle, status):
    record = bundle["records"][0]
    record["status"] = status
    record["command"] = "SENSITIVE_COMMAND_SENTINEL"
    report = evaluate("acceptance", record, bundle["expected"], [])
    assert report["checks"] == [{"path": "input", "status": status, "evidence_class": "live"}]
    assert "SENSITIVE_COMMAND_SENTINEL" not in json.dumps(report)


@pytest.mark.parametrize("name", [
    "registry:/workspace", "ghcr.io//workspace", "ghcr.io/../workspace", "ghcr.io/./workspace",
    "ghcr.io/team//workspace", "ghcr.io/workspace/", "ghcr.io:abc/team/workspace",
    "-registry.example/workspace", "registry-.example/workspace", "ghcr..io/workspace",
    "ghcr.io/team/workspace_", "ghcr.io/team/workspace...x", "ghcr.io/team/workspace___x",
    "[::::]:5000/workspace", "registry.example/" + "a" * 256,
])
def test_malformed_image_reference_fails_even_when_expected_matches(bundle, name):
    reference = name + "@sha256:" + "a" * 64
    bundle["manifest"]["identity"]["images"]["workspace"]["digest"] = reference
    bundle["expected"]["identity"]["images"]["workspace"]["digest"] = reference
    report = evaluate("manifest", bundle["manifest"], bundle["expected"], [])
    assert not report["valid"]
    assert report["issues"][0]["path"] == "input.identity.images.workspace.digest"
    assert reference not in json.dumps(report)


@pytest.mark.parametrize("name", [
    "ghcr.io/norandom/qopenbb-workspace", "registry.example:5000/team/nested/workspace",
    "localhost:5000/workspace", "127.0.0.1:5000/team/workspace",
    "registry-prod.example.co.uk/team_1/workspace.v1--build", "registry.example/team__name/workspace",
    "[2001:db8::1]:5000/team/workspace",
])
def test_valid_configurable_registry_and_repository_names(name):
    reference = name + "@sha256:" + "a" * 64
    assert Image.model_validate({"digest": reference, "architecture": "linux/amd64"}).digest == reference
