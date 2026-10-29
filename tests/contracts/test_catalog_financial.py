"""Projected financial declarations survive freezing and fail closed on drift."""
from copy import deepcopy

import pytest
from qopenbb_ci.catalog import canonical, compatibility, freeze_routes

EXTENSION = "x-qopenbb-financial"
PREFIX = "#/components/schemas/"


@pytest.fixture
def projected():
    query = {"type": "object", "required": ["symbol"], "properties": {
        "symbol": {"type": "string", "minLength": 1},
        "limit": {"type": "integer", "minimum": 1, "maximum": 100, "default": 10},
        "period": {"type": "string", "enum": ["annual", "quarter"], "default": "annual"}}}
    fields = {"value": {"definition": "Reported amount", "unit": "USD", "value_origin": "provider_observation"}}
    variant = {"query_schema": {"$ref": PREFIX + "Query"}, "row_schema": {"$ref": PREFIX + "Row"},
               "fields": fields, "dynamic_fields": False, "runtime_properties": ["fields.unit"],
               "procedural_bounds": {"max_calendar_years": None, "max_symbols": 5},
               "response_policy": {"mode": "clip", "max_rows": None, "limit_parameter": "limit"}}
    descriptor = {"schema_version": 1, "dataset": "ReportedData", "providers": ["fmp"],
                  "provider_policy": "explicit", "variants": {"fmp": variant},
                  "metadata_location": "extra.results_metadata.__qopenbb_financial__",
                  "metadata_schema": {"$ref": PREFIX + "Metadata"},
                  "response_schema": {"$ref": PREFIX + "Response"},
                  "error_schema": {"$ref": PREFIX + "Error"}, "metadata_enforcement": "Fetcher validation"}
    schemas = {"Query": query, "Row": {"type": "object", "properties": {
        "value": {"type": ["number", "null"], "description": "Reported amount"}}},
        "Field": {"type": "object", "required": ["definition"], "properties": {
            "definition": {"type": "string", "minLength": 1}, "unit": {"type": ["string", "null"]}}},
        "Metadata": {"type": "object", "properties": {"fields": {
            "type": "object", "additionalProperties": {"$ref": PREFIX + "Field"}}}},
        "Response": {"type": "object"}, "Error": {"type": "object"}}
    parameters = [{"name": "provider", "in": "query", "required": True,
                   "schema": {"type": "string", "enum": ["fmp"]}}]
    parameters += [{"name": key, "in": "query", "required": key == "symbol", "schema": value}
                   for key, value in query["properties"].items()]
    operation = {"operationId": "reported_data", "parameters": parameters, EXTENSION: descriptor,
                 "responses": {"200": {"content": {"application/json": {
                     "schema": {"$ref": PREFIX + "Response"}}}}}}
    document = {"openapi": "3.1.0", "paths": {"/data": {"get": operation}}, "components": {"schemas": schemas}}
    inventory = {"datasets": [{"id": "amounts", "path": "/data", "provider": "fmp",
                               "parameters": {"provider": "fmp", "symbol": "AAPL", "limit": 10}}]}
    return document, inventory


def test_freeze_preserves_projection_without_mutation(projected):
    document, inventory = projected
    original = deepcopy(projected)
    first = freeze_routes(document, inventory)
    assert first["routes"][0][EXTENSION] == document["paths"]["/data"]["get"][EXTENSION]
    assert first["components"] == document["components"]
    assert canonical(first) == canonical(freeze_routes(document, inventory))
    first["routes"][0][EXTENSION]["variants"]["fmp"]["fields"]["value"]["unit"] = "changed"
    assert projected == original


@pytest.mark.parametrize("name,value", [("limit", "10"), ("limit", 101), ("limit", True),
                                        ("limit", float("nan")), ("period", "monthly"), ("symbol", "")])
def test_examples_obey_schema_constraints(projected, name, value):
    document, inventory = projected
    inventory["datasets"][0]["parameters"][name] = value
    with pytest.raises(ValueError):
        freeze_routes(document, inventory)


@pytest.mark.parametrize("mutation", ["provider", "variant", "policy", "version", "location", "fields", "definition", "bound"])
def test_invalid_descriptor_associations_are_rejected(projected, mutation):
    document, inventory = projected
    descriptor = document["paths"]["/data"]["get"][EXTENSION]
    variant = descriptor["variants"]["fmp"]
    if mutation == "provider":
        descriptor["providers"] = ["other"]
    elif mutation == "variant":
        descriptor["variants"] = {}
    elif mutation == "policy":
        document["paths"]["/data"]["get"]["parameters"][0]["required"] = False
    elif mutation == "version":
        descriptor["schema_version"] = 2
    elif mutation == "location":
        descriptor["metadata_location"] = "results"
    elif mutation == "fields":
        variant["fields"]["absent"] = variant["fields"].pop("value")
    elif mutation == "definition":
        variant["fields"]["value"]["definition"] = "Different meaning"
    else:
        variant["response_policy"]["limit_parameter"] = "absent"
    with pytest.raises(ValueError):
        freeze_routes(document, inventory)


@pytest.mark.parametrize("mutation", ["field", "default", "metadata", "reference", "policy"])
def test_descriptor_and_transitive_schema_drift_identifies_consumers(projected, mutation):
    document, inventory = projected
    before = freeze_routes(document, inventory)
    descriptor = document["paths"]["/data"]["get"][EXTENSION]
    if mutation == "field":
        descriptor["variants"]["fmp"]["fields"]["value"]["unit"] = "millions USD"
    elif mutation == "default":
        document["components"]["schemas"]["Query"]["properties"]["limit"]["default"] = 20
    elif mutation == "metadata":
        document["components"]["schemas"]["Field"]["properties"]["unit"]["description"] = "Effective units"
    elif mutation == "reference":
        document["components"]["schemas"]["Row2"] = deepcopy(document["components"]["schemas"]["Row"])
        descriptor["variants"]["fmp"]["row_schema"] = {"$ref": PREFIX + "Row2"}
    else:
        descriptor["variants"]["fmp"]["procedural_bounds"]["max_symbols"] = 3
    report = compatibility(before, freeze_routes(document, inventory))
    assert report["requires_revalidation"]
    assert EXTENSION in report["changes"][0]["fields"]
    assert report["affected_consumers"] == ["workspace", "agent", "future-excel"]


def test_failure_does_not_echo_supplied_values_or_keys(projected):
    document, inventory = projected
    inventory["datasets"][0]["parameters"]["private_canary_key"] = "private_canary_value"
    with pytest.raises(ValueError) as error:
        freeze_routes(document, inventory)
    assert "private_canary" not in str(error.value)


def test_external_reference_failure_is_safe(projected):
    document, inventory = projected
    document["components"]["schemas"]["Query"] = {"$ref": "https://private_canary.invalid/schema"}
    with pytest.raises(ValueError) as error:
        freeze_routes(document, inventory)
    assert "private_canary" not in str(error.value)


@pytest.mark.parametrize("value", ["2026-02-30", "not-a-date"])
def test_formats_and_referenced_query_constraints_are_enforced(projected, value):
    document, inventory = projected
    schemas = document["components"]["schemas"]
    schemas["Query"]["properties"]["start_date"] = {"type": "string", "format": "date"}
    document["paths"]["/data"]["get"]["parameters"].append({
        "in": "query", "name": "start_date", "schema": schemas["Query"]["properties"]["start_date"]})
    inventory["datasets"][0]["parameters"]["start_date"] = value
    with pytest.raises(ValueError):
        freeze_routes(document, inventory)


def test_inherited_parameter_refs_and_operation_overrides(projected):
    document, inventory = projected
    path = document["paths"]["/data"]
    provider = path["get"]["parameters"].pop(0)
    document["components"]["parameters"] = {"Provider": provider}
    path["parameters"] = [{"$ref": "#/components/parameters/Provider"}]
    frozen = freeze_routes(document, inventory)
    assert frozen["routes"][0]["parameters"][0] == provider
    assert frozen["routes"][0][EXTENSION]["providers"] == ["fmp"]


def test_dynamic_fred_semantics_remain_unknown_without_invention(projected):
    document, inventory = projected
    variant = document["paths"]["/data"]["get"][EXTENSION]["variants"]["fmp"]
    variant["dynamic_fields"] = True
    variant["fields"]["value"]["unit"] = None
    variant["fields"]["value"]["requested_transform"] = "unsupported_transform"
    frozen = freeze_routes(document, inventory)["routes"][0][EXTENSION]["variants"]["fmp"]
    assert frozen["dynamic_fields"] is True
    assert frozen["fields"]["value"]["unit"] is None
    assert frozen["fields"]["value"]["requested_transform"] == "unsupported_transform"


def test_referenced_query_schema_examples_use_combinator_constraints(projected):
    document, inventory = projected
    schemas = document["components"]["schemas"]
    schemas["Query"]["properties"]["symbol"] = {"allOf": [
        {"type": "string"}, {"pattern": "^[A-Z]+$"}], "not": {"const": "BAD"}}
    inventory["datasets"][0]["parameters"]["symbol"] = "BAD"
    with pytest.raises(ValueError):
        freeze_routes(document, inventory)


def test_invalid_default_inside_projected_query_is_rejected(projected):
    document, inventory = projected
    document["components"]["schemas"]["Query"]["properties"]["period"]["default"] = "monthly"
    # The public parameter schema is independent from the projected model.
    document["paths"]["/data"]["get"]["parameters"][3]["schema"] = {
        "type": "string", "enum": ["annual", "quarter"], "default": "annual"}
    with pytest.raises(ValueError):
        freeze_routes(document, inventory)


@pytest.mark.parametrize("value", [None, {}, [], "private_canary_value"])
def test_malformed_extension_is_rejected_safely(projected, value):
    document, inventory = projected
    document["paths"]["/data"]["get"][EXTENSION] = value
    with pytest.raises(ValueError) as error:
        freeze_routes(document, inventory)
    assert "private_canary" not in str(error.value)


def test_legacy_route_output_retains_original_parameter_reference(projected):
    document, inventory = projected
    operation = document["paths"]["/data"]["get"]
    operation.pop(EXTENSION)
    document["components"]["parameters"] = {"Provider": operation["parameters"][0]}
    operation["parameters"][0] = {"$ref": "#/components/parameters/Provider"}
    frozen = freeze_routes(document, inventory)
    assert frozen["routes"][0] == {"dataset": "amounts", "method": "GET", "path": "/data", **operation}


def test_baseline_default_and_additional_provider_remain_discoverable(projected):
    document, inventory = projected
    operation = document["paths"]["/data"]["get"]
    descriptor = operation[EXTENSION]
    descriptor["provider_policy"] = "baseline_default"
    descriptor["providers"].append("other")
    descriptor["variants"]["other"] = deepcopy(descriptor["variants"]["fmp"])
    descriptor["variants"]["other"]["fields"]["value"]["unit"] = "provider-specific units"
    provider = operation["parameters"][0]
    provider["required"] = False
    provider["schema"].update(enum=["fmp", "other"], default="fmp")
    inventory["datasets"][0]["parameters"].update(limit=100, period="quarter")
    frozen = freeze_routes(document, inventory)
    assert frozen["routes"][0][EXTENSION] == descriptor
    assert frozen["routes"][0]["parameters"][0]["schema"]["default"] == "fmp"


def test_unreferenced_schema_change_does_not_invalidate_consumers(projected):
    document, inventory = projected
    before = freeze_routes(document, inventory)
    document["components"]["schemas"]["Unrelated"] = {"type": "string"}
    report = compatibility(before, freeze_routes(document, inventory))
    assert report == {"requires_revalidation": False, "changes": [], "affected_consumers": []}


def test_missing_dataset_route_does_not_echo_supplied_path(projected):
    document, inventory = projected
    inventory["datasets"][0]["path"] = "/private_canary_value"
    with pytest.raises(ValueError) as error:
        freeze_routes(document, inventory)
    assert "private_canary" not in str(error.value)


@pytest.mark.parametrize("property_name,valid", [("unit", True), ("absent", False)])
def test_identifier_field_map_uses_native_pattern_properties(projected, property_name, valid):
    document, inventory = projected
    # Pydantic emits patternProperties for the authoritative Identifier-keyed map.
    document["components"]["schemas"]["Metadata"]["properties"]["fields"] = {
        "type": "object", "patternProperties": {
            "^[A-Za-z0-9_./-]+$": {"$ref": PREFIX + "Field"}}}
    variant = document["paths"]["/data"]["get"][EXTENSION]["variants"]["fmp"]
    variant["runtime_properties"] = ["fields." + property_name]
    if valid:
        frozen = freeze_routes(document, inventory)
        assert frozen["routes"][0][EXTENSION]["variants"]["fmp"]["runtime_properties"] == ["fields.unit"]
    else:
        with pytest.raises(ValueError, match="Invalid projected financial contract"):
            freeze_routes(document, inventory)
