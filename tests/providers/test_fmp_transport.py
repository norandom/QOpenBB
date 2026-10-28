"""Synthetic FMP boundary checks: no credentials or network required."""

import asyncio
from datetime import UTC, datetime
from urllib.parse import parse_qs, urlsplit

import pytest

from openbb_fmp.utils import helpers


class Response:
    def __init__(self, payload, status=200, headers=None):
        self.payload, self.status, self.headers = payload, status, headers or {}

    async def json(self):
        if isinstance(self.payload, Exception):
            raise self.payload
        return self.payload


@pytest.mark.parametrize("status,payload,code", [
    (403, {}, "entitlement"), (429, {}, "throttling"),
    (200, "bad", "invalid_response"), (200, [1], "invalid_response"),
    (200, ValueError("secret-canary"), "invalid_response"),
])
def test_safe_categories(status, payload, code):
    with pytest.raises(Exception) as caught:
        asyncio.run(helpers.response_callback(Response(payload, status, {"Retry-After": "23"}), None))
    error = caught.value
    assert error.code == code
    assert error.provider == "fmp"
    assert error.retry_after_seconds == (23 if code == "throttling" else None)
    assert error.__context__ is None
    assert "secret-canary" not in str(error)


def test_encoded_query_excludes_credential_override():
    url = helpers.create_url(3, "profile", "real&key", {"symbol": "A&B", "apikey": "fake"})
    assert parse_qs(urlsplit(url).query) == {"symbol": ["A&B"], "apikey": ["real&key"]}


def test_acquisition_and_default_payload(monkeypatch):
    from openbb_core.provider.utils import helpers as core
    payload = [{"value": 0}]
    calls = []

    async def request(url, **kwargs):
        calls.append(url)
        return payload

    monkeypatch.setattr(core, "amake_request", request)
    before = datetime.now(UTC)
    acquired = asyncio.run(helpers.get_data_many("https://fmp.test", with_provenance=True))
    assert acquired.payload is payload
    assert before <= acquired.retrieved_at <= datetime.now(UTC)
    assert asyncio.run(helpers.get_data_many("https://fmp.test")) is payload
    assert len(calls) == 2


def test_multi_requests_are_safe_bounded_and_not_retried(monkeypatch):
    from openbb_core.provider.utils import helpers as core
    calls = []

    async def request(url, **kwargs):
        calls.append(url)
        raise TimeoutError("secret-canary")

    monkeypatch.setattr(core, "amake_request", request)
    with pytest.raises(Exception) as caught:
        asyncio.run(helpers.get_data_urls(["https://fmp.test"] * 21))
    assert caught.value.code == "invalid_parameters"
    assert calls == []
    with pytest.raises(Exception) as caught:
        asyncio.run(helpers.get_data_urls(["https://fmp.test"] * 2))
    assert caught.value.code == "timeout"
    assert len(calls) == 1
    assert caught.value.__context__ is None


@pytest.mark.parametrize("symbol,period,limit", [("", "annual", 5), ("A,B", "annual", 5),
    ("A", "ttm", 5), ("A", "annual", 0), ("A", "annual", 1001), ("A", "annual", True)])
def test_statement_bounds(symbol, period, limit):
    from openbb_fmp.utils.definitions import validate_statement_query
    with pytest.raises(Exception) as caught:
        validate_statement_query(symbol, period, limit)
    assert caught.value.code == "invalid_parameters"


def test_statement_conventions():
    from openbb_fmp.utils.definitions import validate_statement_query
    assert validate_statement_query(" aapl ", "quarterly", 5) == {"symbol": "AAPL", "period": "quarter", "limit": 5}
    assert validate_statement_query("AAPL", "annual", 0, allow_zero=True)["limit"] == 0


@pytest.mark.parametrize("typed", [False, True])
def test_error_modes_share_classification(monkeypatch, typed):
    from openbb_core.provider.utils import helpers as core
    from openbb_core.provider.utils.financial_errors import FinancialError
    from openbb_fmp.utils.errors import FMPUnauthorized

    async def request(url, **kwargs):
        return await kwargs["response_callback"](Response({}, 403), None)

    monkeypatch.setattr(core, "amake_request", request)
    with pytest.raises(Exception) as caught:
        asyncio.run(helpers.get_data("https://fmp.test", with_provenance=typed))
    assert type(caught.value) is (FinancialError if typed else FMPUnauthorized)
    assert caught.value.code == "entitlement"


def test_batch_preserves_flattened_default_and_acquisition(monkeypatch):
    from openbb_core.provider.utils import helpers as core

    async def request(url, **kwargs):
        return [{"value": url}]

    monkeypatch.setattr(core, "amake_request", request)
    assert asyncio.run(helpers.get_data_urls(["one", "two"])) == [{"value": "one"}, {"value": "two"}]
    acquired = asyncio.run(helpers.get_data_one("one", with_provenance=True))
    assert acquired.payload == {"value": "one"}
