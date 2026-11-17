"""Batch A consumer inputs preserve the accepted native financial contracts."""
import json
from datetime import date
from pathlib import Path

import pytest
from qopenbb_ci.catalog_financial import resolve

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
def test_batch_a_coverage_separates_adapter_evidence_from_unverified_consumers(dataset_id):
    model, module, _ = BATCH_A[dataset_id]
    coverage = read(ROOT / "docs/reference/provider-coverage.json")
    record, = [item for item in coverage["datasets"] if (item["model"], item["provider"]) == (model, "fmp")]
    for state in ("documented", "retained_source", "adapted"):
        proof = record["states"][state]
        assert proof["status"] == "verified"
        assert (ROOT / proof["proof"]["evidence_path"]).is_file()
    verification = read(ROOT / f"artifacts/reviewed/fmp-expansion-a/{dataset_id}-verification.json")
    assert record["states"]["adapted"]["proof"]["identity"]["source_sha256"] == verification["model_sha256"]
    assert "installed" not in record["states"]
    for state in ("account_access", "real_data", "widget", "future_ai"):
        assert record["states"].get(state, {"status": "unknown"}) == {"status": "unknown"}

