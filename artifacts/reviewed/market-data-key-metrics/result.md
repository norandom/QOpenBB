# Periodic key metrics implementation

Task 2.7 restores the retained FMP key-metrics fields through the existing KeyMetrics/Fetcher contract. Independent review and controller acceptance are pending. Registration, installed API/widget behavior and live entitlement remain outside this source adapter result.

## Financial behavior

One symbol, annual/quarter reporting and the quarterly alias use a strict integer limit of 1 through 1000, default 5. TTM include/only modes fail before I/O; exclude remains a compatibility value. Only the periodic key-metrics endpoint is requested. No date, currency, fiscal year or fiscal period is fabricated. Signed, zero and null values remain unchanged, latest known dates sort first, duplicate dates retain source order and undated rows sort last. Observed local truncation is partial; otherwise completeness is unknown.

Metadata uses the acquisition receipt and field-specific currency, currency/share, fraction, multiple and days units. FY and Q1-Q4 labels determine the reporting basis; calculation windows and annualization remain unknown. Market-input dates and share-count/debt/cash/lease/minority-interest conventions are explicitly unknown. These are provider calculations, not house valuation outputs. Market cap/EV are not assigned an inferred market valuation date.

## Evidence

- Initial RED: `red.log` records the missing model collection failure before production creation, 16.66 seconds. The PowerShell/bash wrapper lost its exit variable; its return status is unreliable. This is observed collection-failure evidence, not a claimed captured pytest exit code.
- First GREEN: 22 tests passed in 10.99 seconds. `run.py` uses subprocess.run and saved the actual pytest return code 0 to `green.exit`.
- Final expanded GREEN: pending serialized run of 32 tests.
- Owning lint: `verification/provider/.venv/bin/python -m ruff check --config vendor/data-api/openbb_platform/providers/fmp/pyproject.toml --no-fix` with both production paths passed, exit 0.
- `measure.py` uses the maintained project-syntax-units-v1 checker. Whole files are 168 physical / 62 logical / 9 maximum callable for key_metrics.py and 210 / 52 / 4 for key_metrics_data.py. Both satisfy 400/300/50. Production and tests use LF with one terminal newline.

The focused pytest command, from WSL Debian repository root, is:

```sh
PYTHONPATH=vendor/data-api/openbb_platform/core:vendor/data-api/openbb_platform/providers/fmp:vendor/data-api/openbb_platform/providers/fred verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_fmp_key_metrics.py -n0 --maxprocesses=2
```

`run.py green-final` captures stdout and actual subprocess return status for the final invocation. Tests exercise invalid query bounds/symbols/TTM, annual/quarterly periods, values and units, nulls/missing metadata, stable duplicates, truncation, safe invalid rows, single periodic transport, spelling aliases and reporting/market-date basis. No installs, live requests or credentials were used.

## Sources and identities

Retained source: data-api revision `2232178fd8c`, key_metrics.py, adapted to current standard model. Current [FMP documentation](https://site.financialmodelingprep.com/developer/docs) supplies stable key spellings and sample financial categories. The [FMP FAQ](https://site.financialmodelingprep.com/faqs?code=marketPerformance) identifies Graham net-net as an amount divided by shares. Exact provider calculation windows and financial bases remain unknown rather than inferred from these samples.

Frozen production SHA-256:

- key_metrics.py: `ceb8dfb49a9f59a9080413baea0680cbc1a64dcd897be11b1ed3d7c9cb48463a`
- key_metrics_data.py: `3992a45dbd9d1dab22d627f6f047d2d8b735858c31a2abc648468c6fde594078`
- tests/providers/test_fmp_key_metrics.py: `e4458c8943b94e76430c17cf351462ea12a012167cf04e82bc2ae594d8edae4b`

No shared helpers, registration, locks, inventory or commits were changed. Controller owns inventory inclusion and final acceptance.

## Status Report
- STATUS: READY_FOR_REVIEW
- Final serialized verification completed: 33 tests passed in 10.63 seconds, actual subprocess exit 0. Controller finalized this record after the worker model reached capacity during reporting; source and verification files were already complete.

Independent review requested extra=ignore and modeled-field limitation; the final source includes both and a regression. Owning FMP Ruff passed after these edits. Earlier hashes/counts in intermediate logs are historical; the frozen identities above are authoritative.
