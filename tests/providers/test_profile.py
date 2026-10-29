"""Installed profile route preserves provider data without real credentials/network."""

import asyncio
from copy import deepcopy
import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from urllib.parse import urlencode
import pytest

FIXTURE = Path(__file__).with_name("fixtures") / "profile.json"
SENTINEL = "fixture-server-key-not-a-credential"


@pytest.fixture
def profile_boundary(monkeypatch):
    from openbb_core.app.model.user_settings import UserSettings
    from openbb_core.app.service.user_service import UserService
    from openbb_core.provider.utils import helpers

    data = json.loads(FIXTURE.read_text())
    calls = []

    async def request(url, **kwargs):
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        assert (parsed.scheme, parsed.netloc, parsed.path) == (
            "https", "financialmodelingprep.com", "/stable/profile"
        )
        assert params["apikey"] == [SENTINEL]
        assert set(params) == {"symbol", "apikey"}
        calls.append(params["symbol"][0])
        return deepcopy(data.get(params["symbol"][0], []))

    settings = UserSettings.model_construct()
    settings.credentials.fmp_api_key = SENTINEL
    monkeypatch.setattr(UserService, "read_from_file", lambda *a, **k: settings)
    monkeypatch.setattr(helpers, "amake_request", request)
    return data, calls


def test_installed_profile_route_financial_values_and_nulls(profile_boundary):
    from openbb_core.api.rest_api import app

    data, calls = profile_boundary
    status, text = asyncio.run(_get_profile(app))
    assert status == 200, text
    body = json.loads(text)
    assert body["provider"] == "fmp"
    assert calls == ["AAPL", "BRK.B"]
    first, partial = body["results"]
    assert first["symbol"] == "AAPL"
    assert first["name"] == "Apple Inc."
    assert first["currency"] == "USD"
    assert first["market_cap"] == 3312456789012
    assert first["last_price"] == 218.75
    assert first["volume_avg"] == 50123456
    assert first["annualized_dividend_amount"] == 1.04
    assert (first["year_low"], first["year_high"]) == (164.08, 260.1)
    assert first["first_stock_price_date"] == "1980-12-12"
    assert first["employees"] == 164000
    assert partial["symbol"] == "BRK.B"
    for field in ("currency", "market_cap", "last_price", "volume_avg", "year_low",
                  "year_high", "is_etf", "is_actively_trading", "is_adr", "is_fund"):
        assert partial.get(field) is None
    assert SENTINEL not in text
    assert data["AAPL"][0]["range"] == "164.08-260.10"


def test_profile_query_encoding_and_nonmutating_transform(profile_boundary):
    from openbb_fmp.models.equity_profile import FMPEquityProfileFetcher as Fetcher

    data, calls = profile_boundary
    query = Fetcher.transform_query({"symbol": " brk.b , ^gspc , aapl "})
    assert query.symbol == "BRK.B,^GSPC,AAPL"
    raw = asyncio.run(Fetcher.aextract_data(query, {"fmp_api_key": SENTINEL}))
    saved = deepcopy(raw)
    result = Fetcher.transform_data(query, raw).result
    assert [row.symbol for row in result] == ["BRK.B", "^GSPC", "AAPL"]
    assert raw == saved
    assert calls == ["BRK.B", "^GSPC", "AAPL"]


def test_empty_profile_is_observable(profile_boundary):
    from openbb_fmp.models.equity_profile import FMPEquityProfileFetcher as Fetcher
    from openbb_core.provider.utils.errors import EmptyDataError

    query = Fetcher.transform_query({"symbol": "MISSING"})
    with pytest.warns(UserWarning, match="No data found"):
        with pytest.raises(EmptyDataError):
            asyncio.run(Fetcher.aextract_data(query, {"fmp_api_key": SENTINEL}))

async def _get_profile(app):
    messages = []
    sent = False

    async def receive():
        nonlocal sent
        if not sent:
            sent = True
            return {"type": "http.request", "body": b"", "more_body": False}
        await asyncio.Future()

    async def send(message):
        messages.append(message)

    scope = {"type": "http", "asgi": {"version": "3.0"}, "http_version": "1.1",
             "method": "GET", "scheme": "http", "path": "/api/v1/equity/profile",
             "raw_path": b"/api/v1/equity/profile", "root_path": "",
             "query_string": urlencode({"provider": "fmp", "symbol": "aapl,brk.b"}).encode(),
             "headers": [], "client": ("127.0.0.1", 12000), "server": ("test", 80)}
    await app(scope, receive, send)
    status = next(m["status"] for m in messages if m["type"] == "http.response.start")
    body = b"".join(m.get("body", b"") for m in messages if m["type"] == "http.response.body")
    return status, body.decode()


def test_profile_metadata(profile_boundary):
    from openbb_fmp.models.equity_profile import FMPEquityProfileFetcher as Fetcher
    query = Fetcher.transform_query({"symbol": "AAPL,BRK.B"})
    raw = asyncio.run(Fetcher.aextract_data(query, {"fmp_api_key": SENTINEL}))
    result = Fetcher.transform_data(query, raw)
    meta = result.metadata["__qopenbb_financial__"]
    assert meta["retrieved_at"] == raw.retrieved_at.isoformat().replace("+00:00", "Z")
    assert meta["fields"]["last_price"]["currency_field"] == "currency"
    assert meta["fields"]["last_price"]["currency"] is None
    assert meta["fields"]["last_price"]["unit"] == "currency/share"
    assert meta["fields"]["market_cap"]["unit"] == "currency"
    assert meta["fields"]["beta"]["value_origin"] == "provider_calculation"
    assert meta["bounds"]["returned_count"] == 2
    assert meta["effective_query"] == {"symbol": "AAPL,BRK.B"}
    from openbb_core.api.rest_api import app
    status, text = asyncio.run(_get_profile(app))
    assert status == 200
    assert json.loads(text)["extra"]["results_metadata"]["__qopenbb_financial__"]["provider"] == "fmp"


def test_profile_declarations_match_runtime_without_shared_mutation(profile_boundary):
    from openbb_core.provider.standard_models.financial_annotations import (
        bind_data_annotation, bind_query_annotation, render_field_templates,
    )
    from openbb_fmp.models.equity_profile import (
        FMPEquityProfileData as Data, FMPEquityProfileQueryParams as Query,
        FMPEquityProfileFetcher as Fetcher,
    )
    policy = bind_query_annotation(Query)
    assert policy.provider_policy == "baseline_default"
    assert policy.response_policy.mode == "provider"
    assert Query.model_fields["symbol"].is_required()
    declaration = bind_data_annotation(Data)
    before = declaration.model_dump()
    assert set(declaration.fields) == set(Data.model_fields)
    assert "fields.availability" in declaration.runtime_properties
    query = Fetcher.transform_query({"symbol": "AAPL,BRK.B"})
    raw = asyncio.run(Fetcher.aextract_data(query, {"fmp_api_key": SENTINEL}))
    raw.payload[1]["currency"] = "GBP"
    raw.payload[1]["price"] = 12.5
    raw.payload[0]["lastFundamentalDate"] = "2026-06-30"
    result = Fetcher.transform_data(query, raw)
    assert [row.currency for row in result.result] == ["USD", "GBP"]
    assert result.result[1].last_price == 12.5
    rendered = render_field_templates(Data)
    for name, unit in {
        "last_price": "currency/share", "year_low": "currency/share",
        "year_high": "currency/share", "annualized_dividend_amount": "currency/share",
        "market_cap": "currency", "volume_avg": "shares", "employees": "people",
        "beta": "dimensionless",
    }.items():
        assert rendered[name].unit == unit
        assert rendered[name].scale == 1
    actual = result.metadata["__qopenbb_financial__"]
    for name, field in rendered.items():
        field.availability = (
            "available" if any(getattr(row, name) is not None for row in result.result)
            else "missing"
        )
        assert actual["fields"][name] == field.model_dump(mode="json")
    for name in ("last_price", "market_cap", "year_low", "year_high"):
        assert actual["fields"][name]["observation_date_field"] is None
        assert actual["fields"][name]["valuation_date_field"] is None
        assert actual["fields"][name]["currency"] is None
        assert actual["fields"][name]["currency_field"] == "currency"
    rendered["last_price"].unit = "changed"
    assert render_field_templates(Data)["last_price"].unit == "currency/share"
    assert bind_data_annotation(Data).model_dump() == before


@pytest.mark.parametrize("value", ["private-invalid-range", "broken"])
def test_profile_range_failure_is_safe(profile_boundary, value):
    from datetime import datetime, UTC
    from openbb_fmp.models.equity_profile import FMPEquityProfileFetcher as Fetcher
    from openbb_fmp.utils.helpers import FMPAcquisition
    from openbb_core.provider.utils.financial_errors import FinancialError
    row = deepcopy(profile_boundary[0]["AAPL"][0])
    row["range"] = value
    query = Fetcher.transform_query({"symbol": "AAPL"})
    with pytest.raises(FinancialError) as error:
        Fetcher.transform_data(query, FMPAcquisition([row], datetime.now(UTC)))
    assert error.value.code == "invalid_response"
    assert value not in str(error.value)


@pytest.mark.parametrize("typed_errors", [False, True])
@pytest.mark.parametrize("failure", ["authentication", "timeout", "missing_data"])
def test_provenance_can_preserve_legacy_errors(monkeypatch, typed_errors, failure):
    from openbb_core.provider.utils import helpers as core
    from openbb_core.provider.utils.financial_errors import FinancialError
    from openbb_fmp.utils import helpers
    from openbb_fmp.utils.errors import FMPUnauthorized, FMPError, FMPEmptyData
    class Response:
        status = 401 if failure == "authentication" else 200
        headers = {}
        async def json(self):
            return []
    async def request(url, **kwargs):
        assert "typed_errors" not in kwargs
        if failure == "timeout":
            raise TimeoutError("unsafe-provider-detail")
        return await kwargs["response_callback"](Response(), None)
    monkeypatch.setattr(core, "amake_request", request)
    expected = FinancialError if typed_errors else {
        "authentication": FMPUnauthorized, "timeout": FMPError, "missing_data": FMPEmptyData
    }[failure]
    with pytest.raises(expected) as error:
        asyncio.run(helpers.get_data_many("https://fmp.test", with_provenance=True,
                                         typed_errors=typed_errors))
    assert error.value.code == failure
    assert "unsafe-provider-detail" not in str(error.value)
    if not typed_errors:
        assert f"FMP[{failure}]" in str(error.value)
