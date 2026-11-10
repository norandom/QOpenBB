"""Common financial semantics survive the native OpenBB result envelope."""

import asyncio
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import json

import pytest
from pydantic import ValidationError

from openbb_core.provider.standard_models.financial_metadata import (
    FINANCIAL_METADATA_KEY,
    FinancialBounds,
    FinancialFieldMetadata,
    FinancialResultMetadata,
    FinancialSource,
    FinancialTransformation,
    validate_series_id,
)


def metadata(**updates):
    values = dict(
        dataset="economy.fred_series", provider="fred",
        retrieved_at=datetime(2026, 10, 28, 12, tzinfo=timezone.utc),
        source=FinancialSource(endpoint="series/observations",
                               documentation="https://fred.stlouisfed.org/docs/api/fred/series_observations.html"),
        effective_query={"symbol": "GDP", "units": "pch", "limit": 5},
        fields={"GDP": FinancialFieldMetadata(
            definition="Gross domestic product change", unit="percent", scale=1,
            value_origin="provider_calculation", availability="available",
            observation_date_field="date", currency=None,
            source_unit="billions of dollars", source_frequency="quarterly",
            effective_frequency="quarterly", seasonal_adjustment="seasonally_adjusted",
        )},
        bounds=FinancialBounds(returned_count=3),
    )
    return FinancialResultMetadata(**(values | updates))


def test_native_annotated_result_to_obbject_preserves_legacy_and_financial_values():
    from openbb_core.app.model.obbject import OBBject
    from openbb_core.provider.abstract.annotated_result import AnnotatedResult

    legacy = {"GDP": {"units": "Billions of Dollars", "frequency": "Quarterly"}}
    original = deepcopy(legacy)
    common = metadata()
    rows = [{"date": "2024-01-01", "GDP": value} for value in [None, 0, -2.5]]
    annotated = AnnotatedResult(result=rows, metadata=common.as_metadata(legacy))

    class Query:
        async def execute(self):
            return annotated

    native = asyncio.run(OBBject.from_query(Query()))
    body = json.loads(native.model_dump_json())
    assert body["results"] == rows
    assert legacy == original
    result_metadata = body["extra"]["results_metadata"]
    assert result_metadata["GDP"] == legacy["GDP"]
    restored = FinancialResultMetadata.model_validate(result_metadata[FINANCIAL_METADATA_KEY])
    assert restored == common
    assert restored.retrieved_at.isoformat() == "2026-10-28T12:00:00+00:00"
    assert restored.bounds.completeness == "unknown"
    assert restored.bounds.truncated is None
    assert restored.fields["GDP"].currency is None


@pytest.mark.parametrize("timestamp", [datetime(2026, 10, 28), "2026-10-28T12:00:00"])
def test_acquisition_requires_aware_timestamp(timestamp):
    with pytest.raises(ValidationError):
        metadata(retrieved_at=timestamp)


def test_acquisition_normalizes_to_utc_without_replacing_actual_time():
    stamp = datetime(2020, 1, 2, 14, tzinfo=timezone(timedelta(hours=2)))
    assert metadata(retrieved_at=stamp).retrieved_at == stamp
    assert metadata(retrieved_at=stamp).retrieved_at.utcoffset() == timedelta(0)
    with pytest.raises(ValidationError):
        FinancialResultMetadata.model_validate({"dataset": "x", "provider": "fred"})


@pytest.mark.parametrize("query", [
    {"apikey": "SECRET_CANARY"}, {"access_token": "SECRET_CANARY"},
    {"symbol": {"token": "SECRET_CANARY"}},
    {"symbol": "https://example.test/data?apikey=SECRET_CANARY"},
    {"url": "https://example.test"},
    {"query": "api-key=SECRET_CANARY"},
    {"query": "access_token=SECRET_CANARY"},
    {"query": "access-token:SECRET_CANARY"},
    {"ttm": "https://example.test/data?apikey=SECRET_CANARY"},
    {"ttm": "access_token=SECRET_CANARY"},
    {"ttm": ["exclude", "password:SECRET_CANARY"]},
    {"ttm": {"mode": "exclude"}},
    {"ttm": float("nan")},
])
def test_effective_queries_reject_private_or_unvalidated_context(query):
    with pytest.raises(ValidationError) as failure:
        metadata(effective_query=query)
    assert "SECRET_CANARY" not in str(failure.value)


@pytest.mark.parametrize("selection", ["exclude", "include", "only"])
def test_public_ttm_query_roundtrips_without_provider_specific_choices(selection):
    common = metadata(effective_query={"symbol": "GDP", "ttm": selection})
    restored = FinancialResultMetadata.model_validate_json(common.model_dump_json())
    assert restored == common
    assert restored.schema_version == 1
    assert restored.effective_query == {"symbol": "GDP", "ttm": selection}
    assert common.as_metadata()[FINANCIAL_METADATA_KEY]["effective_query"] == restored.effective_query


def test_validated_query_names_are_not_subject_to_magic_secret_detection():
    assert metadata(effective_query={"query": "Token Energy Corp", "symbol": "KEY"}).effective_query == {
        "query": "Token Energy Corp", "symbol": "KEY"}


@pytest.mark.parametrize("source", [
    {"endpoint": "https://example.test?apikey=SECRET_CANARY"},
    {"endpoint": "https://example.test/api/SECRET_CANARY"},
    {"endpoint": "profile?apikey=SECRET_CANARY"},
    {"endpoint": "profile", "documentation": "https://user:SECRET_CANARY@example.test/docs"},
    {"endpoint": "profile", "documentation": "https://example.test/docs?token=SECRET_CANARY"},
    {"endpoint": "profile", "documentation": "javascript:SECRET_CANARY"},
])
def test_source_rejects_credential_bearing_urls(source):
    with pytest.raises(ValidationError) as failure:
        metadata(source=source)
    assert "SECRET_CANARY" not in str(failure.value)


def test_namespace_collision_is_rejected_without_renaming_fred_series():
    assert validate_series_id("GDP") == "GDP"
    with pytest.raises(ValueError):
        validate_series_id(FINANCIAL_METADATA_KEY)
    with pytest.raises(ValueError):
        metadata().as_metadata({FINANCIAL_METADATA_KEY: {}})


@pytest.mark.parametrize("source", [
    "https://example.test?apikey=SECRET_CANARY",
    "https://example.test/api/SECRET_CANARY", "series?api-key=SECRET_CANARY",
])
def test_field_source_rejects_request_urls_and_credential_assignments(source):
    with pytest.raises(ValidationError) as failure:
        metadata(fields={"GDP": {"definition": "Gross domestic product", "source": source}})
    assert "SECRET_CANARY" not in str(failure.value)


@pytest.mark.parametrize("bounds", [
    {"returned_count": -1}, {"returned_count": 2, "effective_limit": 1},
    {"returned_count": 1, "truncated": True, "completeness": "complete"},
    {"returned_count": 1, "completeness": "complete"},
    {"returned_count": 1, "native_continuation": "https://example.test?token=SECRET_CANARY"},
])
def test_bounds_reject_false_completeness_and_unsafe_continuation(bounds):
    with pytest.raises(ValidationError):
        metadata(bounds=bounds)


def test_explicit_semantics_transformations_and_unknown_bases_roundtrip():
    common = metadata(
        fields={"net_debt": FinancialFieldMetadata(
            definition="Provider reported net debt", unit="currency", scale=1,
            currency_field="reported_currency", period_basis="fiscal_period",
            value_origin="provider_observation", availability="unknown",
            financial_basis={"lease": None, "minority_interest": None,
                             "share_count": "weighted_average", "market_date": None},
        )},
        transformations=[FinancialTransformation(
            name="unit_conversion", affected_fields=["net_debt"],
            source_basis="Provider values in millions of reported currency",
            definition="Multiply source values by 1000000",
        )],
        limitations=["Publication dates and historical vintages unavailable; not point-in-time safe"],
    )
    restored = FinancialResultMetadata.model_validate_json(common.model_dump_json())
    assert restored == common
    assert restored.fields["net_debt"].financial_basis["lease"] is None
    assert restored.point_in_time_safe is False
    assert restored.publication_date_field is None
    assert metadata(fields={}).fields == {}


@pytest.mark.parametrize("updates", [
    {"schema_version": 2}, {"provider": ""}, {"dataset": "x?token=SECRET_CANARY"},
    {"unexpected": "SECRET_CANARY"},
    {"fields": {"x": {"definition": "x", "value_origin": "invented"}}},
])
def test_invalid_metadata_is_rejected_without_echoing_input(updates):
    with pytest.raises(ValidationError) as failure:
        metadata(**updates)
    assert "SECRET_CANARY" not in str(failure.value)


def statement_row(**updates):
    return dict(row_index=0, source_ordinal=4, fiscal_year=2025, fiscal_period="FY",
                period_end="2025-06-30", requested_frequency="annual", **updates)


def test_statement_contract_preserves_old_nulls_and_omits_only_absent_member():
    old = metadata().model_dump(mode="json")
    assert "statement_provenance" not in old
    assert old["publication_date_field"] is None
    assert FinancialResultMetadata.model_validate(old) == metadata()
    extended = metadata(bounds={"returned_count": 1}, statement_provenance={"rows": [statement_row()]})
    body = extended.model_dump(mode="json")
    assert body["statement_provenance"]["rows"][0]["flow_coverage"] == "unknown"
    assert body["statement_provenance"]["rows"][0]["period_start"] is None
    from pydantic import create_model
    old_fields = {name: (field.annotation, field) for name, field in FinancialResultMetadata.model_fields.items()
                  if name != "statement_provenance"}
    old_reader = create_model("OldStrictReader", __config__={"extra": "forbid"}, **old_fields)
    with pytest.raises(ValidationError):
        old_reader.model_validate(body)


@pytest.mark.parametrize("change", [
    {"row_index": 1}, {"source_ordinal": True}, {"requested_frequency": "monthly"},
    {"flow_coverage": "annual"}, {"coverage_status": "supported"},
    {"period_start": "2025-01-01"}, {"duration_days": 365},
    {"facts": [{"semantic_key": "fiscal_year", "source_field": "token", "value": "SECRET_CANARY", "presence": "value"}]},
    {"facts": [{"semantic_key": "fiscal_year", "source_field": "fiscalYear", "value": True, "presence": "value"}]},
    {"facts": [{"semantic_key": "period_end", "source_field": "date", "value": "2024-06-30", "presence": "value"}]},
    {"instant_dates": {"cash_at_beginning_of_period": "2025-06-30"}},
])
def test_statement_rejects_unproven_or_misattributed_evidence(change):
    row = statement_row() | change
    with pytest.raises(ValidationError) as error:
        metadata(bounds={"returned_count": 1}, statement_provenance={"rows": [row]})
    assert "SECRET_CANARY" not in str(error.value)


def test_statement_fact_presence_conflicts_and_documented_coverage():
    facts = [dict(semantic_key="fiscal_year", source_field=alias, value=value,
                  presence="null" if value is None else "value", evidence_kind="observation")
             for alias, value in [("fiscalYear", 2025), ("calendarYear", None)]]
    row = statement_row(facts=facts, coverage_status="conflicting")
    common = metadata(bounds={"returned_count": 1}, statement_provenance={"rows": [row]})
    assert common.statement_provenance.rows[0].facts[1].value is None
    with pytest.raises(ValidationError):
        metadata(bounds={"returned_count": 1}, statement_provenance={"rows": [row | {"coverage_status": "unavailable"}]})
    convention = dict(semantic_key="flow_coverage", flow_coverage="annual",
                      documentation="https://example.test/docs", evidence_kind="provider_convention")
    supported = statement_row(flow_coverage="annual", coverage_status="supported", conventions=[convention])
    assert metadata(bounds={"returned_count": 1}, statement_provenance={"rows": [supported]}).statement_provenance.rows[0].flow_coverage == "annual"
    supported["conventions"][0]["documentation"] = "https://example.test/docs?token=SECRET_CANARY"
    with pytest.raises(ValidationError) as error:
        metadata(bounds={"returned_count": 1}, statement_provenance={"rows": [supported]})
    assert "SECRET_CANARY" not in str(error.value)


def test_statement_counts_and_source_ordinals_are_unique():
    with pytest.raises(ValidationError):
        metadata(statement_provenance={"rows": [statement_row()]})
    with pytest.raises(ValidationError):
        metadata(bounds={"returned_count": 2}, statement_provenance={"rows": [statement_row(), statement_row() | {"row_index": 1}]})


def test_statement_instant_dates_require_declared_stocks_and_keep_beginning_cash_unknown():
    fields = {name: {"definition": "Reported cash", "period_basis": "instant"}
              for name in ["cash_at_beginning_of_period", "cash_at_end_of_period"]}
    instants = {"cash_at_beginning_of_period": None, "cash_at_end_of_period": "2025-06-30"}
    common = metadata(bounds={"returned_count": 1}, fields=fields,
                      statement_provenance={"rows": [statement_row(instant_dates=instants)]})
    assert common.statement_provenance.rows[0].instant_dates["cash_at_beginning_of_period"] is None
    with pytest.raises(ValidationError):
        metadata(bounds={"returned_count": 1}, fields={},
                 statement_provenance={"rows": [statement_row(instant_dates=instants)]})
    with pytest.raises(ValidationError):
        metadata(bounds={"returned_count": 1}, effective_query={"period": "quarter"},
                 statement_provenance={"rows": [statement_row()]})


@pytest.mark.parametrize("model_name", ["income_statement_data", "balance_sheet_data", "cash_flow_data"])
def test_statement_preserves_existing_unknown_labels_and_midnight_source_dates(model_name):
    from importlib import import_module
    from openbb_core.provider.standard_models.statement_provenance import StatementPeriodRow
    module = import_module("openbb_fmp.models." + model_name)
    model = getattr(module, {"income_statement_data": "FMPIncomeStatementData",
                             "balance_sheet_data": "FMPBalanceSheetData",
                             "cash_flow_data": "FMPCashFlowStatementData"}[model_name])
    source = {"date": "2025-06-30T00:00:00", "fiscalYear": "2025", "period": "H1",
              "filingDate": "2025-07-15T00:00:00"}
    baseline = model.model_validate(source)
    facts = [dict(semantic_key=key, source_field=alias, value=source[alias], presence="value")
             for key, alias in [("period_end", "date"), ("fiscal_year", "fiscalYear"),
                                ("fiscal_period", "period"), ("filing_date", "filingDate")]]
    row = StatementPeriodRow.model_validate(statement_row() | dict(
        fiscal_year=baseline.fiscal_year, fiscal_period=baseline.fiscal_period,
        period_end=baseline.period_ending, filing_date=baseline.filing_date, facts=facts))
    assert row.fiscal_period == "H1"
    assert row.flow_coverage == "unknown"
    assert row.facts[0].value == source["date"]
    assert row.facts[3].value == source["filingDate"]


@pytest.mark.parametrize("key,alias", [("period_end", "date"), ("filing_date", "filingDate"),
                                      ("accepted_date", "acceptedDate")])
def test_statement_date_parser_errors_never_expose_source_values(key, alias):
    from openbb_core.provider.standard_models.statement_provenance import StatementFact
    with pytest.raises(ValidationError) as error:
        StatementFact(semantic_key=key, source_field=alias, value="SECRET_CANARY", presence="value")
    assert "SECRET_CANARY" not in str(error.value)



def test_statement_preserves_existing_integer_year_range():
    from openbb_fmp.models.income_statement_data import FMPIncomeStatementData
    from openbb_core.provider.standard_models.statement_provenance import StatementPeriodRow
    baseline = FMPIncomeStatementData.model_validate({"date": "2025-06-30", "fiscalYear": "999", "period": "H1"})
    row = StatementPeriodRow.model_validate(statement_row() | dict(
        fiscal_year=baseline.fiscal_year, fiscal_period=baseline.fiscal_period,
        facts=[dict(semantic_key="fiscal_year", source_field="fiscalYear", value="999", presence="value")]))
    assert row.fiscal_year == baseline.fiscal_year == 999
