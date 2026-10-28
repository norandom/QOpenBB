# Balance-sheet adapter ready for independent review

Task 2.3 restores the retained FMP balance-sheet schema with bounded annual/quarter requests and financial metadata. Changes are frozen for parent review; provider registration, shared helpers, inventory and source pins remain parent-owned. No commits were made.

## Scope and source

- Fork baseline: `d1bb4821a659e6a9d28b9554ba670e72d80a69fb` plus the changed files below.
- Retained declaration source: `869cfed1259^:openbb_platform/providers/fmp/openbb_fmp/models/balance_sheet.py`.
- Production: `vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/balance_sheet.py` and `balance_sheet_data.py` beside it.
- Tests: `tests/providers/test_balance_sheet_metadata.py`.
- No shared helpers, registration, root metadata or unrelated worker changes were edited.

The query uses the frozen `validate_statement_query` helper and safe core validation: one symbol, annual/quarter (quarterly alias normalized), default five, strict integer 1 through 1000. Original symbol text also passes the adapter validator so helper trimming cannot conceal control characters. Acquisitions request provenance and typed errors from the shared transport.

Amounts, signs, zeroes, nulls, fiscal year, fiscal end, filing and acceptance dates remain source observations. Legacy/current year and filing spellings work. Missing fiscal periods stay missing. Latest reporting dates sort first; duplicate dates retain provider order and are not merged. Over-limit responses are capped with partial/truncated metadata. Stock amounts use instant period basis even when requested quarterly. Row currency, unavailable fields, original acquisition time, unknown debt/cash/lease conventions and absent restatement/vintage guarantees are explicit. No ratios, forecast or local bridge is calculated.

## Verification

Executed in WSL Debian from `/mnt/d/Source/QOpenBB`:

```sh
PYTHONPATH=$PWD/vendor/data-api/openbb_platform/core:$PWD/vendor/data-api/openbb_platform/providers/fmp:$PWD/vendor/data-api/openbb_platform/providers/fred verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_balance_sheet_metadata.py -n0 --maxprocesses=2
```

Final result: **20 passed in 6.91 seconds**, exit 0. Existing aiohttp ClientSession inheritance deprecation warning remains. Checks exercise annual/quarterly legacy/current aliases, signed and zero amounts, absent/null fields, missing dates/periods, invalid bounds before I/O, safe invalid-response handling, typed acquisition, timestamp retention, sorting and observed truncation. An intermediate helper-reuse run exposed newline trimming before validation (1 failed, 19 passed); preserving original symbol text for final model validation repaired the cause and the full focused rerun passed.

Owning fork Ruff command, exit 0: `../../verification/provider/.venv/bin/ruff check --no-fix openbb_platform/providers/fmp/openbb_fmp/models/balance_sheet.py openbb_platform/providers/fmp/openbb_fmp/models/balance_sheet_data.py` from `vendor/data-api`.

Whole-file measurements use `tools.quality.python_units.measure_python` (project-syntax-units-v1), physical `splitlines` counts, CPython 3.13.15:

| File | Physical | Logical | Largest function |
| --- | ---: | ---: | ---: |
| balance_sheet.py | 160 | 58 | 9 |
| balance_sheet_data.py | 260 | 74 | 6 |

Both files satisfy 400/300/50 caps. Parent owns the joined inventory/checker gate.

SHA256 frozen bytes:

- balance_sheet.py: `6fc16c6e7c208ccfc9c7757ec3c3f95e6d3fb70801c0d074f31678ee532248a5`
- balance_sheet_data.py: `b1b444be7243b29fa1c93aa3b7c9a28131d4148c15634224add5e9291fd5e76e`
- test_balance_sheet_metadata.py: `ea448b9ecf0ecca09ee5e7ec9bbb4764fea7a7b28a1b97e9ec638677b3320e15`

Synthetic fixtures establish adapter behavior only. Real-provider entitlement, installed command integration and widget behavior remain unverified in this lane. No credentials were used or recorded.

## Status Report
- STATUS: READY_FOR_REVIEW

## RED_PHASE_OUTPUT

The following excerpt transcribes the actual intermediate pytest output observed in this worker's tool session `48849` (completion chunk `493744`). It is retained as an observed tool-output excerpt, not a separately captured raw log. No failing run was recreated.

```text
collected 20 items

verification/provider ........F...........                               [100%]

=================================== FAILURES ===================================
______________ test_invalid_query_fails_safely_before_io[params4] ______________

params = {'symbol': 'AAPL\n'}

>       with pytest.raises(FinancialError) as error:
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       Failed: DID NOT RAISE FinancialError

tests/providers/test_balance_sheet_metadata.py:74: Failed

FAILED verification/provider::test_invalid_query_fails_safely_before_io[params4]
=================== 1 failed, 19 passed, 1 warning in 11.78s ===================
```

Cause: the shared statement-query helper stripped the trailing newline before the adapter symbol validator received the value. Repair: retain the original symbol input for model validation while retaining the helper's normalized period and bounded integer limit. The final 20-pass run above verifies that repair. This intermediate RED evidence is a regression exposed during helper reuse; the lane did not run an initial pre-implementation RED suite because the controller withheld the suite slot until code and fixtures were ready.

Independent owning-config Ruff found import sorting that the original unconfigured invocation missed. Controller corrected only the datetime imports and reran explicit `--config vendor/data-api/openbb_platform/providers/fmp/pyproject.toml --no-fix` for both files: exit0, All checks passed. No financial logic changed. Final companion hash/count above reflect the repair.

Final source packaging uses LF and one terminal newline. Source commit072a6c6c2bf; the updated hashes/counts above reflect this normalization. Financial AST unchanged against the pre-normalization source commit.
