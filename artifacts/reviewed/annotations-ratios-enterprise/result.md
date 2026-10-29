# Ratio and enterprise declarations ready for independent review

Task 4.5 now uses typed class-owned query/data annotations for periodic ratios and enterprise inputs. Runtime renders independent field templates, resolves actual availability and fiscal-period basis, and reads the declared limit parameter for clipping and bounds. The old ratio category sets and enterprise field-classification loop are removed. Financial definitions, including the existing ratio calculation caveat, live in the owning Field descriptions. Provider input aliases remain unchanged.

Query defaults and numeric bounds come from the owning models. Strict ratio count validation and the accepted quarterly spelling are enforced on those models; transform_query no longer duplicates defaults or invokes a second bounds owner. Enterprise core models and router remain unchanged. Values stay provider observations/calculations: dividend yield fractions and percentage points remain distinct, per-share quantities retain row-currency references, and unknown market/share/debt/cash/lease/minority-interest/forecast conventions remain explicit.

## Evidence

2026-10-29, WSL Debian, Python 3.13.15. Working directory `/mnt/d/Source/QOpenBB`; PYTHONPATH includes owned core, FMP, FRED and equity source directories. No installation, image, browser, live-provider or WSL-restart work ran. The parent serialized the verification slots.

- RED before production edits: `verification/provider/.venv/bin/python artifacts/annotations-ratios-enterprise/run_tests.py red`, actual pytest child rc1, 6 new declaration agreement cases fail with MissingFinancialAnnotation; all 53 original cases pass. See red.log and red.rc. The 11 baseline snapshots were captured before production edits.
- GREEN: `verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_fmp_financial_ratios.py tests/providers/test_enterprise_values.py -n0 --maxprocesses=2`, actual child rc0 recorded by run_tests.py, 61 passed. This retains 29 original ratio and 24 original enterprise cases, adds six declaration agreements, and includes two supplemental response-policy regressions added during self-review. The supplemental cases prove a different declared limit parameter controls clipping and reported bounds. See green.log and green.rc.
- `baseline.py` plus `compare.py`: all 11 complete AnnotatedResult result/metadata snapshots are unchanged. Annual, quarter, unknown and mixed fiscal labels, empty/missing rows, mixed currencies, zero/negative values and clipping are represented. See comparison.log, baseline.json and baseline-green.json.
- `query_compare.py`: all 70 standard query boundary/default/alias/error outcomes match pre-change source loaded from the fork HEAD. Cases include None, booleans, zero, negative and endpoint counts, numeric strings/floats, unsafe/missing symbols, period aliases and TTM options. Error class/code and absent context also agree. See query-comparison.json and query-comparison.log. Fork HEAD during comparison: a78cb2039a55d080ab7630449a1e5b62745df4c5.
- The GREEN pytest/snapshot/query command sequence returned rc0. Existing aiohttp ClientSession inheritance deprecation warning remains.
- Owning lint: `verification/provider/.venv/bin/ruff check --config vendor/data-api/openbb_platform/providers/fmp/pyproject.toml --no-fix` on the three owned production files: rc0, all checks passed. See ruff.log.
- Project `tools.quality.python_units.measure_python` and whole-file physical counts: rc0. See counts.json. Parent owns the combined inventory gate.

| Production file | Physical | Logical | Maximum callable |
| --- | ---: | ---: | ---: |
| financial_ratios.py | 141 | 59 | 10 |
| financial_ratios_data.py | 358 | 78 | 3 |
| enterprise_values.py | 160 | 56 | 8 |

Requirements checked: 4.1, 4.2, 4.7, 6.1, 6.2. Design checked: Financial metadata contract; Discovery and generated consumer contracts; Financial failures and HTTP compatibility; approved financial-annotations amendment and canonical-native-name interface. Core product.md, tech.md and structure.md steering files are absent. Available complexity, testing, documentation, CI and delegation steering was read.

## Frozen source identities

SHA256 hashes after GREEN; full paths and interface/baseline hashes are in hashes.json.

| File | SHA256 |
| --- | --- |
| financial_ratios.py | 8A301B1DB8D14CF32D4A1722D46F45361C307E4B56FA91E6B76846A4918D1D25 |
| financial_ratios_data.py | 52EF1B0023D95978D1F5BBBB87311756A626D8E0B3F7F7E122F3817A961DA3CB |
| enterprise_values.py | 5E5E11B9679D915259D739B2DA2C9E547E44FBFB35F713E62E52F74894417004 |
| test_fmp_financial_ratios.py | CB89AEC5D28A741A30A46D41DF9946A0CC3E6E758EC25986C313CEB429629477 |
| test_enterprise_values.py | A016B7BC9F02536CF8451FCDA556B66F0EF1DCB0F6C60292F1FD6E09C1FED635 |

Only the assigned three production files and two focused test files were edited. No commits, task checkboxes, inventory, pins, core model/schema, router or shared helper changes were made. Edits are frozen. Independent financial review and controller acceptance remain pending; this evidence does not establish live-provider entitlement or native HTTP integration acceptance.
