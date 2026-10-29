# Core annotation contract verification

2026-10-29. Task 1 is ready for independent review. No provider adoption or shared production edit was made. The interface is frozen in [interface.md](interface.md); controller acceptance, combined inventory gate and independent review remain pending.

## Scope and decisions

Added `financial_annotations.py` and focused root provider tests. Query and data declarations are typed class-owned values. Ordinary defaults, requiredness, choices and constraints remain on the actual models. Financial definitions come from Field descriptions at rendering. The template subclasses FinancialFieldMetadata only to allow an unresolved definition, then renders the original result type. This avoids duplicating financial vocabulary or descriptions.

All serialized static fields require templates; empty templates explicitly declare unknowns. References use serialization aliases, then aliases, then Python names and exclude non-emitted fields. Dynamic columns are runtime-owned additions. Runtime-property disclosures never replace static values or fabricate actual dates, units, availability, truncation or completeness.

Query clipping supports a fixed cap or a modeled integer count parameter; the latter retains the query's actual default and ordinary bounds. Income compatibility has no fake cap. Runtime consumers must read these same declarations during adoption.

## Verification

Using WSL Debian, Python 3.13.15 and the existing provider environment:

- Initial RED: missing module collection error, retained in red.log. The outer shell masked that initial return code; the captured error proves RED, not a successful run.
- Query clipping correction RED: 1 failed, 14 passed, exit 1; unsupported limit_parameter. Retained in correction-red.log.
- Static coverage correction RED: 1 failed, 15 passed, exit 1; missing static template was accepted. Retained in coverage-red.log.
- Final GREEN: 16 passed in 5.60s; Python subprocess return code 0, retained in green.log.
- Owning core Ruff: PASS with explicit configuration and --no-fix.
- Existing `tools.quality.python_units.measure_python`: 165 physical lines, 103 logical units, largest function 13; caps 400/300/50. Details in caps.json. Controller owns inventory/combined gate.

Focused command (PYTHONPATH contains core, FMP and FRED source directories):

```sh
verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_financial_annotations.py -n0 --maxprocesses=2
verification/provider/.venv/bin/ruff check --config vendor/data-api/openbb_platform/core/pyproject.toml --no-fix vendor/data-api/openbb_platform/core/openbb_core/provider/standard_models/financial_annotations.py
```

No installs, network calls, keys, provider imports or new dependencies. Existing aiohttp ClientSession inheritance deprecation warning remains. Missing product.md, tech.md and structure.md steering files were observed; existing relevant project steering and approved amendment/tasks were read. Runtime application/API integration is outside this task.

## Frozen source identities

Data fork base: `d8589764cfd03a4fca40cabd14de9620a194f0eb`.

| File | SHA256 |
| --- | --- |
| financial_annotations.py | 535ca76b732e5904231149a28f3dd9d4ff71a00a9d709d41781f18462b55702c |
| test_financial_annotations.py | aa9206432e0e0c55dbb769e42526ca78700824316452423efaba2f29fe103192 |
| interface.md | 1e97854eee8afb1258503c3a3f3bdd2313dbc53b67f50924e4d7ab57471af877 |

Production, tests and interface use LF and one terminal newline. Shared metadata/Data/registry/fetchers, unrelated renderer edits and controller inventory were preserved. No commits were made.
