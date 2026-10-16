import copy
import json

import pytest

from conftest import ROOT


def test_acquisition_is_valid_without_a_release(invoke):
    source = json.loads((ROOT / "sources.lock.json").read_text())
    result, report = invoke("source", source)
    assert result.returncode == 0, result.stderr
    assert report["valid"] is True
    assert report["runtime_accepted"] is False


@pytest.mark.parametrize("scope,key", [("manifest", "manifest"), ("backup", "backup"),
                                      ("acceptance", "records")])
def test_typed_artifacts_validate(invoke, bundle, scope, key):
    payload = bundle[key][0] if key == "records" else bundle[key]
    process, report = invoke(scope, payload, bundle["expected"])
    assert process.returncode == 0, process.stderr
    assert not report["runtime_accepted"]


def test_current_actual_checkpoint_unlocks_excel(invoke, bundle):
    process, report = invoke("excel", bundle["manifest"], bundle["expected"], bundle["records"])
    assert process.returncode == 0, process.stderr
    assert report["runtime_accepted"]


@pytest.mark.parametrize("status", ["failed", "skipped", "unverified"])
def test_nonpassing_anthropic_blocks_even_with_exit_zero(invoke, bundle, status):
    bundle["records"][-1]["status"] = status
    process, report = invoke("excel", bundle["manifest"], bundle["expected"], bundle["records"])
    assert process.returncode == 1
    assert not report["runtime_accepted"]


@pytest.mark.parametrize("change", ["missing", "unrelated", "fixture", "requirements"])
def test_missing_or_irrelevant_acceptance_blocks(invoke, bundle, change):
    record = bundle["records"][-1]
    if change == "missing":
        bundle["records"].pop()
    elif change == "unrelated":
        record["capability"] = "unrelated"
    elif change == "fixture":
        record["evidence_class"] = "fixture"
    else:
        record["requirements"] = ["1.1"]
    assert invoke("excel", bundle["manifest"], bundle["expected"], bundle["records"])[0].returncode == 1


@pytest.mark.parametrize("field", ["release_id", "run_id", "revision", "image", "architecture",
                                   "lock", "contract", "model"])
def test_every_stale_identity_blocks(invoke, bundle, field):
    identity = bundle["records"][-1]["identity"]
    if field in ("release_id", "run_id"):
        identity[field] = "stale"
    elif field == "revision":
        identity["revisions"]["workspace"] = "c" * 40
    elif field == "image":
        identity["images"]["agent"]["digest"] = "ghcr.io/example/agent@sha256:" + "c" * 64
    elif field == "architecture":
        identity["images"]["agent"]["architecture"] = "linux/arm64"
    elif field == "lock":
        identity["lock_hashes"]["tools"] = "sha256:" + "c" * 64
    elif field == "contract":
        identity["contract_hashes"]["widgets"] = "sha256:" + "c" * 64
    else:
        identity["model"]["name"] = "different-model"
    assert invoke("excel", bundle["manifest"], bundle["expected"], bundle["records"])[0].returncode == 1


@pytest.mark.parametrize("mutation", ["unknown", "boolean_version", "mutable", "bad_revision",
                                      "missing_lock", "config_value", "secret_artifact", "missing_image"])
def test_manifest_boundary_rejects_malformed_without_echo(invoke, bundle, mutation):
    manifest = bundle["manifest"]
    secret = "SENSITIVE_SENTINEL_SHOULD_NOT_APPEAR"
    if mutation == "unknown":
        manifest[secret] = secret
    elif mutation == "boolean_version":
        manifest["schema_version"] = True
    elif mutation == "mutable":
        manifest["identity"]["images"]["agent"]["digest"] = "ghcr.io/example/agent:latest"
    elif mutation == "bad_revision":
        manifest["identity"]["revisions"]["workspace"] = "main"
    elif mutation == "missing_lock":
        del manifest["identity"]["lock_hashes"]["dependencies"]
    elif mutation == "config_value":
        manifest["required_configuration"] = ["API_KEY=" + secret]
    elif mutation == "secret_artifact":
        manifest["acceptance_refs"] = ["../.env"]
    else:
        del manifest["identity"]["images"]["workspace"]
    process, report = invoke("manifest", manifest, bundle["expected"])
    assert process.returncode == 1
    assert report["issues"]
    assert secret not in json.dumps(report) + process.stdout + process.stderr


def test_backup_requires_stopped_services(invoke, bundle):
    bundle["backup"]["services_stopped"] = False
    assert invoke("backup", bundle["backup"], bundle["expected"])[0].returncode == 1


def test_candidate_is_not_a_release(invoke, bundle):
    assert invoke("release", bundle["manifest"], bundle["expected"], bundle["records"])[0].returncode == 1


def test_expected_context_is_independent(invoke, bundle):
    for record in bundle["records"]:
        record["identity"]["revisions"]["workspace"] = "c" * 40
    bundle["manifest"]["identity"]["revisions"]["workspace"] = "c" * 40
    assert invoke("excel", bundle["manifest"], bundle["expected"], bundle["records"])[0].returncode == 1
