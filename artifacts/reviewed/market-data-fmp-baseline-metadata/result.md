# FMP baseline metadata review candidate

Task 2.2 is frozen for independent review. The three production files and two test files preserve profile/income baseline rows and errors while adding FinancialResultMetadata through AnnotatedResult. Parent authorized the narrow helpers.py boundary amendment after review exposed acquisition/error-mode coupling. No live calls, installs, builds, registration edits or commits were performed.

Profile acquisition retains the oldest component network timestamp. Field metadata references row currency, assigns currency/share to price and dividend fields and currency to market capitalization, and distinguishes provider calculations. Quote dates remain explicitly unavailable. Income accepts fiscalYear/calendarYear and filingDate/fillingDate, retains nulls, signed values, fiscal and filing dates and every returned baseline row, including nonempty limit=0 responses. Default effective query limit is five. When the provider exceeds its requested count, effective_limit is unknown and a limitation explains the retained rows. Completeness remains unknown without a demonstrated provider guarantee.

The optional typed_errors argument separates acquisition timestamps from exception compatibility. Omitted/None preserves accepted task 2.1 behavior: error typing follows with_provenance. Existing baseline profile/income request with_provenance=True and typed_errors=False, retaining legacy authentication/entitlement HTTP502, FMP category details and empty/connection handling. Classification remains solely in utils/errors.py; no model reconstructs transport categories. Wrapper validation honors the same override.

## Evidence

- error-red.log: six focused failures before the compatibility repair, including explicit error-mode override leaking to request kwargs.
- error-green.log: final frozen source, 79 passed in 27.46s across profile, income, errors and transport; one existing aiohttp inheritance warning.
- ruff.log: explicit owning-FMP configuration, --no-fix, all checks passed for all three production files.
- size.json: project-syntax-units-v1 whole-file profile241 physical/102 logical/max14; income332/96/max11; helpers342/164/max27.
- git diff --check passed for fork source and root tests. All maintained source bytes use LF.
- Earlier red-flag.log records four controlled OFF-stage metadata failures; temporary flag removed. Initial red.log overlapped import/edit and is not valid RED evidence. Earlier green.log records two diagnosed failures; historical intermediate logs do not certify final bytes.

Independent review also identified accidental baseline row slicing, effective-query default and profile field units/origins. All are repaired with regressions, including zero with nonempty provider data. Native API serialization and direct typed fetcher metadata are covered; a separately installed Python client and live entitlement remain unverified.

```sh
PYTHONPATH=$PWD/vendor/data-api/openbb_platform/core:$PWD/vendor/data-api/openbb_platform/providers/fmp verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_profile.py tests/providers/test_income.py tests/providers/test_errors.py tests/providers/test_fmp_transport.py -n0 --maxprocesses=2
verification/provider/.venv/bin/ruff check --config vendor/data-api/openbb_platform/providers/fmp/pyproject.toml --no-fix vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/utils/helpers.py vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/equity_profile.py vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/income_statement.py
```

Requirements checked: 2.1, 2.4, 4.1, 4.2, 4.3, 4.5, 6.3. Design: Provider fetchers and first-batch surface; Financial metadata contract; FRED compatibility and acquisition provenance; Financial failures and HTTP compatibility. Parent owns joined scope/inventory and acceptance.

## Frozen SHA256

- vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/equity_profile.py: 3aa9e903f7f953b0cbb4386e94837cbfcaa99492d26c0ae28f91b44d5a77aa3c
- vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/income_statement.py: ecc7237980330eb97b632dace69547a3c4f2b91c6447a3b2c944736deae8b680
- vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/utils/helpers.py: ba9d11a0f2abb89bbbbecfef24ded442dd4929d86d40a5702eaf2a41cd9fedb4
- tests/providers/test_profile.py: 03bd08c814d6412756acc584147022fe411ef13845bd373012425150494d36f1
- tests/providers/test_income.py: 5f34542bb04467d5a020c33d2acf68937537f871a2465e3eed21f7899b6f94a0
