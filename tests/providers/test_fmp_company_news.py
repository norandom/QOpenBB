"""Production stock news acquisition contracts, entirely offline."""

import asyncio
import json
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest
from openbb_core.provider.standard_models.financial_annotations import (
    bind_data_annotation,
    bind_query_annotation,
    render_field_templates,
)
from openbb_core.provider.standard_models.financial_metadata import (
    FINANCIAL_METADATA_KEY,
)
from openbb_core.provider.utils.financial_errors import FinancialError
from openbb_fmp.models.company_news import FMPCompanyNewsData as Data
from openbb_fmp.models.company_news import FMPCompanyNewsFetcher as Fetcher
from openbb_fmp.models.company_news import FMPCompanyNewsQueryParams as Query

HERE = Path(__file__).parent / "fixtures/fmp_batch_b/documents"
ROW = json.loads((HERE / "serialization_examples.json").read_text())[0]["raw"]


@pytest.fixture
def transport(monkeypatch):
    def install(payload, status=200, failure=None):
        calls = []

        class Response:
            def __init__(self):
                self.headers = {}

            async def json(self):
                return payload

        async def send(url, **kwargs):
            calls.append(url)
            if failure:
                raise failure("secret")
            response = Response()
            response.status = status
            return await kwargs["response_callback"](response, None)

        monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", send)
        return calls

    return install


def test_frozen_schemas():
    contract = json.loads((HERE / "company_news.json").read_text())["expected"]
    for model, prefix in [(Query, "query"), (Data, "row")]:
        for mode in ["validation", "serialization"]:
            schema = model.model_json_schema(mode=mode)
            if model is Data:
                for name, field in schema["properties"].items():
                    assert (
                        field.pop("description") == Data.model_fields[name].description
                    )
            assert schema == contract[f"{prefix}_{mode}"]


def test_canonical_annotation_binding_and_rendering(transport):
    assert bind_query_annotation(Query).response_policy.limit_parameter == "limit"
    bound = bind_data_annotation(Data)
    fields = render_field_templates(Data)
    assert set(fields) == set(Data.model_fields) == set(bound.fields)
    calls = transport([ROW])
    result = asyncio.run(Fetcher.fetch_data({"symbol": "AAPL"}))
    metadata = result.metadata[FINANCIAL_METADATA_KEY]
    for name, field in fields.items():
        assert field.definition == Data.model_fields[name].description
        assert len(field.definition.split()) >= 5
        assert metadata["fields"][name]["definition"] == field.definition
        assert metadata["fields"][name]["source"] == field.source
    assert len(calls) == 1


def test_examples_and_source_order(transport):
    examples = json.loads((HERE / "serialization_examples.json").read_text())
    for example in [x for x in examples if x["model"] == "company_news"]:
        calls = transport([example["raw"]])
        result = asyncio.run(Fetcher.fetch_data(example["query"]))
        assert [x.model_dump(mode="json") for x in result.result] == example["expected"]
        assert len(calls) == 1


@pytest.mark.parametrize(
    "params",
    [
        {},
        {"symbol": None},
        {"symbol": "AAPL,MSFT"},
        {"symbol": "A A"},
        {"symbol": "AAPL", "press_release": True},
        {"symbol": "AAPL", "page": True},
        {"symbol": "AAPL", "page": 100},
        {"symbol": "AAPL", "limit": 0},
        {"symbol": "AAPL", "limit": 51},
        {"symbol": "AAPL", "limit": "2"},
        {"symbol": "AAPL", "start_date": "2026-01-01"},
        {"symbol": "AAPL", "start_date": "2026-01-01", "end_date": "2026-02-01"},
        {"symbol": "AAPL", "start_date": None},
        {"symbol": "AAPL", "start_date": "2026-1-01", "end_date": "2026-01-02"},
    ],
)
def test_invalid_zero_sends(transport, params):
    calls = transport([ROW])
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data(params))
    assert error.value.code == "invalid_parameters" and not calls


def test_wire_bounds_and_literal_text(transport):
    second = {
        **ROW,
        "publishedDate": "2025-01-01T01:02:03",
        "text": "  ",
        "title": "Second",
    }
    calls = transport([ROW, second, ROW])
    params = {
        "symbol": "aapl",
        "start_date": "2026-01-01",
        "end_date": "2026-01-31",
        "page": 0,
        "limit": 2,
    }
    result = asyncio.run(Fetcher.fetch_data(params, {"fmp_api_key": "secret"}))
    assert len(calls) == 1
    url = urlsplit(calls[0])
    assert url.path == "/stable/news/stock"
    assert parse_qs(url.query) == {
        "symbols": ["AAPL"],
        "from": ["2026-01-01"],
        "to": ["2026-01-31"],
        "page": ["0"],
        "limit": ["2"],
        "apikey": ["secret"],
    }
    assert [r.title for r in result.result] == [ROW["title"], "Second"]
    assert (
        result.result[0].author is None
        and result.result[0].publisher == ROW["publisher"]
    )
    assert result.result[0].excerpt == ROW["text"]
    assert result.result[1].content_status == "metadata_only"
    meta = result.metadata[FINANCIAL_METADATA_KEY]
    assert meta["effective_query"]["symbol"] == "AAPL"
    assert meta["bounds"]["truncated"] is True and meta["bounds"]["returned_count"] == 2
    assert meta["source"]["endpoint"] == "news/stock" and meta["retrieved_at"]
    assert "secret" not in str(meta)


@pytest.mark.parametrize(
    "payload,code",
    [
        ([], "missing_data"),
        ({}, "missing_data"),
        ({"rows": [ROW]}, "invalid_response"),
        ([None], "invalid_response"),
        ([{**ROW, "symbol": "MSFT"}], "invalid_response"),
        ([{**ROW, "title": " "}], "invalid_response"),
        ([{**ROW, "text": 42}], "invalid_response"),
        ([{**ROW, "publishedDate": 123}], "invalid_response"),
        ([{**ROW, "url": "javascript:alert(1)"}], "invalid_response"),
        ([{**ROW, "url": "https://user:pass@example.test/"}], "invalid_response"),
        (
            [ROW] * 10 + [{**ROW, "url": "https://example.test/ bad"}],
            "invalid_response",
        ),
    ],
)
def test_empty_malformed_before_clip(transport, payload, code):
    calls = transport(payload)
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data({"symbol": "AAPL"}))
    assert error.value.code == code and len(calls) == 1


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
def test_safe_errors(transport, status, failure, code):
    calls = transport({"error": "secret"}, status, failure)
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data({"symbol": "AAPL"}, {"fmp_api_key": "secret"}))
    assert error.value.code == code and len(calls) == 1
    assert "secret" not in str(error.value.to_dict())


def test_full_page_and_unknown_attribution(transport):
    raw = {k: v for k, v in ROW.items() if k not in {"site", "publisher", "text"}}
    raw.update(author="Must not infer an author", body="Not a supplied article body")
    calls = transport([raw])
    result = asyncio.run(Fetcher.fetch_data({"symbol": "AAPL", "limit": 1}))
    row = result.result[0]
    assert row.source is None and row.publisher is None and row.author is None
    assert row.body is None and row.content_status == "metadata_only"
    bounds = result.metadata[FINANCIAL_METADATA_KEY]["bounds"]
    assert bounds["truncated"] is None and bounds["completeness"] == "unknown"
    assert len(calls) == 1


@pytest.mark.parametrize(
    "timestamp",
    [
        "2026-01-02T03:04:05.1234567",
        "2026-01-02T03:04:05+01:02:03.1234567",
        "2026-01-02T03:04:05+01:60",
        "2026-01-02T03:04:05+24:00",
        "2026-01-02T03:04:05+01:02:03",
        "2026-01-02X03:04:05",
    ],
)
def test_unrepresentable_publication_time_rejects(transport, timestamp):
    calls = transport([{**ROW, "publishedDate": timestamp}])
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data({"symbol": "AAPL"}))
    assert error.value.code == "invalid_response" and len(calls) == 1


@pytest.mark.parametrize(
    "timestamp,expected",
    [
        ("2026-01-02 03:04:05", "2026-01-02T03:04:05"),
        ("2026-01-02T03:04:05.1Z", "2026-01-02T03:04:05.100000Z"),
        ("2026-01-02T03:04:05.123456-05:30", "2026-01-02T03:04:05.123456-05:30"),
    ],
)
def test_representable_publication_time_preserved(transport, timestamp, expected):
    calls = transport([{**ROW, "publishedDate": timestamp}])
    result = asyncio.run(Fetcher.fetch_data({"symbol": "AAPL"}))
    assert result.result[0].model_dump(mode="json")["date"] == expected
    assert len(calls) == 1
