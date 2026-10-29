# Periodic key-metrics declarations ready for independent review

Repair task 2.1 preserves output rows and complete result metadata while query/data ClassVars own provider policy, response clipping and all static field semantics. The runtime renders independent templates and supplies actual fiscal basis and availability. Duplicate unit sets are removed. Query defaults remain model-owned; clipping reads the declared `limit_parameter`.

The accepted core correction at data-fork `28c31b4b0ee` establishes canonical Python names, matching native `response_model_by_alias=False`. No adapter alias translation remains. Existing provider aliases are unchanged. The empty inherited market_cap description is overridden with the former runtime fallback `market_cap`, preserving the metadata definition. Unknown market dates and valuation bases remain explicit.

## Verification

- RED before implementation: 2 failed, 33 passed because declarations were missing. `red.log` retains this output. Its outer WSL shell masked failure as rc0; this is not represented as a successful run.
- Two intermediate runs exposed the core alias assumption and then the empty inherited description. Both returned true child rc1, 17 failed/18 passed. `alias-mismatch.log/json` and `missing-description.log/json` retain their evidence. Those causes were repaired; no repeated unexplained retries occurred.
- Final focused suite: 35 passed in 5.87s, true pytest child rc0. Command: `PYTHONPATH="$PWD/vendor/data-api/openbb_platform/core:$PWD/vendor/data-api/openbb_platform/providers/fmp:$PWD/vendor/data-api/openbb_platform/providers/fred" verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_fmp_key_metrics.py -n0 --maxprocesses=2`, from `/mnt/d/Source/QOpenBB` in WSL Debian. `green.log/json` and `final-focused.log` retain evidence.
- Full preservation comparison: 10 baseline cases passed, true child rc0. `preserve.py` loads the unchanged committed baseline fetcher from data-fork HEAD and compares all row values and the entire metadata dictionary across empty, missing, annual, quarterly, mixed-period and clipped responses. `final-baseline.log` retains output. No live I/O occurs.
- Owning FMP Ruff: `verification/provider/.venv/bin/ruff check --no-fix --config vendor/data-api/ruff.toml vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/key_metrics.py vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/key_metrics_data.py` passed, true child rc0. `final-ruff.log` retains output.
- Whole-file production metrics using `tools.quality.python_units.measure_python`: key_metrics.py 140 physical / 56 logical / 10 maximum function; key_metrics_data.py 293 / 57 / 4. Both meet 400/300/50. Controller owns the joined inventory gate.

`final-verification.json` records exact subprocess commands and returncodes. Existing fixtures are retained; two new tests establish complete declaration/runtime agreement, independent nested copies and actual runtime consumption of class-owned financial bases. The upstream aiohttp ClientSession deprecation warning remains.

## Frozen files

| File | SHA-256 |
| --- | --- |
| vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/key_metrics.py | 8176161130c141e4a69b38064e88788a0e0769d91a6aa308579725f4c34d4e22 |
| vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/key_metrics_data.py | 6355fa459b456dad516990d15ce29282ebe475f83718da68fe7202db44df2bc4 |
| tests/providers/test_fmp_key_metrics.py | 24590f5190b414c52eba7662e5e5543ccf67dd1706b4b9a7cd02e66ca968c413 |

No shared inventory, pins, task checkboxes or commits were changed. Foreign renderer changes are preserved. No installations, image builds, browser sessions, live keys or broad suites were used. The verification slot is released; independent review and controller acceptance remain pending.

## Status Report
- STATUS: READY_FOR_REVIEW
- TASK: repair 2.1
- TASK_BRIEF: Preserve periodic metric output and all metadata while sharing complete class-owned templates and model-owned bounds.
- FILES_CHANGED: vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/key_metrics.py, vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/key_metrics_data.py, tests/providers/test_fmp_key_metrics.py
- REQUIREMENTS_CHECKED: 4.1, 4.2, 4.7, 6.1, 6.2
- DESIGN_CHECKED: Components and Interfaces / Provider fetchers and first-batch surface; Financial metadata and schema projection; amendment Minimal contract and Preserve runtime meaning; corrected canonical core interface
- RED_PHASE_OUTPUT: 2 failed, 33 passed, missing declarations; outer rc0 masking disclosed.
- TESTS_RUN: Focused 35 passed, 5.87s, true rc0; 10 complete baseline comparisons passed rc0; owning FMP Ruff --no-fix passed rc0; whole-file caps passed.
- CONCERNS: Independent review and controller inventory/join gate remain pending; baseline aiohttp deprecation warning only.
- EVIDENCE: final-verification.json, green.log/json, final-focused.log, final-baseline.log, final-ruff.log, counts-hashes.json, brief.md; all three code/test files frozen at hashes above.
