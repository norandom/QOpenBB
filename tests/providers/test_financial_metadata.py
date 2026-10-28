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
])
def test_effective_queries_reject_private_or_unvalidated_context(query):
    with pytest.raises(ValidationError) as failure:
        metadata(effective_query=query)
    assert "SECRET_CANARY" not in str(failure.value)


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
