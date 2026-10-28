"""Safe financial failures at the provider boundary."""

import json

import pytest
from pydantic import BaseModel, ValidationError

from openbb_core.app.model.abstract.error import OpenBBError
from openbb_core.provider.utils.financial_errors import (
    FinancialError, FinancialErrorCode, normalize_financial_error, parse_retry_after,
)
from openbb_core.provider.utils.financial_validation import (
    validate_financial_query, validate_financial_result,
)

CANARY = "private-key-DO-NOT-EXPOSE https://provider.invalid?apikey=private-key"


class Row(BaseModel):
    amount: float


@pytest.mark.parametrize("code,status,retryable", [
    ("authentication", 502, False), ("entitlement", 502, False),
    ("throttling", 400, True), ("timeout", 400, True),
    ("invalid_parameters", 422, False), ("invalid_response", 502, False),
    ("missing_data", 204, False), ("upstream", 400, False),
    ("internal_error", 500, False),
])
def test_fixed_categories(code, status, retryable):
    error = FinancialError(code, provider="fmp", retry_after_seconds="60")
    assert error.code == FinancialErrorCode(code)
    assert error.status_code == status
    assert error.retryable is retryable
    assert error.retry_after_seconds == (60 if retryable else None)
    assert error.to_dict()["provider"] == "fmp"
    assert error.original is None


@pytest.mark.parametrize("value,expected", [
    ("60", 60), (0, 0), (86400, 86400), (86401, None), (-1, None),
    (True, None), (1.5, None), ("1.5", None), (CANARY, None),
    ("9" * 10000, None), (None, None),
])
def test_retry_after_bounds(value, expected):
    assert parse_retry_after(value) == expected


def test_recognized_wrappers_only_and_bounded():
    safe = FinancialError("entitlement", provider="fmp")
    assert normalize_financial_error(OpenBBError(OpenBBError(safe))) is safe
    class Unknown(Exception):
        original = safe
    assert normalize_financial_error(Unknown(CANARY)).code == "internal_error"
    wrapper = OpenBBError(CANARY)
    wrapper.original = wrapper
    assert normalize_financial_error(wrapper).code == "internal_error"
    deeply_nested = safe
    for _ in range(20):
        deeply_nested = OpenBBError(deeply_nested)
    assert normalize_financial_error(deeply_nested).code == "internal_error"


@pytest.mark.parametrize("validator,code,status", [
    (validate_financial_query, "invalid_parameters", 422),
    (validate_financial_result, "invalid_response", 502),
])
def test_query_and_result_validation_hide_inputs(validator, code, status):
    with pytest.raises(FinancialError) as caught:
        validator(Row, {"amount": CANARY}, provider="fmp")
    error = caught.value
    assert error.code == code
    assert error.status_code == status
    assert error.__cause__ is None
    assert error.__context__ is None
    assert CANARY not in str(error)
    assert CANARY not in repr(vars(error))
    assert CANARY not in json.dumps(error.to_dict())


def test_validation_preserves_valid_values_and_safe_unknown_failure():
    assert validate_financial_result(Row, {"amount": -2}).amount == -2
    assert validate_financial_query(Row, {"amount": 0}).amount == 0
    try:
        Row.model_validate({"amount": CANARY})
    except ValidationError as exc:
        error = normalize_financial_error(exc)
    assert error.code == "internal_error"
    assert CANARY not in repr(vars(error))
    assert error.__context__ is None


def test_untrusted_provider_and_unexpected_cause_are_not_retained():
    original = RuntimeError(CANARY)
    error = FinancialError("upstream", provider=CANARY)
    error.__cause__ = original
    # Normalization rebuilds even typed errors carrying unsafe exception chains.
    safe = normalize_financial_error(error)
    assert safe.provider is None
    assert safe.__cause__ is None
    assert safe.__context__ is None
    assert CANARY not in json.dumps(safe.to_dict())
    internal = normalize_financial_error(original)
    assert internal.code == "internal_error"
    assert internal.to_dict()["correlation_id"]
    assert CANARY not in repr(vars(internal))


def test_retry_after_http_dates_are_bounded():
    from datetime import UTC, datetime
    now = datetime(2026, 10, 28, 12, 0, tzinfo=UTC)
    assert parse_retry_after("Wed, 28 Oct 2026 12:01:00 GMT", now=now) == 60
    assert parse_retry_after("Wed, 28 Oct 2026 11:59:00 GMT", now=now) is None
    assert parse_retry_after("Fri, 30 Oct 2026 12:00:00 GMT", now=now) is None
    assert parse_retry_after(CANARY, now=now) is None


def test_openbb_subclasses_are_not_implicitly_trusted():
    class UnknownOpenBB(OpenBBError):
        pass
    safe = FinancialError("authentication", provider="fred")
    assert normalize_financial_error(UnknownOpenBB(safe)).code == "internal_error"
    assert normalize_financial_error(RuntimeError("authentication")).code == "internal_error"
