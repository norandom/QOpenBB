"""Installed discovery keeps executable contracts separate from coverage evidence."""

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest
from qopenbb_data.financial_catalog import build_financial_catalog
from test_financial_openapi import project, refs

pytest_plugins = ["test_financial_openapi"]

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "docs/reference/provider-coverage.json"
HASH = "a" * 64
IMAGE = "sha256:" + "b" * 64
STATES = {"documented", "retained_source", "adapted", "installed", "account_access",
          "real_data", "widget", "future_ai"}


@pytest.fixture
def coverage():
    result = json.loads(INDEX.read_text(encoding="utf-8"))
    result["datasets"] = [{"model": "Prices", "provider": "fmp", "family": "markets",
                           "states": {}}]
    return result


def build(document, coverage, **kwargs):
    return build_financial_catalog(
        document, coverage, source_revision="d" * 40, generation_revision="e" * 40,
        generated_at="2026-10-29T12:00:00Z", **kwargs,
    )


def proof(**identity):
    return {"status": "verified", "proof": {"checked_on": "2026-10-29",
            "evidence_path": "artifacts/reviewed/example/accepted.md", "identity": identity}}


def test_operation_response_changes_invalidate_consumer_proofs(source, coverage):
    document = project(source)
    kwargs = {"source_hashes": {"Prices": {"fmp": HASH}}, "image_digest": IMAGE}
    contract = build(document, coverage, **kwargs)["datasets"][0]["contract_sha256"]["fmp"]
    states = coverage["datasets"][0]["states"]
    states["adapted"] = proof(source_sha256=HASH)
    states["real_data"] = proof(source_sha256=HASH, contract_sha256=contract)
    states["widget"] = proof(source_sha256=HASH, contract_sha256=contract, image_digest=IMAGE)
    operation = document["paths"]["/prices"]["get"]
    operation["responses"]["422"] = {"description": "Installed safe request failure", "content": {
        "application/json": {"schema": operation["x-qopenbb-financial"]["error_schema"]}}}
    result = build(document, coverage, **kwargs)["datasets"][0]["coverage"]["fmp"]
    assert result["real_data"]["status"] == result["widget"]["status"] == "stale"
    assert result["adapted"]["status"] == "verified"


def test_installed_descriptors_have_resolvable_semantics_and_no_input_mutation(source, coverage):
    document = project(source)
    document["user_settings"] = {"api_key": "DO-NOT-PUBLISH"}
    before = deepcopy((document, coverage))
    result = build(document, coverage)
    dataset = result["datasets"][0]
    assert dataset["dataset"] == "Prices"
    assert dataset["command"] == {"path": "/prices", "method": "GET", "operation_id": "prices"}
    assert dataset["purpose"] == "Prices"
    assert dataset["providers"] == ["fmp"]
    assert dataset["variants"]["fmp"] == document["paths"]["/prices"]["get"]["x-qopenbb-financial"]["variants"]["fmp"]
    assert dataset["parameters"][0]["required"] is True
    assert dataset["metadata_location"] == "extra.results_metadata.__qopenbb_financial__"
    states = dataset["coverage"]["fmp"]
    assert set(states) == STATES
    assert states["installed"]["status"] == "verified"
    assert states["account_access"]["status"] == "unknown"
    assert "DO-NOT-PUBLISH" not in json.dumps(result)
    for ref in refs(result):
        target = result
        for part in ref.removeprefix("#/").split("/"):
            target = target[part.replace("~1", "/").replace("~0", "~")]
    assert (document, coverage) == before
    assert result == build(document, coverage)
    result["datasets"][0]["variants"]["fmp"]["fields"].clear()
    assert (document, coverage) == before


def test_all_agreed_families_and_open_work_remain_visible(source):
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    result = build(project(source), index)
    families = {item["id"]: item for item in result["coverage"]["families"]}
    assert len([item for item in families.values() if item["provider"] == "fmp"]) == 13
    assert families["reports-documents"]["label"] == "Reports/documents"
    assert families["funds"]["label"] == "Funds"
    assert families["ownership"]["outstanding"]
    assert "futures" in families["other-assets"]["outstanding"].lower()
    assert "COT" in families["macro-positioning"]["outstanding"]
    assert all(item["status"] == "open" for item in families.values())
    # Git publishes LF text; Windows checkouts may materialize CRLF bytes.
    csv_text = (ROOT / "docs/reference/fmp-endpoints.csv").read_text(encoding="utf-8")
    csv_digest = hashlib.sha256(csv_text.encode("utf-8")).hexdigest()
    assert all(item["documented"]["proof"]["identity"] == {"source_sha256": csv_digest}
               for item in families.values() if item["provider"] == "fmp")
    assert {item["model"] for item in index["datasets"]} >= {
        "EquityInfo", "IncomeStatement", "BalanceSheet", "CashFlowStatement",
        "EquitySearch", "EquityPeers", "EquityHistorical", "KeyMetrics",
        "FinancialRatios", "EnterpriseValues", "FredSeries"}
    assert all(item["states"]["installed"]["status"] == "unknown"
               for item in result["coverage"]["datasets"])


def test_independent_blocked_access_does_not_promote_synthetic_consumers(source, coverage):
    states = coverage["datasets"][0]["states"]
    states["account_access"] = {"status": "blocked", "proof": {
        "checked_on": "2026-10-29", "evidence_path": "artifacts/reviewed/example/accepted.md",
        "identity": {"source_sha256": HASH}}}
    states["adapted"] = proof(source_sha256=HASH)
    result = build(project(source), coverage, source_hashes={"Prices": {"fmp": HASH}})
    states = result["datasets"][0]["coverage"]["fmp"]
    assert states["installed"]["status"] == "verified"
    assert states["adapted"]["status"] == "verified"
    assert states["account_access"]["status"] == "blocked"
    assert all(states[key]["status"] == "unknown" for key in ("real_data", "widget", "future_ai"))


def test_proofs_are_scoped_to_relevant_source_contract_and_image(source, coverage):
    document = project(source)
    initial = build(document, coverage, source_hashes={"Prices": {"fmp": HASH}}, image_digest=IMAGE)
    contract = initial["datasets"][0]["contract_sha256"]["fmp"]
    states = coverage["datasets"][0]["states"]
    states["documented"] = proof()
    states["adapted"] = proof(source_sha256=HASH)
    states["real_data"] = proof(source_sha256=HASH, contract_sha256=contract)
    states["widget"] = proof(source_sha256=HASH, contract_sha256=contract, image_digest=IMAGE)
    kwargs = {"source_hashes": {"Prices": {"fmp": HASH}}, "image_digest": IMAGE}
    unchanged = build(document, coverage, **kwargs)
    document["components"]["schemas"]["Unrelated"] = {"type": "string"}
    document["paths"]["/health"]["get"]["summary"] = "Unrelated route change"
    unrelated = build(document, coverage, **kwargs)
    assert unchanged["identity"]["schema_sha256"] != unrelated["identity"]["schema_sha256"]
    assert unchanged["datasets"] == unrelated["datasets"]
    image_change = build(document, coverage, source_hashes=kwargs["source_hashes"])
    image_states = image_change["datasets"][0]["coverage"]["fmp"]
    assert image_states["widget"]["status"] == "stale"
    assert image_states["real_data"]["status"] == "verified"
    query = unrelated["datasets"][0]["variants"]["fmp"]["query_schema"]["$ref"].split("/")[-1]
    document["components"]["schemas"][query]["properties"]["limit"]["maximum"] = 50
    changed = build(document, coverage, **kwargs)["datasets"][0]["coverage"]["fmp"]
    assert changed["documented"]["status"] == changed["adapted"]["status"] == "verified"
    assert changed["real_data"]["status"] == changed["widget"]["status"] == "stale"
    source_change = build(document, coverage, source_hashes={"Prices": {"fmp": "f" * 64}})
    assert source_change["datasets"][0]["coverage"]["fmp"]["adapted"]["status"] == "stale"
    assert states["widget"]["status"] == "verified"


@pytest.mark.parametrize("contract_name", ["response_schema", "error_schema"])
def test_response_and_error_dependencies_invalidate_only_consumer_proofs(source, coverage, contract_name):
    document = project(source)
    descriptor = document["paths"]["/prices"]["get"]["x-qopenbb-financial"]
    component = descriptor[contract_name]["$ref"].split("/")[-1]
    schemas = document["components"]["schemas"]
    schemas[component].setdefault("properties", {})["contract_detail"] = {
        "$ref": "#/components/schemas/ContractDetail"}
    schemas["ContractDetail"] = {"type": "string", "maxLength": 80}
    kwargs = {"source_hashes": {"Prices": {"fmp": HASH}}, "image_digest": IMAGE}
    contract = build(document, coverage, **kwargs)["datasets"][0]["contract_sha256"]["fmp"]
    states = coverage["datasets"][0]["states"]
    states["adapted"] = proof(source_sha256=HASH)
    states["account_access"] = proof(source_sha256=HASH)
    states["real_data"] = proof(source_sha256=HASH, contract_sha256=contract)
    states["widget"] = proof(source_sha256=HASH, contract_sha256=contract, image_digest=IMAGE)
    unchanged = build(document, coverage, **kwargs)["datasets"][0]["coverage"]["fmp"]
    assert all(unchanged[name]["status"] == "verified" for name in states)
    schemas["ContractDetail"]["maxLength"] = 40
    changed = build(document, coverage, **kwargs)["datasets"][0]["coverage"]["fmp"]
    assert changed["adapted"]["status"] == changed["account_access"]["status"] == "verified"
    assert changed["real_data"]["status"] == changed["widget"]["status"] == "stale"


@pytest.mark.parametrize("mutation", [
    lambda value: value.update(account_id="SECRET-CANARY"),
    lambda value: value["datasets"][0]["states"].update(installed=proof()),
    lambda value: value["datasets"][0]["states"].update(real_data=proof()),
    lambda value: value["datasets"][0]["states"].update(widget={"status": "verified"}),
    lambda value: value["datasets"][0].update(family="SECRET-CANARY"),
    lambda value: value["datasets"].append(deepcopy(value["datasets"][0])),
    lambda value: value["datasets"][0]["states"].update(documented={"status": "unknown", "account": "SECRET-CANARY"}),
    lambda value: value["datasets"][0]["states"].update(documented={"status": "verified", "proof": {"checked_on": "2026-10-29", "evidence_path": "https://example.com?apikey=SECRET-CANARY", "identity": {}}}),
])
def test_coverage_is_closed_and_diagnostics_do_not_echo_values(source, coverage, mutation):
    mutation(coverage)
    with pytest.raises(ValueError) as error:
        build(project(source), coverage)
    assert str(error.value) == "Invalid financial discovery input"
    assert "SECRET-CANARY" not in str(error.value)


def test_missing_refs_and_unsafe_identity_fail_closed(source, coverage):
    document = project(source)
    descriptor = document["paths"]["/prices"]["get"]["x-qopenbb-financial"]
    descriptor["variants"]["fmp"]["query_schema"] = {"$ref": "https://example.com/SECRET-CANARY"}
    with pytest.raises(ValueError, match="^Invalid financial discovery input$"):
        build(document, coverage)
    with pytest.raises(ValueError, match="^Invalid financial discovery input$"):
        build(project(source), coverage, source_hashes={"Prices": {"fmp": "SECRET-CANARY"}})


def test_native_installed_baseline_and_first_batch_seam(native_first_batch):
    from openbb_core.api.rest_api import app as native
    from openbb_core.app.route_iter import iter_api_routes
    from openbb_core.provider.registry_map import RegistryMap
    from qopenbb_data.financial_openapi import project_financial_openapi

    index = json.loads(INDEX.read_text(encoding="utf-8"))
    required = {"EquityInfo", "IncomeStatement", "FredSeries"}
    document = project_financial_openapi(native.openapi(), list(iter_api_routes(native)),
                                        RegistryMap(), required_models=required)
    result = build(document, index)
    assert {item["dataset"] for item in result["datasets"]} == required
    assert all(next(param for param in item["parameters"] if param["name"] == "provider")
               ["schema"]["default"] in item["providers"] for item in result["datasets"])
    app, mapping, _ = native_first_batch
    document = project_financial_openapi(app.openapi(), app.routes, mapping,
                                        required_models=set(mapping.original_models))
    result = build(document, index)
    assert len(result["datasets"]) == 11
    assert all(item["coverage"][provider]["installed"]["status"] == "verified"
               for item in result["datasets"] for provider in item["providers"])
    assert all(item["coverage"][provider]["account_access"]["status"] == "unknown"
               for item in result["datasets"] for provider in item["providers"])
    canonical = json.dumps(document, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    assert result["identity"]["schema_sha256"] == hashlib.sha256(canonical).hexdigest()
    source_hashes = {item["model"]: {item["provider"]: item["states"]["adapted"]["proof"]
                     ["identity"]["source_sha256"]} for item in index["datasets"]
                     if "adapted" in item["states"]}
    result = build(document, index, source_hashes=source_hashes)
    adapted = {item["dataset"]: item["coverage"]["fmp"]["adapted"]["status"]
               for item in result["datasets"] if item["dataset"] in source_hashes}
    assert set(adapted.values()) == {"verified"}
    source_hashes["BalanceSheet"]["fmp"] = "c" * 64
    changed = build(document, index, source_hashes=source_hashes)
    after = {item["dataset"]: item["coverage"]["fmp"]["adapted"]["status"]
             for item in changed["datasets"] if item["dataset"] in source_hashes}
    assert after.pop("BalanceSheet") == "stale"
    assert set(after.values()) == {"verified"}
