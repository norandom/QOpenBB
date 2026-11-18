"""Historical splits preserve listing identity and new:old orientation."""

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
from openbb_fmp.models.historical_splits import FMPHistoricalSplitsData as Data
from openbb_fmp.models.historical_splits import FMPHistoricalSplitsFetcher as Fetcher
from openbb_fmp.models.historical_splits import FMPHistoricalSplitsQueryParams as Query
from openbb_fmp.utils.helpers import FMPAcquisition

ROW = {"date": "2024-01-02", "numerator": 1, "denominator": 10}
STAMP = datetime(2024, 2, 3, tzinfo=UTC)


class Response:
    def __init__(self, payload, status=200):
        self.payload, self.status, self.headers = payload, status, {}

    async def json(self):
        return self.payload


def test_schemas():
    contract = json.loads(
        (
            Path(__file__).parent / "fixtures/fmp_batch_b/events/historical_splits.json"
        ).read_text()
    )
    for model, key in [(Query, "query"), (Data, "data")]:
        for mode in ["validation", "serialization"]:
            assert model.model_json_schema(mode=mode) == contract[key][mode]


@pytest.mark.parametrize(
    "params",
    [
        {},
        {"symbol": None},
        {"symbol": True},
        {"symbol": ["ABC"]},
        {"symbol": "A,B"},
        {"symbol": "A&apikey=x"},
        {"symbol": "A" * 51},
        {"symbol": "A B"},
        {"symbol": "ABC", "limit": 1},
    ],
)
def test_invalid_zero_sends(monkeypatch, params):
    async def forbidden(*args, **kwargs):
        pytest.fail("Invalid query reached transport")

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", forbidden)
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data(params))
    assert error.value.code == "invalid_parameters"


@pytest.mark.parametrize(
    "payload,code",
    [
        ([], "missing_data"),
        ({}, "missing_data"),
        ([ROW], None),
        ([ROW] * 101, None),
        ([ROW] * 100 + [{**ROW, "numerator": 0}], "invalid_response"),
        ([{**ROW, "symbol": "OTHER"}], "invalid_response"),
        ([{**ROW, "symbol": None}], "invalid_response"),
    ],
)
def test_transport_and_bounds(monkeypatch, payload, code):
    calls = []

    async def transport(url, **kwargs):
        calls.append(url)
        return await kwargs["response_callback"](Response(payload), None)

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", transport)
    if code:
        with pytest.raises(FinancialError) as error:
            asyncio.run(Fetcher.fetch_data({"symbol": "abc"}))
        assert error.value.code == code
    else:
        result = asyncio.run(Fetcher.fetch_data({"symbol": "abc"}))
        assert len(result.result) == min(len(payload), 100)
        assert result.result[0].numerator == 1 and result.result[0].denominator == 10
        assert result.result[0].symbol == "ABC"
        meta = result.metadata[FINANCIAL_METADATA_KEY]
        assert meta["effective_query"] == {"symbol": "ABC"}
        assert meta["bounds"]["returned_count"] == len(result.result)
        assert meta["bounds"]["truncated"] == (True if len(payload) > 100 else None)
        assert set(meta["fields"]) == set(Data.model_fields)
    assert len(calls) == 1
    assert urlsplit(calls[0]).path == "/stable/splits"
    assert parse_qs(urlsplit(calls[0]).query) == {"symbol": ["ABC"]}


@pytest.mark.parametrize(
    "patch",
    [
        {"date": "2024-1-02"},
        {"date": None},
        {"numerator": True},
        {"denominator": float("inf")},
        {"numerator": -1},
        {"symbol": " ABC "},
        {"symbol": 5},
    ],
)
def test_malformed_rows(patch):
    with pytest.raises(FinancialError):
        Fetcher.transform_data(
            Query(symbol="ABC"), FMPAcquisition([{**ROW, **patch}], STAMP)
        )


def test_order_nullable_components_and_receipt():
    result = Fetcher.transform_data(
        Query(symbol="ABC"), FMPAcquisition([ROW, {"date": "2020-01-01"}, ROW], STAMP)
    )
    assert [str(r.date) for r in result.result] == [
        "2024-01-02",
        "2020-01-01",
        "2024-01-02",
    ]
    assert result.result[1].numerator is None
    assert (
        datetime.fromisoformat(result.metadata[FINANCIAL_METADATA_KEY]["retrieved_at"])
        == STAMP
    )


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
        return await kwargs["response_callback"](
            Response({"error": "secret"}, status), None
        )

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", transport)
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data({"symbol": "ABC"}, {"fmp_api_key": "secret"}))
    assert error.value.code == code
    assert "secret" not in str(error.value.to_dict())


def test_frozen_serialization_example():
    examples = json.loads(
        (
            Path(__file__).parent
            / "fixtures/fmp_batch_b/events/serialization_examples.json"
        ).read_text()
    )
    example = next(e for e in examples if e["model"] == "historical_splits")
    result = Fetcher.transform_data(
        Query(symbol=example["requested_symbol"]),
        FMPAcquisition([example["raw"]], STAMP),
    )
    assert result.result[0].model_dump(mode="json") == example["expected"]


@pytest.mark.parametrize("value", ["", "A B", "abc", None, True])
def test_native_data_identity(value):
    with pytest.raises(ValueError):
        Data(**ROW, symbol=value)


@pytest.mark.parametrize(
    "failure,code", [(TimeoutError, "timeout"), (ConnectionError, "upstream")]
)
def test_transport_failure_without_retry(monkeypatch, failure, code):
    calls = []

    async def transport(url, **kwargs):
        calls.append(url)
        raise failure("secret")

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", transport)
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data({"symbol": "ABC"}))
    assert error.value.code == code and len(calls) == 1
