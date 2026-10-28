# Statement adapter independent review

Review date: 2026-10-28. Scope: market-data-integrations tasks 2.3 and 2.4, requirements 2.1, 2.4, 4.2, 4.3, 4.5 and 4.7. Actual restored source, native standard models, alias handling, shared validation/transport and focused tests were inspected. Root diff does not expose ignored fork files; fork status identifies the four new production files. No registration or shared transport changes belong to these tasks.

Final packaging verification: both verdicts remain APPROVED at balance commit `072a6c6c2bf374d4f33b43bbed5d95c5eff34275` and cash commit `93d34aebaef3d1c0ddaaa981f5aefd9bdb2f546d`. All four production files are LF-only with one terminating newline. Both balance files were compared against retained pre-normalization commit `82c992343b2d00a32449a84fa5e938806778b158`: prior hashes match the previously reviewed bytes, exact newline/EOF normalization reproduces current bytes, and Python ASTs are identical. Cash adapter bytes are unchanged; final cash declarations were reinspected after newline/EOF cleanup. Because original cash companion bytes were not retained for an exact AST comparison, the controller authorized final-byte regression verification: the same combined command below passed **54 tests in 12.32 seconds, exit 0**, at the final commits. The final hashes and physical counts below supersede the earlier worker snapshots. Controller also reports the joined 78-file complexity gate passed with zero errors or violations before whitespace-only cleanup.

## Review Verdict
- VERDICT: APPROVED
- TASK: 2.3
- MECHANICAL_RESULTS:
  - Tests: PASS. Independent combined command below returned 54 passed, exit 0, including all 20 frozen balance tests. The only subsequent balance change splits datetime imports; behavior and tests are unchanged.
  - TBD/TODO grep: CLEAN.
  - Secrets grep: CLEAN; inspected credentials handling uses request credentials and publishes only allowlisted effective query fields.
  - Static checks: PASS after repair, explicit owning FMP configuration, exit 0.
  - Boundary: WITHIN; balance fetcher, companion declarations and focused tests only.
  - Boundary audit: CLEAN; native Fetcher, standard models, AnnotatedResult and frozen common helpers are reused.
  - RED phase: VERIFIED intermediate regression evidence in ../market-data-balance/result.md. The actual newline-validation failure preceded its repair; no initial preimplementation run is claimed.
- FINDINGS:
  1. Important, resolved: the companion datetime import block failed owning-provider Ruff I001. The earlier unconfigured lint command did not establish the owning check. Controller split the imports; independent explicit-config Ruff now passes.
  2. FYI: amounts remain instant stocks, signed/null/zero observations are preserved, missing fiscal periods remain missing, and unknown debt/cash/lease conventions are disclosed. Acquisition timestamps are retained. Current and legacy filing/year aliases use native model normalization.
- REMEDIATION: None outstanding in the task boundary.
- SUMMARY: The bounded balance adapter meets its source-level acceptance criteria; live and installed-consumer acceptance remain separate.

## Review Verdict
- VERDICT: APPROVED
- TASK: 2.4
- MECHANICAL_RESULTS:
  - Tests: PASS. Frozen corrected source: 34 passed in 7.31 seconds, exit 0, retained worker evidence inspected. Independent combined run also passed 54 cases; its timing limitation is recorded below.
  - TBD/TODO grep: CLEAN.
  - Secrets grep: CLEAN; actual transport fixtures assert safe empty/invalid/timeout failures and exclude canary text.
  - Static checks: PASS, independent explicit owning FMP configuration, exit 0.
  - Boundary: WITHIN; cash-flow fetcher, companion declarations and focused tests only.
  - Boundary audit: CLEAN; no registration, local valuation model, quarter derivation or shared transport edit.
  - RED phase: VERIFIED regression sensitivity, with chronology limitation. No preimplementation RED was captured. Inspected in-memory diagnostic restores the two rejected behaviors and yields 5 failed / 15 passed / 14 deselected, inner pytest exit 1; wrapper exit 0 means the expected failures occurred. Production bytes were untouched. Controller explicitly accepted this transparently labeled postimplementation evidence instead of a fabricated historical RED phase.
- FINDINGS:
  1. Important, resolved: beginning and ending cash initially inherited annual/discrete-quarter duration metadata. They now use instant basis. Beginning cash explicitly has no observation-date reference, with unavailable period-start date disclosed; ending cash references period end. Two annual/quarter regressions detect the original stock-basis defect.
  2. Important, resolved: direct Pydantic query coercion accepted boolean, numeric-string and integral-float limits instead of the frozen strict statement-query contract. The adapter now reuses validate_statement_query and preserves the original symbol for control-character validation. Invalid input tests fail before transport; the diagnostic detects all three original coercions.
  3. FYI: explicit typed_errors=True makes transport intent clear. Its prior omission was not itself a defect because the frozen helper defaults typed errors to with_provenance.
  4. FYI: signed/zero/null amounts, fiscal dates, row currency and acquisition timestamps remain intact. Provider free/operating cash-flow calculations are identified separately from observations without inventing a house formula. Unknown/mixed fiscal labels remain unknown and no YTD-to-quarter conversion occurs.
- REMEDIATION: None outstanding in the task boundary.
- SUMMARY: The repaired cash-flow adapter meets its bounded source-level criteria with meaningful regression evidence; live and installed-consumer acceptance remain separate.

## Verification and source identity

Independent command, WSL Debian, CPython 3.13.15, repository root:

```sh
PYTHONPATH=$PWD/vendor/data-api/openbb_platform/core:$PWD/vendor/data-api/openbb_platform/providers/fmp:$PWD/vendor/data-api/openbb_platform/providers/fred verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_balance_sheet_metadata.py tests/providers/test_cash_flow_metadata.py -n0 --maxprocesses=2
```

Result: 54 passed in 12.28 seconds, exit 0, one existing aiohttp deprecation warning. Cash was reopened for repair as this command started; its final frozen verification is therefore recorded separately rather than relying on run timing.

Independent static command, exit 0:

```sh
verification/provider/.venv/bin/python -m ruff check --no-fix --config vendor/data-api/openbb_platform/providers/fmp/pyproject.toml vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/balance_sheet.py vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/balance_sheet_data.py vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/cash_flow.py vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/cash_flow_data.py
```

Reviewed SHA256 identities:

| File | SHA256 |
| --- | --- |
| balance_sheet.py | 6fc16c6e7c208ccfc9c7757ec3c3f95e6d3fb70801c0d074f31678ee532248a5 |
| balance_sheet_data.py | b1b444be7243b29fa1c93aa3b7c9a28131d4148c15634224add5e9291fd5e76e |
| test_balance_sheet_metadata.py | ea448b9ecf0ecca09ee5e7ec9bbb4764fea7a7b28a1b97e9ec638677b3320e15 |
| cash_flow.py | 792a160a6d94fe2da1d7b25499afaa5226b02c041e86409dc3e68814bfbdb60e |
| cash_flow_data.py | cf0baa1a8fa3c5968a4c23c8b99aef38225a04819235c7596ec0678f938f79d4 |
| test_cash_flow_metadata.py | 9bb0c0ecbd99d033b23c0a5c510624af80e7e209dd9548b8b5359b037616663b |

Whole-file measurements remain below 400 physical / 300 logical / 50 per function: balance adapter 160/58/9, balance declarations 260/74/6 after import-only repair; cash adapter 136/56/14 and declarations 263/61/6. The controller owns the joined inventory/checker gate. No provider account, installed route, widget, image or live financial acceptance is asserted here.
