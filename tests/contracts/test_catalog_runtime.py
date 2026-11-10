"""Opt-in schema/catalog checks run without provider network access."""
import json
import os
import subprocess
from pathlib import Path

import pytest
from qopenbb_ci.catalog import canonical, generate
from qopenbb_ci.catalog_runtime import (
    capture_schema,
    image_identity,
    upstream_widgets,
    verified_sources,
)

ROOT = Path(__file__).resolve().parents[2]
IMAGE = os.environ.get("QOPENBB_DATA_IMAGE")


@pytest.mark.parametrize("prefix", ["sha256:", ""])
def test_image_identity_accepts_exact_engine_id(monkeypatch, prefix):
    digest = "a" * 64
    identity = {"Id": prefix + digest, "Config": {"Labels": {"revision": "accepted"}}}
    calls = []
    def inspect(*args):
        calls.append(args)
        return json.dumps([identity])
    monkeypatch.setattr("qopenbb_ci.catalog_runtime.docker", inspect)
    assert image_identity("sha256:" + digest) == identity
    assert calls == [("image", "inspect", "sha256:" + digest)]


@pytest.mark.parametrize("reported", [
    "sha256:" + "b" * 64, "b" * 64, "sha512:" + "a" * 64,
    "a" * 63, "a" * 65, "A" * 64, "sha256:sha256:" + "a" * 64,
    "a" * 64 + "\n", "latest", None, [], {}, 123,
])
def test_image_identity_rejects_different_or_malformed_engine_id(monkeypatch, reported):
    monkeypatch.setattr("qopenbb_ci.catalog_runtime.docker", lambda *args: json.dumps([{"Id": reported}]))
    with pytest.raises(ValueError, match="image ID mismatch"):
        image_identity("sha256:" + "a" * 64)


@pytest.mark.parametrize("image", ["latest", "a" * 64, "sha256:" + "a" * 63])
def test_image_identity_requires_exact_external_id_before_inspection(monkeypatch, image):
    def unexpected_inspection(*args):
        pytest.fail("invalid external image must fail before inspection")
    monkeypatch.setattr("qopenbb_ci.catalog_runtime.docker", unexpected_inspection)
    with pytest.raises(ValueError, match="exact local image ID"):
        image_identity(image)


def test_modified_generator_is_rejected_before_execution(tmp_path):
    with pytest.raises(ValueError, match="source"):
        verified_sources(tmp_path, "0" * 40)


def test_changed_source_blob_fails_closed(tmp_path):
    from qopenbb_ci.catalog_runtime import ASSET, UTILS
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    for relative in [f"{UTILS}/widgets.py", f"{UTILS}/openapi.py", ASSET]:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("accepted source\n")
    subprocess.run(["git", "-C", str(tmp_path), "add", UTILS, ASSET], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                    "commit", "-qm", "accepted fixture"], check=True)
    (tmp_path / UTILS / "widgets.py").write_text("modified source\n")
    with pytest.raises(ValueError, match="differs"):
        verified_sources(tmp_path, "HEAD")


@pytest.mark.skipif(not IMAGE, reason="requires exact accepted loaded data image")
def test_served_schema_and_upstream_generator_repeat(tmp_path):
    revision = json.loads((ROOT / "sources.lock.json").read_text())["data_api"]["revision"]
    source = ROOT / "vendor/data-api"
    provenance = verified_sources(source, revision)
    schema, identity = capture_schema(IMAGE)
    inventory = json.loads((ROOT / "contracts/datasets.json").read_text())
    raw = upstream_widgets(IMAGE, source, schema, inventory, tmp_path)
    bundled = json.loads((source / "openbb_platform/providers/fred/openbb_fred/assets/apps.json").read_text())
    first = generate(schema, inventory, raw, bundled, "/data")
    second_raw = upstream_widgets(IMAGE, source, schema, inventory, tmp_path)
    assert canonical(first) == canonical(generate(schema, inventory, second_raw, bundled, "/data"))
    assert len(first["widgets.json"]) == len(inventory["datasets"])
    assert {"equity_profile_fmp_obb", "equity_fundamental_income_fmp_obb",
            "economy_fred_series_fred_obb"} <= set(first["widgets.json"])
    assert len(first["apps.json"]) == 2
    assert set(identity["Config"]["Labels"].values()) >= {revision}
    assert provenance["revision"] == revision
    evidence = os.environ.get("QOPENBB_CATALOG_EVIDENCE")
    if evidence:
        destination = Path(evidence)
        destination.mkdir(parents=True, exist_ok=True)
        for name, value in {**first, "source-provenance.json": provenance,
                            "image-identity.json": identity, "upstream-widgets.json": raw}.items():
            (destination / name).write_bytes(canonical(value))
