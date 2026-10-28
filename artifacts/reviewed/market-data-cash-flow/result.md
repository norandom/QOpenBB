# Cash-flow adapter: ready for independent review

Task 2.4 restores the retained cash-flow contract with bounded annual and quarterly requests, acquisition provenance and financial field metadata. This is synthetic adapter evidence; provider access, registration, installed API behavior and live financial acceptance remain unverified.

## Scope and source

- Production: `vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/cash_flow.py` and controller-approved companion `cash_flow_data.py`.
- Tests: `tests/providers/test_cash_flow_metadata.py`.
- Retained declarations recovered from owned-fork history `2232178fd8c:openbb_platform/providers/fmp/openbb_fmp/models/cash_flow.py`; current baseline had no cash-flow adapter. Class names remain `FMPCashFlowStatementQueryParams`, `FMPCashFlowStatementData` and `FMPCashFlowStatementFetcher`.
- No shared helpers, provider registration, root metadata or source pins were changed by this worker. No commit was made.

## Financial behavior

One nonblank symbol, annual/quarter requests and strict integer limits 1 to 1000 validate through the frozen shared validator before transport. Boolean, string and float limits are rejected; original symbols reject control bytes before normalization. `quarterly` normalizes to native `quarter`; unsupported TTM is rejected. Amounts retain provider signs, zeroes, nulls and row currency. Current and legacy fiscal-year/filing-date keys are accepted. Additional retained debt/dividend/tax/interest fields have explicit source aliases.

Rows sort newest first, retaining provider order for equal dates. Observed over-limit results are clipped and marked partial; otherwise historical completeness stays unknown. Period metadata uses observed FY/Q1-Q4 labels, with unknown or mixed labels leaving the common basis null. No quarter is derived from year-to-date figures. Cash classification and restricted-cash definitions remain unknown. Provider operating/free cash flow is labeled provider calculation without supplying a house formula. Beginning and ending cash are instant stocks. Beginning cash has no known observation date because no period-start date is supplied; it does not inherit period end. Receipt timestamps pass through unchanged; metadata makes no point-in-time claim. Typed transport errors are now explicitly requested.

## Fresh verification, 2026-10-28

The controller granted the serialized suite slot. From `/mnt/d/Source/QOpenBB` in WSL Debian:

```sh
PYTHONPATH=$PWD/vendor/data-api/openbb_platform/core:$PWD/vendor/data-api/openbb_platform/providers/fmp:$PWD/vendor/data-api/openbb_platform/providers/fred verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_cash_flow_metadata.py -n0 --maxprocesses=2
```

Exit 0: **34 passed** in 7.31 seconds, no skipped checks. One existing aiohttp ClientSession inheritance deprecation warning was emitted. Fixtures exercise annual/quarter observations, dates/year/currency, all retained amount aliases, signed/null/zero values, provenance, invalid pre-I/O inputs, safe invalid rows, actual transport empty/invalid/timeout failures, period-label uncertainty, duplicates and observed clipping.

```sh
verification/provider/.venv/bin/python -m ruff check --no-fix --config vendor/data-api/openbb_platform/providers/fmp/pyproject.toml vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/cash_flow.py vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/cash_flow_data.py
```

Exit 0: all checks passed. Initial configuration-path discovery failed against absent `vendor/data-api/pyproject.toml`; the final command uses the owning FMP configuration. An import-order finding was repaired before the passing final check.

Canonical `tools.quality.python_units.measure_python` on the whole current files, using `pipeline/.venv/bin/python`: adapter **136 physical / 56 logical / 14 maximum callable**; declarations **263 / 61 / 6**. All are below 400/300/50. The controller owns the joined inventory/combined gate.

## Independent-review repair and regression sensitivity

The reviewer identified cash stock period/date semantics and coercible limit inputs. The repaired 34-case run above includes eight added cases for stock instants and strict query validation. Owning lint passed again after the repair. No historical failed test run was captured before implementation; this record does not claim a TDD RED phase.

Postimplementation diagnostic: `regression_sensitivity.py` compiles an in-memory adapter copy with strict query validation and stock instant basis deliberately removed. It does not edit reviewed production files. Under the same source override and Python environment, its 20 selected cases produced **5 failed / 15 passed / 14 deselected in 7.05 seconds**. The three bool/string/float limit cases reached the forbidden transport stub; both annual/quarter stock tests detected the incorrect duration basis. Its inner pytest exit was 1, and the diagnostic wrapper exited 0 because that failure was expected. The corrected frozen source passed all 34 tests in the earlier final run; no reviewed source changed during the diagnostic.

Frozen SHA-256:

- `cash_flow.py`: `792A160A6D94FE2DA1D7B25499AFAA5226B02C041E86409DC3E68814BFBDB60E`
- `cash_flow_data.py`: `CA19EB06C9B2C45FFA780B914EE24DB321735AE5992EC9B2266F361BD1B430AF`
- `tests/providers/test_cash_flow_metadata.py`: `9BB0C0ECBD99D033B23C0A5C510624AF80E7E209DD9548B8B5359B037616663B`

## Review gate

STATUS: READY_FOR_REVIEW. Worker edits are frozen. Independent acceptance, joined regression checks, source identity promotion and provider registration remain controller work. Disprove readiness by an incorrect alias/sign/date, fabricated period basis, timestamp reset, unsafe typed failure, or bound bypass in the owned scope.

Final declaration packaging normalized LF and stripped blank EOF lines only. Source commit93d34aebaef; final-source.json records current bytes/counts. Final independent tests establish the normalized snapshot.
