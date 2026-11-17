"""Quote identity, source timestamps and financial units survive native fetching."""

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
from openbb_fmp.models.equity_quote import (
    FMPEquityQuoteData as Row,
)
from openbb_fmp.models.equity_quote import (
    FMPEquityQuoteFetcher as Fetcher,
)
from openbb_fmp.models.equity_quote import (
    FMPEquityQuoteQueryParams as Query,
)

FROZEN = json.loads(
    (
        Path(__file__).parent / "fixtures/fmp_batch_a/contracts/equity_quote.json"
    ).read_text()
)


class Response:
    def __init__(self, payload, status):
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


def test_frozen_contract():
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
    [
        {"symbol": x}
        for x in [None, True, "", "A,B", "A&x=y", "A" * 51, "A\n", "A\t", "A\x7f"]
    ]
    + [{"symbol": "A", "limit": 1}, {}],
)
def test_raw_query_rejected_before_io(monkeypatch, params):
    async def forbidden(*args, **kwargs):
        pytest.fail("Invalid query reached transport")

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", forbidden)
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data(params, {}))
    assert error.value.code == "invalid_parameters"


def test_encoded_single_request_and_receipt(monkeypatch):
    before = datetime.now(UTC)
    result, calls = run(monkeypatch, [{"symbol": "BRK/B"}], {"symbol": " brk/b "})
    url, _ = calls[0]
    assert urlsplit(url).path == "/stable/quote"
    assert "BRK%2FB" in url and "canary%26secret" in url
    assert parse_qs(urlsplit(url).query) == {
        "symbol": ["BRK/B"],
        "apikey": ["canary&secret"],
    }
    meta = result.metadata[FINANCIAL_METADATA_KEY]
    assert before <= datetime.fromisoformat(meta["retrieved_at"]) <= datetime.now(UTC)
    assert meta["effective_query"] == {"symbol": "BRK/B"}
    assert "canary" not in json.dumps(meta)


@pytest.mark.parametrize("stamp", [0, 1785430812, 1785430812.125, "0", None])
def test_timestamp_zero_precision_and_null(monkeypatch, stamp):
    result, _ = run(
        monkeypatch,
        [
            {
                "symbol": "MSFT",
                "timestamp": stamp,
                "changePercentage": 0,
                "change": -1.25,
            }
        ],
    )
    row = result.result[0]
    assert row.last_timestamp == (
        None if stamp is None else datetime.fromtimestamp(float(stamp), UTC)
    )
    assert row.change_percent == 0 and row.change == -1.25


@pytest.mark.parametrize("payload", [[], [{"symbol": "MSFT", "price": None}]])
def test_empty_and_unavailable_financial_metadata(monkeypatch, payload):
    result, _ = run(monkeypatch, payload)
    meta = result.metadata[FINANCIAL_METADATA_KEY]
    assert len(result.result) == len(payload)
    assert meta["bounds"]["returned_count"] == len(payload)
    assert meta["bounds"]["completeness"] == "unknown"
    assert meta["point_in_time_safe"] is False
    assert set(meta["fields"]) == set(Row.model_fields)
    assert meta["fields"]["last_price"]["availability"] == "missing"
    for field in meta["fields"].values():
        assert field["currency"] is None and field["publication_date_field"] is None
    assert meta["fields"]["market_cap"]["observation_date_field"] is None
    assert meta["fields"]["market_cap"]["financial_basis"] == {
        "market_date": None,
        "share_count": None,
    }


def test_source_values_aliases_and_units(monkeypatch):
    payload = {
        "symbol": "MSFT",
        "price": 101.25,
        "open": 100,
        "dayHigh": 103,
        "dayLow": 99,
        "close": 100.5,
        "bid": 101,
        "ask": 102,
        "previousClose": 98,
        "changePercentage": 2.5,
        "change": 3.25,
        "volume": 0,
        "marketCap": 0,
        "priceAvg50": 97.5,
        "priceAvg200": 92.5,
    }
    result, _ = run(monkeypatch, [payload])
    row = result.result[0]
    assert [
        row.last_price,
        row.open,
        row.high,
        row.low,
        row.close,
        row.bid,
        row.ask,
        row.prev_close,
    ] == [101.25, 100, 103, 99, 100.5, 101, 102, 98]
    assert row.change_percent == 0.025 and row.change == 3.25
    assert row.volume == row.market_cap == 0
    assert row.ma50 == 97.5 and row.ma200 == 92.5
    assert row.model_dump(by_alias=True)["ma_50"] == 97.5
    assert set(row.model_dump(by_alias=True)) == set(
        FROZEN["data"]["serialization"]["properties"]
    )
    fields = result.metadata[FINANCIAL_METADATA_KEY]["fields"]
    assert fields["volume"]["unit"] == "shares"
    assert fields["last_price"]["unit"] == "currency/share"
    assert fields["market_cap"]["value_origin"] == "provider_calculation"


@pytest.mark.parametrize(
    "payload",
    [
        [{"symbol": "MSFT"}] * 2,
        [{"symbol": "OTHER"}],
        [{}],
        [{"symbol": None}],
        {"bad": "canary"},
        [None],
    ],
)
def test_cardinality_identity_and_required_facts(monkeypatch, payload):
    assert_invalid(monkeypatch, payload)


def assert_invalid(monkeypatch, payload):
    with pytest.raises(FinancialError) as error:
        run(monkeypatch, payload)
    assert error.value.code == "invalid_response"
    assert error.value.__cause__ is None and error.value.__context__ is None
    assert "canary" not in str(error.value)


@pytest.mark.parametrize(
    "field",
    [
        "bidSize",
        "askSize",
        "lastSize",
        "sequenceNumber",
        "volume",
        "price",
        "marketCap",
        "changePercentage",
    ],
)
@pytest.mark.parametrize(
    "value", ["malformed-canary", float("inf"), float("nan"), {}, True]
)
def test_bad_numbers_safe_native_fetch(monkeypatch, field, value):
    assert_invalid(monkeypatch, [{"symbol": "MSFT", field: value}])


@pytest.mark.parametrize(
    "stamp", ["bad-canary", "2026-01-01", {}, True, float("nan"), float("inf"), 10**25]
)
def test_invalid_timestamp(monkeypatch, stamp):
    assert_invalid(monkeypatch, [{"symbol": "MSFT", "timestamp": stamp}])


@pytest.mark.parametrize(
    "payload,status,code",
    [
        ({"Error Message": "canary"}, 401, "authentication"),
        ({"Error Message": "canary"}, 403, "entitlement"),
        ({"Error Message": "canary"}, 429, "throttling"),
        (TimeoutError("canary"), 200, "timeout"),
        (ValueError("canary"), 200, "invalid_response"),
    ],
)
def test_transport_errors(monkeypatch, payload, status, code):
    with pytest.raises(FinancialError) as error:
        run(monkeypatch, payload, status=status)
    assert error.value.code == code
    assert "canary" not in str(error.value)
    assert error.value.__cause__ is None and error.value.__context__ is None
    if code == "throttling":
        assert error.value.retry_after_seconds == 23


def test_all_aliases_and_optional_dates(monkeypatch):
    payload = {"symbol": "MSFT"}
    for name, field in Row.model_fields.items():
        if name == "symbol":
            continue
        source = FROZEN["effective_aliases"].get(name, field.validation_alias or name)
        if name.endswith("timestamp"):
            payload[source] = (
                0 if name == "last_timestamp" else "2026-11-17T12:34:56.123456+00:00"
            )
        elif name in {
            "asset_type",
            "name",
            "exchange",
            "bid_exchange",
            "ask_exchange",
            "market_center",
            "last_tick",
        }:
            payload[source] = "source text"
        else:
            payload[source] = 0
    result, _ = run(monkeypatch, [payload])
    row = result.result[0]
    assert all(getattr(row, name) is not None for name in Row.model_fields)
    assert row.participant_timestamp.microsecond == 123456
    assert all(
        field["availability"] == "available"
        for field in result.metadata[FINANCIAL_METADATA_KEY]["fields"].values()
    )


@pytest.mark.parametrize(
    "field", ["participantTimestamp", "trfTimestamp", "sipTimestamp"]
)
@pytest.mark.parametrize("value", ["1785430812", 1785430812, "bad", {}, True])
def test_optional_timestamps_do_not_guess_unix(monkeypatch, field, value):
    assert_invalid(monkeypatch, [{"symbol": "MSFT", field: value}])


def test_optional_timestamps_null(monkeypatch):
    result, _ = run(
        monkeypatch,
        [
            {
                "symbol": "MSFT",
                "timestamp": None,
                "participantTimestamp": None,
                "trfTimestamp": None,
                "sipTimestamp": None,
            }
        ],
    )
    assert all(
        getattr(result.result[0], name) is None for name in FROZEN["date_contracts"]
    )


def test_owned_package_origins():
    import importlib

    root = Path(__file__).resolve().parents[2]
    api = root.parent / "data-api/openbb_platform"
    expected = {
        "qopenbb_data": root / "services/data-api/qopenbb_data",
        "openbb_core": api / "core/openbb_core",
        "openbb_fmp": api / "providers/fmp/openbb_fmp",
        "openbb_fred": api / "providers/fred/openbb_fred",
        "openbb_equity": api / "extensions/equity/openbb_equity",
        "openbb_economy": api / "extensions/economy/openbb_economy",
    }
    for package, directory in expected.items():
        module = importlib.import_module(package)
        assert Path(module.__file__).resolve().parent == directory.resolve()
