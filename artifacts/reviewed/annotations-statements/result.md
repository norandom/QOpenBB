# Balance-sheet and cash-flow declarations ready for review

Task 4.2 now uses typed query/data declarations as the source for static financial semantics. Runtime rendering fills observed availability and cash-flow periods on independent copies. Complete serialized rows and metadata match the original adapters in all 14 comparison scenarios.

The four model files and two existing test files are frozen at the SHA-256 identities in `hashes.json`. Controller acceptance, shared inventory/source pins and independent review remain pending. No commits or shared production edits were made by this worker.

## Verification

The focused command ran in Debian WSL from `/mnt/d/Source/QOpenBB`, with source PYTHONPATH entries for core, FMP and FRED:

```sh
verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_balance_sheet_metadata.py tests/providers/test_cash_flow_metadata.py -n0 --maxprocesses=2
```

- RED: 12 new agreement cases failed for missing query declarations; all 54 original cases passed, 12.95 seconds, actual child exit 1 (`red.log`).
- GREEN: 66 passed, 6.94 seconds, actual child exit 0 (`green.log`). The only warning is the existing aiohttp ClientSession inheritance deprecation.
- Full baseline comparison: 14 scenarios, actual child exit 0 (`preserve.log`); signed/zero/null amounts, all modeled fields, fiscal labels, annual/quarter/mixed/unknown/YTD/empty periods and clipping/duplicate behavior retained.
- Owning Ruff: `verification/provider/.venv/bin/ruff check --config vendor/data-api/ruff.toml --no-fix` on the four changed production files, actual child exit 0.
- Whole-file checker: `PYTHONPATH=. pipeline/.venv/bin/python artifacts/annotations-statements/caps.py`, actual child exit 0. Uses the repository's `tools.quality.python_units.measure_python` convention; controller still owns the combined inventory gate.
- Scoped root/fork `git diff --check` passed.

| File | Physical | Logical | Largest function |
| --- | ---: | ---: | ---: |
| balance_sheet.py | 148 | 50 | 9 |
| balance_sheet_data.py | 356 | 78 | 6 |
| cash_flow.py | 138 | 57 | 12 |
| cash_flow_data.py | 336 | 64 | 6 |

## Preserved contracts

Complete explicit canonical field mappings replace the former runtime unit/category sets and field-name inference. Field descriptions remain definition owners; cash-flow free_cash_flow now owns the exact former runtime fallback, "Provider-reported free cash flow; calculation definition unavailable." Query model fields retain ordinary defaults and constraints. Declarations use response clipping through `limit_parameter="limit"`; clipping consumes the bound declaration.

Balance amounts remain instant stocks. Cash-flow annual/discrete-quarter inference remains driven by actual returned fiscal labels, including identity fields as in the original metadata. Opening/closing cash remain instants, and opening cash retains an unknown observation date. Provider observations/calculations, financial-basis unknowns, signs, nulls, aliases, receipt timestamps, errors, ordering and observed clipping remain unchanged. No formulas or calculations were added.

## Status Report
- STATUS: READY_FOR_REVIEW
- TASK: 4.2
- TASK_BRIEF: Adopt authoritative balance/cash query and data templates while preserving all existing runtime values and metadata, within 400/300/50 caps.
- FILES_CHANGED: balance_sheet.py, balance_sheet_data.py, cash_flow.py, cash_flow_data.py, tests/providers/test_balance_sheet_metadata.py, tests/providers/test_cash_flow_metadata.py
- REQUIREMENTS_CHECKED: 4.1, 4.2, 4.3, 4.7, 6.1, 6.2
- DESIGN_CHECKED: Provider fetchers and first-batch surface; Financial metadata contract; API/widget projection; approved financial-annotations amendment.
- RED_PHASE_OUTPUT: Focused command above: 12 failed missing declarations, 54 passed; actual child exit 1.
- TESTS_RUN: 66 passed; 14 complete baseline comparisons passed; owning Ruff passed; four whole-file cap checks passed; actual child exits 0.
- CONCERNS: Independent financial review and controller acceptance remain pending. Core product.md/tech.md/structure.md steering files are absent; applicable explicit amendment and present steering were read. Initial shell launch had CRLF and was corrected to LF before the meaningful RED run; no production code had changed. First Ruff invocation used pipeline Python without Ruff; corrected to existing provider Ruff executable, no installs.
- EVIDENCE: brief.md, red.log, green.log, baseline.py/baseline.json, preserve.log, caps.py/caps.json, hashes.json, verification.json; owned modules and focused tests.
