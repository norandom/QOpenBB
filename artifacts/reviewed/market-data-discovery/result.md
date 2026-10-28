# FMP discovery adapter review

Task 2.5 is implemented for deterministic review. Name and symbol searches retain provider alternatives; peer candidates are explicitly provider suggestions. Registration, source pin promotion and live entitlement acceptance remain separate controller tasks.

## Scope and semantics

- `equity_search.py`: `search-name` and `search-symbol`, default 20 and strict integer range 1 to 100 before I/O. The retained historical `equity_search.py` was a financial screener; the approved named-search contract intentionally does not restore those unrelated screener filters.
- `equity_peers.py`: retained `stock-peers` adapter, default 20 and strict integer range 1 to 100. Provider peer order is retained; the local cap is not advertised as a native provider pagination guarantee. Zero price/market cap remain zero.
- `discovery_data.py`: typed listing/issuer attributes, qualified identities and common acquisition/financial metadata. CIK qualifies issuer identity only when supplied. A symbol with unknown exchange does not establish a globally unique listing. No ticker-based issuer consolidation or cross-provider mapping is inferred.
- Explicit modeled fields discard undeclared provider extras. Available exchange, currency, CIK, ISIN and instrument type remain typed attributes. Price is currency/share; market cap is a provider calculation in the row currency, which can remain unknown. No observation/publication date is invented.
- Metadata retains the actual transport acquisition timestamp, endpoint/search mode, query, row limit, clipping and unknown completeness. Qualification and suggestion labeling have an explicit transformation record.

Official references: [symbol search](https://site.financialmodelingprep.com/developer/docs/stable/search-symbol), [name search](https://site.financialmodelingprep.com/developer/docs/stable/search-name), [peer candidates](https://site.financialmodelingprep.com/developer/docs/stable/peers). These references do not establish account entitlement. Historical recovery: search `be7f0c30d2b^`, peers `869cfed12599^` in the data fork.

## Verification

Tests were written before production files. The actual first run collected zero tests and failed importing the absent `openbb_fmp.models.equity_search`; see `red.txt` (17.75 seconds). The first shell wrapper printed the failure but exited zero because its final command was `cat`; it is not passing test evidence. The pytest output records the collection error. No invented historical assertion failure is claimed.

The initial implementation passed 27 tests in 7.79 seconds. Subsequent changes add typed malformed-row protection, explicit extra-field exclusion and metadata units/origins. Final validation follows below.

Commands use WSL Debian from `/mnt/d/Source/QOpenBB` with source overrides:

```sh
PYTHONPATH=vendor/data-api/openbb_platform/core:vendor/data-api/openbb_platform/providers/fmp:vendor/data-api/openbb_platform/providers/fred verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_fmp_discovery.py -n0 --maxprocesses=2
verification/provider/.venv/bin/ruff check --config vendor/data-api/openbb_platform/providers/fmp/pyproject.toml --no-fix vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/{equity_search,equity_peers,discovery_data}.py
```

Owning FMP Ruff passes on the final source. Local whole-file counts use the existing `tools.quality.python_units.measure_python` implementation; controller inventory/combined gate remains required. All production files use LF with exactly one terminal newline. No credentials, live calls, dependency installs, provider registration, locks, commits or shared helper edits were made.

| Production file | Physical | Logical | Largest function | SHA-256 |
| --- | ---: | ---: | ---: | --- |
| equity_search.py | 74 | 35 | 5 | 0f85c495323418258a177880d7a6ded9d2b349cc4826bb278cae9ea031d374f8 |
| equity_peers.py | 77 | 38 | 6 | deb6f9279768685dab48904ccdfc7bf6f6933d6e92b1141e912f28e9a1b0e20c |
| discovery_data.py | 76 | 34 | 7 | 05d6499cf26808ae042794f748eeac0656a36fa8b0841a3756aaecedef54a768 |

Independent acceptance remains pending. Endpoint access, real financial values, installed routes/widgets and packaged/runtime behavior are unverified.

## Final focused result

Final source passes 37 tests in 10.20 seconds, exit 0 (`final-green.txt`). One existing aiohttp `ClientSession` inheritance deprecation warning remains. Coverage includes both search endpoint choices, escaped query transport, default/strict bounds, invalid symbols/search terms, ambiguous listings/currencies/issuer unknowns, acquisition timestamps, metadata serialization, zero/null peer values, provider suggestion/source mapping, clipping, empty results and typed malformed-row failures. The source SHA values above are frozen for independent review.

## Status Report

- STATUS: READY_FOR_REVIEW
- Final pytest: 37 passed, 10.20 seconds, exit 0.
- Owning FMP Ruff: PASS, explicit owning configuration and `--no-fix`.
- Whole production caps: PASS, 74/35/5; 77/38/6; 76/34/7 against 400/300/50.
- Independent review, controller combined gate/inventory, registration and live provider acceptance: pending.
