"""Financial consumer snapshots retain installed contracts and editable queries."""
import json
import os
import re
from copy import deepcopy
from pathlib import Path

import pytest
from qopenbb_ci.catalog import canonical, digest, freeze_routes, generate, validate_refs
from qopenbb_ci.catalog_financial import resolve
from qopenbb_ci.catalog_upstream import widget_schema

ROOT = Path(__file__).resolve().parents[2]
EXTENSION = "x-qopenbb-financial"
BASELINE = {
    "company-profile": ("/api/v1/equity/profile", "fmp", "equity_profile_fmp_obb"),
    "annual-income": ("/api/v1/equity/fundamental/income", "fmp", "equity_fundamental_income_fmp_obb"),
    "gdp": ("/api/v1/economy/fred_series", "fred", "economy_fred_series_fred_obb"),
}
ACCEPTED = {
    "/api/v1/equity/profile": "fmp",
    "/api/v1/equity/fundamental/income": "fmp",
    "/api/v1/economy/fred_series": "fred",
    "/api/v1/equity/search": "fmp",
    "/api/v1/equity/compare/peers": "fmp",
    "/api/v1/equity/fundamental/balance": "fmp",
    "/api/v1/equity/fundamental/cash": "fmp",
    "/api/v1/equity/fundamental/metrics": "fmp",
    "/api/v1/equity/fundamental/ratios": "fmp",
    "/api/v1/equity/fundamental/enterprise_values": "fmp",
    "/api/v1/equity/price/historical": "fmp",
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def proposal():
    directory = Path(os.environ.get("QOPENBB_FINANCIAL_PROPOSAL", ROOT / "contracts"))
    return {name: read(directory / name) for name in (
        "datasets.json", "openapi.json", "routes.json", "widgets.json", "apps.json",
        "catalog-report.json", "provenance.json")}


def test_root_inventory_selects_all_eleven_accepted_models():
    datasets = read(ROOT / "contracts/datasets.json")["datasets"]
    assert len(datasets) == 11
    assert {item["path"]: item["provider"] for item in datasets} == ACCEPTED
    assert len({item["id"] for item in datasets}) == 11
    for dataset in datasets:
        assert dataset["parameters"]["provider"] == dataset["provider"]
    by_id = {item["id"]: item for item in datasets}
    for name, (path, provider, _) in BASELINE.items():
        assert by_id[name]["path"] == path
        assert by_id[name]["provider"] == provider
        assert by_id[name]["parameters"]["symbol"] == ("GDP" if provider == "fred" else "AAPL")
    assert by_id["annual-income"]["parameters"] == {
        "provider": "fmp", "symbol": "AAPL", "limit": 1, "period": "annual"}


def test_proposal_retains_baseline_widget_ids_and_complete_native_mapping(proposal):
    widgets = proposal["widgets.json"]
    datasets = proposal["datasets.json"]["datasets"]
    mapping = proposal["catalog-report.json"]["mapping"]
    assert len(widgets) == len(mapping) == len(datasets) == 11
    assert {item["path"]: item["provider"] for item in mapping} == ACCEPTED
    assert {item["dataset"] for item in mapping} == {item["id"] for item in datasets}
    for path, provider, widget_id in BASELINE.values():
        assert widgets[widget_id]["endpoint"] == path
        assert widgets[widget_id]["widgetId"] == widget_id
    for item in mapping:
        widget = widgets[item["widget"]]
        assert widget["endpoint"] == item["path"]
        assert widget["widgetId"] == item["widget"]
        provider = next(param for param in widget["params"] if param["paramName"] == "provider")
        assert provider["value"] == item["provider"]
        assert provider["options"] == [{"label": item["provider"].upper(), "value": item["provider"]}]
        assert widget["data"]["dataKey"] == "results"
        assert not {"results", "rows", "values"}.intersection(widget["data"])
        operation = proposal["openapi.json"]["paths"][item["path"]]["get"]
        variant = operation[EXTENSION]["variants"][item["provider"]]
        row = resolve(proposal["openapi.json"], variant["row_schema"])
        expected_fields = set(row.get("properties", {}))
        columns = widget["data"]["table"]["columnsDefs"]
        assert expected_fields
        assert {column["field"] for column in columns} == expected_fields


def test_frozen_proposal_retains_native_financial_semantics_and_references(proposal):
    schema = proposal["openapi.json"]
    routes = proposal["routes.json"]
    validate_refs(routes)
    assert routes == freeze_routes(schema, proposal["datasets.json"])
    assert len(routes["routes"]) == 11
    for route in routes["routes"]:
        operation = schema["paths"][route["path"]]["get"]
        descriptor = route[EXTENSION]
        assert descriptor == operation[EXTENSION]
        assert descriptor["metadata_location"] == "extra.results_metadata.__qopenbb_financial__"
        assert descriptor["metadata_schema"]["$ref"].startswith("#/components/schemas/")
        variant = descriptor["variants"][ACCEPTED[route["path"]]]
        for reference in (variant["query_schema"], variant["row_schema"], descriptor["response_schema"]):
            assert reference["$ref"].startswith("#/components/schemas/")
        assert variant["fields"]
        assert route["responses"] == operation["responses"]


@pytest.mark.parametrize("path", sorted(ACCEPTED))
def test_native_queries_accept_non_example_company_or_series(proposal, path):
    dataset = deepcopy(next(item for item in proposal["datasets.json"]["datasets"] if item["path"] == path))
    inventory = {"datasets": [dataset]}
    params = dataset["parameters"]
    if path.endswith("/search"):
        params["query"] = "Microsoft"
    else:
        params["symbol"] = "UNRATE" if ACCEPTED[path] == "fred" else "MSFT"
    if "period" in params:
        params["period"] = "quarter"
    if path.endswith("/historical"):
        params.update(start_date="2024-01-02", end_date="2024-01-31")
    frozen = freeze_routes(proposal["openapi.json"], inventory)
    assert len(frozen["routes"]) == 1
    regenerated = generate(proposal["openapi.json"], inventory, proposal["widgets.json"], [], "/data")
    mapping = next(item for item in regenerated["catalog-report.json"]["mapping"]
                   if item["dataset"] == dataset["id"])
    widget_params = {item["paramName"]: item
                     for item in regenerated["widgets.json"][mapping["widget"]]["params"]}
    assert params.keys() <= widget_params.keys()
    identity_parameter = "query" if path.endswith("/search") else "symbol"
    assert widget_params[identity_parameter].get("show", True) is True
    layout = regenerated["apps.json"][0]["tabs"]["Data"]["layout"]
    state = next(item["state"]["params"] for item in layout if item["i"] == mapping["widget"])
    assert state == params
    assert state.get("symbol", state.get("query")) not in {"AAPL", "GDP"}


@pytest.mark.parametrize("path,changes", [
    ("/api/v1/equity/fundamental/balance", {"period": "monthly"}),
    ("/api/v1/equity/fundamental/cash", {"limit": True}),
    ("/api/v1/equity/price/historical", {"start_date": "2024-02-30"}),
    ("/api/v1/equity/search", {"unknown_filter": "unsupported"}),
    ("/api/v1/equity/compare/peers", {"provider": "fred"}),
])
def test_proposal_rejects_unsupported_query_combinations(proposal, path, changes):
    dataset = deepcopy(next(item for item in proposal["datasets.json"]["datasets"] if item["path"] == path))
    inventory = {"datasets": [dataset]}
    dataset["parameters"].update(changes)
    with pytest.raises(ValueError):
        freeze_routes(proposal["openapi.json"], inventory)


def test_proposal_reproduction_preserves_values_metadata_and_source_identity(proposal):
    original = deepcopy(proposal)
    inputs = (proposal["openapi.json"], proposal["datasets.json"], proposal["widgets.json"], [], "/data")
    first = generate(*inputs)
    assert canonical(first) == canonical(generate(*inputs))
    assert first["widgets.json"] == proposal["widgets.json"]
    assert first["openapi.json"] == proposal["openapi.json"]
    assert proposal == original
    provenance = proposal["provenance.json"]
    assert provenance["repeat_identical"] is True
    assert provenance["inventory_sha256"] == digest(proposal["datasets.json"])
    assert re.fullmatch(r"[0-9a-f]{40}", provenance["revision"])
    assert provenance["image_labels"]["org.qopenbb.source.data_api"] == provenance["revision"]
    assert re.fullmatch(r"sha256:[0-9a-f]{64}", provenance["image"])
    assert provenance["generator"].endswith("widgets.py:build_json")
    assert provenance["files_sha256"]
    assert provenance["maintained_generator_sha256"]
    assert {"catalog.py", "catalog_financial.py", "catalog_upstream.py", "catalog_cli.py"} <= set(
        provenance["maintained_generator_sha256"])
    for checksum in [*provenance["files_sha256"].values(), *provenance["maintained_generator_sha256"].values()]:
        assert re.fullmatch(r"[0-9a-f]{64}", checksum)


@pytest.fixture
def composed_response():
    prefix = "#/components/schemas/"
    response = {"$ref": prefix + "FinancialResponse"}
    operation = {EXTENSION: {"response_schema": response}, "responses": {
        "200": {"content": {"application/json": {"schema": deepcopy(response)}}}},
        "widget_config": {"data": {"table": {"showAll": True}}}}
    return {"paths": {"/financial": {"get": operation}, "/legacy": {"get": {
        "responses": deepcopy(operation["responses"])}}}, "components": {"schemas": {
            "FinancialResponse": {"allOf": [{"$ref": prefix + "Envelope"}, {
                "type": "object", "properties": {"extra": {"type": "object"}}}]},
            "Envelope": {"type": "object", "properties": {"results": {
                "type": "array", "items": {"$ref": prefix + "FinancialRow"}}}},
            "FinancialRow": {"type": "object", "properties": {"value": {
                "type": ["number", "null"], "description": "Provider observation in USD.",
                "examples": [None, 0, 125.5]}}}}}}


def test_widget_bridge_preserves_served_contract_and_financial_values(composed_response):
    before = deepcopy(composed_response)
    adapted = widget_schema(composed_response)
    assert composed_response == before
    assert adapted["components"] == before["components"]
    assert adapted["paths"]["/legacy"] == before["paths"]["/legacy"]
    original = before["paths"]["/financial"]["get"]
    operation = adapted["paths"]["/financial"]["get"]
    assert operation[EXTENSION] == original[EXTENSION]
    envelope = operation["responses"]["200"]["content"]["application/json"]["schema"]
    assert envelope == {"type": "object", "properties": {
        "results": before["components"]["schemas"]["Envelope"]["properties"]["results"]}}
    assert operation["widget_config"]["data"] == {"dataKey": "results", "table": {"showAll": True}}
    assert canonical(adapted) == canonical(widget_schema(before))
    adapted["components"]["schemas"]["FinancialRow"]["properties"]["value"]["examples"] = [999]
    assert composed_response == before


@pytest.mark.parametrize("fault", ["cyclic", "missing", "external", "ambiguous", "absent"])
def test_widget_bridge_rejects_unresolvable_or_ambiguous_results(composed_response, fault):
    schemas = composed_response["components"]["schemas"]
    reference = {"$ref": "#/components/schemas/FinancialResponse"}
    if fault == "cyclic":
        schemas["Envelope"] = reference
    elif fault == "missing":
        del schemas["Envelope"]
    elif fault == "external":
        schemas["Envelope"] = {"$ref": "https://example.invalid/schema"}
    elif fault == "ambiguous":
        schemas["FinancialResponse"]["allOf"].append(deepcopy(schemas["Envelope"]))
    else:
        schemas["Envelope"]["properties"] = {}
    before = deepcopy(composed_response)
    with pytest.raises(ValueError):
        widget_schema(composed_response)
    assert composed_response == before
