"""Exercise the frozen earnings calendar contract through safe FMP acquisition."""

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest
from openbb_core.provider.standard_models.financial_metadata import (
    FINANCIAL_METADATA_KEY,
)
from openbb_core.provider.utils.financial_errors import FinancialError
from openbb_fmp.models.calendar_earnings import FMPCalendarEarningsData as Data
from openbb_fmp.models.calendar_earnings import FMPCalendarEarningsFetcher as Fetcher
from openbb_fmp.models.calendar_earnings import FMPCalendarEarningsQueryParams as Query
from openbb_fmp.utils.helpers import FMPAcquisition

FIXTURES = Path(__file__).parent / "fixtures/fmp_batch_b/events"
PARAMS = {"start_date": "2026-01-01", "end_date": "2026-01-07"}
ROW = {"date": "2026-01-02", "symbol": "AAPL", "epsActual": 0}
STAMP = datetime(2026, 1, 3, tzinfo=UTC)


class Response:
    def __init__(self, payload, status):
        self.payload, self.status, self.headers = payload, status, {}

    async def json(self):
        return self.payload


def test_frozen_schemas_and_example():
    contract = json.loads((FIXTURES / "calendar_earnings.json").read_text())
    for model, key in [(Query, "query"), (Data, "data")]:
        for mode in ["validation", "serialization"]:
            assert model.model_json_schema(mode=mode) == contract[key][mode]
    examples = json.loads((FIXTURES / "serialization_examples.json").read_text())
    example = next(row for row in examples if row["model"] == "calendar_earnings")
    result = Fetcher.transform_data(
        Query(**PARAMS), FMPAcquisition([example["raw"]], STAMP)
    )
    assert result.result[0].model_dump(mode="json") == example["expected"]
    meta = result.metadata[FINANCIAL_METADATA_KEY]
    assert meta["source"]["endpoint"] == "earnings-calendar"
    assert datetime.fromisoformat(meta["retrieved_at"]) == STAMP
    assert set(meta["fields"]) == set(contract["fields"])
    for field, definition in contract["fields"].items():
        for key in ("unit", "scale", "currency", "period_basis", "value_origin"):
            assert meta["fields"][field][key] == definition[key]
    assert meta["fields"]["eps_actual"]["availability"] == "available"
    assert meta["fields"]["revenue_actual"]["availability"] == "missing"


@pytest.mark.parametrize(
    "params",
    [
        {},
        {"start_date": PARAMS["start_date"]},
        {"end_date": PARAMS["end_date"]},
        {**PARAMS, "symbol": "AAPL"},
        {**PARAMS, "limit": 1},
        {**PARAMS, "from": PARAMS["start_date"]},
        {**PARAMS, "end_date": "2026-01-08"},
        {**PARAMS, "end_date": "2025-12-31"},
        {**PARAMS, "start_date": "2026-1-01"},
        {**PARAMS, "start_date": "2026-02-30"},
        {**PARAMS, "start_date": "2026-01-01T00:00:00"},
        {**PARAMS, "start_date": None},
        {**PARAMS, "end_date": True},
        {**PARAMS, "end_date": 1767225600},
        {**PARAMS, "end_date": ["2026-01-01", "2026-01-02"]},
    ],
)
def test_invalid_queries_never_send(monkeypatch, params):
    async def forbidden(*args, **kwargs):
        pytest.fail("Invalid query reached transport")

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", forbidden)
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data(params))
    assert error.value.code == "invalid_parameters"


@pytest.fixture
def transport(monkeypatch):
    def install(payload, status=200, failure=None):
        calls = []

        async def send(url, **kwargs):
            calls.append(url)
            if failure:
                raise failure("secret")
            return await kwargs["response_callback"](Response(payload, status), None)

        monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", send)
        return calls

    return install


@pytest.mark.parametrize("end_date", ["2026-01-01", "2026-01-07"])
@pytest.mark.parametrize("count", [3, 250, 251])
def test_wire_order_and_bounds(transport, count, end_date):
    params = {**PARAMS, "end_date": end_date}
    first = {**ROW, "date": PARAMS["start_date"]}
    second = {**first, "date": end_date, "symbol": "MSFT", "lastUpdated": " "}
    payload = [first, second] + [first] * (count - 2)
    calls = transport(payload)
    result = asyncio.run(Fetcher.fetch_data(params, {"fmp_api_key": "secret"}))
    assert len(calls) == 1
    url = urlsplit(calls[0])
    assert (url.scheme, url.netloc, url.path) == (
        "https",
        "financialmodelingprep.com",
        "/stable/earnings-calendar",
    )
    assert parse_qs(url.query) == {
        "from": [PARAMS["start_date"]],
        "to": [end_date],
        "apikey": ["secret"],
    }
    assert len(result.result) == min(count, 250)
    assert [row.symbol for row in result.result[:3]] == ["AAPL", "MSFT", "AAPL"]
    assert result.result[1].last_updated is None
    meta = result.metadata[FINANCIAL_METADATA_KEY]
    assert meta["effective_query"] == params
    assert meta["bounds"] == {
        "completeness_basis": None,
        "native_continuation": None,
        "requested_limit": 250,
        "effective_limit": 250,
        "returned_count": min(count, 250),
        "truncated": True if count > 250 else None,
        "completeness": "partial" if count > 250 else "unknown",
    }
    assert "secret" not in str(result.metadata)


@pytest.mark.parametrize(
    "payload,code",
    [
        ([], "missing_data"),
        ({}, "missing_data"),
        ({"rows": [ROW]}, "invalid_response"),
        ([ROW, None], "invalid_response"),
        ([{"symbol": "AAPL"}], "invalid_response"),
        ([{**ROW, "date": ""}], "invalid_response"),
        ([{**ROW, "date": "2026-1-02"}], "invalid_response"),
        ([{**ROW, "symbol": "  "}], "invalid_response"),
        ([{**ROW, "symbol": None}], "invalid_response"),
        ([{**ROW, "epsActual": True}], "invalid_response"),
        ([{**ROW, "eps_previous": "0"}], "invalid_response"),
        ([{**ROW, "revenueEstimated": float("inf")}], "invalid_response"),
        ([{**ROW, "lastUpdated": "2026-01-02T00:00:00"}], "invalid_response"),
        ([ROW] * 250 + [{**ROW, "revenueActual": "secret"}], "invalid_response"),
    ],
)
def test_empty_and_malformed_acquisitions(transport, payload, code):
    calls = transport(payload)
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data(PARAMS))
    assert error.value.code == code and len(calls) == 1
    assert "secret" not in str(error.value.to_dict())


@pytest.mark.parametrize(
    "status,failure,code",
    [
        (401, None, "authentication"),
        (403, None, "entitlement"),
        (429, None, "throttling"),
        (500, None, "upstream"),
        (200, TimeoutError, "timeout"),
        (200, ConnectionError, "upstream"),
    ],
)
def test_safe_errors_without_retry(transport, status, failure, code):
    calls = transport({"error": "secret"}, status=status, failure=failure)
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data(PARAMS, {"fmp_api_key": "secret"}))
    assert error.value.code == code and len(calls) == 1
    assert "secret" not in str(error.value.to_dict())
