"""Class-owned financial annotations preserve modeled and runtime ownership."""

from typing import ClassVar, Literal

import pytest
from pydantic import BaseModel, Field, ValidationError

from openbb_core.provider.standard_models.financial_annotations import (
    FinancialDataAnnotation, FinancialFieldTemplate, FinancialQueryAnnotation,
    MissingFinancialAnnotation, InvalidFinancialAnnotation, ProceduralBounds,
    ResponsePolicy, bind_data_annotation, bind_query_annotation,
    render_field_templates,
)


class Query(BaseModel):
    financial_query_annotation: ClassVar[FinancialQueryAnnotation] = FinancialQueryAnnotation(
        provider_policy="explicit", procedural_bounds=ProceduralBounds(max_calendar_years=5),
        response_policy=ResponsePolicy(mode="clip", max_rows=5000),
    )
    start_date: str | None = None
    end_date: str | None = None
    interval: Literal["1d"] = Field(default="1d", description="Daily interval")


class Row(BaseModel):
    financial_data_annotation: ClassVar[FinancialDataAnnotation] = FinancialDataAnnotation(
        fields={"value": FinancialFieldTemplate(unit="currency", currency_field="currency"),
                "currency": FinancialFieldTemplate()},
        runtime_properties=["fields.availability", "retrieved_at"],
    )
    value: float | None = Field(default=None, serialization_alias="price", description="Observed price")
    currency: str = Field(description="Quotation currency")


def test_binding_keeps_model_schema_as_ordinary_parameter_authority():
    annotation = bind_query_annotation(Query)
    assert annotation.model_dump(mode="json")["provider_policy"] == "explicit"
    assert annotation.procedural_bounds.max_calendar_years == 5
    schema = Query.model_json_schema()
    assert schema["properties"]["interval"]["default"] == "1d"
    assert "parameters" not in annotation.model_dump()


def test_templates_derive_definitions_and_render_independent_metadata():
    bound = bind_data_annotation(Row)
    assert bound.fields["value"].definition is None
    first = render_field_templates(Row)
    second = render_field_templates(Row)
    assert first["value"].definition == "Observed price"
    assert first["value"].unit == "currency"
    assert first["value"].currency is None
    first["value"].financial_basis["debt"] = "changed"
    assert second["value"].financial_basis == {}
    assert Row.financial_data_annotation.fields["value"].financial_basis == {}
    assert set(first) == {"value", "currency"}


@pytest.mark.parametrize("changes", [
    {"fields": {"price": FinancialFieldTemplate(unit="currency")}},
    {"fields": {"value": FinancialFieldTemplate(currency_field="absent")}},
    {"fields": {"value": FinancialFieldTemplate(observation_date_field="price")}},
])
def test_invalid_canonical_references_fail_explicitly(changes):
    class Invalid(Row):
        financial_data_annotation: ClassVar[FinancialDataAnnotation] = FinancialDataAnnotation(
            fields={"currency": FinancialFieldTemplate(), **changes["fields"]})
    with pytest.raises(InvalidFinancialAnnotation):
        bind_data_annotation(Invalid)


def test_missing_is_distinct_from_malformed_and_unknown():
    class Absent(BaseModel):
        pass
    class Malformed(BaseModel):
        financial_data_annotation: ClassVar[dict] = {}
    with pytest.raises(MissingFinancialAnnotation):
        bind_data_annotation(Absent)
    with pytest.raises(InvalidFinancialAnnotation):
        bind_data_annotation(Malformed)
    template = render_field_templates(Row)["value"]
    assert template.value_origin == "unknown"
    assert template.currency is None


def test_runtime_dynamic_properties_are_disclosures_without_observed_values():
    annotation = FinancialDataAnnotation(dynamic_fields=True, runtime_properties=[
        "fields", "observation_provenance", "retrieved_at", "bounds",
    ])
    assert annotation.model_dump(mode="json")["dynamic_fields"] is True
    assert "retrieved_at" not in annotation.model_dump()
    with pytest.raises(ValidationError):
        FinancialDataAnnotation(runtime_properties=["invented_property"])


@pytest.mark.parametrize("values", [
    {"mode": "clip"}, {"mode": "provider", "max_rows": 5},
    {"mode": "income_compatibility", "max_rows": 5}, {"mode": "clip", "max_rows": 0},
])
def test_response_policy_rejects_fake_or_missing_caps(values):
    with pytest.raises(ValidationError):
        ResponsePolicy(**values)


def test_baseline_policy_and_income_compatibility_do_not_duplicate_defaults():
    annotation = FinancialQueryAnnotation(provider_policy="baseline_default", response_policy=
        ResponsePolicy(mode="income_compatibility"))
    assert annotation.response_policy.max_rows is None
    assert "default_provider" not in annotation.model_dump()
    with pytest.raises(ValidationError):
        ProceduralBounds(max_symbols=True)
    with pytest.raises(ValidationError):
        FinancialQueryAnnotation(provider_policy="automatic")


def test_invalid_query_references_and_description_conflicts():
    class NoDates(BaseModel):
        financial_query_annotation: ClassVar[FinancialQueryAnnotation] = Query.financial_query_annotation
    with pytest.raises(InvalidFinancialAnnotation):
        bind_query_annotation(NoDates)
    class Conflict(Row):
        financial_data_annotation: ClassVar[FinancialDataAnnotation] = FinancialDataAnnotation(
            fields={"value": FinancialFieldTemplate(definition="Different definition"),
                    "currency": FinancialFieldTemplate()})
    with pytest.raises(InvalidFinancialAnnotation):
        render_field_templates(Conflict)


def test_malformed_mutated_declaration_and_binding_copies():
    bound = bind_data_annotation(Row)
    bound.fields["value"].unit = "changed"
    assert Row.financial_data_annotation.fields["value"].unit == "currency"
    class Mutated(Row):
        financial_data_annotation: ClassVar[FinancialDataAnnotation] = FinancialDataAnnotation()
    Mutated.financial_data_annotation.runtime_properties.append("invented")
    with pytest.raises(InvalidFinancialAnnotation):
        bind_data_annotation(Mutated)


def test_query_parameter_clipping_derives_cap_from_actual_query_field():
    class Limited(BaseModel):
        financial_query_annotation: ClassVar[FinancialQueryAnnotation] = FinancialQueryAnnotation(
            provider_policy="explicit", response_policy=ResponsePolicy(mode="clip", limit_parameter="limit"))
        limit: int = Field(default=100, ge=1, le=1000)
    policy = bind_query_annotation(Limited).response_policy
    assert policy.limit_parameter == "limit"
    assert policy.max_rows is None
    assert Limited.model_fields["limit"].default == 100
    class Invalid(Limited):
        limit: str = "many"
    with pytest.raises(InvalidFinancialAnnotation):
        bind_query_annotation(Invalid)
    with pytest.raises(ValidationError):
        ResponsePolicy(mode="clip", max_rows=5, limit_parameter="limit")
    with pytest.raises(ValidationError):
        ResponsePolicy(mode="income_compatibility", limit_parameter="limit")


def test_absent_static_field_template_is_not_explicit_unknown():
    class Partial(Row):
        financial_data_annotation: ClassVar[FinancialDataAnnotation] = FinancialDataAnnotation(
            fields={"value": FinancialFieldTemplate()}, dynamic_fields=True)
    with pytest.raises(InvalidFinancialAnnotation):
        bind_data_annotation(Partial)


class NativeNames(BaseModel):
    financial_data_annotation: ClassVar[FinancialDataAnnotation] = FinancialDataAnnotation(
        fields={"ev_to_ebitda": FinancialFieldTemplate(observation_date_field="date"),
                "date": FinancialFieldTemplate()})
    ev_to_ebitda: float = Field(alias="evToEBITDA", description="Provider enterprise value to EBITDA")
    date: str = Field(alias="observationDate", description="Observation date")
    internal: str = Field(default="private", exclude=True)


def test_native_false_serialization_and_templates_use_canonical_names():
    row = NativeNames(evToEBITDA=12.5, observationDate="2026-10-29")
    assert set(row.model_dump(by_alias=False)) == {"ev_to_ebitda", "date"}
    assert set(render_field_templates(NativeNames)) == set(row.model_dump(by_alias=False))
    assert render_field_templates(NativeNames)["ev_to_ebitda"].observation_date_field == "date"


@pytest.mark.parametrize("fields", [
    {"evToEBITDA": FinancialFieldTemplate(), "date": FinancialFieldTemplate()},
    {"ev_to_ebitda": FinancialFieldTemplate(observation_date_field="observationDate"),
     "date": FinancialFieldTemplate()},
    {"ev_to_ebitda": FinancialFieldTemplate(), "date": FinancialFieldTemplate(),
     "internal": FinancialFieldTemplate()},
])
def test_alias_only_keys_references_and_excluded_fields_are_rejected(fields):
    class Invalid(NativeNames):
        financial_data_annotation: ClassVar[FinancialDataAnnotation] = FinancialDataAnnotation(fields=fields)
    with pytest.raises(InvalidFinancialAnnotation):
        bind_data_annotation(Invalid)


def test_query_limit_references_use_canonical_names_even_with_input_alias():
    class Limited(BaseModel):
        financial_query_annotation: ClassVar[FinancialQueryAnnotation] = FinancialQueryAnnotation(
            provider_policy="explicit", response_policy=ResponsePolicy(mode="clip", limit_parameter="limit"))
        limit: int = Field(default=100, alias="rowLimit")
    assert bind_query_annotation(Limited).response_policy.limit_parameter == "limit"
    class Invalid(Limited):
        financial_query_annotation: ClassVar[FinancialQueryAnnotation] = FinancialQueryAnnotation(
            provider_policy="explicit", response_policy=ResponsePolicy(mode="clip", limit_parameter="rowLimit"))
    with pytest.raises(InvalidFinancialAnnotation):
        bind_query_annotation(Invalid)
