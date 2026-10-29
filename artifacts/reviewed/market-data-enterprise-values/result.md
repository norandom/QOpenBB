# Enterprise-value inputs: fixture verification

The isolated task 2.9 adapter is ready for independent review. It returns provider price, shares, market capitalization, cash, debt and enterprise value without a local valuation calculation. Registration, router mounting, installed API acceptance and live entitlement verification remain controller-owned work.

## Status Report
- STATUS: READY_FOR_REVIEW
- Task: market-data-integrations 2.9; requirements 2.1, 4.1, 4.2, 4.7, 5.4.
- Review: pending; no task checkbox, source pin or registration was changed.
- Verification: VERIFIED for focused fixture tests and owning Ruff checks only.

The new core contract is `vendor/data-api/openbb_platform/core/openbb_core/provider/standard_models/enterprise_values.py`. FMP supplies `FMPEnterpriseValuesQueryParams`, `FMPEnterpriseValuesData` and `FMPEnterpriseValuesFetcher` in `vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/enterprise_values.py`. The unmounted `vendor/data-api/openbb_platform/extensions/equity/openbb_equity/fundamental/enterprise_router.py` exports `router` with no prefix; the controller can include it in the existing `/fundamental` router. Its native command uses model `EnterpriseValues` and `OBBject.from_query(Query(**locals()))`.

## Financial contract

One safe listing symbol, annual or quarter frequency, and strict integer limit 1 through 1000 are supported; the default is annual/five observations. The `quarterly` input alias normalizes to `quarter`. Undeclared query options and TTM fail as typed financial errors before transport. The native Query lifecycle passes model parameters separately from provider selection and credentials.

[FMP's primary endpoint documentation](https://site.financialmodelingprep.com/developer/docs/stable/enterprise-values), checked 2026-10-29, explicitly lists symbol, limit and period with annual/quarter choices and a 1000-record maximum. The adapter sends these documented parameters to `/stable/enterprise-values` through existing `get_data_many(with_provenance=True, typed_errors=True)` and preserves `FMPAcquisition.retrieved_at`.

Rows expose `symbol`, `date`, `currency`, `stock_price`, `number_of_shares`, `market_cap`, `cash_and_cash_equivalents`, `total_debt` and `enterprise_value`. Source date is an observation date, without asserting the price/share market date or alignment of market and financial inputs. Currency stays null unless explicitly supplied. Stable camel-case and canonical snake-case aliases are retained. The provider's `minusCashAndCashEquivalents` and `addTotalDebt` values retain their signs. Price unit is currency/share, shares unit is shares, and monetary components use currency with row currency references. Market capitalization and EV are provider calculations. Share-count, debt, cash, lease, minority-interest, forecast and market-date conventions remain explicit nulls. No adjusted EV bridge or reconciliation is calculated.

Rows sort newest known date first, undated rows last; equal dates retain provider order. Missing values stay null; zeros and signed values survive. Observed excess rows are clipped with partial completeness and truncation true; otherwise completeness remains unknown. Unmodeled provider fields are omitted. Finite numeric and date validation failures are sanitized by the existing financial-result validator.

## Evidence

Tests were written before production. [red.log](red.log) records actual missing-module collection failure before the three production files existed. Its outer PowerShell command expanded shell status variables and produced a subsequent shell exit error; that exit status is not used as the pytest result. The displayed pytest collection failure proves RED.

The final Python subprocess runner [check.py](check.py) records true command return codes in [mechanical.json](mechanical.json). Command: `PYTHONPATH=. verification/provider/.venv/bin/python artifacts/market-data-enterprise-values/check.py` from the repository root in WSL Debian. It supplies source overrides for core, FMP, FRED and equity. The focused pytest command is `verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_enterprise_values.py -n0 --maxprocesses=2`.

- Final pytest: 24 passed, one inherited aiohttp deprecation warning, 9.95 seconds, subprocess returncode 0; [output](pytest.log).
- Core, FMP and equity Ruff checks each passed with explicit owning `pyproject.toml`, `--no-fix`, returncode 0; [core](ruff-core.log), [FMP](ruff-fmp.log), [equity](ruff-equity.log).
- Existing `tools.quality.python_units.measure_python` measured complete production files against 400 physical/300 logical/50 per function; all pass. All four source/test files are LF-only with one terminal newline.
- No installs, keys, live requests, shared helper edits, provider registration, shared mount edits or commits occurred. Combined inventory/source-pin acceptance and independent financial review remain pending.

## Frozen source identities

| File | Physical/logical/max function | SHA-256 |
| --- | --- | --- |
| Core standard model | 34/21/0 | `fa4f7eae01af309ab143cfb27aa29c400354b10aa045a8717ebeff8f7b5521b4` |
| FMP adapter | 122/51/8 | `c71960cf626bdc2cc81f3064b8266849c1662d029d6b6a338e91c64f59492acc` |
| Isolated enterprise router | 25/9/1 | `8c2db4e33061281536ad3c1f2c95929e32b9178aed8a54c80a6d2ef191d97ff4` |
| Focused tests | Excluded from production caps | `e2482389f8ff10936168e33288cbb33e80ff41395f6f5994d61e21b7f2b555cc` |

The fixture checks do not prove provider access, installed discovery, mounted API behavior or consumer compatibility. Independent review should challenge the source aliases and unknown financial bases, then the controller must mount/register the accepted adapter in task 5.1 before making installed-route claims.
