"""Geographic observations retain exact labels, fiscal association and safe failures."""

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest
from openbb_core.provider.standard_models.financial_annotations import (
    bind_query_annotation,
)
from openbb_core.provider.standard_models.financial_metadata import (
    FINANCIAL_METADATA_KEY,
)
from openbb_core.provider.utils.financial_errors import FinancialError
from openbb_fmp.models.revenue_geographic import (
    FMPRevenueGeographicData as Data,
)
from openbb_fmp.models.revenue_geographic import (
    FMPRevenueGeographicFetcher as Fetcher,
)
from openbb_fmp.models.revenue_geographic import (
    FMPRevenueGeographicQueryParams as Query,
)
from openbb_fmp.utils.helpers import FMPAcquisition

CONTRACT = json.loads(
    (
        Path(__file__).parent / "fixtures/fmp_batch_a/contracts/revenue_geographic.json"
    ).read_text()
)
STAMP = datetime(2024, 2, 3, tzinfo=UTC)
ROW = {
    "date": "2023-12-31",
    "fiscalYear": 2023,
    "period": "FY",
    "filingDate": "2024-02-01",
    "data": {" North America, Inc. ": 0, "a": -1.5},
}


def result(rows):
    return Fetcher.transform_data(
        Fetcher.transform_query({"symbol": "BRK/B"}), FMPAcquisition(rows, STAMP)
    )


def test_exact_contract():
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


@pytest.mark.parametrize(
    "params",
    [
        {},
        *[{"symbol": v} for v in [None, True, [], "A,B", "A&x=1", "A\x7f", "A" * 51]],
        *[
            {"symbol": "A", "period": v}
            for v in [None, True, [], "FY", "quarterly ", 1]
        ],
        *[
            {"symbol": "A", k: v}
            for k, v in [
                ("limit", 1000),
                ("page", 0),
                ("structure", "flat"),
                ("provider", "fmp"),
            ]
        ],
    ],
)
def test_invalid_zero_io(monkeypatch, params):
    async def forbidden(*args, **kwargs):
        pytest.fail("invalid query reached transport")

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", forbidden)
    with pytest.raises(FinancialError) as exc:
        asyncio.run(Fetcher.fetch_data(params))
    assert exc.value.code == "invalid_parameters" and exc.value.__context__ is None


def test_periods():
    assert Fetcher.transform_query({"symbol": " a "}).model_dump() == {
        "symbol": "A",
        "period": "annual",
    }
    assert (
        Fetcher.transform_query({"symbol": "a", "period": "quarterly"}).period
        == "quarter"
    )


def test_labels_order_and_fiscal_association():
    second = {
        "date": "2022-12-31",
        "fiscalYear": 2022,
        "period": "FY",
        "data": {"a": 9, "Other regions!": 10},
    }
    rows = result([ROW, second, ROW]).result
    assert [r.region for r in rows] == [
        " North America, Inc. ",
        "a",
        "a",
        "Other regions!",
        " North America, Inc. ",
        "a",
    ]
    assert [r.revenue for r in rows] == [0, -1.5, 9, 10, 0, -1.5]
    assert [r.fiscal_year for r in rows] == [2023, 2023, 2022, 2022, 2023, 2023]
    assert (
        rows[0].filing_date.isoformat() == "2024-02-01" and rows[2].filing_date is None
    )


@pytest.mark.parametrize("count", [0, 1000, 1001])
def test_bounds_and_metadata(count):
    output = result(
        [{**ROW, "data": {f"segment {i}": i for i in range(count)}}] if count else []
    )
    meta = output.metadata[FINANCIAL_METADATA_KEY]
    assert len(output.result) == min(count, 1000)
    assert meta["retrieved_at"] == STAMP.isoformat().replace("+00:00", "Z")
    assert meta["effective_query"] == {"symbol": "BRK/B", "period": "annual"}
    assert meta["bounds"]["truncated"] is (True if count > 1000 else None)
    assert meta["bounds"]["completeness"] == ("partial" if count > 1000 else "unknown")
    assert meta["fields"]["revenue"]["currency"] is None
    assert meta["fields"]["revenue"]["scale"] == 1
    assert meta["fields"]["revenue"]["availability"] == (
        "available" if count else "missing"
    )
    assert not urlsplit(meta["source"]["documentation"]).query


class Response:
    status = 200

    def __init__(self, payload):
        self.payload = payload
        self.headers = {}

    async def json(self):
        return self.payload


def fetch(monkeypatch, payload, *, status=200):
    calls = []

    async def transport(url, **kwargs):
        calls.append(url)
        response = Response(payload)
        response.status, response.headers = status, {"Retry-After": "7"}
        return await kwargs["response_callback"](response, None)

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", transport)
    output = asyncio.run(
        Fetcher.fetch_data({"symbol": " brk/b "}, {"fmp_api_key": "synthetic-secret"})
    )
    return output, calls


@pytest.mark.parametrize("payload", [[], [ROW]])
def test_real_fetcher_encoded_request(monkeypatch, payload):
    output, calls = fetch(monkeypatch, payload)
    assert len(calls) == 1 and "BRK%2FB" in calls[0]
    assert urlsplit(calls[0]).path == "/stable/revenue-geographic-segmentation"
    assert parse_qs(urlsplit(calls[0]).query) == {
        "symbol": ["BRK/B"],
        "period": ["annual"],
        "structure": ["flat"],
        "apikey": ["synthetic-secret"],
    }
    assert len(output.result) == (2 if payload else 0)
    assert FINANCIAL_METADATA_KEY in output.metadata
    assert "synthetic-secret" not in str(output.metadata)


BAD = [None, True, [], {}, "", "bad", float("inf"), float("nan")]
DATE_BAD = [*BAD, "2023-02-29", "2024-13-01", 1700000000]


@pytest.mark.parametrize(
    "payload",
    [
        [None],
        [[]],
        [{**ROW, "data": None}],
        [{**ROW, "data": []}],
        [{k: v for k, v in ROW.items() if k != "date"}],
        *[[{**ROW, "date": v}] for v in DATE_BAD],
        *[[{**ROW, "filingDate": v}] for v in DATE_BAD if v is not None],
        *[[{**ROW, "data": {"A": v}}] for v in BAD],
    ],
)
def test_actual_fetcher_malformed_safe(monkeypatch, payload):
    with pytest.raises(FinancialError) as exc:
        fetch(monkeypatch, payload)
    assert exc.value.code == "invalid_response"
    assert exc.value.__context__ is None and "synthetic-secret" not in str(exc.value)


@pytest.mark.parametrize(
    "status,code", [(401, "authentication"), (403, "entitlement"), (429, "throttling")]
)
def test_http_safe(monkeypatch, status, code):
    with pytest.raises(FinancialError) as exc:
        fetch(monkeypatch, {"error": "synthetic-secret"}, status=status)
    assert exc.value.code == code and exc.value.__context__ is None
    assert "synthetic-secret" not in str(exc.value)
    if status == 429:
        assert exc.value.retry_after_seconds == 7


@pytest.mark.parametrize("payload", [{}, None])
def test_transport_missing_data(monkeypatch, payload):
    with pytest.raises(FinancialError) as exc:
        fetch(monkeypatch, payload)
    assert exc.value.code == "missing_data"


def test_timeout_safe(monkeypatch):
    async def timeout(*args, **kwargs):
        raise TimeoutError("synthetic-secret")

    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", timeout)
    with pytest.raises(FinancialError) as exc:
        asyncio.run(Fetcher.fetch_data({"symbol": "A"}))
    assert exc.value.code == "timeout" and exc.value.__context__ is None
    assert "synthetic-secret" not in str(exc.value)


@pytest.mark.parametrize(
    "name,value",
    [
        ("fiscalYear", True),
        ("fiscalYear", 2023.5),
        ("fiscalYear", []),
        ("fiscalYear", {}),
        ("fiscalYear", float("inf")),
        ("period", []),
        ("period", True),
    ],
)
def test_optional_fiscal_fact_safety(monkeypatch, name, value):
    with pytest.raises(FinancialError) as exc:
        fetch(monkeypatch, [{**ROW, name: value}])
    assert exc.value.code == "invalid_response" and exc.value.__context__ is None


def test_aliases_and_optional_dates():
    canonical = {
        "period_ending": "2023-12-31",
        "revenue": 0,
        "filing_date": None,
        "fiscal_period": "FY",
        "fiscal_year": 2023,
        "region": " Asia/Pacific ",
    }
    alias = {
        "periodEnding": "2023-12-31",
        "revenue": 0,
        "filingDate": None,
        "fiscalPeriod": "FY",
        "fiscalYear": 2023,
        "region": " Asia/Pacific ",
    }
    assert (
        Data.model_validate(canonical).model_dump()
        == Data.model_validate(alias).model_dump()
    )
    for name, contract in CONTRACT["accepted_validation_aliases"].items():
        field = Data.model_fields[name]
        assert field.validation_alias == contract["generated_schema_alias"]
        assert field.serialization_alias == contract["serialization"]
    assert (
        Data.model_validate(
            {"period_ending": "2023-12-31", "revenue": 9007199254740993}
        ).revenue
        == 9007199254740993
    )


def test_no_invalid_row_dropping_after_bound(monkeypatch):
    payload = [
        {**ROW, "data": {str(i): i for i in range(1000)}},
        {**ROW, "data": {"missing": None}},
    ]
    with pytest.raises(FinancialError) as exc:
        fetch(monkeypatch, payload)
    assert exc.value.code == "invalid_response"


@pytest.mark.parametrize(
    "payload",
    [
        [{"date": "2023-12-31"}],
        [{"data": {}}],
        [{"date": None, "data": {}}],
        [{"date": "bad", "data": {}}],
        [{"date": "2023-12-31", "fiscalYear": True, "data": {}}],
    ],
)
def test_empty_inner_mapping_cannot_hide_malformed_facts(monkeypatch, payload):
    with pytest.raises(FinancialError) as exc:
        fetch(monkeypatch, payload)
    assert exc.value.code == "invalid_response" and exc.value.__context__ is None


@pytest.mark.parametrize("period", [None, "quarter", "quarterly"])
def test_actual_receipt_and_effective_frequency(monkeypatch, period):
    from openbb_fmp.utils import helpers

    original = helpers.get_data_many
    receipts, calls = [], []

    async def capture(*args, **kwargs):
        assert (
            kwargs["allow_empty"]
            and kwargs["with_provenance"]
            and kwargs["typed_errors"]
        )
        value = await original(*args, **kwargs)
        receipts.append(value.retrieved_at)
        return value

    async def transport(url, **kwargs):
        calls.append(url)
        return await kwargs["response_callback"](Response([]), None)

    monkeypatch.setattr(helpers, "get_data_many", capture)
    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", transport)
    params = {"symbol": "A", **({"period": period} if period else {})}
    output = asyncio.run(Fetcher.fetch_data(params))
    meta = output.metadata[FINANCIAL_METADATA_KEY]
    assert meta["retrieved_at"] == receipts[0].isoformat().replace("+00:00", "Z")
    assert meta["effective_query"]["period"] == ("quarter" if period else "annual")
    assert len(calls) == 1
    assert parse_qs(urlsplit(calls[0]).query)["period"] == [
        meta["effective_query"]["period"]
    ]


def test_empty_fiscal_mapping_and_split_period():
    assert result([{"date": "2023-12-31", "data": {}}]).result == []
    rows = result([{"date": "2023-12-31", "data": {"Asia": 0}}]).result
    assert rows[0].fiscal_year is None and rows[0].fiscal_period is None
    assert rows[0].filing_date is None and rows[0].region == "Asia"
    output = result(
        [
            {**ROW, "data": {f"region {i}": i for i in range(999)}},
            {"date": "2022-12-31", "data": {" Europe ": -2, "Asia/Pacific": 3}},
        ]
    )
    assert len(output.result) == 1000
    assert output.result[-1].region == " Europe "
    assert output.result[-1].revenue == -2
    assert output.result[-1].period_ending.isoformat() == "2022-12-31"
    bounds = output.metadata[FINANCIAL_METADATA_KEY]["bounds"]
    assert bounds["truncated"] is True and bounds["completeness"] == "partial"
