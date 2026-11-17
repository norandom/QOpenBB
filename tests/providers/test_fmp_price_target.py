"""Price-target events retain publication precision, attribution and unknown bases."""

import asyncio
import json
from datetime import UTC, date, datetime, time
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest
from openbb_core.provider.standard_models.financial_annotations import (
    bind_query_annotation,
    render_field_templates,
)
from openbb_core.provider.standard_models.financial_metadata import (
    FINANCIAL_METADATA_KEY,
)
from openbb_core.provider.utils.financial_errors import FinancialError
from openbb_fmp.models.price_target import (
    FMPPriceTargetData as Data,
)
from openbb_fmp.models.price_target import (
    FMPPriceTargetFetcher as Fetcher,
)
from openbb_fmp.models.price_target import (
    FMPPriceTargetQueryParams as Query,
)
from openbb_fmp.utils.helpers import FMPAcquisition

CONTRACT = json.loads(
    (
        Path(__file__).parent / "fixtures/fmp_batch_a/contracts/price_target.json"
    ).read_text()
)
STAMP = datetime(2024, 2, 3, tzinfo=UTC)
ROW = {
    "symbol": "ABC",
    "publishedDate": "2024-01-02",
    "priceTarget": 0,
    "priceWhenPosted": 12,
    "analystCompany": "Firm",
    "newGrade": "Buy",
    "previousGrade": "Hold",
    "newsTitle": "Headline",
    "newsURL": "https://example.test/news",
}


def result(rows, limit=20):
    return Fetcher.transform_data(
        Fetcher.transform_query({"symbol": "ABC", "limit": limit}),
        FMPAcquisition(rows, STAMP),
    )


def test_frozen_schemas_annotations():
    for model, key in [(Query, "query"), (Data, "data")]:
        for mode in ["validation", "serialization"]:
            assert model.model_json_schema(mode=mode) == CONTRACT[key][mode]
    assert (
        bind_query_annotation(Query).model_dump(mode="json")
        == CONTRACT["query_annotation"]
    )
    assert (
        Data.financial_data_annotation.model_dump(mode="json")
        == CONTRACT["data_annotation"]
    )
    assert set(render_field_templates(Data)) == set(CONTRACT["canonical_fields"])


@pytest.mark.parametrize(
    "params",
    [
        {},
        {"symbol": None},
        {"symbol": True},
        {"symbol": []},
        {"symbol": "A,B"},
        {"symbol": "A&x=1"},
        {"symbol": "A\x7f"},
        {"symbol": "A" * 51},
        *[
            {"symbol": "ABC", "limit": value}
            for value in [None, True, False, "20", 0, 101, 1.5, float("inf"), []]
        ],
        *[
            {"symbol": "ABC", key: value}
            for key, value in [
                ("page", 0),
                ("period", "annual"),
                ("provider", "fmp"),
                ("unknown", None),
            ]
        ],
    ],
)
def test_invalid_query_zero_io(monkeypatch, params):
    async def forbidden(*args, **kwargs):
        pytest.fail("invalid query reached transport")

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", forbidden)
    with pytest.raises(FinancialError) as exc:
        asyncio.run(Fetcher.fetch_data(params))
    assert exc.value.code == "invalid_parameters"
    assert exc.value.__context__ is None


@pytest.mark.parametrize(
    "published,kind",
    [
        ("2024-01-02", date),
        ("2024-01-02T00:00:00", datetime),
        ("2024-01-02 12:34:56.123456", datetime),
        ("2024-01-02T12:34:56+05:30", datetime),
        ("2024-01-02T12:34:56Z", datetime),
    ],
)
def test_publication_precision(published, kind):
    row = result([{**ROW, "publishedDate": published}]).result[0]
    assert type(row.published_date) is kind
    expected = (
        date.fromisoformat(published)
        if kind is date
        else datetime.fromisoformat(published)
    )
    assert row.published_date == expected
    assert row.published_time is None


@pytest.mark.parametrize(
    "value", ["12:34:56", "12:34:56.123456", "12:34:56+05:30", "12:34:56Z", None]
)
def test_separate_publication_time(value):
    row = result([{**ROW, "publishedTime": value}]).result[0]
    assert row.published_time == (None if value is None else time.fromisoformat(value))


@pytest.mark.parametrize(
    "field,value",
    [
        ("publishedDate", None),
        ("publishedDate", "bad"),
        ("publishedDate", 0),
        ("publishedDate", True),
        ("publishedDate", float("inf")),
        ("publishedTime", 0),
        ("publishedTime", True),
        ("publishedTime", "bad"),
        ("symbol", None),
        ("symbol", True),
        ("priceTarget", True),
        ("priceTarget", "bad"),
        ("priceTarget", float("inf")),
    ],
)
def test_malformed_rows_safe(field, value):
    with pytest.raises(FinancialError) as exc:
        result([{**ROW, field: value}])
    assert exc.value.code == "invalid_response"
    assert exc.value.__context__ is None


@pytest.mark.parametrize("field", ["publishedDate", "symbol"])
def test_missing_required(field):
    with pytest.raises(FinancialError):
        result([{key: value for key, value in ROW.items() if key != field}])


def test_order_attribution_optional_zero_null():
    rows = [{**ROW, "priceTarget": n} for n in [3, 0, None, 2]]
    output = result(rows)
    assert [row.price_target for row in output.result] == [3, 0, None, 2]
    row = output.result[0]
    assert (
        row.analyst_firm,
        row.rating_current,
        row.rating_previous,
        row.news_title,
        row.news_url,
    ) == ("Firm", "Buy", "Hold", "Headline", "https://example.test/news")
    assert row.price_when_posted == 12 and row.currency is None
    assert len({row.published_date for row in output.result}) == 1


@pytest.mark.parametrize("size", [0, 1, 20, 21])
def test_metadata_bounds(size):
    output = result([ROW] * size)
    meta = output.metadata[FINANCIAL_METADATA_KEY]
    assert (
        meta["provider"] == "fmp" and meta["dataset"] == "equity/estimates/price_target"
    )
    assert meta["effective_query"] == {"symbol": "ABC", "limit": 20}
    assert datetime.fromisoformat(meta["retrieved_at"]) == STAMP
    assert len(output.result) == min(size, 20)
    assert meta["bounds"]["returned_count"] == min(size, 20)
    assert meta["bounds"]["requested_limit"] == meta["bounds"]["effective_limit"] == 20
    assert meta["bounds"]["completeness"] == ("partial" if size > 20 else "unknown")
    assert meta["bounds"]["truncated"] == (True if size > 20 else None)
    assert meta["point_in_time_safe"] is False
    assert not urlsplit(meta["source"]["documentation"]).query
    assert not urlsplit(meta["source"]["documentation"]).fragment
    assert set(meta["fields"]) == set(CONTRACT["canonical_fields"])
    for name in [
        "price_target",
        "adj_price_target",
        "price_target_previous",
        "previous_adj_price_target",
        "price_when_posted",
    ]:
        field = meta["fields"][name]
        assert field["unit"] == "currency/share" and field["scale"] == 1
        assert field["currency_field"] == "currency" and field["currency"] is None
        assert field["value_origin"] == (
            "provider_observation" if name == "price_when_posted" else "estimate"
        )
        assert field["publication_date_field"] == "published_date"


class Response:
    status = 200

    def __init__(self, payload):
        self.payload, self.headers = payload, {}

    async def json(self):
        return self.payload


@pytest.mark.parametrize("payload", [[], [ROW]])
def test_real_fetcher_one_request(monkeypatch, payload):
    calls = []

    async def transport(url, **kwargs):
        calls.append(url)
        assert set(kwargs) == {"response_callback"}
        return await kwargs["response_callback"](Response(payload), None)

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", transport)
    output = asyncio.run(
        Fetcher.fetch_data(
            {"symbol": " brk/b ", "limit": 1}, {"fmp_api_key": "synthetic-secret"}
        )
    )
    assert len(calls) == 1 and len(output.result) == len(payload)
    assert urlsplit(calls[0]).path == "/stable/price-target-news"
    assert "BRK%2FB" in calls[0]
    assert parse_qs(urlsplit(calls[0]).query) == {
        "symbol": ["BRK/B"],
        "limit": ["1"],
        "apikey": ["synthetic-secret"],
    }
    assert FINANCIAL_METADATA_KEY in output.metadata
    assert "synthetic-secret" not in str(output.metadata)


@pytest.mark.parametrize(
    "status,code", [(401, "authentication"), (403, "entitlement"), (429, "throttling")]
)
def test_safe_http_failures(monkeypatch, status, code):
    async def transport(url, **kwargs):
        response = Response({"error": "synthetic-secret"})
        response.status, response.headers = status, {"Retry-After": "7"}
        return await kwargs["response_callback"](response, None)

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", transport)
    with pytest.raises(FinancialError) as exc:
        asyncio.run(
            Fetcher.fetch_data({"symbol": "ABC"}, {"fmp_api_key": "synthetic-secret"})
        )
    envelope = exc.value.to_dict()
    assert envelope["code"] == code and "synthetic-secret" not in str(envelope)
    if status == 429:
        assert envelope["retry_after_seconds"] == 7


@pytest.mark.parametrize("payload", [None, {}, "bad", ["bad"], [{}], {"data": []}])
def test_malformed_transport(monkeypatch, payload):
    async def transport(url, **kwargs):
        return await kwargs["response_callback"](Response(payload), None)

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", transport)
    with pytest.raises(FinancialError):
        asyncio.run(Fetcher.fetch_data({"symbol": "ABC"}))


def test_timeout(monkeypatch):
    async def transport(url, **kwargs):
        raise TimeoutError("synthetic-secret")

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", transport)
    with pytest.raises(FinancialError) as exc:
        asyncio.run(Fetcher.fetch_data({"symbol": "ABC"}))
    assert exc.value.code == "timeout" and "synthetic-secret" not in str(
        exc.value.to_dict()
    )


@pytest.mark.parametrize("name,entry", CONTRACT["accepted_validation_aliases"].items())
def test_all_field_aliases(name, entry):
    baseline = Data.model_validate(ROW).model_dump()
    value = baseline[name]
    if value is None:
        annotation = CONTRACT["data"]["validation"]["properties"][
            entry["generated_schema_alias"]
        ]
        types = [item.get("type") for item in annotation.get("anyOf", [annotation])]
        value = (
            7.5
            if "number" in types
            else ("13:14:15+02:00" if name == "published_time" else "supplied")
        )
    for alias in {
        entry["canonical"],
        entry["generated_schema_alias"],
        *entry["source_aliases"],
    }:
        supplied = {key: val for key, val in baseline.items() if key != name}
        row = Data.model_validate({**supplied, alias: value})
        expected = (
            time.fromisoformat(value)
            if name == "published_time" and isinstance(value, str)
            else value
        )
        assert getattr(row, name) == expected
        assert set(row.model_dump()) == set(CONTRACT["canonical_fields"])


@pytest.mark.parametrize(
    "name",
    [
        "priceTarget",
        "adjPriceTarget",
        "priceTargetPrevious",
        "previousAdjPriceTarget",
        "priceWhenPosted",
    ],
)
@pytest.mark.parametrize(
    "value", [True, False, [], {}, float("nan"), float("-inf"), 10**1000]
)
def test_each_monetary_field_safely_rejects(name, value):
    with pytest.raises(FinancialError) as exc:
        result([{**ROW, name: value}])
    assert exc.value.code == "invalid_response" and exc.value.__context__ is None


def test_clip_validates_tail_instead_of_hiding_malformed_source():
    with pytest.raises(FinancialError):
        result([ROW, {**ROW, "publishedDate": None}], limit=1)


@pytest.mark.parametrize("limit", [1, 100])
def test_real_transport_clips_and_discloses_bounds(monkeypatch, limit):
    calls = []

    async def transport(url, **kwargs):
        calls.append(url)
        return await kwargs["response_callback"](Response([ROW] * (limit + 1)), None)

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", transport)
    output = asyncio.run(Fetcher.fetch_data({"symbol": "ABC", "limit": limit}))
    assert len(calls) == 1 and len(output.result) == limit
    bounds = output.metadata[FINANCIAL_METADATA_KEY]["bounds"]
    assert bounds["truncated"] is True and bounds["completeness"] == "partial"
