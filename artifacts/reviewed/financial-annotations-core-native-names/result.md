# Native-name annotation correction

2026-10-29. Ready for independent review. Core declarations now use canonical Python field names, matching the native response alias flag. [The corrected interface](interface.md) supersedes the earlier alias-first wording. This bounded correction changes no provider input aliases, runtime output rows or public binding signatures.

## Evidence

Authority: `vendor/data-api/openbb_platform/core/openbb_core/app/router.py:143` defaults response_model_by_alias to False. The previous helper instead selected serialization_alias/alias, which rejected native metadata field names during actual adoption. `_canonical_fields` now selects model_fields names and excludes Field(exclude=True).

Tests were edited before production. Native-false rendering and aliased query clipping failed in RED: 2 failed, 19 passed, exit 1, 10.72s (red.log). Existing 16 cases were retained with canonical fixture keys; five cases add native row/output agreement, alias-only key/reference rejection, excluded-field rejection and canonical query-limit references.

Final focused GREEN: 21 passed, 4.83s; captured Python subprocess return code 0 (green.log). Explicit owning core Ruff --no-fix passed. Existing executable Python metric: 162 physical / 100 logical / 13 largest function, below 400/300/50 (caps.json). Source/tests/interface use LF with one terminal newline.

Commands run under WSL Debian from the project root, with source PYTHONPATH for core/FMP/FRED:

```sh
verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_financial_annotations.py -n0 --maxprocesses=2
verification/provider/.venv/bin/ruff check --config vendor/data-api/openbb_platform/core/pyproject.toml --no-fix vendor/data-api/openbb_platform/core/openbb_core/provider/standard_models/financial_annotations.py
```

No commits, pins, inventory updates, installs or live calls. Other workers' model/projection changes remain untouched. Combined inventory acceptance and Astra review remain controller-owned. The aiohttp inheritance deprecation warning is unchanged.

## Frozen SHA256

| File | SHA256 |
| --- | --- |
| financial_annotations.py | 08c93215756303d7a6644049314776d8a7616507cc827785f12cb68d8ecffde8 |
| test_financial_annotations.py | ef94bce00e4d131796b23934f1d87744a92d1227ab8f4d7d94d7d396a88acfbd |
| interface.md | 8100e7b7c18b5cf647c1ddd8d454c3b79e4706824de3978ddcccd08fd3c99ded |
