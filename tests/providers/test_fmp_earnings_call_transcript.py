"""Offline transcript contract through the production Fetcher and safe transport."""

import asyncio
import json
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest
from openbb_core.provider.utils.financial_errors import FinancialError
from openbb_fmp.models.earnings_call_transcript import (
    FMPEarningsCallTranscriptData as Data,
)
from openbb_fmp.models.earnings_call_transcript import (
    FMPEarningsCallTranscriptFetcher as Fetcher,
)
from openbb_fmp.models.earnings_call_transcript import (
    FMPEarningsCallTranscriptQueryParams as Query,
)

FIXTURES = Path(__file__).parent / "fixtures/fmp_batch_b/documents"
PARAMS = {"symbol": "aapl", "year": 2025, "quarter": 1}
ROW = {
    "symbol": "AAPL",
    "year": 2025,
    "period": "Q1",
    "date": "2025-02-02T17:30:01-05:00",
    "content": "  Speaker: <script>x</script>\n\n",
}


class Response:
    def __init__(self, payload, status=200):
        self.payload, self.status, self.headers = payload, status, {}

    async def json(self):
        return self.payload


def intercept(monkeypatch, payload, status=200):
    calls = []

    async def transport(url, **kwargs):
        calls.append(url)
        return await kwargs["response_callback"](Response(payload, status), None)

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", transport)
    return calls


@pytest.mark.parametrize(
    "patch",
    [
        {"quarter": True},
        {"quarter": "1"},
        {"quarter": 0},
        {"quarter": 5},
        {"quarter": None},
        {"year": True},
        {"year": 1899},
        {"symbol": "A,B"},
        {"symbol": None},
        {"extra": 1},
    ],
)
def test_invalid_zero_sends(monkeypatch, patch):
    calls = intercept(monkeypatch, [ROW])
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data({**PARAMS, **patch}))
    assert error.value.code == "invalid_parameters"
    assert calls == []


def test_one_send_literal_text_and_metadata(monkeypatch):
    calls = intercept(monkeypatch, [ROW])
    result = asyncio.run(Fetcher.fetch_data(PARAMS))
    row = result.result[0]
    assert row.content == ROW["content"]
    assert str(row.date) == "2025-02-02"
    assert row.event_datetime.isoformat() == ROW["date"]
    assert row.quarter == "Q1"
    meta = result.metadata["__qopenbb_financial__"]
    assert meta["effective_query"] == {**PARAMS, "symbol": "AAPL"}
    assert meta["bounds"]["returned_count"] == 1
    assert meta["bounds"]["completeness"] == "unknown"
    assert len(calls) == 1
    assert urlsplit(calls[0]).path == "/stable/earning-call-transcript"
    assert parse_qs(urlsplit(calls[0]).query) == {
        "symbol": ["AAPL"],
        "year": ["2025"],
        "quarter": ["1"],
    }


@pytest.mark.parametrize(
    "payload,code",
    [
        ([], "missing_data"),
        ([ROW, ROW], "invalid_response"),
        ([{**ROW, "period": "Q2"}], "invalid_response"),
        ([{**ROW, "year": 2024}], "invalid_response"),
        ([{**ROW, "symbol": "OTHER"}], "invalid_response"),
        ([{**ROW, "content": " \n"}], "invalid_response"),
        ([{**ROW, "date": "bad"}], "invalid_response"),
        ([{}], "invalid_response"),
        ("bad", "invalid_response"),
    ],
)
def test_invalid_response(monkeypatch, payload, code):
    calls = intercept(monkeypatch, payload)
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data(PARAMS))
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
def test_safe_errors(monkeypatch, status, code):
    calls = intercept(monkeypatch, {"error": "secret"}, status)
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data(PARAMS, {"fmp_api_key": "secret"}))
    assert error.value.code == code
    assert "secret" not in str(error.value.to_dict())
    assert len(calls) == 1


def test_frozen_examples(monkeypatch):
    for example in json.loads((FIXTURES / "serialization_examples.json").read_text()):
        if example["model"] != "earnings_call_transcript":
            continue
        intercept(monkeypatch, [example["raw"]])
        result = asyncio.run(Fetcher.fetch_data(example["query"]))
        assert [r.model_dump(mode="json") for r in result.result] == example["expected"]


def test_schema_shape():
    expected = json.loads((FIXTURES / "earnings_call_transcript.json").read_text())[
        "expected"
    ]
    for cls, key in [(Query, "query"), (Data, "row")]:
        for mode in ["validation", "serialization"]:
            schema = cls.model_json_schema(mode=mode)
            for field in schema["properties"].values():
                field.pop("description", None)
            assert schema == expected[f"{key}_{mode}"]


@pytest.mark.parametrize(
    "failure,code", [(TimeoutError, "timeout"), (ConnectionError, "upstream")]
)
def test_no_retry_transport_failure(monkeypatch, failure, code):
    calls = []

    async def transport(url, **kwargs):
        calls.append(url)
        raise failure("secret")

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", transport)
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data(PARAMS))
    assert error.value.code == code
    assert "secret" not in str(error.value.to_dict())
    assert len(calls) == 1


@pytest.mark.parametrize("field", ["symbol", "year", "quarter"])
def test_missing_required_input_zero_sends(monkeypatch, field):
    calls = intercept(monkeypatch, [ROW])
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data({k: v for k, v in PARAMS.items() if k != field}))
    assert error.value.code == "invalid_parameters"
    assert calls == []


@pytest.mark.parametrize(
    "wire",
    [
        "20250202",
        "2025-02-02T17:30:01+01:60",
        "2025-02-02T17:30:01+24:00",
        "2025-W05-7",
        "2025W057",
        "2025-02-02T17:30:01.1234567",
        "2025-02-02T17:30:01,1234567",
        "2025-02-02T17:30:01+01:02:03",
        "2025-02-02T17:30:01+00:00:00.1",
        "2025-02-02T17:30:01+01:02:03.1234567",
        "2025-02-02T17.1234567",
        "2025-02-02T17:30.1234567",
    ],
)
def test_reject_unrepresentable_or_noncanonical_event_time(monkeypatch, wire):
    calls = intercept(monkeypatch, [{**ROW, "date": wire}])
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data(PARAMS))
    assert error.value.code == "invalid_response"
    assert len(calls) == 1


@pytest.mark.parametrize(
    "wire,expected",
    [
        ("2025-02-02", None),
        ("2025-02-02T00:00:00", "2025-02-02T00:00:00"),
        ("2025-02-02 17:30:01.123456", "2025-02-02T17:30:01.123456"),
        ("2025-02-02T17:30:01.123456-05:30", "2025-02-02T17:30:01.123456-05:30"),
        ("2025-02-02T17:30:01Z", "2025-02-02T17:30:01+00:00"),
    ],
)
def test_supported_event_time_preserves_values(monkeypatch, wire, expected):
    intercept(monkeypatch, [{**ROW, "date": wire}])
    row = asyncio.run(Fetcher.fetch_data(PARAMS)).result[0]
    assert str(row.date) == "2025-02-02"
    assert (row.event_datetime.isoformat() if row.event_datetime else None) == expected
