# Task 1.3 implementation evidence

Ready for independent review. The two core helpers expose fixed financial failure categories, safe public projections, recognized OpenBB wrapper unwrapping, bounded retry intervals, and separate query/result Pydantic validation. They do not install API handlers or change dispatch.

Requirements checked: 7.1, 7.2, 7.4, 8.4. Design: Financial failures and HTTP compatibility; task boundary 1.3.

Source baseline: accepted foundation e457034; this lane adds only financial_errors.py, financial_validation.py and test_financial_errors.py. Other lane changes were preserved. Controller owns inventory and combined complexity acceptance.

## Verification

All runs used WSL Debian at /mnt/d/Source/QOpenBB:

```sh
PYTHONPATH="$PWD/vendor/data-api/openbb_platform/core" verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_financial_errors.py -n0 --maxprocesses=2
```

- red.log: expected collection failure, FinancialError export absent with feature flag OFF (pytest exit 2).
- green.log: 25 passed, 8.86s (pytest exit 0).
- retry-date-red.log: HTTP-date support test failed for missing now keyword; 26 passed, 1 failed (pytest exit 1).
- final-green.log: 27 passed, 9.05s (pytest exit 0).
- git diff --check: exit 0, existing inventory newline warning only.

One existing ClientSession inheritance deprecation warning remains. No live provider requests, handler integration, dependency installs, builds or commits ran.

## Frozen exports

financial_errors: FinancialError, FinancialErrorCode, normalize_financial_error(error), parse_retry_after(value, now=None), MAX_RETRY_AFTER_SECONDS=86400, MAX_WRAPPER_DEPTH=8.

FinancialError accepts code, keyword provider and retry_after_seconds. Attributes: code, provider, status_code, retryable, retry_after_seconds, detail, correlation_id; to_dict() returns only safe fields. Provider IDs are allowlisted fmp/fred/yfinance; unknown IDs become null. Unknown codes fail closed. Only exact OpenBBError.original wrappers are followed. Unknown subclasses, unknown exceptions, cycles and over-depth chains fail closed to internal_error. Known typed errors carrying cause/context are rebuilt. No upstream repr/body/URL is parsed. Retry-After supports bounded integer delta seconds and HTTP dates; invalid, negative or greater-than-one-day delays are omitted.

financial_validation: validate_financial_query(model, payload, provider=None) and validate_financial_result(model, payload, provider=None). Both return model.model_validate output. Pydantic failures become invalid_parameters/422 or invalid_response/502 respectively, raised outside the Pydantic handler so raw validation errors are absent from cause and context. Other unexpected errors remain subject to the safe normalizer at the runtime boundary.

Malformed provider rows and inputs contain synthetic secret canaries in tests. Tests assert no canary in error messages, attributes, JSON or retained cause/context. Unknown Pydantic errors fail closed when no explicit query/result context exists. Runtime wiring and mounted-API canary coverage belong to later tasks.

## Review formatting remediation

Applied the reviewer-requested multiline import in financial_validation.py only. Scoped `verification/provider/.venv/bin/python -m ruff check vendor/data-api/openbb_platform/core/openbb_core/provider/utils/financial_errors.py vendor/data-api/openbb_platform/core/openbb_core/provider/utils/financial_validation.py` passed with exit 0; output retained in ruff.log. No tests repeated for formatting alone. Frozen financial_validation SHA256: B7076CBF7C0F8E7D40EFFFB39CD45E3CAD0413E3722FBC5C9D56FA33D1CE05A6. Other source hashes unchanged.

The owning fork requires its explicit configuration: `verification/provider/.venv/bin/python -m ruff check --no-fix --config vendor/data-api/openbb_platform/core/pyproject.toml vendor/data-api/openbb_platform/core/openbb_core/provider/utils/financial_errors.py vendor/data-api/openbb_platform/core/openbb_core/provider/utils/financial_validation.py`. The first explicit-config check found import ordering differed from the root config. Corrected ordering; final explicit-config check passed (ruff.log). Final financial_validation SHA256 supersedes the previous formatting hash: 6D6265533492E71D9B92CA0694DACE40A70187B556B5893FDE2DC41A6DDC5F75. Only imports changed.
