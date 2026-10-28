# Periodic metrics and ratios source review

Tasks 2.7 and 2.8 are approved after two bounded repairs. This is source-adapter acceptance; controller inventory integration, provider registration, installed API/widget behavior, live entitlement and real-provider acceptance remain separate gates.

Independent review on 2026-10-28 used `.agents/skills/kiro-review/SKILL.md`, the approved market-data-integrations requirements/design/tasks and complexity/testing/documentation steering. The configured product/tech/structure steering files are absent. Git showed four new untracked model files, so their complete contents and both tests were read directly. No shared helper or registration changes belong to this review.

## Review Verdict
- VERDICT: APPROVED
- TASK: 2.7
- MECHANICAL_RESULTS:
  - Tests: PASS. Independent combined run below: 62 passed, zero skipped, subprocess exit 0, 10.61 seconds; 33 cases exercise key metrics.
  - TBD/TODO grep: CLEAN across scoped production files.
  - Secrets review: CLEAN; transport receives credentials at runtime, fixtures contain synthetic placeholders only.
  - Static checks: PASS, owning FMP Ruff with explicit configuration and `--no-fix`, exit 0.
  - Boundary: WITHIN key_metrics.py, key_metrics_data.py and scoped test.
  - Boundary audit: CLEAN; existing standard model, Fetcher, acquisition and financial metadata contracts reused.
  - RED phase: VERIFIED actual missing-module collection error captured before production existed. Original wrapper exit status is unreliable; this is observed collection failure, not a claimed assertion-level RED.
  - Caps: PASS. Adapter 168 physical / 62 logical / 9 maximum callable; declarations 210 / 52 / 4 against 400/300/50.
- FINDINGS:
  1. Resolved Important: inherited `extra=allow` could emit quantities absent field metadata, violating requirement 4.2 and task 2.7. Explicit `extra=ignore`, modeled-field limitation and an unknown-amount regression now constrain emitted data to described fields.
  2. No remaining blocking findings. Actual fiscal labels, signed/zero/null values, R&D spelling compatibility, FCFE/FCFF currency amounts, Graham per-share units, day quantities and explicit unknown market/calculation bases are retained without house calculations.
- REMEDIATION: None.
- SUMMARY: Periodic metrics meet the bounded source contract and preserve unknown conventions without TTM fabrication.

## Review Verdict
- VERDICT: APPROVED
- TASK: 2.8
- MECHANICAL_RESULTS:
  - Tests: PASS. Same independent combined run: 29 cases exercise financial ratios.
  - TBD/TODO grep: CLEAN across scoped production files.
  - Secrets review: CLEAN; no actual credentials in scoped code or synthetic tests.
  - Static checks: PASS, same owning FMP Ruff invocation, exit 0.
  - Boundary: WITHIN financial_ratios.py, financial_ratios_data.py and scoped test.
  - Boundary audit: CLEAN; no local valuation engine or shared registration mutation.
  - RED phase: VERIFIED actual missing-module collection error captured before production existed; wrapper outcome is not substituted for pytest evidence.
  - Caps: PASS. Adapter 176 physical / 61 logical / 18 maximum callable; declarations 270 / 74 / 3.
- FINDINGS:
  1. Resolved Important: computed valuation fields previously used fiscal period ending as their observation date despite an unknown market date (requirements 4.1/4.7). Calculated field observation dates are now null, identity period basis is null, and limitations distinguish fiscal labels from calculation windows and annualization. Focused assertions verify these semantics.
  2. Controller-noted solvency classification is corrected to fraction; explicit multiple categories and coverage assertion cover every modeled financial field. Dividend yield fraction and dividend yield percentage remain separate without rescaling.
  3. No remaining blocking findings. Missing dates produce a safe invalid-response error; missing currency/year/period and financial values are retained without fabrication.
- REMEDIATION: None.
- SUMMARY: Periodic ratios meet the bounded source contract with distinct units and unknown valuation dates.

## Reproduction and source identity

`review_checks.py` ran hidden in WSL Debian from the repository root, without installs or live requests. `mechanical.json` records exact commands, subprocess return codes, whole-file checker measurements and all six SHA-256 identities; `pytest.log` and `ruff.log` retain outputs. The only test warning is the existing aiohttp ClientSession inheritance deprecation.

```sh
PYTHONPATH=vendor/data-api/openbb_platform/core:vendor/data-api/openbb_platform/providers/fmp:vendor/data-api/openbb_platform/providers/fred verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_fmp_key_metrics.py tests/providers/test_fmp_financial_ratios.py -n0 --maxprocesses=2
verification/provider/.venv/bin/python -m ruff check --config vendor/data-api/openbb_platform/providers/fmp/pyproject.toml --no-fix vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/key_metrics.py vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/key_metrics_data.py vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/financial_ratios.py vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/financial_ratios_data.py
```

| File | Reviewed SHA-256 |
| --- | --- |
| key_metrics.py | ceb8dfb49a9f59a9080413baea0680cbc1a64dcd897be11b1ed3d7c9cb48463a |
| key_metrics_data.py | 3992a45dbd9d1dab22d627f6f047d2d8b735858c31a2abc648468c6fde594078 |
| financial_ratios.py | 731ebd6fd7eb418ca8b5d5ed44d1c64640dd4fa8c7dee6ee6df98e5e5405550b |
| financial_ratios_data.py | befc340f9625dff50f1a9fdfecbe8303374fb062e619c3483858c5482b171455 |
| test_fmp_key_metrics.py | e4458c8943b94e76430c17cf351462ea12a012167cf04e82bc2ae594d8edae4b |
| test_fmp_financial_ratios.py | 2cdf60cffa064e7cded66818582a1d3136f19bc1681b862f24057653a781c6e6 |

These identities match the final worker reports. Requirements 2.1, 4.2, 4.3, 4.5, 4.6 and 4.7 and the design's FMP/financial-metadata contracts were assessed within their task boundaries. Both adapters use one symbol, annual/quarter/quarterly alias, strict limits 1-1000 default five, explicit unsupported TTM rejection, actual acquisition timestamps, deterministic stable duplicates and honest partial/unknown completeness.

Public [key-metrics documentation](https://site.financialmodelingprep.com/developer/docs/stable/key-metrics) and [ratios documentation](https://site.financialmodelingprep.com/developer/docs/stable/metrics-ratios) confirm endpoint identities; they do not establish live account access or every calculation window. Provider calculations are not independently validated house-model outputs. The controller's combined inventory gate remains required before final acceptance.
