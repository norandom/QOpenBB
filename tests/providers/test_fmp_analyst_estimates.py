"""Forecast estimates preserve source distinctions and unknown publication vintage."""

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest
from openbb_core.provider.standard_models.financial_annotations import (
    bind_data_annotation,
    bind_query_annotation,
)
from openbb_core.provider.standard_models.financial_metadata import (
    FINANCIAL_METADATA_KEY,
)
from openbb_core.provider.utils.financial_errors import FinancialError
from openbb_fmp.models.analyst_estimates import (
    FMPAnalystEstimatesData as Row,
)
from openbb_fmp.models.analyst_estimates import (
    FMPAnalystEstimatesFetcher as Fetcher,
)
from openbb_fmp.models.analyst_estimates import (
    FMPAnalystEstimatesQueryParams as Query,
)

FROZEN = json.loads(
    (
        Path(__file__).parent / "fixtures/fmp_batch_a/contracts/analyst_estimates.json"
    ).read_text()
)


class Response:
    def __init__(self, payload, status=200):
        self.payload, self.status, self.headers = payload, status, {"Retry-After": "23"}

    async def json(self):
        if isinstance(self.payload, Exception):
            raise self.payload
        return self.payload


def run(monkeypatch, payload, params=None, status=200):
    calls = []

    async def request(url, **kwargs):
        calls.append((url, kwargs))
        if isinstance(payload, TimeoutError):
            raise payload
        return await kwargs["response_callback"](Response(payload, status), None)

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", request)
    result = asyncio.run(
        Fetcher.fetch_data(
            params or {"symbol": " msft "}, {"fmp_api_key": "canary&secret"}
        )
    )
    assert len(calls) == 1
    return result, calls


def test_frozen_schema_and_annotations():
    for mode in ["validation", "serialization"]:
        assert Query.model_json_schema(mode=mode) == FROZEN["query"][mode]
        assert Row.model_json_schema(mode=mode) == FROZEN["data"][mode]
    assert (
        bind_query_annotation(Query).model_dump(mode="json")
        == FROZEN["query_annotation"]
    )
    assert (
        bind_data_annotation(Row).model_dump(mode="json") == FROZEN["data_annotation"]
    )
    assert Query.__dict__["__qopenbb_strict_admission__"] is True


@pytest.mark.parametrize(
    "params",
    [{"symbol": v} for v in [None, True, "", "A,B", "A&x=y", "A" * 51, "A\n"]]
    + [
        {"symbol": "A", k: v}
        for k, values in {
            "limit": [None, True, 0, 101, "20", 20.0],
            "page": [None, True, -1, 11, "0", 0.0],
            "period": [None, True, "ttm"],
            "extra": [0],
        }.items()
        for v in values
    ],
)
def test_invalid_raw_queries_zero_io(monkeypatch, params):
    async def forbidden(*args, **kwargs):
        pytest.fail("invalid query reached transport")

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", forbidden)
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data(params, {"fmp_api_key": "canary"}))
    assert error.value.code == "invalid_parameters"


@pytest.mark.parametrize(
    "period,expected",
    [("annual", "annual"), ("quarter", "quarter"), ("quarterly", "quarter")],
)
def test_one_request_encoding_and_effective_query(monkeypatch, period, expected):
    result, calls = run(
        monkeypatch,
        [{"symbol": "MSFT", "date": "2030-06-30"}],
        {"symbol": " brk/b ", "period": period, "limit": 1, "page": 10},
    )
    url, kwargs = calls[0]
    assert urlsplit(url).path == "/stable/analyst-estimates"
    assert parse_qs(urlsplit(url).query) == {
        "symbol": ["BRK/B"],
        "period": [expected],
        "limit": ["1"],
        "page": ["10"],
        "apikey": ["canary&secret"],
    }
    assert "allow_empty" not in kwargs and "typed_errors" not in kwargs
    meta = result.metadata[FINANCIAL_METADATA_KEY]
    assert meta["effective_query"] == {
        "symbol": "BRK/B",
        "period": expected,
        "limit": 1,
        "page": 10,
    }
    assert "canary" not in json.dumps(meta)


def test_aliases_all_fields_units_and_unknowns(monkeypatch):
    payload = {"symbol": "MSFT", "date": "2030-06-30"}
    for source in FROZEN["effective_aliases"].values():
        payload[source] = 0
    result, _ = run(monkeypatch, [payload])
    row = result.result[0]
    meta = result.metadata[FINANCIAL_METADATA_KEY]
    assert not row.model_extra
    assert meta["point_in_time_safe"] is False
    assert meta["publication_date_field"] is None
    assert meta["observation_date_field"] is None
    assert set(meta["fields"]) == set(Row.model_fields)
    for name, field in meta["fields"].items():
        assert field["availability"] == "available"
        assert field["currency"] is None and field["currency_field"] is None
        assert field["publication_date_field"] is None
        if name.startswith("estimated_"):
            assert getattr(row, name) == 0
            assert field["value_origin"] == "estimate"
            assert field["unit"] == ("currency/share" if "eps" in name else "currency")
            assert field["scale"] == 1
        if name.startswith("number_"):
            assert getattr(row, name) == 0 and field["unit"] == "count"
    assert row.date.isoformat() == "2030-06-30"
    assert urlsplit(meta["source"]["documentation"]).query == ""
    assert urlsplit(meta["source"]["documentation"]).fragment == ""


@pytest.mark.parametrize(
    "payload", [[], [{"symbol": "MSFT", "date": "2030-06-30", "epsLow": None}]]
)
def test_empty_and_missing_optional_real_fetcher(monkeypatch, payload):
    before = datetime.now(UTC)
    result, _ = run(monkeypatch, payload)
    meta = result.metadata[FINANCIAL_METADATA_KEY]
    assert len(result.result) == len(payload)
    assert before <= datetime.fromisoformat(meta["retrieved_at"]) <= datetime.now(UTC)
    assert meta["bounds"]["completeness"] == "unknown"
    assert meta["bounds"]["returned_count"] == len(payload)
    assert meta["fields"]["estimated_eps_low"]["availability"] == "missing"
    assert meta["effective_query"] == {
        "symbol": "MSFT",
        "period": "annual",
        "limit": 20,
        "page": 0,
    }


def test_clip_source_order_duplicates_and_no_invented_total(monkeypatch):
    payload = [{"symbol": "MSFT", "date": "2030-06-30", "epsLow": i} for i in [3, 2, 1]]
    result, _ = run(monkeypatch, payload, {"symbol": "MSFT", "limit": 2})
    assert [r.estimated_eps_low for r in result.result] == [3, 2]
    bounds = result.metadata[FINANCIAL_METADATA_KEY]["bounds"]
    assert bounds["truncated"] is True and bounds["completeness"] == "partial"
    assert bounds["requested_limit"] == bounds["effective_limit"] == 2


@pytest.mark.parametrize(
    "payload",
    [
        [{"symbol": "MSFT"}],
        [{"symbol": "MSFT", "date": None}],
        [{"symbol": "MSFT", "date": "bad"}],
        [{"symbol": "MSFT", "date": "2030-06-30", "epsLow": "secret-canary"}],
        [{"symbol": "MSFT", "date": "2030-06-30", "epsLow": float("inf")}],
        {},
        "bad",
        [1],
    ],
)
def test_malformed_safe(monkeypatch, payload):
    with pytest.raises(FinancialError) as error:
        run(monkeypatch, payload)
    assert error.value.code == ("missing_data" if payload == {} else "invalid_response")
    assert "secret-canary" not in str(error.value)


@pytest.mark.parametrize(
    "status,payload,code",
    [
        (401, {}, "authentication"),
        (403, {}, "entitlement"),
        (429, {}, "throttling"),
        (200, TimeoutError("canary&secret"), "timeout"),
        (200, ValueError("canary&secret"), "invalid_response"),
    ],
)
def test_safe_failures_no_retry(monkeypatch, status, payload, code):
    calls = []

    async def request(url, **kwargs):
        calls.append(url)
        if isinstance(payload, TimeoutError):
            raise payload
        return await kwargs["response_callback"](Response(payload, status), None)

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", request)
    with pytest.raises(FinancialError) as error:
        asyncio.run(
            Fetcher.fetch_data({"symbol": "MSFT"}, {"fmp_api_key": "canary&secret"})
        )
    assert len(calls) == 1 and error.value.code == code
    assert error.value.retry_after_seconds == (23 if status == 429 else None)
    assert "canary" not in str(error.value)
    assert error.value.__context__ is None


@pytest.mark.parametrize(
    "canonical,definition", FROZEN["accepted_validation_aliases"].items()
)
def test_all_frozen_validation_aliases(canonical, definition):
    if canonical in {"date", "symbol"}:
        return
    for alias in [
        definition["canonical"],
        definition["generated_schema_alias"],
        *definition["source_aliases"],
    ]:
        value = Row.model_validate({"symbol": "MSFT", "date": "2030-06-30", alias: 9})
        assert getattr(value, canonical) == 9
        assert value.model_dump()[canonical] == 9 and not value.model_extra


def test_maximum_boundary_and_unclipped_page(monkeypatch):
    result, _ = run(
        monkeypatch,
        [{"symbol": "MSFT", "date": "2030-06-30", "epsHigh": None}] * 100,
        {"symbol": "MSFT", "limit": 100, "page": 0},
    )
    meta = result.metadata[FINANCIAL_METADATA_KEY]
    assert len(result.result) == 100 and meta["bounds"]["truncated"] is None
    assert meta["bounds"]["completeness"] == "unknown"
    assert meta["fields"]["estimated_eps_high"]["availability"] == "missing"


@pytest.mark.parametrize("source", list(FROZEN["effective_aliases"].values()))
@pytest.mark.parametrize(
    "value",
    [
        "private-upstream-canary",
        float("inf"),
        float("nan"),
        {"private-upstream-canary": 1},
    ],
)
def test_malformed_amount_and_count_conversion_is_safe(monkeypatch, source, value):
    calls = []

    async def request(url, **kwargs):
        calls.append(url)
        payload = [{"symbol": "MSFT", "date": "2030-06-30", source: value}]
        return await kwargs["response_callback"](Response(payload), None)

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", request)
    with pytest.raises(FinancialError) as error:
        asyncio.run(
            Fetcher.fetch_data({"symbol": "MSFT"}, {"fmp_api_key": "synthetic"})
        )
    assert len(calls) == 1
    assert error.value.code == "invalid_response"
    assert "private-upstream-canary" not in str(error.value)
    assert error.value.__context__ is None


@pytest.mark.parametrize("value", [None, 0])
def test_amounts_counts_and_eps_preserve_null_and_zero(monkeypatch, value):
    payload = {"symbol": "MSFT", "date": "2030-06-30"}
    payload.update({source: value for source in FROZEN["effective_aliases"].values()})
    result, _ = run(monkeypatch, [payload])
    for canonical in FROZEN["effective_aliases"]:
        assert getattr(result.result[0], canonical) == value
