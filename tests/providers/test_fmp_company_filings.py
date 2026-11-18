"""Production filing metadata acquisition contracts, entirely offline."""

import asyncio
import json
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest
from openbb_core.provider.standard_models.financial_annotations import (
    render_field_templates,
)
from openbb_core.provider.standard_models.financial_metadata import (
    FINANCIAL_METADATA_KEY,
)
from openbb_core.provider.utils.financial_errors import FinancialError
from openbb_fmp.models.company_filings import FMPCompanyFilingsData as Data
from openbb_fmp.models.company_filings import FMPCompanyFilingsFetcher as Fetcher
from openbb_fmp.models.company_filings import FMPCompanyFilingsQueryParams as Query

HERE = Path(__file__).parent / "fixtures/fmp_batch_b/documents"
ROW = next(
    x["raw"]
    for x in json.loads((HERE / "serialization_examples.json").read_text())
    if x["model"] == "company_filings"
)
PARAMS = {"symbol": "AAPL", "start_date": "2026-01-01", "end_date": "2026-01-31"}


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
    contract = json.loads((HERE / "company_filings.json").read_text())["expected"]
    for model, prefix in [(Query, "query"), (Data, "row")]:
        for mode in ["validation", "serialization"]:
            schema = model.model_json_schema(mode=mode)
            # Descriptions add financial semantics without changing frozen structural contracts.
            for prop in schema["properties"].values():
                prop.pop("description", None)
            assert schema == contract[f"{prefix}_{mode}"]


def test_examples_and_source_order(transport):
    examples = json.loads((HERE / "serialization_examples.json").read_text())
    for example in [x for x in examples if x["model"] == "company_filings"]:
        calls = transport([example["raw"]])
        result = asyncio.run(Fetcher.fetch_data(example["query"]))
        assert [x.model_dump(mode="json") for x in result.result] == example["expected"]
        assert len(calls) == 1


@pytest.mark.parametrize(
    "change",
    [
        {"symbol": None},
        {"symbol": "AAPL,MSFT"},
        {"symbol": "A A"},
        {"cik": "123"},
        {"form_type": "10-Q"},
        {"page": True},
        {"page": 100},
        {"page": -1},
        {"limit": 0},
        {"limit": 101},
        {"limit": "2"},
        {"start_date": None},
        {"start_date": "2026-1-01"},
        {"end_date": "2027-01-01"},
        {"end_date": "2025-12-31"},
        {"start_date": "2026-01-01T00:00:00"},
        {"end_date": 123},
    ],
)
def test_invalid_zero_sends(transport, change):
    calls = transport([ROW])
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data({**PARAMS, **change}))
    assert error.value.code == "invalid_parameters" and not calls


@pytest.mark.parametrize("missing", ["symbol", "start_date", "end_date"])
def test_missing_zero_sends(transport, missing):
    calls = transport([ROW])
    with pytest.raises(FinancialError) as error:
        asyncio.run(
            Fetcher.fetch_data({k: v for k, v in PARAMS.items() if k != missing})
        )
    assert error.value.code == "invalid_parameters" and not calls


def test_wire_bounds_metadata_and_source_order(transport):
    second = {**ROW, "formType": "8-K", "filingDate": "2026-01-03"}
    calls = transport([ROW, second, ROW])
    result = asyncio.run(
        Fetcher.fetch_data(
            {**PARAMS, "symbol": "aapl", "limit": 2}, {"fmp_api_key": "secret"}
        )
    )
    assert len(calls) == 1
    url = urlsplit(calls[0])
    assert url.path == "/stable/sec-filings-search/symbol"
    assert parse_qs(url.query) == {
        "symbol": ["AAPL"],
        "from": ["2026-01-01"],
        "to": ["2026-01-31"],
        "page": ["0"],
        "limit": ["2"],
        "apikey": ["secret"],
    }
    assert [r.report_type for r in result.result] == ["10-Q", "8-K"]
    row = result.result[0]
    assert row.cik == "0000320193" and row.content_status == "metadata_only"
    assert row.filing_url != row.report_url
    meta = result.metadata[FINANCIAL_METADATA_KEY]
    assert meta["effective_query"]["symbol"] == "AAPL"
    assert meta["bounds"]["truncated"] is True and meta["bounds"]["returned_count"] == 2
    assert (
        meta["source"]["endpoint"] == "sec-filings-search/symbol"
        and meta["retrieved_at"]
    )
    assert meta["fields"]["accepted_date"]["source"] == "acceptedDate"
    assert "secret" not in str(meta)


@pytest.mark.parametrize(
    "payload,code",
    [
        ([], "missing_data"),
        ({}, "missing_data"),
        ({"rows": [ROW]}, "invalid_response"),
        ([None], "invalid_response"),
        ([{**ROW, "symbol": "MSFT"}], "invalid_response"),
        ([{**ROW, "symbol": "A A"}], "invalid_response"),
        ([{**ROW, "cik": 320193}], "invalid_response"),
        ([{**ROW, "acceptedDate": 123}], "invalid_response"),
        ([{**ROW, "acceptedDate": "not-a-date"}], "invalid_response"),
        ([{**ROW, "filingDate": "2026-01-02T12:00:00"}], "invalid_response"),
        ([{**ROW, "finalLink": "javascript:alert(1)"}], "invalid_response"),
        ([{**ROW, "link": "https://user:pass@example.test/"}], "invalid_response"),
        ([{**ROW, "finalLink": "https://example.test:bad/x"}], "invalid_response"),
        (
            [ROW] * 20 + [{**ROW, "finalLink": "https://example.test/ bad"}],
            "invalid_response",
        ),
    ],
)
def test_empty_malformed_before_clip(transport, payload, code):
    calls = transport(payload)
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data(PARAMS))
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
        asyncio.run(Fetcher.fetch_data(PARAMS, {"fmp_api_key": "secret"}))
    assert error.value.code == code and len(calls) == 1
    assert "secret" not in str(error.value.to_dict())


def test_inclusive_window_and_unknown_completeness(transport):
    calls = transport(
        [{**ROW, "body": "must not retrieve or expose", "text": "ignored"}]
    )
    result = asyncio.run(
        Fetcher.fetch_data({**PARAMS, "end_date": "2026-12-31", "limit": 1})
    )
    assert len(calls) == 1
    assert result.result[0].content_status == "metadata_only"
    assert "body" not in result.result[0].model_dump()
    bounds = result.metadata[FINANCIAL_METADATA_KEY]["bounds"]
    assert bounds["truncated"] is None and bounds["completeness"] == "unknown"


def test_canonical_field_annotations():
    fields = render_field_templates(Data)
    assert set(fields) == set(Data.model_fields)
    for name, template in fields.items():
        assert template.definition == Data.model_fields[name].description
    assert fields["accepted_date"].source == "acceptedDate"
    assert fields["content_status"].value_origin == "locally_derived"


@pytest.mark.parametrize(
    "value",
    [
        "2026-W01-1T12:30:00",
        "20260102T12:30:00",
        "2026-01-02T12",
        "2026-01-02T12:30",
        "2026-01-02X12:30:00",
        "2026-01-02T12:30:00.1234567",
        "2026-01-02T12:30:00+0130",
        "2026-01-02T12:30:00+01:30:15",
    ],
)
def test_unsupported_acceptance_lexemes_fail(transport, value):
    calls = transport([{**ROW, "acceptedDate": value}])
    with pytest.raises(FinancialError) as error:
        asyncio.run(Fetcher.fetch_data(PARAMS))
    assert error.value.code == "invalid_response" and len(calls) == 1


@pytest.mark.parametrize(
    "value",
    [
        "2026-01-02T12:30:00.1",
        "2026-01-02T12:30:00.123456Z",
        "2026-01-02T12:30:00.120-05:00",
        "2026-01-02T12:30:00-00:00",
        "2026-01-02 12:30:00+01:30",
    ],
)
def test_supported_acceptance_precision_preserved(transport, value):
    calls = transport([{**ROW, "acceptedDate": value}])
    result = asyncio.run(Fetcher.fetch_data(PARAMS))
    assert result.result[0].model_dump(mode="json")["accepted_date"] == value
    assert len(calls) == 1
