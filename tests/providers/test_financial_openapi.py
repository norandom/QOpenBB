"""Fixture contracts for additive financial OpenAPI projection."""

from copy import deepcopy
from types import SimpleNamespace
from typing import ClassVar, Literal

import pytest
from fastapi import APIRouter
from openbb_core.app.provider_interface import ProviderInterface
from openbb_core.provider.standard_models.financial_annotations import (
    FinancialDataAnnotation,
    FinancialFieldTemplate,
    FinancialQueryAnnotation,
    InvalidFinancialAnnotation,
    MissingFinancialAnnotation,
    ResponsePolicy,
)
from pydantic import BaseModel, Field
from qopenbb_data.financial_openapi import project_financial_openapi


class Query(BaseModel):
    financial_query_annotation: ClassVar = FinancialQueryAnnotation(
        provider_policy="explicit", response_policy=ResponsePolicy(mode="provider")
    )
    period: Literal["annual", "quarter"] = Field(default="annual", alias="providerPeriod")
    limit: int = Field(default=12, ge=0, le=100)


class Row(BaseModel):
    financial_data_annotation: ClassVar = FinancialDataAnnotation(
        fields={"ev_to_ebitda": FinancialFieldTemplate()},
        runtime_properties=["fields.valuation_date_field"],
    )
    ev_to_ebitda: float = Field(alias="evToEBITDA", description="Provider enterprise multiple")


@pytest.fixture
def source():
    router = APIRouter()

    @router.get("/prices", openapi_extra={"model": "Prices"}, response_model_by_alias=False)
    def prices():
        return []

    registry = SimpleNamespace(original_models={"Prices": {
        "fmp": {"query": Query, "data": Row, "results_type": list},
    }})
    document = {"openapi": "3.1.0", "paths": {"/prices": {"get": {
        "operationId": "prices", "parameters": [{"name": "provider", "in": "query",
            "schema": {"enum": ["fmp"], "default": "fmp"}}],
        "responses": {"200": {"description": "Native", "content": {
            "application/json": {"schema": {"$ref": "#/components/schemas/Native"}}
        }}}}}, "/health": {"get": {"responses": {}}}},
        "components": {"schemas": {"Native": {"type": "object",
            "properties": {"results": {"type": "array"}, "extra": {"type": "object"}}}}}}
    return document, router.routes, registry


def project(source):
    return project_financial_openapi(*source, required_models={"Prices"})


def refs(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "$ref":
                yield item
            else:
                yield from refs(item)
    elif isinstance(value, list):
        for item in value:
            yield from refs(item)


def test_projection_is_deterministic_idempotent_and_nonmutating(source):
    before = deepcopy(source[0])
    declarations = Row.financial_data_annotation.model_dump()
    result = project(source)
    assert source[0] == before
    assert Row.financial_data_annotation.model_dump() == declarations
    assert result == project(source)
    assert result == project((result, *source[1:]))
    assert result["paths"]["/health"] == before["paths"]["/health"]
    assert result["components"]["schemas"]["Native"] == before["components"]["schemas"]["Native"]
    for ref in refs(result):
        assert ref.startswith("#/components/schemas/")
        assert ref.removeprefix("#/components/schemas/") in result["components"]["schemas"]


def test_descriptor_derives_models_aliases_choices_and_unknowns(source):
    result = project(source)
    operation = result["paths"]["/prices"]["get"]
    descriptor = operation["x-qopenbb-financial"]
    assert descriptor["metadata_location"] == "extra.results_metadata.__qopenbb_financial__"
    assert descriptor["provider_policy"] == "explicit"
    assert descriptor["providers"] == ["fmp"]
    variant = descriptor["variants"]["fmp"]
    assert variant["fields"]["ev_to_ebitda"]["unit"] is None
    assert variant["fields"]["ev_to_ebitda"]["definition"] == "Provider enterprise multiple"
    assert variant["fields"]["ev_to_ebitda"]["value_origin"] == "unknown"
    query = result["components"]["schemas"][variant["query_schema"]["$ref"].split("/")[-1]]
    assert query["properties"]["providerPeriod"]["enum"] == ["annual", "quarter"]
    native = ProviderInterface._create_field("period", Query.model_fields["period"], query=True)
    assert native.default.alias == "providerPeriod"
    assert query["properties"]["limit"]["default"] == 12
    assert query["properties"]["limit"]["maximum"] == 100
    row = result["components"]["schemas"][variant["row_schema"]["$ref"].split("/")[-1]]
    assert set(row["properties"]) == {"ev_to_ebitda"}
    assert Row(evToEBITDA=12).model_dump(by_alias=False) == {"ev_to_ebitda": 12}
    assert operation["parameters"][0]["required"] is True
    assert "default" not in operation["parameters"][0]["schema"]
    response = operation["responses"]["200"]["content"]["application/json"]["schema"]
    assert response["$ref"] == descriptor["response_schema"]["$ref"]
    envelope = result["components"]["schemas"][response["$ref"].split("/")[-1]]
    assert envelope["allOf"][0] == {"$ref": "#/components/schemas/Native"}
    extra = envelope["allOf"][1]["properties"]["extra"]
    assert extra["properties"]["results_metadata"]["properties"]["__qopenbb_financial__"] == descriptor["metadata_schema"]


def test_missing_annotations_and_required_associations_fail(source):
    class Missing(BaseModel):
        value: float

    source[2].original_models["Prices"]["fmp"]["data"] = Missing
    with pytest.raises(MissingFinancialAnnotation):
        project(source)
    with pytest.raises(InvalidFinancialAnnotation):
        project_financial_openapi(*source, required_models={"NotMounted"})


def test_invalid_annotations_and_variant_policy_disagreement_fail(source):
    class Bad(Row):
        financial_data_annotation: ClassVar = "bad"

    source[2].original_models["Prices"]["fmp"]["data"] = Bad
    with pytest.raises(InvalidFinancialAnnotation):
        project(source)
    source[2].original_models["Prices"]["fmp"]["data"] = Row

    class Baseline(Query):
        financial_query_annotation: ClassVar = FinancialQueryAnnotation(
            provider_policy="baseline_default", response_policy=ResponsePolicy(mode="provider")
        )

    source[2].original_models["Prices"]["other"] = {
        "query": Baseline, "data": Row, "results_type": list,
    }
    with pytest.raises(InvalidFinancialAnnotation, match="policy"):
        project(source)


def test_dynamic_fields_remain_runtime_owned_and_baseline_default_survives(source):
    class Dynamic(BaseModel):
        financial_data_annotation: ClassVar = FinancialDataAnnotation(
            dynamic_fields=True, runtime_properties=["fields", "observation_provenance"]
        )

    class Baseline(Query):
        financial_query_annotation: ClassVar = FinancialQueryAnnotation(
            provider_policy="baseline_default", response_policy=ResponsePolicy(mode="provider")
        )

    source[2].original_models["Prices"]["fmp"].update(query=Baseline, data=Dynamic)
    operation = project(source)["paths"]["/prices"]["get"]
    variant = operation["x-qopenbb-financial"]["variants"]["fmp"]
    assert variant["dynamic_fields"] is True
    assert variant["fields"] == {}
    assert variant["runtime_properties"] == ["fields", "observation_provenance"]
    assert operation["parameters"][0]["schema"]["default"] == "fmp"


def test_component_collision_fails_without_overwriting(source):
    result = project(source)
    name = next(key for key in result["components"]["schemas"] if key.startswith("QOpenBBFinancial"))
    source[0]["components"]["schemas"][name] = {"type": "boolean"}
    with pytest.raises(InvalidFinancialAnnotation, match="collision"):
        project(source)


def test_missing_registry_and_document_operations_fail(source):
    source[2].original_models.clear()
    with pytest.raises(InvalidFinancialAnnotation, match="variants"):
        project(source)
    source[2].original_models["Prices"] = {"fmp": {"query": Query, "data": Row}}
    source[0]["paths"]["/prices"].clear()
    with pytest.raises(InvalidFinancialAnnotation, match="operation"):
        project(source)


def test_serialized_field_template_mismatch_fails(source):
    class Bad(Row):
        financial_data_annotation: ClassVar = FinancialDataAnnotation(
            fields={"evToEBITDA": FinancialFieldTemplate()}
        )

    source[2].original_models["Prices"]["fmp"]["data"] = Bad
    with pytest.raises(InvalidFinancialAnnotation, match="canonical"):
        project(source)


def test_provider_reference_and_path_parameter_are_copied(source):
    parameter = source[0]["paths"]["/prices"]["get"].pop("parameters")[0]
    source[0]["components"]["parameters"] = {"Provider": parameter}
    source[0]["paths"]["/prices"]["parameters"] = [{"$ref": "#/components/parameters/Provider"}]
    result = project(source)
    assert result["components"]["parameters"]["Provider"] == parameter
    operation = result["paths"]["/prices"]["get"]
    assert operation["parameters"][0]["required"] is True
    assert result["paths"]["/prices"]["parameters"] == source[0]["paths"]["/prices"]["parameters"]


def test_namespaced_nested_definitions_do_not_replace_native_components(source):
    class Nested(BaseModel):
        amount: float

    class Structured(Row):
        financial_data_annotation: ClassVar = FinancialDataAnnotation(
            fields={"ev_to_ebitda": FinancialFieldTemplate(), "nested": FinancialFieldTemplate()}
        )
        nested: Nested = Field(description="Structured provider observation")

    source[2].original_models["Prices"]["fmp"]["data"] = Structured
    source[0]["components"]["schemas"]["Nested"] = {"type": "boolean"}
    result = project(source)
    assert result["components"]["schemas"]["Nested"] == {"type": "boolean"}
    assert all(not ref.startswith("#/$defs/") for ref in refs(result))
    for ref in refs(result):
        assert ref.split("/")[-1] in result["components"]["schemas"]


def test_unrelated_model_without_annotation_is_preserved(source):
    source[1].append(SimpleNamespace(openapi_extra={"model": "Foreign"}, path="/health", methods={"GET"}))
    assert project(source)["paths"]["/health"] == source[0]["paths"]["/health"]
    assert project_financial_openapi(*source, required_models=set()) == source[0]


def test_error_contract_preserves_existing_response_definitions(source):
    source[0]["paths"]["/prices"]["get"]["responses"]["422"] = {"description": "Native request error"}
    result = project(source)
    operation = result["paths"]["/prices"]["get"]
    assert operation["responses"]["422"] == {"description": "Native request error"}
    reference = operation["x-qopenbb-financial"]["error_schema"]["$ref"]
    error = result["components"]["schemas"][reference.split("/")[-1]]
    assert "invalid_response" in error["properties"]["code"]["enum"]
    assert "handler installation is separate" in error["description"]


@pytest.mark.parametrize("mode", [True, None, "false"])
def test_unsupported_or_unknown_route_serialization_fails(source, mode):
    source[1][0].response_model_by_alias = mode
    with pytest.raises(InvalidFinancialAnnotation, match="response_model_by_alias"):
        project(source)


def test_missing_route_serialization_flag_fails(source):
    del source[1][0].response_model_by_alias
    with pytest.raises(InvalidFinancialAnnotation, match="response_model_by_alias"):
        project(source)


def test_unresolvable_aliased_query_bound_fails(source):
    class AliasedLimit(Query):
        financial_query_annotation: ClassVar = FinancialQueryAnnotation(
            provider_policy="explicit",
            response_policy=ResponsePolicy(mode="clip", limit_parameter="limit"),
        )
        limit: int = Field(default=12, alias="providerLimit")

    source[2].original_models["Prices"]["fmp"]["query"] = AliasedLimit
    with pytest.raises(InvalidFinancialAnnotation, match="public parameter reference"):
        project(source)


def _native_result_properties(document, schema):
    """Follow every success-schema branch, including native allOf constraints."""
    if "$ref" in schema:
        schema = document["components"]["schemas"][schema["$ref"].split("/")[-1]]
    if "results" in schema.get("properties", {}):
        yield from _native_row_properties(document, schema["properties"]["results"])
    for kind in ("allOf", "anyOf", "oneOf"):
        for branch in schema.get(kind, []):
            yield from _native_result_properties(document, branch)


def _native_row_properties(document, schema):
    if "$ref" in schema:
        schema = document["components"]["schemas"][schema["$ref"].split("/")[-1]]
    if schema.get("type") == "array":
        yield from _native_row_properties(document, schema["items"])
    elif "properties" in schema:
        yield set(schema["properties"])
    for kind in ("allOf", "anyOf", "oneOf"):
        for branch in schema.get(kind, []):
            yield from _native_row_properties(document, branch)


def test_installed_native_baseline_associations_and_success_rows():
    from openbb_core.api.rest_api import app
    from openbb_core.app.route_iter import iter_api_routes
    from openbb_core.provider.registry_map import RegistryMap
    from openbb_core.provider.standard_models.financial_annotations import (
        bind_data_annotation,
    )

    registry = RegistryMap()
    interface = ProviderInterface()
    required = {"EquityInfo", "IncomeStatement", "FredSeries"}
    routes = [route for route in iter_api_routes(app)
              if (getattr(route, "openapi_extra", None) or {}).get("model") in required]
    assert {route.openapi_extra["model"] for route in routes} == required
    document = project_financial_openapi(app.openapi(), routes, registry, required_models=required)
    for route in routes:
        dataset = route.openapi_extra["model"]
        assert route.response_model is interface.return_annotations[dataset]
        operation = document["paths"][route.path]["get"]
        descriptor = operation["x-qopenbb-financial"]
        assert descriptor["provider_policy"] == "baseline_default"
        assert set(descriptor["variants"]) == set(registry.original_models[dataset])
        for provider, models in registry.original_models[dataset].items():
            annotation = bind_data_annotation(models["data"])
            assert set(descriptor["variants"][provider]["fields"]) == set(annotation.fields)
            canonical = set(models["data"].model_json_schema(by_alias=False, mode="serialization")["properties"])
            success = operation["responses"]["200"]["content"]["application/json"]["schema"]
            branches = list(_native_result_properties(document, success))
            assert branches, dataset
            assert all(fields == canonical for fields in branches), (dataset, branches, canonical)


@pytest.fixture
def native_first_batch():
    from importlib import import_module

    from fastapi import FastAPI
    from openbb_core.provider.abstract.provider import Provider
    from openbb_core.provider.registry import Registry
    from openbb_core.provider.registry_map import RegistryMap

    names = {
        "EquityInfo": ("equity_profile", "FMPEquityProfileFetcher"),
        "IncomeStatement": ("income_statement", "FMPIncomeStatementFetcher"),
        "BalanceSheet": ("balance_sheet", "FMPBalanceSheetFetcher"),
        "CashFlowStatement": ("cash_flow", "FMPCashFlowStatementFetcher"),
        "EquitySearch": ("equity_search", "FMPEquitySearchFetcher"),
        "EquityPeers": ("equity_peers", "FMPEquityPeersFetcher"),
        "EquityHistorical": ("equity_historical", "FMPEquityHistoricalFetcher"),
        "KeyMetrics": ("key_metrics", "FMPKeyMetricsFetcher"),
        "FinancialRatios": ("financial_ratios", "FMPFinancialRatiosFetcher"),
        "EnterpriseValues": ("enterprise_values", "FMPEnterpriseValuesFetcher"),
    }
    fetchers = {name: getattr(import_module("openbb_fmp.models." + module), cls)
                for name, (module, cls) in names.items()}
    from openbb_fred.models.series import FredSeriesFetcher
    registry = Registry()
    registry.include_provider(Provider(name="fmp", description="Isolated accepted classes", fetcher_dict=fetchers))
    registry.include_provider(Provider(name="fred", description="Isolated dynamic series", fetcher_dict={"FredSeries": FredSeriesFetcher}))
    mapping = RegistryMap(registry)
    # Bypass only singleton caching; execute the real native schema assembly.
    interface = object.__new__(ProviderInterface)
    ProviderInterface.__init__(interface, mapping)
    app = FastAPI()
    for dataset, response in interface.return_annotations.items():
        def endpoint(provider: str):
            return []
        app.add_api_route("/" + dataset, endpoint, response_model=response,
                          response_model_by_alias=False, openapi_extra={"model": dataset})
    return app, mapping, fetchers


def test_native_first_batch_registry_projection(native_first_batch):
    from openbb_core.provider.standard_models.financial_annotations import (
        bind_data_annotation,
        bind_query_annotation,
    )

    app, mapping, _ = native_first_batch
    required = set(mapping.original_models)
    assert len(required) == 11 and "EnterpriseValues" in required
    document = project_financial_openapi(app.openapi(), app.routes, mapping, required_models=required)
    for dataset, variants in mapping.original_models.items():
        operation = document["paths"]["/" + dataset]["get"]
        descriptor = operation["x-qopenbb-financial"]
        for provider, models in variants.items():
            # Installed byte identity belongs to discovery tests; projection must
            # work with the same provider classes in wheels and source checkouts.
            assert models["data"].__module__.startswith(f"openbb_{provider}.models.")
            data = bind_data_annotation(models["data"])
            query = bind_query_annotation(models["query"])
            variant = descriptor["variants"][provider]
            assert descriptor["provider_policy"] == query.provider_policy
            assert variant["response_policy"] == query.response_policy.model_dump(mode="json")
            assert variant["procedural_bounds"] == query.procedural_bounds.model_dump(mode="json")
            canonical = set(models["data"].model_json_schema(by_alias=False, mode="serialization")["properties"])
            assert set(variant["fields"]) == set(data.fields) == canonical
            assert variant["dynamic_fields"] is (provider == "fred")
            success = operation["responses"]["200"]["content"]["application/json"]["schema"]
            branches = list(_native_result_properties(document, success))
            assert branches, dataset
            assert all(fields == canonical for fields in branches), dataset
    for reference in refs(document):
        assert reference.split("/")[-1] in document["components"]["schemas"]


@pytest.mark.parametrize("dataset", ["KeyMetrics", "EnterpriseValues", "FredSeries"])
def test_native_serialized_financial_metadata_agrees(native_first_batch, dataset):
    import asyncio
    import json
    from datetime import UTC, datetime

    from openbb_core.app.model.obbject import OBBject
    from openbb_core.provider.standard_models.financial_metadata import (
        FinancialResultMetadata,
    )
    from openbb_fmp.utils.helpers import FMPAcquisition

    app, mapping, fetchers = native_first_batch
    stamp = datetime(2024, 2, 3, tzinfo=UTC)
    if dataset == "FredSeries":
        from openbb_fred.models.series import FredSeriesFetcher
        fetcher = FredSeriesFetcher
        query = fetcher.transform_query({"symbol": "GDP", "transform": "pch"})
        raw = [{"GDP": {"title": "Gross domestic product", "units": "Billions of Dollars",
                         "frequency": "Quarterly", "seasonal_adjustment": "Seasonally Adjusted",
                         "notes": None, "data": {"2023-12-31": 0.0},
                         "_retrieved_at": stamp, "_provenance": {}}}]
    else:
        fetcher = fetchers[dataset]
        query = fetcher.transform_query({"symbol": "ABC"})
        raw = FMPAcquisition([{"symbol": "ABC", "date": "2023-12-31", "period": "FY",
                               "fiscalYear": "2023", "reportedCurrency": "EUR",
                               "marketCap": 100, "evToEBITDA": 0, "stockPrice": 0,
                               "numberOfShares": 10, "enterpriseValue": -7}], stamp)
    result = fetcher.transform_data(query, raw)

    class ExecutedQuery:
        async def execute(self):
            return result

    native = asyncio.run(OBBject.from_query(ExecutedQuery()))
    body = json.loads(native.model_dump_json(by_alias=False))
    metadata = body["extra"]["results_metadata"]["__qopenbb_financial__"]
    restored = FinancialResultMetadata.model_validate(metadata)
    assert restored.retrieved_at == stamp
    assert body["results"] == [row.model_dump(mode="json", by_alias=False) for row in result.result]
    document = project_financial_openapi(app.openapi(), app.routes, mapping,
                                         required_models=set(mapping.original_models))
    descriptor = document["paths"]["/" + dataset]["get"]["x-qopenbb-financial"]
    provider = "fred" if dataset == "FredSeries" else "fmp"
    fields = descriptor["variants"][provider]["fields"]
    if provider == "fred":
        assert set(fields) == {"date"} and set(metadata["fields"]) == {"GDP"}
        assert metadata["fields"]["GDP"]["unit"] == "Percent Change"
        assert metadata["fields"]["GDP"]["source_unit"] == "Billions of Dollars"
        assert body["extra"]["results_metadata"]["GDP"]["units"] == "Billions of Dollars"
    else:
        assert set(fields) == set(metadata["fields"])
        for name, template in fields.items():
            for key in ("unit", "scale", "value_origin", "financial_basis"):
                assert metadata["fields"][name][key] == template[key], (dataset, name, key)


def test_native_typed_projection_is_repeatable_and_preserves_native_components(native_first_batch):
    app, mapping, _ = native_first_batch
    before = deepcopy(app.openapi())
    required = set(mapping.original_models)
    result = project_financial_openapi(before, app.routes, mapping, required_models=required)
    assert before == app.openapi()
    assert result == project_financial_openapi(before, app.routes, mapping, required_models=required)
    assert result == project_financial_openapi(result, app.routes, mapping, required_models=required)
    for name, schema in before["components"]["schemas"].items():
        assert result["components"]["schemas"][name] == schema
    route = next(route for route in app.routes if getattr(route, "path", None) == "/KeyMetrics")
    response = result["paths"][route.path]["get"]["responses"]["200"]["content"]["application/json"]["schema"]
    component = result["components"]["schemas"][response["$ref"].split("/")[-1]]
    component["allOf"][0] = before["paths"][route.path]["get"]["responses"]["200"]["content"]["application/json"]["schema"]
    with pytest.raises(InvalidFinancialAnnotation, match="collision"):
        project_financial_openapi(result, app.routes, mapping, required_models=required)


def test_native_missing_real_declaration_and_unsupported_response_fail(native_first_batch, monkeypatch):
    app, mapping, _ = native_first_batch
    required = set(mapping.original_models)
    models = mapping.original_models["EnterpriseValues"]["fmp"]
    monkeypatch.delattr(models["data"], "financial_data_annotation")
    with pytest.raises(MissingFinancialAnnotation):
        project_financial_openapi(app.openapi(), app.routes, mapping, required_models=required)
    monkeypatch.undo()
    route = next(route for route in app.routes if getattr(route, "path", None) == "/EnterpriseValues")
    response_data = models["data"]
    monkeypatch.setattr(route, "response_model", list[response_data])
    with pytest.raises(InvalidFinancialAnnotation, match="supported response model"):
        project_financial_openapi(app.openapi(), app.routes, mapping, required_models=required)
