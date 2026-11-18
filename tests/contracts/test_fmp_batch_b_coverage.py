"""Batch B coverage claims bind accepted live/browser evidence to the shipped source and contract.

Live API acceptance (task 5.2) covers all eight operations. Browser acceptance (task 5.3) covers
five representative widgets on one recorded local data-API image; on any other image the widget
claim projects as stale rather than verified. Future AI use remains unknown.
"""
import json
from hashlib import sha256
from pathlib import Path

import pytest
from qopenbb_data.financial_catalog import _descriptor, build_financial_catalog

ROOT = Path(__file__).resolve().parents[2]
HANDOFFS = {item["model"]: item for item in json.loads(
    (ROOT / "tests/providers/fixtures/fmp_batch_b/handoffs.json").read_text(encoding="utf-8"))["widgets"]}
LIVE = "artifacts/reviewed/fmp-expansion-b/live-matrix-verification.json"
BROWSER = "artifacts/reviewed/fmp-expansion-b/native-browser-verification.json"
BROWSER_MODELS = {"HistoricalDividends", "CalendarEarnings", "CompanyNews", "EarningsCallTranscript", "CompanyFilings"}


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def source_hash(model):
    module = HANDOFFS[model]["module"]
    return sha256((ROOT / f"vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/{module}.py").read_bytes()).hexdigest()


def contract_hash(document, model):
    path = HANDOFFS[model]["route"]
    return _descriptor(document, path, "get", document["paths"][path]["get"], document["paths"][path])["contract_sha256"]["fmp"]


def records():
    coverage = read(ROOT / "docs/reference/provider-coverage.json")
    found = {item["model"]: item for item in coverage["datasets"] if item["provider"] == "fmp" and item["model"] in HANDOFFS}
    assert set(found) == set(HANDOFFS)
    return coverage, found


@pytest.mark.parametrize("model", sorted(HANDOFFS))
def test_batch_b_live_claims_bind_accepted_evidence_to_shipped_source_and_contract(model):
    _, found = records()
    states, document = found[model]["states"], read(ROOT / "contracts/openapi.json")
    current = source_hash(model)
    for state in ("documented", "retained_source", "adapted"):
        assert states[state]["status"] == "verified"
        assert (ROOT / states[state]["proof"]["evidence_path"]).is_file()
    # A repaired adapter must not keep a proof for the bytes it replaced.
    assert states["adapted"]["proof"]["identity"]["source_sha256"] == current
    live = read(ROOT / LIVE)
    assert live["task"] == "5.2" and live["status"] == "VERIFIED"
    assert live["review_sha256"] == sha256((ROOT / live["review"]).read_bytes()).hexdigest()
    assert live["models"][model]["source_sha256"] == current
    for state in ("account_access", "real_data"):
        assert states[state]["status"] == "verified"
        assert states[state]["proof"]["evidence_path"] == LIVE
        assert states[state]["proof"]["identity"]["source_sha256"] == current
    assert states["real_data"]["proof"]["identity"]["contract_sha256"] == contract_hash(document, model)
    assert states["future_ai"] == {"status": "unknown"}


def test_batch_b_widget_claims_are_five_sampled_models_and_stale_on_another_image():
    coverage, found = records()
    browser = read(ROOT / BROWSER)
    assert browser["task"] == "5.3" and browser["status"] == "VERIFIED"
    assert browser["review_sha256"] == sha256((ROOT / browser["review"]).read_bytes()).hexdigest()
    assert set(browser["spec_updates"]["browser_models"]) == BROWSER_MODELS
    assert set(browser["spec_updates"]["unsampled_models"]) == set(HANDOFFS) - BROWSER_MODELS
    image = browser["spec_updates"]["local_candidate_images"]["data-api"]
    assert {model for model, record in found.items() if record["states"]["widget"]["status"] == "verified"} == BROWSER_MODELS
    for model, record in found.items():
        if model not in BROWSER_MODELS:
            assert record["states"]["widget"] == {"status": "unknown"}
            continue
        proof = record["states"]["widget"]["proof"]
        assert proof["evidence_path"] == BROWSER
        assert proof["identity"] == {**record["states"]["real_data"]["proof"]["identity"], "image_digest": image}
    document = read(ROOT / "contracts/openapi.json")
    hashes = {model: {"fmp": source_hash(model)} for model in HANDOFFS}

    def projected(runtime_image):
        result = build_financial_catalog(document, coverage, source_revision=browser["api_commit"],
            generation_revision=browser["api_commit"], generated_at="2026-11-18T00:00:00+00:00",
            source_hashes=hashes, image_digest=runtime_image)
        return {item["dataset"]: item["coverage"]["fmp"] for item in result["datasets"] if item["dataset"] in HANDOFFS}

    current = projected(image)
    other = projected("sha256:" + ("0" if image != "sha256:" + "0" * 64 else "1") * 64)
    for model in HANDOFFS:
        assert current[model]["real_data"]["status"] == other[model]["real_data"]["status"] == "verified"
        assert current[model]["widget"]["status"] == ("verified" if model in BROWSER_MODELS else "unknown")
        assert other[model]["widget"]["status"] == ("stale" if model in BROWSER_MODELS else "unknown")
