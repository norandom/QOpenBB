# Independent review: FMP discovery and daily history

Tasks 2.5 and 2.6 are approved at the adapter boundary on 2026-10-28. Independent inspection covered the actual new files, approved requirements and design, the worker RED logs, and the final frozen tests. Provider registration, live entitlement/data, installed routes, widgets and deployment remain separate acceptance work.

## Review Verdict
- VERDICT: APPROVED
- TASK: 2.5
- MECHANICAL_RESULTS:
  - Tests: PASS. Independent combined command below collected 68 tests (37 discovery and 31 daily), passed in 13.29 seconds, exit 0.
  - TBD/TODO grep: CLEAN; no TBD, TODO, FIXME, HACK or XXX markers in the reviewed source/tests.
  - Secrets inspection: CLEAN; credentials enter only the encoded transport request, synthetic test canaries are not production credentials.
  - Static checks: PASS; owning FMP Ruff configuration, explicit --no-fix, all four production files, exit 0.
  - Boundary: WITHIN; search/peers and cohesive identity/metadata declarations only, with dedicated tests. No tracked fork diff in shared helpers, core or registration.
  - Boundary audit: CLEAN; named search and provider peer candidates retain shared transport/metadata contracts without downstream consumer coupling.
  - RED phase: VERIFIED; ../market-data-discovery/red.txt records the absent equity_search module collection failure before restoration. The initial wrapper's zero exit was not treated as a passing test.
- FINDINGS:
  1. No remaining blocking findings. Requirements 2.1 and 3.1-3.3 are supported by name/symbol endpoint routing, retained ambiguous alternatives, exchange/currency and optional identifiers, qualified listing versus issuer identity, and source-symbol peer provenance.
  2. Strict 1-100 limits, nonblank safe queries, malformed row validation, null/zero preservation, local clipping and unknown completeness are implemented. Peer price uses currency/share; market cap is a provider calculation with unknown currency retained when absent.
  3. Empty direct transformations are tested; actual shared transport classifies empty upstream data as missing_data. No live empty-search success claim follows from the transform fixture.
- REMEDIATION: None.
- SUMMARY: Named discovery and bounded provider peer suggestions satisfy the approved local responsibility and preserve identity uncertainty.

## Review Verdict
- VERDICT: APPROVED
- TASK: 2.6
- MECHANICAL_RESULTS:
  - Tests: PASS. The same independent 68-test run includes all 31 daily-history tests, exit 0.
  - TBD/TODO grep: CLEAN.
  - Secrets inspection: CLEAN; no production credential values or unsafe public request URLs were introduced.
  - Static checks: PASS; owning FMP Ruff, explicit --no-fix, exit 0.
  - Boundary: WITHIN; daily model and its dedicated tests only.
  - Boundary audit: CLEAN; safe shared transport is reused without changing helpers/core/registration or adding local pricing calculations.
  - RED phase: VERIFIED; ../market-data-daily-history/red.log records the absent equity_historical module collection failure before restoration.
- FINDINGS:
  1. No remaining blocking findings. Requirements 2.1, 2.4, 2.5, 4.2, 4.4, 4.5 and 7.3 are supported by mandatory ordered dates, the five-calendar-year bound, daily-only interval and split-only adjustment, stable ascending dates with retained duplicates, 5000-row cap, explicit clipping, and unknown historical completeness.
  2. The initially inspected price units were too coarse. Final frozen code and assertions correct OHLC/change/VWAP to currency/share and classify the percentage-point conversion as locally_derived. Source basis and conversion are explicit; zero and null remain distinct.
  3. Fixtures demonstrate input nonmutation, missing dates are not fabricated, invalid/out-of-window rows fail safely, and point-in-time safety is not asserted.
- REMEDIATION: None; the financial metadata correction was verified before approval.
- SUMMARY: Bounded daily history preserves provider adjustment semantics, observed values and honest completeness without expanding into intraday or local adjustment work.

## Reproducible evidence

From the repository root in WSL Debian:

```sh
PYTHONPATH=vendor/data-api/openbb_platform/core:vendor/data-api/openbb_platform/providers/fmp:vendor/data-api/openbb_platform/providers/fred verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_fmp_discovery.py tests/providers/test_fmp_daily_history.py -n0 --maxprocesses=2
verification/provider/.venv/bin/ruff check --config vendor/data-api/openbb_platform/providers/fmp/pyproject.toml --no-fix vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/equity_search.py vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/equity_peers.py vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/discovery_data.py vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/equity_historical.py
```

Evidence: [independent tests](review-tests.log), [exit code](review-tests-exit.txt), [Ruff](review-ruff.log). Python 3.13.15, pytest 9.1.1. One pre-existing aiohttp ClientSession inheritance deprecation warning was reported. The first Windows WSL launcher failed with console-title error 0xE9 before emitting pytest output. A hidden Start-Process invocation completed the identical focused command successfully; the launcher failure is not a test failure or RED evidence.

Whole-file complexity measurements use the existing project Python syntax-unit checker. The recorded physical/logical/largest-function counts are 74/35/5 for search, 77/38/6 for peers, 76/34/7 for shared discovery declarations, and 165/73/12 for daily history, below 400/300/50. Worker metric files and the frozen source identities were inspected; controller combined inventory/manifest gate remains the delivery gate.

| Frozen file | SHA-256 |
| --- | --- |
| equity_search.py | 0f85c495323418258a177880d7a6ded9d2b349cc4826bb278cae9ea031d374f8 |
| equity_peers.py | deb6f9279768685dab48904ccdfc7bf6f6933d6e92b1141e912f28e9a1b0e20c |
| discovery_data.py | 05d6499cf26808ae042794f748eeac0656a36fa8b0841a3756aaecedef54a768 |
| equity_historical.py | a9d43baaba1cf04fa32b6ea0ed081759d3bbc0f957318feabe00e653b237af42 |
| tests/providers/test_fmp_discovery.py | 28d78f881753c4484bcbd57b2b2933b1e8ae6b95ac2739912e472fe47628d9ba |
| tests/providers/test_fmp_daily_history.py | 560aafcdbf2ae26172c3a32b6872707d25d5a80834a41ff66e38340f5ded32d0 |

Production basenames above resolve under vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models. This review made no production edits, live requests, installs or registration changes.
