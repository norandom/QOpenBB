# FRED generic-series metadata: ready for independent review

Task 3.3 preserves the legacy series map and wide results while adding validated financial metadata. Source units/frequency remain separate from requested transform, aggregation and effective measure. Real-time intervals survive pivoting, without implying point-in-time safety or supported vintage queries. Retrieval time is the oldest observation/series-metadata acquisition across every requested series.

Requirements checked: 3.5, 4.1, 4.4, 4.6, 4.8, 5.6, 6.3, 7.5. Design: FinancialResultMetadata contract; FRED compatibility and acquisition provenance. Files frozen in frozen-hashes.json; no commits or shared-contract edits by this worker. Legacy test_fred.py is unchanged.

Verification, WSL Debian, Python 3.13.15:

- RED: 9 failed before implementation (red.log), including missing financial metadata, incomplete intervals dropping rows, reserved identifier accepted.
- GREEN: 21 passed in 25.85s, one existing aiohttp ClientSession deprecation warning (green.log). Command: `PYTHONPATH=vendor/data-api/openbb_platform/core:vendor/data-api/openbb_platform/providers/fred verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_fred_series_metadata.py tests/providers/test_fred.py -n0 --maxprocesses=2`.
- Owning-provider lint: `verification/provider/.venv/bin/ruff check --config vendor/data-api/openbb_platform/providers/fred/pyproject.toml --no-fix vendor/data-api/openbb_platform/providers/fred/openbb_fred/models/series.py`: PASS (ruff.log).
- Whole-file project-syntax-units-v1 check: 308 physical lines, 85 logical units, maximum function 22 (complexity.json). Parent owns combined gate/inventory update.

Coverage includes mixed-age memory/disk component fixtures, multi-series identity, zero/missing values, absent interval endpoint, untouched legacy metadata, source/effective level and percent-change semantics, all remaining transform options explicitly unknown, three aggregation methods, date/limit propagation, unequal-date alignment without interpolation, reserved namespace rejection before I/O, and the existing public route/error regressions.

Limits: synthetic acceptance only; no live FRED calls, installation, build or entitlement assertion. Only level, pch and pc1 effective units are established; other supported options remain accepted with explicit unknown-unit limitations. Core product.md, tech.md and structure.md steering files are absent; relevant available policies and approved spec were read. Parent independent review and acceptance remain pending.
