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
