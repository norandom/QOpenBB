"""Historical capitalization preserves dated provider calculations and unknown bases."""

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
from openbb_fmp.models.historical_market_cap import (
    FmpHistoricalMarketCapData as Data,
)
from openbb_fmp.models.historical_market_cap import (
    FmpHistoricalMarketCapFetcher as Fetcher,
)
from openbb_fmp.models.historical_market_cap import (
    FmpHistoricalMarketCapQueryParams as Query,
)
from openbb_fmp.utils.helpers import FMPAcquisition

STAMP = datetime(2024, 2, 3, tzinfo=UTC)
PARAMS = {"symbol": " abc ", "start_date": "2024-01-01", "end_date": "2024-12-31"}
ROW = {"symbol": "ABC", "date": "2024-01-02", "marketCap": 0}


def test_frozen_schemas():
    contract = json.loads(
        (
            Path(__file__).parent
            / "fixtures/fmp_batch_a/contracts/historical_market_cap.json"
        ).read_text()
    )
    for model, key in [(Query, "query"), (Data, "data")]:
        for mode in ["validation", "serialization"]:
            assert model.model_json_schema(mode=mode) == contract[key][mode]


@pytest.mark.parametrize(
    "extra",
    [
        {"symbol": None},
        {"symbol": True},
        {"symbol": "A,B"},
        {"symbol": "A&apikey=x"},
        {"symbol": "A\x7f"},
        {"symbol": "A" * 51},
        {"limit": 1},
        {"start_date": True},
        {"start_date": 0},
        {"start_date": "2024-01-01T00:00:00"},
        {"start_date": "2025-01-01"},
        {"start_date": "2023-01-01"},
    ],
)
def test_invalid_before_io(monkeypatch, extra):
    async def forbidden(*args, **kwargs):
        pytest.fail("invalid query reached transport")

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", forbidden)
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data({**PARAMS, **extra}))
    assert error.value.code == "invalid_parameters"


@pytest.mark.parametrize("size", [0, 1, 5000, 5001])
def test_financial_rows_and_bounds(size):
    result = Fetcher.transform_data(
        Fetcher.transform_query(PARAMS), FMPAcquisition([ROW] * size, STAMP)
    )
    meta = result.metadata[FINANCIAL_METADATA_KEY]
    assert len(result.result) == min(size, 5000)
    assert meta["bounds"]["returned_count"] == min(size, 5000)
    assert (
        meta["bounds"]["requested_limit"] == meta["bounds"]["effective_limit"] == 5000
    )
    assert meta["bounds"]["completeness"] == ("partial" if size > 5000 else "unknown")
    assert set(meta["fields"]) == {"date", "symbol", "market_cap"}
    field = meta["fields"]["market_cap"]
    assert field["unit"] == "currency" and field["scale"] == 1
    assert field["value_origin"] == "provider_calculation" and field["currency"] is None
    assert (
        meta["observation_date_field"] == "date" and meta["point_in_time_safe"] is False
    )
    assert meta["effective_query"]["start_date"] == "2024-01-01"
    assert datetime.fromisoformat(meta["retrieved_at"]) == STAMP
    assert not urlsplit(meta["source"]["documentation"]).query
    if size:
        assert result.result[0].market_cap == 0


@pytest.mark.parametrize(
    "field,value",
    [
        ("date", None),
        ("date", "bad"),
        ("marketCap", None),
        ("marketCap", "bad"),
        ("marketCap", True),
    ],
)
def test_required_malformed(field, value):
    with pytest.raises(FinancialError) as error:
        Fetcher.transform_data(
            Fetcher.transform_query(PARAMS),
            FMPAcquisition([{**ROW, field: value}], STAMP),
        )
    assert error.value.code == "invalid_response"


@pytest.mark.parametrize("missing", ["date", "marketCap", "symbol"])
def test_missing_required(missing):
    with pytest.raises(FinancialError):
        Fetcher.transform_data(
            Fetcher.transform_query(PARAMS),
            FMPAcquisition([{k: v for k, v in ROW.items() if k != missing}], STAMP),
        )


class Response:
    status = 200

    def __init__(self, payload):
        self.headers = {}
        self.payload = payload

    async def json(self):
        return self.payload


@pytest.mark.parametrize("payload", [[], [ROW]])
def test_real_fetcher_transport(monkeypatch, payload):
    calls = []

    async def transport(url, **kwargs):
        calls.append(url)
        assert set(kwargs) == {"response_callback"}
        return await kwargs["response_callback"](Response(payload), None)

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", transport)
    result = asyncio.run(
        Fetcher.fetch_data(PARAMS, {"fmp_api_key": "synthetic-secret"})
    )
    assert len(calls) == 1 and len(result.result) == len(payload)
    assert urlsplit(calls[0]).path == "/stable/historical-market-capitalization"
    assert parse_qs(urlsplit(calls[0]).query) == {
        "symbol": ["ABC"],
        "from": ["2024-01-01"],
        "to": ["2024-12-31"],
        "limit": ["5000"],
        "apikey": ["synthetic-secret"],
    }
    assert FINANCIAL_METADATA_KEY in result.metadata


@pytest.mark.parametrize(
    "status,code", [(401, "authentication"), (403, "entitlement"), (429, "throttling")]
)
def test_safe_http_errors(monkeypatch, status, code):
    async def transport(url, **kwargs):
        response = Response({"error": "synthetic-secret"})
        response.status = status
        response.headers = {"Retry-After": "7"}
        return await kwargs["response_callback"](response, None)

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", transport)
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data(PARAMS, {"fmp_api_key": "synthetic-secret"}))
    envelope = error.value.to_dict()
    assert envelope["code"] == code and "synthetic-secret" not in str(envelope)
    if status == 429:
        assert envelope["retry_after_seconds"] == 7


@pytest.mark.parametrize(
    "params,start,end",
    [
        ({"symbol": "ABC"}, "2023-12-03", "2024-12-02"),
        ({"symbol": "ABC", "end_date": "2024-01-01"}, "2023-01-01", "2024-01-01"),
        ({"symbol": "ABC", "start_date": "2024-01-01"}, "2024-01-01", "2024-12-02"),
        (
            {"symbol": "ABC", "start_date": "2023-12-02", "end_date": "2024-12-02"},
            "2023-12-02",
            "2024-12-02",
        ),
    ],
)
def test_omitted_dates_and_utc_boundary(monkeypatch, params, start, end):
    class Clock:
        calls = 0

        @classmethod
        def now(cls, zone):
            assert zone is UTC
            cls.calls += 1
            return datetime(2024, 12, 2 if cls.calls == 1 else 3, tzinfo=UTC)

    calls = []

    async def transport(url, **kwargs):
        calls.append(parse_qs(urlsplit(url).query))
        return await kwargs["response_callback"](Response([]), None)

    monkeypatch.setattr("openbb_fmp.models.historical_market_cap.datetime", Clock)
    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", transport)
    result = asyncio.run(Fetcher.fetch_data(params))
    assert calls[0]["from"] == [start] and calls[0]["to"] == [end]
    effective = result.metadata[FINANCIAL_METADATA_KEY]["effective_query"]
    assert effective == {"symbol": "ABC", "start_date": start, "end_date": end}


def test_source_order_and_canonical_alias():
    rows = [
        {**ROW, "date": "2024-01-03", "marketCap": 3},
        {"symbol": "ABC", "date": "2024-01-01", "market_cap": 0},
        {**ROW, "date": "2024-01-03", "marketCap": 2},
    ]
    result = Fetcher.transform_data(
        Fetcher.transform_query(PARAMS), FMPAcquisition(rows, STAMP)
    )
    assert [row.market_cap for row in result.result] == [3, 0, 2]


@pytest.mark.parametrize("payload", [None, {}, "bad", ["bad"], [{"date": "bad"}]])
def test_real_malformed_response(monkeypatch, payload):
    async def transport(url, **kwargs):
        return await kwargs["response_callback"](Response(payload), None)

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", transport)
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data(PARAMS))
    assert error.value.code in {"invalid_response", "missing_data"}


def test_timeout_redaction(monkeypatch):
    async def transport(url, **kwargs):
        raise TimeoutError("synthetic-secret")

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", transport)
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data(PARAMS))
    assert error.value.code == "timeout"
    assert "synthetic-secret" not in str(error.value.to_dict())


def test_unresolved_invalid_window_before_transport(monkeypatch):
    class Clock:
        @staticmethod
        def now(zone):
            return datetime(2024, 1, 1, tzinfo=UTC)

    async def forbidden(*args, **kwargs):
        pytest.fail("invalid resolved window reached transport")

    monkeypatch.setattr("openbb_fmp.models.historical_market_cap.datetime", Clock)
    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", forbidden)
    with pytest.raises(FinancialError):
        asyncio.run(Fetcher.fetch_data({"symbol": "ABC", "start_date": "2024-01-02"}))


@pytest.mark.parametrize(
    "field,value",
    [
        ("date", 0),
        ("date", True),
        ("marketCap", float("nan")),
        ("marketCap", float("inf")),
    ],
)
def test_nonfinite_or_noncalendar_facts(field, value):
    with pytest.raises(FinancialError):
        Fetcher.transform_data(
            Fetcher.transform_query(PARAMS),
            FMPAcquisition([{**ROW, field: value}], STAMP),
        )


def test_date_underflow_safe(monkeypatch):
    async def forbidden(*args, **kwargs):
        pytest.fail("date underflow reached transport")

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", forbidden)
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data({"symbol": "ABC", "end_date": "0001-01-01"}))
    assert error.value.code == "invalid_parameters"


def test_frozen_annotations():
    from openbb_core.provider.standard_models.financial_annotations import (
        bind_data_annotation,
        bind_query_annotation,
    )

    contract = json.loads(
        (
            Path(__file__).parent
            / "fixtures/fmp_batch_a/contracts/historical_market_cap.json"
        ).read_text()
    )
    assert (
        bind_data_annotation(Data).model_dump(mode="json")
        == contract["data_annotation"]
    )
    assert (
        bind_query_annotation(Query).model_dump(mode="json")
        == contract["query_annotation"]
    )
