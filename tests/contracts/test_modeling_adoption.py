"""Check both sides of the initial saved-output contract adoption offline."""

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.openapi.models import OpenAPI
from qopenbb_ci.financial_compat_replay import verify_source_export

ROOT = Path(__file__).resolve().parents[2]
CONSUMERS = ROOT / "contracts/consumers/financial-modeling"
CONSUMER = CONSUMERS / "saved-output.v1.json"
BUNDLE = ROOT / "contracts/modeling/v1"


def _check_payload(revision, bundle, consumer, cwd, env):
    subprocess.run(
        [
            sys.executable,
            "-m",
            "qopenbb_ci.modeling_bundle",
            "check",
            "--revision",
            revision,
            "--output",
            str(bundle),
            "--consumer",
            str(consumer),
        ],
        cwd=cwd,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )


def _verify_adoption(pin, bundle):
    """Regenerate from both the adopted commit and the current implementation."""
    assert pin["repository"] == "norandom/QOpenBB"
    assert pin["bundle"] == BUNDLE.relative_to(ROOT).as_posix()
    assert re.fullmatch("[0-9a-f]{40}", pin["source_revision"])
    manifest = (bundle / "manifest.json").read_bytes()
    assert pin["manifest_sha256"] == hashlib.sha256(manifest).hexdigest()
    assert pin["contract_version"] == 1
    revision = pin["source_revision"]
    env = os.environ | {"GIT_NO_LAZY_FETCH": "1", "GIT_NO_REPLACE_OBJECTS": "1"}
    verify_source_export(revision, bundle, CONSUMER)
    _check_payload(revision, bundle, CONSUMER, ROOT, env)


def test_pinned_bundle_reproduces_from_pinned_and_current_sources():
    pin = json.loads((CONSUMERS / "provider.lock.json").read_bytes())
    _verify_adoption(pin, BUNDLE)


def test_recomputed_digest_cannot_attest_a_missing_revision(tmp_path):
    pin = json.loads((CONSUMERS / "provider.lock.json").read_bytes())
    revision = "0" * 40
    fake = tmp_path / "bundle"
    fake.mkdir()
    manifest = json.loads((BUNDLE / "manifest.json").read_bytes())
    manifest.update(source_revision=revision, consumer_source_revision=revision)
    body = (json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n").encode()
    (fake / "manifest.json").write_bytes(body)
    pin.update(
        source_revision=revision, manifest_sha256=hashlib.sha256(body).hexdigest()
    )
    with pytest.raises(subprocess.CalledProcessError) as failure:
        _verify_adoption(pin, fake)
    assert failure.value.cmd[1] == "rev-parse"


def test_consumer_binds_exported_operation_and_widget():
    manifest = json.loads(CONSUMER.read_bytes())
    operation, response = manifest["operation"], manifest["response"]
    api = json.loads((BUNDLE / "openapi.json").read_bytes())
    OpenAPI.model_validate(api)
    api_operation = api["paths"][operation["path"]][operation["method"].lower()]
    assert api_operation["operationId"] == operation["id"]
    assert {"url": operation["base_path"]} in api["servers"]
    widget = json.loads((BUNDLE / "widgets.json").read_bytes())[manifest["widget_id"]]
    assert widget["endpoint"] == operation["path"].lstrip("/")
    assert widget["data"]["dataKey"] == response["data_key"]
    fields = [field["name"] for field in response["row_fields"]]
    assert fields == [
        column["field"] for column in widget["data"]["table"]["columnsDefs"]
    ]
    parameters = [
        (parameter["parameter"], parameter["required"])
        for parameter in operation["query"]
    ]
    assert parameters == [(p["paramName"], not p["optional"]) for p in widget["params"]]
    assert parameters == [
        (p["name"], p.get("required", False))
        for p in api_operation["parameters"]
        if p["in"] == "query"
    ]
