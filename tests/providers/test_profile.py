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
    result = Fetcher.transform_data(query, raw)
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

