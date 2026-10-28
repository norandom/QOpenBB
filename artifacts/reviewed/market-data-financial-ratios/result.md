## Status Report
- STATUS: READY_FOR_REVIEW

Task 2.8 restores periodic FMP ratios with provider calculations, explicit field units and safe pre-I/O validation. Controller acceptance and registration are pending.

The adapter accepts one symbol, annual/quarter and quarterly alias, strict integer limits 1-1000 defaulting to five. It rejects TTM include/only, retains periodic exclude compatibility, and never calls ratios-ttm. Signed, zero and null values remain unchanged. The model retains upstream field names and verified stable aliases, adds current diluted P/E and dividend yield percentage fields, and accepts legacy calendarYear without inventing a year.

Units distinguish fractions, multiples, percentage points and currency/share. Dividend yield fraction and percentage remain distinct. The current ratios endpoint declares no day quantities. Reporting basis follows actual FY/Q labels; unknown/mixed labels remain unknown. Calculation observation/valuation dates remain unknown because fiscal period ending does not establish the market date or calculation window. Financial basis conventions remain explicitly unknown. This imports provider calculations rather than validating a house model.

Source reference: [FMP periodic ratios documentation](https://site.financialmodelingprep.com/developer/docs/stable/metrics-ratios), inspected 2026-10-28. Retained declarations recovered from data-api revision 9f0d5928392. Exact accounting, averaging and PEG growth conventions are not established by the public response example.

### Verification

- Actual RED: missing financial_ratios module, captured before production creation in red.log. Shell wrapper returned 1; pytest collection error is direct evidence, not a claimed clean assertion failure.
- Final focused suite: 29 passed in 11.48s, no skips, subprocess returncode 0. One upstream aiohttp inheritance deprecation warning.
- Owning provider Ruff: all checks passed, command chain exit 0; initial import-order findings repaired manually.
- Whole-file project-syntax-units-v1: financial_ratios.py 176 physical / 61 logical / maximum callable 18; financial_ratios_data.py 270 / 74 / 3. Measured using tools.quality.python_units.measure_python; tests excluded. Controller owns combined inventory gate.
- LF, one terminal newline, no blank EOF: PASS.
- Synthetic tests only. No live API, keys, installations, provider registration, shared helper edits or commits.

Commands from WSL Debian, /mnt/d/Source/QOpenBB:

```sh
PYTHONPATH=vendor/data-api/openbb_platform/core:vendor/data-api/openbb_platform/providers/fmp:vendor/data-api/openbb_platform/providers/fred verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_fmp_financial_ratios.py -n0 --maxprocesses=2
verification/provider/.venv/bin/ruff check --config vendor/data-api/openbb_platform/providers/fmp/pyproject.toml --no-fix vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/financial_ratios.py vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/financial_ratios_data.py
```

The final pytest subprocess command/returncode is recorded in green-status.json through run.py; stdout is green.log. Unknown provider completeness remains unknown unless observed clipping proves partial coverage. Stable newest-first sorting retains duplicate order before limiting.

### Frozen source hashes (SHA-256)

- vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/financial_ratios.py: `731ebd6fd7eb418ca8b5d5ed44d1c64640dd4fa8c7dee6ee6df98e5e5405550b`
- vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/financial_ratios_data.py: `befc340f9625dff50f1a9fdfecbe8303374fb062e619c3483858c5482b171455`
- tests/providers/test_fmp_financial_ratios.py: `2cdf60cffa064e7cded66818582a1d3136f19bc1681b862f24057653a781c6e6`

### Verification Result

- STATUS: VERIFIED
- CLAIM_TYPE: TEST_OR_BUILD
- CLAIM: Frozen task-local tests and owning-provider lint pass.
- EVIDENCE: Final 29-case pytest subprocess exit 0; final owning Ruff PASS; source hashes unchanged.
- GAPS: Independent reviewer/controller acceptance, combined inventory gate and live entitlement remain outside this worker claim.
