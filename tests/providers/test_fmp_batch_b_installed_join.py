"""Installed Batch B joins through native generated SDK and mounted HTTP policy."""

import asyncio
import json
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlsplit

import pytest
from fastapi import FastAPI
from test_runtime import get

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests/providers/fixtures/fmp_batch_b"
HANDOFFS = json.loads((FIXTURES / "handoffs.json").read_text())["widgets"]
SAMPLES = [
    sample
    for folder in ("events", "documents")
    for sample in json.loads(
        (FIXTURES / folder / "serialization_examples.json").read_text()
    )
]
CASES = [
    (next(h for h in HANDOFFS if h["module"] == sample["model"]), sample)
    for sample in SAMPLES
]
SECRET = "synthetic-join-credential"


@pytest.fixture
def joined(monkeypatch):
    from openbb import obb
    from openbb_core.api.rest_api import app as native
    from openbb_core.app.route_iter import iter_api_routes
    from openbb_core.provider.utils import helpers
    from qopenbb_data.app import _financial_runtime
    from qopenbb_data.config import configure
    from qopenbb_data.financial_policy import FinancialProviderPolicy

    monkeypatch.setenv("FMP_API_KEY", SECRET)
    monkeypatch.setenv("FRED_API_KEY", "synthetic-fred")
    monkeypatch.setenv("QOPENBB_DATA_SOURCE_REVISION", "7" * 40)
    monkeypatch.setenv("QOPENBB_DATA_GENERATION_REVISION", "7" * 40)
    import qopenbb_data.config as configuration

    monkeypatch.setattr(
        configuration, "COVERAGE", ROOT / "docs/reference/provider-coverage.json"
    )
    configure()
    obb.user.credentials.fmp_api_key = SECRET
    inner, document, _, registry = _financial_runtime(native)
    app = FastAPI()
    app.add_middleware(
        FinancialProviderPolicy,
        document=document,
        registry=registry,
        routes=tuple(iter_api_routes(inner)),
    )
    app.mount("/", inner)
    state = {"calls": [], "payload": [], "status": 200}

    class Response:
        def __init__(self):
            self.headers = {}

        @property
        def status(self):
            return state["status"]

        async def json(self):
            return deepcopy(state["payload"])

    async def transport(url, **kwargs):
        state["calls"].append(url)
        return await kwargs["response_callback"](Response(), None)

    async def forbidden(*args, **kwargs):
        raise AssertionError("Live network forbidden during installed join")

    monkeypatch.setattr(helpers, "amake_request", transport)
    monkeypatch.setattr("aiohttp.ClientSession._request", forbidden)
    return obb, app, state, registry


def invoke(joined, handoff, entry, params):
    obb, app, _, _ = joined
    if entry == "http":
        status, raw = asyncio.run(
            get(app, handoff["route"], urlencode(params).encode(), raw=True)
        )
        return status, json.loads(raw) if raw else None
    method = obb
    for part in handoff["route"].removeprefix("/api/v1/").split("/"):
        method = getattr(method, part)
    result = method(**params)
    selected = joined[3].original_models[handoff["model"]]["fmp"]["data"]
    assert all(type(row) is selected for row in result.results)
    return 200, result.model_dump(mode="json")


@pytest.mark.parametrize("entry", ["sdk", "http"])
@pytest.mark.parametrize(
    "handoff,sample", CASES, ids=[f"{s['model']}-{i}" for i, (_, s) in enumerate(CASES)]
)
def test_installed_raw_rows_and_financial_envelope(joined, handoff, sample, entry):
    state = joined[2]
    state["payload"] = [deepcopy(sample["raw"])]
    params = dict(sample.get("query", handoff["params"]), provider="fmp")
    expected = sample["expected"]
    expected = expected if isinstance(expected, list) else [expected]
    before = datetime.now(UTC)
    status, body = invoke(joined, handoff, entry, params)
    assert status == 200, body
    assert len(state["calls"]) == 1
    assert body["provider"] == "fmp"
    assert len(body["results"]) == len(expected)
    for actual, wanted in zip(body["results"], expected):
        assert set(actual) <= set(wanted)
        for key, value in wanted.items():
            assert actual.get(key) == value, (key, actual, wanted)
    metadata = body["extra"]["results_metadata"]["__qopenbb_financial__"]
    query = (
        joined[3]
        .original_models[handoff["model"]]["fmp"]["query"]
        .model_validate({k: v for k, v in params.items() if k != "provider"})
    )
    expected_query = query.model_dump(mode="json")
    if handoff["module"] == "calendar_earnings" and "symbol" not in params:
        expected_query.pop("symbol")
    assert metadata["effective_query"] == expected_query
    assert metadata["provider"] == "fmp"
    assert metadata["dataset"] == handoff["route"].removeprefix("/api/v1/")
    assert metadata["bounds"]["returned_count"] == len(expected)
    assert (
        before <= datetime.fromisoformat(metadata["retrieved_at"]) <= datetime.now(UTC)
    )
    assert set(metadata["fields"]) == set(
        joined[3].original_models[handoff["model"]]["fmp"]["data"].model_fields
    )
    endpoints = {
        "historical_dividends": "dividends",
        "historical_splits": "splits",
        "calendar_earnings": "earnings-calendar",
        "calendar_dividend": "dividends-calendar",
        "calendar_splits": "splits-calendar",
        "company_news": "news/stock",
        "company_filings": "sec-filings-search/symbol",
        "earnings_call_transcript": "earning-call-transcript",
    }
    upstream = urlsplit(state["calls"][0])
    assert upstream.path == "/stable/" + endpoints[handoff["module"]]
    wire = parse_qs(upstream.query)
    assert wire["apikey"] == [SECRET]
    if "symbol" in params:
        assert wire["symbols" if handoff["module"] == "company_news" else "symbol"] == [
            "AAPL"
        ]
    if (
        handoff["module"].startswith("calendar")
        or handoff["module"] == "company_filings"
    ):
        assert wire["from"] == [params["start_date"]] and wire["to"] == [
            params["end_date"]
        ]
    assert SECRET not in json.dumps(body)


@pytest.mark.parametrize("entry", ["sdk", "http"])
@pytest.mark.parametrize("handoff", HANDOFFS, ids=lambda h: h["module"])
def test_installed_empty_and_entitlement_are_safe(joined, handoff, entry):
    state = joined[2]
    for status, code in [(200, "missing_data"), (403, "entitlement")]:
        state["status"] = status
        state["calls"].clear()
        if entry == "http":
            actual, body = invoke(joined, handoff, entry, handoff["params"])
            if code == "missing_data":
                assert actual == 204 and body is None
            else:
                assert actual == 502 and body["code"] == code, body
            assert SECRET not in json.dumps(body)
        else:
            with pytest.raises(Exception) as caught:
                invoke(joined, handoff, entry, handoff["params"])
            from openbb_core.provider.utils.financial_errors import (
                normalize_financial_error,
            )

            assert normalize_financial_error(caught.value).code == code
            assert SECRET not in str(caught.value)
        assert len(state["calls"]) == 1


@pytest.mark.parametrize("handoff", HANDOFFS, ids=lambda h: h["module"])
def test_installed_http_explicit_provider_and_no_substitution(joined, handoff):
    params = dict(handoff["params"])
    for provider in (None, "fred", "unknown"):
        params.pop("provider", None)
        if provider is not None:
            params["provider"] = provider
        status, body = invoke(joined, handoff, "http", params)
        assert status == 422 and body["code"] == "invalid_parameters"
    assert joined[2]["calls"] == []


@pytest.mark.parametrize("entry", ["sdk", "http"])
@pytest.mark.parametrize("quarter", [0, 5, True, None])
def test_installed_quarter_rejected_before_transport(joined, entry, quarter):
    handoff = next(h for h in HANDOFFS if h["module"] == "earnings_call_transcript")
    params = dict(handoff["params"], quarter=quarter)
    if entry == "http":
        status, body = invoke(joined, handoff, entry, params)
        assert status == 422 and body["code"] == "invalid_parameters"
    else:
        with pytest.raises(Exception, match="invalid_parameters"):
            invoke(joined, handoff, entry, params)
    assert joined[2]["calls"] == []


@pytest.mark.parametrize("entry", ["sdk", "http"])
@pytest.mark.parametrize("handoff", HANDOFFS, ids=lambda h: h["module"])
def test_installed_missing_credential_never_sends(joined, monkeypatch, handoff, entry):
    from qopenbb_data.config import configure

    monkeypatch.delenv("FMP_API_KEY", raising=False)
    configure()
    joined[0].user.credentials.fmp_api_key = None
    if entry == "http":
        status, body = invoke(joined, handoff, entry, handoff["params"])
        assert status == 502 and body["code"] == "authentication", body
        assert SECRET not in json.dumps(body)
    else:
        with pytest.raises(Exception) as caught:
            invoke(joined, handoff, entry, handoff["params"])
        from openbb_core.provider.utils.financial_errors import (
            normalize_financial_error,
        )

        assert normalize_financial_error(caught.value).code == "authentication"
        assert SECRET not in str(caught.value)
    assert joined[2]["calls"] == []


@pytest.mark.parametrize("entry", ["sdk", "http"])
@pytest.mark.parametrize("quarter", [1, 2, 3, 4])
def test_installed_exact_transcript_period_one_send(joined, entry, quarter):
    handoff, sample = next(
        (h, s) for h, s in CASES if s["model"] == "earnings_call_transcript"
    )
    raw = dict(sample["raw"], period=f"Q{quarter}")
    joined[2]["payload"] = [raw]
    params = dict(sample["query"], provider="fmp", quarter=quarter)
    status, body = invoke(joined, handoff, entry, params)
    assert status == 200, body
    assert body["results"][0]["quarter"] == f"Q{quarter}"
    assert body["results"][0]["year"] == params["year"]
    assert len(joined[2]["calls"]) == 1
    wire = parse_qs(urlsplit(joined[2]["calls"][0]).query)
    assert wire["quarter"] == [str(quarter)] and wire["year"] == [str(params["year"])]


@pytest.mark.parametrize("handoff", HANDOFFS, ids=lambda h: h["module"])
def test_native_sdk_default_provider_preserves_selected_fmp(joined, handoff):
    _, sample = next((h, s) for h, s in CASES if h["model"] == handoff["model"])
    joined[2]["payload"] = [deepcopy(sample["raw"])]
    params = dict(sample.get("query", handoff["params"]))
    params.pop("provider", None)
    status, body = invoke(joined, handoff, "sdk", params)
    assert status == 200 and body["provider"] == "fmp"
    assert len(joined[2]["calls"]) == 1


@pytest.mark.parametrize("entry", ["sdk", "http"])
@pytest.mark.parametrize("mismatch", ["year", "period", "symbol"])
def test_installed_transcript_rejects_period_or_company_substitution(
    joined, entry, mismatch
):
    from openbb_core.provider.utils.financial_errors import normalize_financial_error

    handoff, sample = next(
        (h, s) for h, s in CASES if s["model"] == "earnings_call_transcript"
    )
    raw = dict(sample["raw"])
    raw[mismatch] = {"year": 2025, "period": "Q4", "symbol": "OTHER"}[mismatch]
    joined[2]["payload"] = [raw]
    params = dict(sample["query"], provider="fmp")
    if entry == "http":
        status, body = invoke(joined, handoff, entry, params)
        assert status == 502 and body["code"] == "invalid_response", body
    else:
        with pytest.raises(Exception) as caught:
            invoke(joined, handoff, entry, params)
        assert normalize_financial_error(caught.value).code == "invalid_response"
    assert len(joined[2]["calls"]) == 1


@pytest.mark.parametrize("entry", ["sdk", "http"])
def test_installed_locally_empty_history_retains_bounds(joined, entry):
    handoff, sample = next(
        (h, s) for h, s in CASES if s["model"] == "historical_dividends"
    )
    joined[2]["payload"] = [deepcopy(sample["raw"])]
    params = dict(handoff["params"], start_date="2026-02-01", end_date="2026-02-02")
    status, body = invoke(joined, handoff, entry, params)
    assert status == 200, body
    assert body["results"] == []
    metadata = body["extra"]["results_metadata"]["__qopenbb_financial__"]
    assert metadata["bounds"]["returned_count"] == 0
    assert metadata["effective_query"]["start_date"] == "2026-02-01"
    assert metadata["effective_query"]["end_date"] == "2026-02-02"
    assert len(joined[2]["calls"]) == 1


@pytest.mark.parametrize("entry", ["http", "sdk"])
def test_listing_calendar_selects_before_market_clip(joined, entry):
    handoff = next(h for h in HANDOFFS if h["module"] == "calendar_earnings")
    row = {"date": "2025-07-30", "symbol": "AAPL"}
    state = joined[2]
    state["payload"] = [row] * 1333 + [{**row, "symbol": "MSFT", "epsActual": 0}]
    params = dict(handoff["params"], start_date=row["date"], end_date=row["date"], symbol="msft")
    status, body = invoke(joined, handoff, entry, params)
    assert status == 200, body
    selected, = body["results"]
    assert selected["symbol"] == "MSFT" and selected["eps_actual"] == 0
    metadata = body["extra"]["results_metadata"]["__qopenbb_financial__"]
    assert metadata["effective_query"]["symbol"] == "MSFT"
    assert metadata["bounds"]["returned_count"] == 1
    wire, = state["calls"]
    assert set(parse_qs(urlsplit(wire).query)) == {"from", "to", "apikey"}


def test_calendar_distinguishes_empty_market_from_no_matching_listing(joined):
    handoff = next(h for h in HANDOFFS if h["module"] == "calendar_earnings")
    params = dict(handoff["params"], symbol="MSFT")
    state = joined[2]
    status, body = invoke(joined, handoff, "http", params)
    assert status == 204 and body is None
    state["payload"] = [{"date": params["start_date"], "symbol": "AAPL"}]
    status, body = invoke(joined, handoff, "http", params)
    assert status == 200 and body["results"] == []
    metadata = body["extra"]["results_metadata"]["__qopenbb_financial__"]
    assert metadata["retrieved_at"] and metadata["effective_query"]["symbol"] == "MSFT"
    assert metadata["bounds"]["returned_count"] == 0
