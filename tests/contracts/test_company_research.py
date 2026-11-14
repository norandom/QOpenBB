"""Curated research layout preserves parameter boundaries and research storage."""
from copy import deepcopy
import json
from pathlib import Path

import pytest

from qopenbb_ci.catalog import canonical, generate

ROOT = Path(__file__).resolve().parents[2]
PRIMARY = {
    "company-profile": "equity_profile_fmp_obb",
    "annual-income": "equity_fundamental_income_fmp_obb",
    "annual-balance-sheet": "equity_fundamental_balance_fmp_obb",
    "annual-cash-flow": "equity_fundamental_cash_fmp_obb",
    "daily-prices": "equity_price_historical_fmp_obb",
}
STATEMENTS = {PRIMARY[key] for key in ("annual-income", "annual-balance-sheet", "annual-cash-flow")}


@pytest.fixture
def inputs():
    return tuple(json.loads((ROOT / "contracts" / name).read_text())
                 for name in ("openapi.json", "datasets.json", "widgets.json", "apps.json"))


def research(output):
    return next(app for app in output["apps.json"] if app["name"] == "Company Research")


def test_research_composition_and_frozen_renderer(inputs):
    output = generate(*inputs, "/data")
    app = research(output)
    items = app["tabs"]["Research"]["layout"]
    assert [item["i"] for item in items] == [*PRIMARY.values(), "company_research"]
    assert app["allowCustomization"] is True
    assert "Apple Inc." in app["description"] and "AAPL" in app["description"]
    widget = output["widgets.json"]["company_research"]
    assert widget["widgetId"] == widget["type"] == "company_research"
    assert "endpoint" not in widget
    assert widget["name"] == "Peer Research"
    assert all(item["w"] > 0 and item["h"] > 0 for item in items)
    for index, item in enumerate(items):
        for previous in items[:index]:
            assert (item["x"] >= previous["x"] + previous["w"]
                    or previous["x"] >= item["x"] + item["w"]
                    or item["y"] >= previous["y"] + previous["h"]
                    or previous["y"] >= item["y"] + item["h"])


def test_only_primary_tables_share_symbol_and_only_statements_share_period(inputs):
    output = generate(*inputs, "/data")
    app = research(output)
    assert app["groups"] == [
        {"name": "Symbol", "type": "param", "paramName": "symbol", "defaultValue": "AAPL"},
        {"name": "Statement period", "type": "param", "paramName": "period", "defaultValue": "annual"},
    ]
    items = app["tabs"]["Research"]["layout"]
    assert {i["i"] for i in items if "Symbol" in i.get("groups", [])} == set(PRIMARY.values())
    assert {i["i"] for i in items if "Statement period" in i.get("groups", [])} == STATEMENTS
    for item in items:
        if item["i"] in PRIMARY.values():
            assert item["state"]["params"]["symbol"] == "AAPL"
        if item["i"] in STATEMENTS:
            assert item["state"]["params"]["period"] == "annual"
            assert item["state"]["params"]["limit"] == 3
    price = next(i for i in items if i["i"] == PRIMARY["daily-prices"])
    assert price["state"]["params"]["start_date"] == "2025-01-02"
    assert price["state"]["params"]["end_date"] == "2025-01-31"
    assert not any("date" in group["paramName"] for group in app["groups"])


def test_peer_storage_survives_direct_append_and_inputs_remain_unchanged(inputs):
    before = deepcopy(inputs)
    first = generate(*inputs, "/data")
    peer = research(first)["tabs"]["Research"]["layout"][-1]
    assert peer.get("groups", []) == []
    assert peer["state"] == {"storage": {"companyResearch": {
        "version": 1, "peers": [], "period": "annual", "limit": 3}}}
    assert canonical(first) == canonical(generate(*inputs, "/data"))
    assert inputs == before
    assert not any(item.get("widget") == "company_research"
                   for item in first["catalog-report.json"]["omitted"])
    assert len(first["apps.json"]) == len(inputs[3]) + 2
    assert set(inputs[2]) <= first["widgets.json"].keys()


@pytest.mark.parametrize("widget_id", PRIMARY.values())
def test_ineligible_primary_renderer_rejected(inputs, widget_id):
    inputs[2][widget_id]["type"] = "chart"
    with pytest.raises(ValueError, match="research.*table"):
        generate(*inputs, "/data")


def test_partial_inventory_reports_missing_research_capability(inputs):
    inputs[1]["datasets"] = inputs[1]["datasets"][:1]
    output = generate(*inputs, "/data")
    assert not any(app["name"] == "Company Research" for app in output["apps.json"])
    status = output["catalog-report.json"]["company_research"]
    assert status["status"] == "unavailable"
    assert set(status["missing_datasets"]) == set(PRIMARY) - {"company-profile"}
    assert "company_research" not in output["widgets.json"]
