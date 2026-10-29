# Daily-price declarations ready for independent review

Repair 2.2 moves static daily-price semantics into typed query/data ClassVars. Calendar validation, row clipping and effective-limit metadata now consume the single declared five-calendar-year/5000-row policy. Nine explicit templates cover the canonical data fields; runtime rendering supplies availability using independent copies. The date field owns the former runtime fallback description, preserving metadata text. No rows, percentage conversions, source timestamps, error categories or adjustment behavior changed.

Requirements checked: 4.2, 4.4, 6.1, 6.2, 7.3. Design checked: FMP query/adapter policy, Financial metadata contract and the approved financial-annotations amendment. The corrected native-name interface is authoritative. Only equity_historical.py and tests/providers/test_fmp_daily_history.py changed in the implementation boundary. No commits, source-pin or inventory changes were made.

## Verification

The existing 31 cases remain intact. Two added cases test exact rendered/runtime field agreement, canonical keys, independent copies and changed declared bounds controlling validation/clipping/metadata. This source ownership refactor has no new user behavior and uses ordinary TDD.

| Check | Observed result | Evidence |
| --- | --- | --- |
| RED before production | 31 passed, 2 failed; 12.49s; true subprocess exit 1, missing declarations | red.log, red.json |
| First GREEN | Collection failed, true exit 2: adding a Field default exposed Python date name/type collision | green.log, green.json |
| Final focused | 33 passed; 5.76s; true exit 0 | final-focused.log, final-focused.json |
| Full baseline agreement | Seven fixtures compare all serialized rows and entire metadata; exit 0 | final-baseline.log, preserve.py |
| Owning FMP Ruff | All checks passed; explicit config and --no-fix; exit 0 | final-ruff.log, final-verification.json |

The type collision was fixed using the standard model's dateType import convention; this aliases the same datetime.date type. Baseline comparisons load the pre-edit module with its own old Query, Data and Fetcher classes, avoiding shared new-class references. Fixtures cover nulls, zero values, positive/negative/null percentage conversion, stable duplicate ordering and observed 5001-row clipping.

Canonical focused command: `verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_fmp_daily_history.py -n0 --maxprocesses=2`, from WSL Debian repository root with provider/core PYTHONPATH. verify.py records the child return code. check.py records exact baseline and Ruff commands and return codes. Whole-file counts use tools.quality.python_units.measure_python and normalized physical lines; controller combined inventory acceptance remains separate.

## Frozen identity

| File | SHA256 | Physical | Logical | Max function |
| --- | --- | --- | --- | --- |
| equity_historical.py | 2ae8eeb7387510d3cb8aff15ea39de02a4884ef9bf268aa876bc29aabdfbee13 | 214 | 73 | 12 |
| test_fmp_daily_history.py | 6d227d1dc9f4289112b07073fca53ef7e071d20dee581204afbae944809fb328 | 164 | 115 | 21 |

Production passes 400/300/50 caps. No live provider, image, browser, installed registry or projection join acceptance is claimed. Independent review and controller acceptance are pending.

## Status Report
- STATUS: READY_FOR_REVIEW
- TASK: Repair 2.2
- TASK_BRIEF: Class-owned daily-price declarations and single-owner bounds preserve all runtime values and metadata.
- FILES_CHANGED: vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/equity_historical.py, tests/providers/test_fmp_daily_history.py
- REQUIREMENTS_CHECKED: 4.2, 4.4, 6.1, 6.2, 7.3
- DESIGN_CHECKED: FMP query/adapter policy; Financial metadata contract; approved financial-annotations amendment
- RED_PHASE_OUTPUT: 31 passed, 2 failed, true exit 1 before production; red.log/json
- TESTS_RUN: 33 passed 5.76s exit 0; seven complete baseline comparisons exit 0; owning FMP Ruff exit 0
- CONCERNS: Independent review and controller combined inventory acceptance pending; existing aiohttp inheritance deprecation warning remains.
- EVIDENCE: final-focused.log/json, final-verification.json, final-baseline.log, final-ruff.log, counts-hashes.json
