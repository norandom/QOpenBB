"""FRED GDP fixture behavior through the installed public route."""
import asyncio
from copy import deepcopy
import json
from urllib.parse import parse_qs, urlparse

import pytest
from test_runtime import get, packaged_catalog, runtime


@pytest.fixture
def fred_boundary(monkeypatch):
    from openbb_core.provider.utils import helpers
    from openbb_fred.utils import rate_limiter
    calls = []
    state = {"failure": None}
    async def acquire():
        return None
    monkeypatch.setattr(rate_limiter, "acquire", acquire)
    rate_limiter.cache_clear()
    async def request(url, response_callback, **kwargs):
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        assert query["api_key"] == ["fixture-runtime-fred"]
        assert parsed.netloc == "api.stlouisfed.org"
        calls.append(parsed.path)
        failure = state["failure"]
        class Response:
            status = {"auth": 400, "throttle": 429, "missing": 404}.get(failure, 200)
            headers = {}
            async def json(self):
                if failure:
                    return {"error_code": self.status, "error_message": f"{failure} {url}"}
                if parsed.path.endswith("observations"):
                    return {"observations": [
                        {"date": "2024-01-01", "value": "28624.069", "realtime_start": "2025-01-01", "realtime_end": "2025-01-01"},
                        {"date": "2024-04-01", "value": ".", "realtime_start": "2025-01-01", "realtime_end": "2025-01-01"},
                    ]}
                return {"seriess": [{"title": "Gross Domestic Product", "units": "Billions of Dollars", "frequency": "Quarterly", "seasonal_adjustment": "Seasonally Adjusted Annual Rate"}]}
        return await response_callback(Response(), None)
    monkeypatch.setattr(helpers, "amake_request", request)
    return state, calls


def fetch(runtime):
    return asyncio.run(get(runtime, "/api/v1/economy/fred_series", b"provider=fred&symbol=GDP&use_cache=false"))


def test_gdp_dates_values_missing_frequency_units(runtime, fred_boundary):
    status, body = fetch(runtime)
    assert status == 200, body
    assert body["provider"] == "fred"
    assert body["results"] == [{"date": "2024-01-01", "GDP": 28624.069}, {"date": "2024-04-01", "GDP": None}]
    meta = body["extra"]["results_metadata"]["GDP"]
    assert meta["frequency"] == "Quarterly"
    assert meta["units"] == "Billions of Dollars"
    assert meta["seasonal_adjustment"] == "Seasonally Adjusted Annual Rate"


@pytest.mark.parametrize("failure,category", [("auth", "authentication"), ("throttle", "rate limit"), ("missing", "unavailable")])
def test_fred_failures_visible_and_sanitized(runtime, fred_boundary, failure, category, monkeypatch, caplog):
    state, calls = fred_boundary
    state["failure"] = failure
    # No retry waits in deterministic failure checks; production retries stay bounded.
    from openbb_fred.utils import rate_limiter
    original = rate_limiter.fred_get
    async def once(*args, **kwargs):
        kwargs["max_retries"] = 0
        return await original(*args, **kwargs)
    monkeypatch.setattr(rate_limiter, "fred_get", once)
    status, body = fetch(runtime)
    assert status >= 400, body
    assert category in json.dumps(body).lower()
    for text in (json.dumps(body), caplog.text):
        assert "fixture-runtime" not in text
        assert "api_key=" not in text
        assert "https://" not in text
    assert calls




def test_fred_transport_exception_is_sanitized(runtime, fred_boundary, monkeypatch, caplog):
    from openbb_core.app.model.abstract.error import OpenBBError
    async def broken(*args, **kwargs):
        raise OpenBBError("https://example.invalid/?api_key=fixture-runtime-fred")
    monkeypatch.setattr("openbb_core.provider.utils.helpers.amake_request", broken)
    status, body = fetch(runtime)
    assert status >= 400
    assert body["detail"] == "FRED request failed."
    assert "fixture-runtime" not in caplog.text
