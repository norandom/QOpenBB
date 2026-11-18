"""Verify the frozen dividend-calendar contract through the safe FMP transport."""

import asyncio
import importlib.util
import json
import sys
from datetime import UTC, date, datetime
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest
from openbb_core.provider.standard_models.financial_metadata import (
    FINANCIAL_METADATA_KEY,
    FinancialResultMetadata,
)
from openbb_core.provider.utils.financial_errors import FinancialError

ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT.parent
    / "data-api/openbb_platform/providers/fmp/openbb_fmp/models/calendar_dividend.py"
)
SPEC = importlib.util.spec_from_file_location(
    "openbb_fmp.models.calendar_dividend", SOURCE
)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)
Query = MODULE.FMPCalendarDividendQueryParams
Data = MODULE.FMPCalendarDividendData
Fetcher = MODULE.FMPCalendarDividendFetcher
FIXTURE = ROOT / "tests/providers/fixtures/fmp_batch_b/events/calendar_dividend.json"
PARAMS = {"start_date": "2026-11-16", "end_date": "2026-11-22"}
ROW = {"date": "2026-11-20", "symbol": "MSFT", "yield": 2.5}
SYNTHETIC_KEY = "synthetic-secret"


class Response:
    def __init__(self, payload, status):
        self.headers = {}
        self.payload = payload
        self.status = status

    async def json(self):
        return self.payload


def intercept(monkeypatch, payload, status=200):
    calls = []

    async def transport(url, **kwargs):
        calls.append(url)
        return await kwargs["response_callback"](Response(payload, status), None)

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", transport)
    return calls


def fetch(params):
    return asyncio.run(Fetcher.fetch_data(params, {"fmp_api_key": SYNTHETIC_KEY}))


def test_frozen_schemas():
    contract = json.loads(FIXTURE.read_text(encoding="utf-8"))
    for model, key in [(Query, "query"), (Data, "data")]:
        for mode in ("validation", "serialization"):
            actual = model.model_json_schema(mode=mode)
            expected = contract[key][mode]
            actual.pop("description", None)
            actual["title"] = expected["title"]
            assert actual == expected
    assert Data.__alias_dict__ == contract["retained_baseline"]["aliases"]


@pytest.mark.parametrize(
    "params",
    [{**PARAMS, "start_date": value} for value in (True, 0, None, "2026-11-6", "")]
    + [{**PARAMS, "end_date": value} for value in ([], "2026-11-23", "2026-11-15")]
    + [
        {**PARAMS, "symbol": "MSFT"},
        {**PARAMS, "limit": 1},
        {},
        {"end_date": date(2026, 11, 22)},
    ],
)
def test_invalid_admission_has_zero_sends(monkeypatch, params):
    calls = intercept(monkeypatch, [ROW])
    with pytest.raises(FinancialError) as error:
        fetch(params)
    assert error.value.code == "invalid_parameters"
    assert calls == []


@pytest.mark.parametrize("count", [2, 250, 251])
def test_marketwide_calendar_and_provenance(monkeypatch, count):
    earlier = {
        "date": "2026-11-17",
        "symbol": "AAPL",
        "dividend": 0,
        "adjDividend": 1.25,
        "yield": 0,
        "recordDate": "",
        "declarationDate": "2026-11-01",
        "paymentDate": "2026-12-01",
    }
    calls = intercept(monkeypatch, [ROW, earlier] + [ROW] * (count - 2))
    result = fetch(PARAMS)
    assert len(calls) == 1
    wire = urlsplit(calls[0])
    assert (wire.scheme, wire.netloc, wire.path) == (
        "https",
        "financialmodelingprep.com",
        "/stable/dividends-calendar",
    )
    assert parse_qs(wire.query) == {
        "from": ["2026-11-16"],
        "to": ["2026-11-22"],
        "apikey": [SYNTHETIC_KEY],
    }
    first, second = result.result[:2]
    assert (first.symbol, second.symbol) == ("MSFT", "AAPL")
    assert first.ex_dividend_date == date(2026, 11, 20)
    assert first.amount is None and first.adjusted_amount is None
    assert first.dividend_yield == 0.025
    assert second.model_dump(mode="json") == {
        "ex_dividend_date": "2026-11-17",
        "symbol": "AAPL",
        "amount": 0.0,
        "name": None,
        "record_date": None,
        "payment_date": "2026-12-01",
        "declaration_date": "2026-11-01",
        "adjusted_amount": 1.25,
        "dividend_yield": 0.0,
        "frequency": None,
    }
    meta = FinancialResultMetadata.model_validate(
        result.metadata[FINANCIAL_METADATA_KEY]
    )
    assert len(result.result) == meta.bounds.returned_count == min(count, 250)
    assert meta.bounds.requested_limit is None
    assert meta.bounds.effective_limit == 250
    assert meta.bounds.truncated is (True if count > 250 else None)
    assert meta.bounds.completeness == ("partial" if count > 250 else "unknown")
    assert meta.provider == "fmp"
    assert meta.source.endpoint == "dividends-calendar"
    assert meta.retrieved_at.utcoffset() == UTC.utcoffset(datetime.now(UTC))
    assert meta.model_dump(mode="json")["effective_query"] == PARAMS
    assert meta.fields["amount"].currency is None
    assert meta.fields["dividend_yield"].unit == "ratio"
    assert meta.fields["dividend_yield"].value_origin == "provider_calculation"
    assert SYNTHETIC_KEY not in str(result.metadata)


@pytest.mark.parametrize(
    "payload,code",
    [
        ([], "missing_data"),
        (None, "missing_data"),
        ({"historical": [ROW]}, "invalid_response"),
        ([ROW] * 250 + [None], "invalid_response"),
        ([ROW] * 250 + [{"date": ROW["date"]}], "invalid_response"),
        ([ROW] * 250 + [{**ROW, "symbol": " "}], "invalid_response"),
        ([ROW] * 250 + [{**ROW, "date": ""}], "invalid_response"),
        ([ROW] * 250 + [{**ROW, "date": "2026-11-2"}], "invalid_response"),
        ([ROW] * 250 + [{**ROW, "recordDate": True}], "invalid_response"),
        ([ROW] * 250 + [{**ROW, "dividend": True}], "invalid_response"),
        ([ROW] * 250 + [{**ROW, "adjDividend": "2"}], "invalid_response"),
        ([ROW] * 250 + [{**ROW, "yield": float("inf")}], "invalid_response"),
    ],
)
def test_empty_or_malformed_acquisition(monkeypatch, payload, code):
    calls = intercept(monkeypatch, payload)
    with pytest.raises(FinancialError) as error:
        fetch(PARAMS)
    assert error.value.code == code
    assert len(calls) == 1


@pytest.mark.parametrize(
    "status,code",
    [
        (401, "authentication"),
        (403, "entitlement"),
        (429, "throttling"),
        (500, "upstream"),
    ],
)
def test_safe_transport_errors(monkeypatch, status, code):
    calls = intercept(monkeypatch, {"error": SYNTHETIC_KEY}, status)
    with pytest.raises(FinancialError) as error:
        fetch(PARAMS)
    assert error.value.code == code
    assert SYNTHETIC_KEY not in str(error.value.to_dict())
    assert len(calls) == 1


def test_frozen_serialization_example(monkeypatch):
    examples = json.loads(
        FIXTURE.with_name("serialization_examples.json").read_text(encoding="utf-8")
    )
    sample = next(item for item in examples if item["model"] == "calendar_dividend")
    calls = intercept(monkeypatch, [sample["raw"]])
    result = fetch({"start_date": date(2026, 1, 1), "end_date": date(2026, 1, 1)})
    assert result.result[0].model_dump(mode="json") == sample["expected"]
    assert len(calls) == 1


@pytest.mark.parametrize(
    "failure,code", [(TimeoutError, "timeout"), (ConnectionError, "upstream")]
)
def test_transport_failures_do_not_retry(monkeypatch, failure, code):
    calls = []

    async def transport(url, **kwargs):
        calls.append(url)
        raise failure(SYNTHETIC_KEY)

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", transport)
    with pytest.raises(FinancialError) as error:
        fetch(PARAMS)
    assert error.value.code == code
    assert SYNTHETIC_KEY not in str(error.value.to_dict())
    assert len(calls) == 1
