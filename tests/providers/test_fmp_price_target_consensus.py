"""Consensus statistics retain provider values and unknown temporal bases."""

import asyncio
import json
from datetime import UTC, datetime
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
from openbb_fmp.models.price_target_consensus import (
    FMPPriceTargetConsensusData as Data,
)
from openbb_fmp.models.price_target_consensus import (
    FMPPriceTargetConsensusFetcher as Fetcher,
)
from openbb_fmp.models.price_target_consensus import (
    FMPPriceTargetConsensusQueryParams as Query,
)
from openbb_fmp.utils.helpers import FMPAcquisition

CONTRACT = json.loads(
    (
        Path(__file__).parent
        / "fixtures/fmp_batch_a/contracts/price_target_consensus.json"
    ).read_text()
)
STAMP = datetime(2024, 2, 3, tzinfo=UTC)
ROW = {
    "symbol": "BRK/B",
    "targetHigh": 10,
    "targetLow": 0,
    "targetConsensus": 7,
    "targetMedian": None,
}


def result(rows):
    return Fetcher.transform_data(
        Fetcher.transform_query({"symbol": "BRK/B"}), FMPAcquisition(rows, STAMP)
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
        Fetcher.fetch_data({"symbol": " brk/b "}, {"fmp_api_key": "synthetic-secret"})
    )
    assert len(calls) == 1 and len(output.result) == len(payload)
    assert urlsplit(calls[0]).path == "/stable/price-target-consensus"
    assert "BRK%2FB" in calls[0]
    assert parse_qs(urlsplit(calls[0]).query) == {
        "symbol": ["BRK/B"],
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


@pytest.mark.parametrize("rows", [[ROW, ROW], [{**ROW, "symbol": "OTHER"}]])
def test_singleton_identity(rows):
    with pytest.raises(FinancialError) as exc:
        result(rows)
    assert exc.value.code == "invalid_response"


@pytest.mark.parametrize(
    "field", ["targetHigh", "targetLow", "targetMedian", "targetConsensus"]
)
@pytest.mark.parametrize(
    "value", [True, [], {}, "bad", float("inf"), float("nan"), 10**1000]
)
def test_malformed_estimate(field, value):
    with pytest.raises(FinancialError) as exc:
        result([{**ROW, field: value}])
    assert exc.value.code == "invalid_response" and exc.value.__context__ is None


@pytest.mark.parametrize("rows", [[], [ROW]])
def test_metadata(rows):
    output = result(rows)
    meta = output.metadata[FINANCIAL_METADATA_KEY]
    assert meta["bounds"]["completeness"] == "unknown"
    assert meta["bounds"]["returned_count"] == len(rows)
    assert meta["point_in_time_safe"] is False
    assert meta["effective_query"] == {"symbol": "BRK/B"}
    assert datetime.fromisoformat(meta["retrieved_at"]) == STAMP
    for name, field in meta["fields"].items():
        assert field["availability"] == (
            "available"
            if rows and getattr(output.result[0], name) is not None
            else "missing"
        )
        if name.startswith("target_"):
            assert (
                field["unit"] == "currency/share"
                and field["value_origin"] == "estimate"
            )
            assert field["currency"] is None and field["publication_date_field"] is None
    if rows:
        assert output.result[0].target_low == 0
        assert output.result[0].target_median is None


@pytest.mark.parametrize("name,entry", CONTRACT["accepted_validation_aliases"].items())
def test_all_field_aliases(name, entry):
    baseline = Data.model_validate(ROW).model_dump()
    value = 5.5 if name.startswith("target_") else "supplied"
    for alias in {
        entry["canonical"],
        entry["generated_schema_alias"],
        *entry["source_aliases"],
    }:
        supplied = {key: val for key, val in baseline.items() if key != name}
        row = Data.model_validate({**supplied, alias: value})
        assert getattr(row, name) == value
        assert set(row.model_dump()) == set(CONTRACT["canonical_fields"])


@pytest.mark.parametrize(
    "row",
    [
        {},
        {"symbol": None},
        {"symbol": True},
        {"symbol": []},
        {"symbol": "BRK/B", "name": []},
    ],
)
def test_required_and_malformed_identity(row):
    with pytest.raises(FinancialError) as exc:
        result([row])
    assert exc.value.code == "invalid_response" and exc.value.__context__ is None


def test_optional_absence_and_null():
    row = result([{"symbol": "BRK/B"}]).result[0]
    assert all(
        getattr(row, name) is None
        for name in CONTRACT["canonical_fields"]
        if name != "symbol"
    )


def test_exact_query_boundary_and_runtime_metadata():
    query = Fetcher.transform_query({"symbol": "a" * 50})
    assert query.symbol == "A" * 50
    assert Query.__dict__["__qopenbb_strict_admission__"] is True
    assert Query.__bases__[0].__name__ == "PriceTargetConsensusQueryParams"
    meta = result([ROW]).metadata[FINANCIAL_METADATA_KEY]
    assert meta["dataset"] == "equity/estimates/consensus"
    assert meta["source"]["endpoint"] == "price-target-consensus"
    assert not urlsplit(meta["source"]["documentation"]).query
    assert not urlsplit(meta["source"]["documentation"]).fragment
    assert meta["bounds"]["truncated"] is None
    assert any(
        "2026-11-17" in text and "not verified" in text for text in meta["limitations"]
    )
