"""FRED GDP fixture behavior through the installed public route."""
import asyncio
import json
from typing import ClassVar
from urllib.parse import parse_qs, urlparse

import pytest
from test_runtime import get
from test_runtime import packaged_catalog as packaged_catalog  # noqa: PLC0414
from test_runtime import runtime as runtime  # noqa: PLC0414


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
            headers: ClassVar[dict] = {}
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


@pytest.mark.parametrize("failure,category", [("auth", "authentication"), ("throttle", "throttling"), ("missing", "missing_data")])
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
    assert status == 400, body
    assert body["code"] == category
    assert body["provider"] == "fred"
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
    assert status == 400
    assert body["detail"] == "Provider request failed."
    assert body["code"] == "upstream"
    assert body["provider"] == "fred"
    for text in (json.dumps(body), caplog.text):
        assert "fixture-runtime" not in text
        assert "api_key=" not in text
        assert "https://" not in text


@pytest.mark.parametrize("message,code", [
    ("FRED authentication failed.", "authentication"),
    ("FRED data unavailable.", "missing_data"),
    ("FRED API rate limit exceeded (HTTP 429). Please wait a moment and try again.", "throttling"),
    ("FRED request failed.", "upstream"),
    ("https://example.invalid/?api_key=fixture-runtime-fred", "upstream"),
    ("FRED authentication failed. https://example.invalid/?api_key=fixture-runtime-fred", "upstream"),
])
def test_safe_error_canonical_categories(message, code):
    from openbb_core.app.model.abstract.error import OpenBBError
    from openbb_core.provider.utils.financial_errors import (
        FinancialError,
        normalize_financial_error,
    )
    from openbb_fred.utils.response import safe_error

    safe = safe_error(OpenBBError(message))
    assert type(safe) is FinancialError
    normalized = normalize_financial_error(OpenBBError(OpenBBError(safe)))
    assert normalized.code.value == code
    assert normalized.provider == "fred"
    assert normalized.__context__ is None and normalized.__cause__ is None
    assert "fixture-runtime" not in json.dumps(normalized.to_dict())
    assert "https://" not in str(normalized)


def test_safe_error_rebuilds_typed_context_without_raw_chain():
    from openbb_core.provider.utils.financial_errors import (
        FinancialError,
        normalize_financial_error,
    )
    from openbb_fred.utils.response import safe_error

    try:
        raise RuntimeError("https://example.invalid/?api_key=fixture-runtime-fred")
    except RuntimeError:
        typed = FinancialError("throttling", provider="fmp", retry_after_seconds=12)
        typed.__context__ = RuntimeError("fixture-runtime-fred")
    safe = safe_error(typed)
    assert type(safe) is FinancialError and safe is not typed
    assert normalize_financial_error(safe).to_dict() == {
        "detail": "Provider rate limit reached. Try again later.",
        "code": "throttling", "provider": "fred", "retryable": True,
        "retry_after_seconds": 12,
    }
    assert safe.original is None
    assert safe.__context__ is None and safe.__cause__ is None


@pytest.mark.parametrize("kind,code", [("protocol", "authentication"), ("unexpected", "upstream"), ("typed", "throttling")])
def test_series_errors_retain_safe_type_without_raw_chain(monkeypatch, kind, code):
    from openbb_core.app.model.abstract.error import OpenBBError
    from openbb_core.provider.utils.financial_errors import (
        FinancialError,
        normalize_financial_error,
    )
    from openbb_fred.models.series import FredSeriesFetcher, FredSeriesQueryParams

    async def broken(*args, **kwargs):
        try:
            raise RuntimeError("https://example.invalid/?api_key=fixture-runtime-fred")
        except RuntimeError:
            if kind == "protocol":
                raise OpenBBError("FRED authentication failed.") from None
            if kind == "typed":
                raise FinancialError("throttling", provider="fred", retry_after_seconds=7) from None
            raise ValueError("fixture-runtime-fred") from None

    monkeypatch.setattr("openbb_fred.utils.rate_limiter.fred_get", broken)
    with pytest.raises(FinancialError) as caught:
        asyncio.run(FredSeriesFetcher.aextract_data(
            FredSeriesQueryParams(symbol="GDP"), {"fred_api_key": "fixture-runtime-fred"},
        ))
    safe = caught.value
    assert type(safe) is FinancialError
    assert safe.code.value == code and safe.provider == "fred"
    assert safe.__context__ is None and safe.__cause__ is None
    assert safe.original is None
    if kind == "typed":
        assert safe.retry_after_seconds == 7
    assert normalize_financial_error(OpenBBError(safe)).code.value == code
    assert "fixture-runtime" not in json.dumps(safe.to_dict())
