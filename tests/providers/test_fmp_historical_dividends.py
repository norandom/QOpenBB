"""Historical dividend contracts through the actual single-send transport."""

import asyncio
import importlib.util
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest
from openbb_core.provider.standard_models.financial_metadata import (
    FINANCIAL_METADATA_KEY,
)
from openbb_core.provider.utils.financial_errors import FinancialError
from openbb_fmp.utils.helpers import FMPAcquisition

ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT.parent
    / "data-api/openbb_platform/providers/fmp/openbb_fmp/models/historical_dividends.py"
)
spec = importlib.util.spec_from_file_location(
    "openbb_fmp.models.historical_dividends", SOURCE
)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
Query, Data, Fetcher = (
    getattr(module, "FMPHistoricalDividends" + suffix)
    for suffix in ("QueryParams", "Data", "Fetcher")
)
FIX = ROOT / "tests/providers/fixtures/fmp_batch_b/events"
ROW = {"date": "2026-01-01", "dividend": 0, "yield": 0}
STAMP = datetime(2026, 1, 1, tzinfo=UTC)


def test_schema_and_serialization():
    contract = json.loads((FIX / "historical_dividends.json").read_text())
    for model, key in [(Query, "query"), (Data, "data")]:
        for mode in ("validation", "serialization"):
            actual = model.model_json_schema(mode=mode)
            expected = contract[key][mode]
            actual.pop("description", None)
            actual["title"] = expected["title"]
            assert actual == expected
    sample = json.loads((FIX / "serialization_examples.json").read_text())[0]
    result = Fetcher.transform_data(
        Query(symbol="AAPL"), FMPAcquisition([sample["raw"]], STAMP)
    )
    assert result.result[0].model_dump(mode="json") == sample["expected"]


@pytest.mark.parametrize(
    "params",
    [{"symbol": v} for v in (None, True, "", "A,B", "A&x=1", "A B", "A" * 51)]
    + [{"symbol": "A", "limit": v} for v in (True, None, 0, 101, "2")]
    + [{"symbol": "A", "start_date": v} for v in (None, True, 0, "2026-01-01T01:00:00")]
    + [
        {"symbol": "A", "unknown": 1},
        {"symbol": "A", "start_date": "2026-02-01", "end_date": "2026-01-01"},
    ],
)
def test_invalid_zero_send(monkeypatch, params):
    async def forbidden(*args, **kwargs):
        pytest.fail("Invalid query reached transport")

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", forbidden)
    with pytest.raises(FinancialError) as exc:
        asyncio.run(Fetcher.fetch_data(params))
    assert exc.value.code == "invalid_parameters"


class Response:
    status = 200

    def __init__(self, payload):
        self.headers = {}
        self.payload = payload

    async def json(self):
        return self.payload


@pytest.mark.parametrize("payload", [[ROW], []])
def test_one_send(monkeypatch, payload):
    calls = []

    async def transport(url, **kwargs):
        calls.append(url)
        return await kwargs["response_callback"](Response(payload), None)

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", transport)
    if not payload:
        with pytest.raises(FinancialError) as exc:
            asyncio.run(
                Fetcher.fetch_data({"symbol": "aapl"}, {"fmp_api_key": "synthetic"})
            )
        assert exc.value.code == "missing_data"
    else:
        result = asyncio.run(
            Fetcher.fetch_data({"symbol": "aapl"}, {"fmp_api_key": "synthetic"})
        )
        assert result.result[0].dividend_yield == 0
    assert len(calls) == 1
    assert urlsplit(calls[0]).path == "/stable/dividends"
    assert parse_qs(urlsplit(calls[0]).query) == {
        "symbol": ["AAPL"],
        "limit": ["20"],
        "apikey": ["synthetic"],
    }


def test_filter_clip_order_and_metadata():
    query = Query(symbol="AAPL", limit=1, start_date="2026-01-02")
    result = Fetcher.transform_data(
        query, FMPAcquisition([ROW, {**ROW, "date": "2026-01-03"}], STAMP)
    )
    assert result.result == []
    meta = result.metadata[FINANCIAL_METADATA_KEY]
    assert meta["bounds"]["truncated"] is True
    assert meta["bounds"]["completeness"] == "partial"
    assert meta["bounds"]["returned_count"] == 0
    assert meta["effective_query"]["limit"] == 1
    assert datetime.fromisoformat(meta["retrieved_at"]) == STAMP
    assert meta["fields"]["amount"]["currency"] is None


@pytest.mark.parametrize(
    "bad",
    [
        {"date": "bad"},
        {"dividend": True},
        {"dividend": "1"},
        {"yield": float("inf")},
        {"yield": True},
        {"recordDate": 0},
        {"symbol": "FOREIGN"},
        {"symbol": None},
    ],
)
def test_all_rows_validated_before_clip(bad):
    with pytest.raises(FinancialError) as exc:
        Fetcher.transform_data(
            Query(symbol="AAPL", limit=1), FMPAcquisition([ROW, {**ROW, **bad}], STAMP)
        )
    assert exc.value.code == "invalid_response"


def test_dates_amounts_duplicates():
    rows = [
        {
            **ROW,
            "yield": 2.5,
            "adjDividend": None,
            "recordDate": "",
            "declarationDate": "2025-12-01",
            "paymentDate": "2026-01-10",
        },
        {**ROW, "adjDividend": 0},
    ]
    result = Fetcher.transform_data(Query(symbol="AAPL"), FMPAcquisition(rows, STAMP))
    assert len(result.result) == 2
    first, second = result.result
    assert first.dividend_yield == 0.025 and first.adjusted_amount is None
    assert first.record_date is None and second.adjusted_amount == 0
    assert first.symbol == "AAPL"


@pytest.mark.parametrize(
    "status,code",
    [
        (401, "authentication"),
        (403, "entitlement"),
        (429, "throttling"),
        (500, "upstream"),
    ],
)
def test_safe_errors(monkeypatch, status, code):
    async def transport(url, **kwargs):
        response = Response({"error": "synthetic-secret"})
        response.status = status
        return await kwargs["response_callback"](response, None)

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", transport)
    with pytest.raises(FinancialError) as exc:
        asyncio.run(
            Fetcher.fetch_data({"symbol": "AAPL"}, {"fmp_api_key": "synthetic-secret"})
        )
    assert exc.value.code == code
    assert "synthetic-secret" not in str(exc.value.to_dict())


@pytest.mark.parametrize(
    "payload", [None, {}, {"historical": [ROW]}, [None], [{"date": "2026-01-01"}]]
)
def test_malformed_acquisition(monkeypatch, payload):
    async def transport(url, **kwargs):
        return await kwargs["response_callback"](Response(payload), None)

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", transport)
    with pytest.raises(FinancialError):
        asyncio.run(Fetcher.fetch_data({"symbol": "AAPL"}))


@pytest.mark.parametrize("count,limit", [(0, 20), (1, 1), (20, 20)])
def test_full_page_cannot_prove_exhaustive_history(count, limit):
    result = Fetcher.transform_data(
        Query(symbol="AAPL", limit=limit), FMPAcquisition([ROW] * count, STAMP)
    )
    bounds = result.metadata[FINANCIAL_METADATA_KEY]["bounds"]
    assert bounds["completeness"] == "unknown"
    assert bounds["truncated"] is None
    assert bounds["returned_count"] == count
