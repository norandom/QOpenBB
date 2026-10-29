# Profile declarations ready for independent review

Repair task 4.3 moves static units, scales, row-currency references and value origins into FMPEquityProfileData.financial_data_annotation. FMPEquityProfileQueryParams declares baseline_default provider selection and provider response policy. _profile_metadata renders independent copies and fills only actual availability; the complete metadata envelope remains unchanged. Ordinary symbol requiredness and multi-symbol schema stay on the query model. All input aliases and typed_errors=False transport behavior are preserved.

The new agreement test covers every emitted canonical model field, all eight measured field categories, mixed USD/GBP rows, unknown quote observation/valuation dates despite a financial date, complete per-field metadata equality and independent rendering. Existing installed-route, ordering, normalization, null/range and transport assertions remain.

## Verification

WSL Debian, /mnt/d/Source/QOpenBB. PYTHONPATH points to owned core, FMP and FRED source directories. No installs, builds, live-provider requests or browser processes ran.

- RED before production edits: 13 tests collected; 12 passed and the new agreement test failed MissingFinancialAnnotation. red.log retains output. The initial shell wrapper incorrectly surfaced outer exit0, so red-receipt.log and red-receipt.rc retain a selected declaration-test repeat with actual pytest child rc1 (1 failed,12 deselected). This extra repeat was unnecessary and overlapped the controller handoff; subsequent verification waited for the controller slot.
- GREEN: verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_profile.py -n0 --maxprocesses=2; 13 passed, actual pytest child rc0 recorded by run_tests.py in green.rc. One existing aiohttp ClientSession inheritance deprecation warning remains.
- Complete baseline comparison: baseline.py captured full AnnotatedResult rows and metadata before production edits for single, multiple, partial, empty and mixed-currency scenarios. compare.py compared all five after the change: unchanged, child rc0. comparison.log, baseline.json, baseline-green.json and baseline-green.rc retain evidence.
- Owning lint: verification/provider/.venv/bin/ruff check --config vendor/data-api/openbb_platform/providers/fmp/pyproject.toml --no-fix vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/equity_profile.py; pass after correcting import order. ruff.log retains output.
- Project measure_python checker: equity_profile.py has 308 physical lines, 97 logical units, maximum callable 14; within 400/300/50. counts.json retains callable details. Parent owns the combined scope/inventory acceptance gate.

Requirements checked: 4.1, 4.2, 5.2, 6.1, 6.2, 6.3. Design checked: Financial metadata contract; Discovery and generated consumer contracts; Financial failures and HTTP compatibility; approved financial-annotations amendment. The requested core steering files product.md, tech.md and structure.md are absent; this did not require invented substitute guidance. Complexity, testing, documentation, CI and delegation steering were read.

## Frozen source identities

SHA256, source bytes frozen after GREEN:

| File | SHA256 |
| --- | --- |
| vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/equity_profile.py | 49266456FE1080D2D92806468649B479656BD382E5495D4B46D3811B37903DFA |
| tests/providers/test_profile.py | 48DD382D229AC5C582E64723D24834692EB91E25A9F1D4BC446D47ECBE6FFEAC |
| baseline.json | D4A9A6E04E30594F1B47698E8858B5DBF0FFA3254872F8DECA34680AC89004BE |
| artifacts/reviewed/financial-annotations-core-native-names/interface.md | 8100E7B7C18B5CF647C1DDD8D454C3B79E4706824DE3978DDCCCD08FD3C99DED |
| vendor/data-api/openbb_platform/core/openbb_core/provider/standard_models/financial_annotations.py | 08C93215756303D7A6644049314776D8A7616507CC827785F12CB68D8ECFFDE8 |

Source changes are limited to the two assigned files. No commits, tasks checkboxes, inventory, source pins, shared helpers or core modules were changed. Edits are frozen for independent review; controller acceptance remains separate.
