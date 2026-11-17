"""Batch A consumer inputs preserve the accepted native financial contracts."""
import json
from hashlib import sha256
from datetime import date
from pathlib import Path

import pytest
from qopenbb_ci.catalog_financial import resolve
from qopenbb_data.financial_catalog import _descriptor, build_financial_catalog

ROOT = Path(__file__).resolve().parents[2]
BATCH_A = {
    "analyst-estimates": ("AnalystEstimates", "analyst_estimates", "estimates/historical"),
    "price-target": ("PriceTarget", "price_target", "estimates/price_target"),
    "price-target-consensus": ("PriceTargetConsensus", "price_target_consensus", "estimates/consensus"),
    "revenue-business-line": ("RevenueBusinessLine", "revenue_business_line", "fundamental/revenue_per_segment"),
    "revenue-geographic": ("RevenueGeographic", "revenue_geographic", "fundamental/revenue_per_geography"),
    "historical-market-cap": ("HistoricalMarketCap", "historical_market_cap", "historical_market_cap"),
    "share-statistics": ("ShareStatistics", "share_statistics", "ownership/share_statistics"),
    "equity-quote": ("EquityQuote", "equity_quote", "price/quote"),
    "income-statement-growth": ("IncomeStatementGrowth", "income_statement_growth", "fundamental/income_growth"),
    "balance-sheet-growth": ("BalanceSheetGrowth", "balance_sheet_growth", "fundamental/balance_growth"),
    "cash-flow-growth": ("CashFlowStatementGrowth", "cash_flow_growth", "fundamental/cash_growth"),
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("dataset_id", BATCH_A)
def test_batch_a_inventory_has_only_bounded_canonical_native_parameters(dataset_id):
    _, module, route = BATCH_A[dataset_id]
    contract = read(ROOT / f"tests/providers/fixtures/fmp_batch_a/contracts/{module}.json")
    datasets = read(ROOT / "contracts/datasets.json")["datasets"]
    item = next(item for item in datasets if item["id"] == dataset_id)
    assert item["path"] == "/api/v1/equity/" + route
    assert item["provider"] == "fmp"
    fields = contract["query"]["validation"]["properties"]
    expected = {"provider": "fmp", "symbol": "MSFT"}
    expected.update({key: value for key, value in {"period": "annual", "limit": 3, "page": 0}.items()
                     if key in fields})
    if "start_date" in fields:
        expected.update(start_date="2025-01-02", end_date="2025-01-31")
        assert 0 <= (date.fromisoformat(expected["end_date"]) - date.fromisoformat(expected["start_date"])).days <= 366
    assert item["parameters"] == expected


@pytest.mark.parametrize("dataset_id", BATCH_A)
def test_batch_a_generated_contract_retains_metadata_units_and_consumer_association(dataset_id):
    _, module, route = BATCH_A[dataset_id]
    contract = read(ROOT / f"tests/providers/fixtures/fmp_batch_a/contracts/{module}.json")
    document = read(ROOT / "contracts/openapi.json")
    operation = document["paths"]["/api/v1/equity/" + route]["get"]
    descriptor = operation["x-qopenbb-financial"]
    variant = descriptor["variants"]["fmp"]
    assert descriptor["metadata_location"] == "extra.results_metadata.__qopenbb_financial__"
    assert resolve(document, variant["query_schema"]) == contract["query"]["validation"]
    row = resolve(document, variant["row_schema"])
    assert set(row["properties"]) == set(contract["canonical_fields"])
    for key in ("procedural_bounds", "response_policy"):
        assert variant[key] == contract["query_annotation"][key]
    assert set(variant["runtime_properties"]) == set(contract["query_annotation"]["runtime_properties"]) | set(contract["data_annotation"]["runtime_properties"])
    for field, annotation in contract["data_annotation"]["fields"].items():
        actual = variant["fields"][field]
        for key in ("unit", "scale", "currency", "currency_field", "period_basis", "value_origin", "financial_basis"):
            assert actual[key] == annotation[key], (dataset_id, field, key)
    mapping = read(ROOT / "contracts/catalog-report.json")["mapping"]
    match, = [item for item in mapping if item["dataset"] == dataset_id]
    widget = read(ROOT / "contracts/widgets.json")[match["widget"]]
    assert widget["endpoint"] == "/api/v1/equity/" + route
    assert widget["data"]["dataKey"] == "results"
    assert {column["field"] for column in widget["data"]["table"]["columnsDefs"]} == set(row["properties"])
    inventory = next(item for item in read(ROOT / "contracts/datasets.json")["datasets"] if item["id"] == dataset_id)
    starter = read(ROOT / "contracts/apps.json")[0]
    state, = [item["state"]["params"] for item in starter["tabs"]["Data"]["layout"] if item["i"] == match["widget"]]
    assert state == inventory["parameters"]


@pytest.mark.parametrize("dataset_id", BATCH_A)
def test_batch_a_coverage_binds_scoped_live_evidence_to_actual_source_and_contract(dataset_id):
    model, module, _ = BATCH_A[dataset_id]
    coverage = read(ROOT / "docs/reference/provider-coverage.json")
    record, = [item for item in coverage["datasets"] if (item["model"], item["provider"]) == (model, "fmp")]
    for state in ("documented", "retained_source", "adapted"):
        proof = record["states"][state]
        assert proof["status"] == "verified"
        assert (ROOT / proof["proof"]["evidence_path"]).is_file()
    verification = read(ROOT / record["states"]["adapted"]["proof"]["evidence_path"])
    assert record["states"]["adapted"]["proof"]["identity"]["source_sha256"] == verification["model_sha256"]
    assert "installed" not in record["states"]
    source = ROOT / f"vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/{module}.py"
    source_hash = sha256(source.read_bytes()).hexdigest()
    assert record["states"]["adapted"]["proof"]["identity"]["source_sha256"] == source_hash
    _, _, route = BATCH_A[dataset_id]
    document = read(ROOT / "contracts/openapi.json")
    path = "/api/v1/equity/" + route
    descriptor = _descriptor(document, path, "get", document["paths"][path]["get"], document["paths"][path])
    live_path = "artifacts/reviewed/fmp-expansion-a/live-matrix-verification.json"
    accepted = read(ROOT / live_path)
    assert accepted["task"] == "5.2" and accepted["status"] == "VERIFIED"
    for state in ("account_access", "real_data"):
        proof = record["states"][state]["proof"]
        assert record["states"][state]["status"] == "verified"
        assert proof["evidence_path"] == live_path
        assert proof["identity"]["source_sha256"] == source_hash
    assert record["states"]["real_data"]["proof"]["identity"]["contract_sha256"] == descriptor["contract_sha256"]["fmp"]
    assert record["states"]["future_ai"] == {"status": "unknown"}


def test_batch_a_widget_acceptance_is_four_scoped_models_and_stales_on_another_image():
    selected = {"AnalystEstimates", "RevenueGeographic", "IncomeStatementGrowth", "EquityQuote"}
    coverage = read(ROOT / "docs/reference/provider-coverage.json")
    models = {model: module for model, module, _ in BATCH_A.values()}
    records = {item["model"]: item for item in coverage["datasets"]
               if item["provider"] == "fmp" and item["model"] in models}
    assert len(records) == 11
    assert all(record["states"]["future_ai"] == {"status": "unknown"} for record in records.values())
    browser_path = "artifacts/reviewed/fmp-expansion-a/native-browser-verification.json"
    if not (ROOT / browser_path).exists():
        assert all(record["states"]["widget"] == {"status": "unknown"} for record in records.values())
        return  # No browser proof is fabricated to exercise the accepted-image branch.
    browser = read(ROOT / browser_path)
    assert browser["task"] == "5.3" and browser["status"] == "VERIFIED"
    image = browser["spec_updates"]["local_candidate_images"]["data-api"]
    assert {model for model, record in records.items() if record["states"]["widget"]["status"] == "verified"} == selected
    for model, record in records.items():
        if model not in selected:
            assert record["states"]["widget"] == {"status": "unknown"}
            continue
        proof = record["states"]["widget"]["proof"]
        assert proof["evidence_path"] == browser_path
        assert proof["identity"] == {**record["states"]["real_data"]["proof"]["identity"], "image_digest": image}
    document = read(ROOT / "contracts/openapi.json")
    hashes = {model: {"fmp": sha256((ROOT / f"vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/{module}.py").read_bytes()).hexdigest()}
              for model, module in models.items()}
    def projected(runtime_image):
        result = build_financial_catalog(document, coverage, source_revision=browser["api_commit"],
            generation_revision=browser["api_commit"], generated_at="2026-11-17T00:00:00+00:00",
            source_hashes=hashes, image_digest=runtime_image)
        return {item["dataset"]: item["coverage"]["fmp"] for item in result["datasets"] if item["dataset"] in models}
    current = projected(image)
    other = projected("sha256:" + ("0" if image != "sha256:" + "0" * 64 else "1") * 64)
    for model in models:
        assert current[model]["account_access"]["status"] == other[model]["account_access"]["status"] == "verified"
        assert current[model]["real_data"]["status"] == other[model]["real_data"]["status"] == "verified"
        assert other[model]["widget"]["status"] == ("stale" if model in selected else "unknown")
        assert current[model]["widget"]["status"] == ("verified" if model in selected else "unknown")

