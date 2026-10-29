# FRED declaration repair ready for independent review

Task 4.6 adds typed query/data ClassVars to the generic FRED series model. Query selection stays baseline_default and response bounds stay provider-owned. The static date coordinate renders its existing Field definition. Dynamically named quantities resolve through the existing financial metadata location; units, frequency, transformations, availability and vintage facts remain runtime-owned. No date quantity is added to result metadata.

Only series.py and its existing focused metadata test file changed. All runtime function ASTs are identical to the accepted baseline. No cache/rate limiter, shared core, inventory, pin, source registration or task checkbox changed. Independent review and controller acceptance remain pending.

## Verification

The owning criteria are requirements 4.1, 4.4, 4.8, 6.1, 6.2 and 7.5; design sections Financial metadata contract, FRED compatibility and acquisition provenance, Discovery and generated consumer contracts; and the approved financial-annotations amendment.

- RED: the assigned pytest command collected 18 cases: both added cases failed with MissingFinancialAnnotation and all 16 existing cases passed. Logs: red.log and red-receipt.log. A shell interpolation error masked the first wrapper status as 0 and made the second wrapper exit 2; neither is claimed as the actual pytest child status. The pytest RED failures themselves are explicit. The redundant receipt run had already started when the controller instructed against another RED run.
- GREEN: `wsl -d Debian --cd /mnt/d/Source/QOpenBB --exec verification/provider/.venv/bin/python artifacts/annotations-fred/verify.py green`. The runner uses source PYTHONPATH and executes `python -m pytest -c verification/provider/pyproject.toml tests/providers/test_fred_series_metadata.py -n0 --maxprocesses=2`. Actual subprocess child code 0; 18 passed in 14.53 seconds; one existing aiohttp ClientSession deprecation warning. Receipts: green.log and green.rc.
- Baseline: source-PYTHONPATH provider Python ran compare.py, exit 0. All 36 full result-row/metadata envelopes matched accepted baseline source across nine transform choices and native/annual avg/sum/eop options. comparison.json retains baseline and output hashes. The fixture exercises wide GDP/CPIAUCSL rows, missing observations, oldest acquisition time and observation provenance without live requests.
- Owning Ruff: provider environment `ruff check --config vendor/data-api/openbb_platform/providers/fred/pyproject.toml --no-fix vendor/data-api/openbb_platform/providers/fred/openbb_fred/models/series.py`, exit 0, all checks passed.
- Whole-file project checker: tools.quality.python_units.measure_python, exit 0: 334 physical lines, 88 logical units, maximum callable 22; limits 400/300/50. caps.json contains all callable counts. No companion extraction required. The controller owns combined inventory acceptance.

## Frozen source hashes

- series.py SHA256: af040a3fc7c92d38b1b3fe3a09319b363cbe91689a864f0840d4ab77ae0bfced
- test_fred_series_metadata.py SHA256: 8e1dd4a5ad88403bcc70db2f908183a40560043c14e76736d0ba464ea666c4ba
- Accepted baseline source SHA256: e7bf6e4a5edf560f094e059d3af77da637acc841371dcfa79e35e2c0c73e6b25

No installed runtime, live provider, cache implementation, browser or image acceptance is claimed.

## Status Report
- STATUS: READY_FOR_REVIEW
- TASK: 4.6
- TASK_BRIEF: Declare dynamic FRED semantics while preserving all existing quantities, dates, provenance and baseline policy.
- FILES_CHANGED: vendor/data-api/openbb_platform/providers/fred/openbb_fred/models/series.py; tests/providers/test_fred_series_metadata.py
- REQUIREMENTS_CHECKED: 4.1, 4.4, 4.8, 6.1, 6.2, 7.5
- DESIGN_CHECKED: Financial metadata contract; FRED compatibility and acquisition provenance; Discovery and generated consumer contracts; approved financial-annotations amendment.
- RED_PHASE_OUTPUT: 2 MissingFinancialAnnotation failures and 16 existing passes before declarations; actual pytest child status was not captured by the faulty shell wrapper.
- TESTS_RUN: 18 passed, actual child code 0; 36 full-output baseline comparisons code 0; owning FRED Ruff code 0; whole-file caps code 0.
- CONCERNS: Independent review and controller acceptance pending; RED shell status limitation is recorded explicitly.
- EVIDENCE: green.log, green.rc, comparison.json, caps.json; class declarations and focused static/dynamic agreement tests.
