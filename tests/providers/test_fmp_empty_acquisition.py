"""Empty-array acquisition contracts using real helpers and intercepted transport."""

import asyncio
import inspect
import json
import traceback
from datetime import UTC, datetime

import pytest
from openbb_core.provider.utils import helpers as transport
from openbb_core.provider.utils.financial_errors import FinancialError
from openbb_fmp.utils import helpers
from openbb_fmp.utils.errors import FMPEmptyData, FMPError, FMPUnauthorized

URL = "https://example.invalid?apikey=secret-canary"
MODES = [(False, None), (True, None), (False, True), (True, False)]


class Response:
    def __init__(self, payload, status=200):
        self.payload, self.status = payload, status
        self.headers = {"Retry-After": "17"}
        self.reads = 0

    async def json(self):
        self.reads += 1
        if isinstance(self.payload, Exception):
            raise self.payload
        return self.payload


@pytest.fixture
def intercept(monkeypatch):
    def install(payload, status=200, error=None):
        response, calls = Response(payload, status), []

        async def request(url, **kwargs):
            calls.append((url, kwargs))
            assert "allow_empty" not in kwargs
            if error:
                raise error
            return await kwargs["response_callback"](response, None)

        monkeypatch.setattr(transport, "amake_request", request)
        return response, calls

    return install


def assert_failure(error, code, provenance, typed_errors):
    typed = provenance if typed_errors is None else typed_errors
    legacy = FMPUnauthorized if code in {"authentication", "entitlement"} else (
        FMPEmptyData if code == "missing_data" else FMPError
    )
    assert type(error) is (FinancialError if typed else legacy)
    assert error.code == code
    assert error.provider == "fmp"
    assert error.retry_after_seconds == (17 if code == "throttling" else None)
    assert "secret-canary" not in "".join(traceback.format_exception(error))
    assert error.__context__ is None


@pytest.mark.parametrize("provenance,typed_errors", MODES)
@pytest.mark.parametrize("helper", [helpers.get_data, helpers.get_data_many])
@pytest.mark.parametrize("payload", [[], [{"value": 0}]])
@pytest.mark.parametrize("allow_empty", [False, True])
def test_acquisition_matrix(intercept, provenance, typed_errors, helper, payload, allow_empty):
    _, calls = intercept(payload)
    options = {"with_provenance": provenance, "typed_errors": typed_errors}
    if allow_empty:
        options["allow_empty"] = True
    if not payload and not allow_empty:
        with pytest.raises(Exception) as caught:
            asyncio.run(helper(URL, **options))
        assert_failure(caught.value, "missing_data", provenance, typed_errors)
    else:
        result = asyncio.run(helper(URL, **options))
        assert isinstance(result, helpers.FMPAcquisition) is provenance
        assert (result.payload if provenance else result) is payload
    assert len(calls) == 1


@pytest.mark.parametrize("typed", [False, True])
def test_callback_opt_in_and_signature(typed):
    for helper in (helpers.response_callback, helpers.get_data, helpers.get_data_many):
        option = inspect.signature(helper).parameters["allow_empty"]
        assert option.kind is inspect.Parameter.KEYWORD_ONLY
        assert option.default is False
        assert option.annotation is bool
    assert asyncio.run(helpers.response_callback(Response([]), None, typed=typed, allow_empty=True)) == []
    with pytest.raises(Exception) as caught:
        asyncio.run(helpers.response_callback(Response([]), None, typed=typed))
    assert_failure(caught.value, "missing_data", typed, None)


FAILURES = [
    ([], 401, "authentication"), ([], 403, "entitlement"),
    ([], 404, "missing_data"), ([], 429, "throttling"), ([], 500, "upstream"),
    ({"Error Message": "Invalid API key secret-canary"}, 200, "authentication"),
    ({"error": "rate limit secret-canary"}, 200, "throttling"),
    ({"error": "premium secret-canary"}, 200, "entitlement"),
    ({"error": "secret-canary"}, 200, "upstream"),
    ({}, 200, "missing_data"), (None, 200, "missing_data"),
    (ValueError("secret-canary"), 200, "invalid_response"),
    ("secret-canary", 200, "invalid_response"), (1, 200, "invalid_response"),
    (False, 200, "invalid_response"), ([None], 200, "invalid_response"),
    ([{"value": 1}, 2], 200, "invalid_response"),
]


@pytest.mark.parametrize("provenance,typed_errors", MODES)
@pytest.mark.parametrize("payload,status,code", FAILURES)
def test_opt_in_preserves_failures(intercept, provenance, typed_errors, payload, status, code):
    response, calls = intercept(payload, status)
    with pytest.raises(Exception) as caught:
        asyncio.run(helpers.get_data_many(URL, allow_empty=True,
            with_provenance=provenance, typed_errors=typed_errors))
    assert_failure(caught.value, code, provenance, typed_errors)
    assert len(calls) == 1
    assert response.reads == (1 if status == 200 else 0)


@pytest.mark.parametrize("provenance,typed_errors", MODES)
@pytest.mark.parametrize("payload,code", [
    ({"other": []}, "missing_data"), ({"rows": []}, "missing_data"),
    ({"rows": None}, "invalid_response"), ({"rows": {}}, "invalid_response"),
    ({"rows": [None]}, "invalid_response"), ({"rows": "bad"}, "invalid_response"),
])
def test_extracted_empty_is_not_top_level(intercept, provenance, typed_errors, payload, code):
    _, calls = intercept(payload)
    with pytest.raises(Exception) as caught:
        asyncio.run(helpers.get_data_many(URL, sub_dict="rows", allow_empty=True,
            with_provenance=provenance, typed_errors=typed_errors))
    assert_failure(caught.value, code, provenance, typed_errors)
    assert len(calls) == 1


@pytest.mark.parametrize("provenance,typed_errors", MODES)
@pytest.mark.parametrize("error,code", [(TimeoutError("secret-canary"), "timeout"),
    (ConnectionError("secret-canary"), "upstream"), (RuntimeError("secret-canary"), "upstream")])
def test_transport_redaction(intercept, provenance, typed_errors, error, code):
    _, calls = intercept(None, error=error)
    with pytest.raises(Exception) as caught:
        asyncio.run(helpers.get_data_many(URL, allow_empty=True,
            with_provenance=provenance, typed_errors=typed_errors))
    assert_failure(caught.value, code, provenance, typed_errors)
    assert len(calls) == 1


@pytest.mark.parametrize("helper,args", [(helpers.get_data_one, (URL,)),
    (helpers.get_data_urls, ([URL, URL],))])
@pytest.mark.parametrize("provenance,typed_errors", MODES)
def test_other_helper_defaults(intercept, helper, args, provenance, typed_errors):
    _, calls = intercept([])
    with pytest.raises(Exception) as caught:
        asyncio.run(helper(*args, with_provenance=provenance, typed_errors=typed_errors))
    assert_failure(caught.value, "missing_data", provenance, typed_errors)
    assert len(calls) == 1


def test_exact_network_receipt(monkeypatch):
    receipt = datetime(2026, 11, 17, 12, 13, 14, 123456, tzinfo=UTC)
    events = []

    class Clock:
        @staticmethod
        def now(zone):
            assert zone is UTC
            assert events == ["network-complete"]
            events.append("clock")
            return receipt

    async def request(url, **kwargs):
        result = await kwargs["response_callback"](Response([]), None)
        events.append("network-complete")
        return result

    monkeypatch.setattr(helpers, "datetime", Clock)
    monkeypatch.setattr(transport, "amake_request", request)
    acquired = asyncio.run(helpers.get_data_many(URL, allow_empty=True, with_provenance=True))
    assert acquired.retrieved_at is receipt
    assert acquired.payload == []
    assert events == ["network-complete", "clock"]


def test_native_fetcher_obbject_financial_json(intercept):
    """Dedicated carrier proof; endpoint registration/SDK/HTTP joins are separate."""
    from openbb_core.app.model.obbject import OBBject
    from openbb_core.provider.standard_models.financial_metadata import (
        FINANCIAL_METADATA_KEY,
    )
    from openbb_fmp.models.enterprise_values import FMPEnterpriseValuesFetcher

    class EmptyCarrier(FMPEnterpriseValuesFetcher):
        @staticmethod
        async def aextract_data(query, credentials, **kwargs):
            return await helpers.get_data_many(URL, allow_empty=True, with_provenance=True)

    class Query:
        async def execute(self):
            return await EmptyCarrier.fetch_data({"symbol": "AAPL", "period": "annual", "limit": 5})

    _, calls = intercept([])
    result = asyncio.run(OBBject.from_query(Query()))
    encoded = json.loads(result.model_dump_json())
    assert encoded["results"] == []
    metadata = encoded["extra"]["results_metadata"][FINANCIAL_METADATA_KEY]
    assert metadata["dataset"] == "equity/fundamental/enterprise_values"
    assert metadata["provider"] == "fmp"
    assert metadata["source"]["endpoint"] == "enterprise-values"
    assert metadata["effective_query"] == {"symbol": "AAPL", "period": "annual", "limit": 5}
    assert metadata["bounds"]["returned_count"] == 0
    assert metadata["fields"]["enterprise_value"]["availability"] == "missing"
    assert datetime.fromisoformat(metadata["retrieved_at"]).utcoffset().total_seconds() == 0
    assert len(calls) == 1
