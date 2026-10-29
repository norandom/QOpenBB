# Enterprise-value input source review

Task 2.9 is approved for source-level acceptance on 2026-10-29. The three isolated production modules preserve provider components and explicit unknown valuation conventions. This review does not accept registration, installed routes, live entitlement or consumer behavior.

## Review Verdict
- VERDICT: APPROVED
- TASK: market-data-integrations 2.9
- MECHANICAL_RESULTS:
  - Tests: PASS. Independent WSL run of `verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_enterprise_values.py -n0 --maxprocesses=2`, with source PYTHONPATH for core, FMP, FRED and equity: 24 passed in 9.34 seconds, exit 0. One inherited aiohttp ClientSession deprecation warning.
  - TBD/TODO grep: CLEAN across all four reviewed source/test files, including FIXME/HACK/XXX.
  - Secrets grep: CLEAN; manual inspection confirms the only API-key value is a synthetic test marker and production obtains credentials from the native credentials argument.
  - Static checks: PASS. Independently executed `verification/provider/.venv/bin/python -m ruff check --config <owning pyproject.toml> --no-fix <file>` for core, FMP and equity; each exit 0.
  - Complexity: PASS. Existing checker evidence reports physical/logical/maximum-function units of 34/21/0 for core, 122/51/8 for FMP, and 25/9/1 for the router. Each meets 400/300/50. Source hashes independently match the frozen evidence. Controller's combined inventory gate remains required.
  - Boundary: WITHIN. New core model, FMP adapter, isolated enterprise router and focused tests only. Shared registration and router mounting remain task 5.1 work.
  - Boundary audit: CLEAN. Native Fetcher, shared acquisition transport, Query and OBBject are retained; no local enterprise-value calculation or consumer-specific fetch path is introduced.
  - RED phase: VERIFIED. The actual red.log contains missing-module pytest collection failure for openbb_fmp.models.enterprise_values before implementation. Its reported outer-shell status is not used as pytest evidence.
- FINDINGS:
  1. No blocking findings in task 2.9's source boundary.
  2. FYI: authoritative schema projection remains blocked by the separate declaration-sidecar gap. This review does not claim task 4.1 completion or require this adapter to invent a new annotation interface.
- REMEDIATION: None for task 2.9. Complete the controller-owned inventory/source acceptance gate before marking the task accepted.
- SUMMARY: The bounded source adapter preserves FMP enterprise-value components, dates, currency and unknown financial bases without claiming an analyst-adjusted valuation bridge.

## Contract assessment

Reviewed the actual untracked production files and tests, task 2.9, requirements 2.1/4.1/4.2/4.7/5.4, and the design's provider lifecycle and financial metadata contract. Core product.md, tech.md and structure.md steering files are absent; applicable complexity, testing, documentation and delegation policies were read.

The aliases retain stockPrice, numberOfShares, marketCapitalization, minusCashAndCashEquivalents, addTotalDebt and enterpriseValue without sign reversal or recomputation. Canonical names are also accepted through native model aliases. Units distinguish currency/share, shares and currency; available currency references the row. EV and market capitalization are labeled provider calculations. Missing components stay null, numeric zeros and signed values survive, and unsupported finite-value/date payloads produce safe typed validation errors.

Queries enforce one safe symbol, annual/quarter periods, default five and strict limits 1 through 1000; quarterly normalizes to quarter. TTM and undeclared options are rejected before extraction. The new extra-forbid policy agrees with inspected native Query.execute: only standard and filtered extra parameter dictionaries enter params, while provider choice, credentials and preferences remain separate executor arguments. The unmounted router follows the native Query/OBBject command shape; installed dispatch is not exercised here.

Extraction uses shared typed-error acquisition with provenance. Transformation retains acquisition time, sorts dated observations newest first, keeps duplicate source order and puts undated rows last. Excess observations disclose clipping and partial completeness; non-clipped results remain explicitly unknown. Metadata makes observation versus market-date uncertainty explicit and does not claim point-in-time safety. Unknown share, cash/debt, lease, minority-interest and forecast bases remain null.

The focused fixtures exercise normal and malformed queries, aliases, monetary/share units, provenance, empty and missing observations, duplicate stability, clipping, invalid numerics/dates and endpoint parameters. Shared transport failure implementation is reused rather than duplicated. Live provider access and mounted API behavior require later evidence.

## Frozen inputs

SHA-256 values independently checked against the worker evidence:

| Input | SHA-256 |
| --- | --- |
| Core enterprise_values.py | fa4f7eae01af309ab143cfb27aa29c400354b10aa045a8717ebeff8f7b5521b4 |
| FMP enterprise_values.py | c71960cf626bdc2cc81f3064b8266849c1662d029d6b6a338e91c64f59492acc |
| enterprise_router.py | 8c2db4e33061281536ad3c1f2c95929e32b9178aed8a54c80a6d2ef191d97ff4 |
| test_enterprise_values.py | e2482389f8ff10936168e33288cbb33e80ff41395f6f5994d61e21b7f2b555cc |

Supporting local evidence: [implementation report](../market-data-enterprise-values/result.md), [RED output](../market-data-enterprise-values/red.log), and [checker measurements](../market-data-enterprise-values/mechanical.json).
