# Financial OpenAPI projection prerequisite assessment

Task 4.1 cannot yet produce the approved authoritative projection from the installed declarations. Required financial sidecar semantics remain in adapter runtime helpers rather than query/data schema extras or class metadata. The controller must repair that upstream contract before this task can claim completion.

## Status Report

- STATUS: BLOCKED
- Date: 2026-10-29
- Scope: market-data-integrations task 4.1 only.
- Root revision inspected: `8e29a9b5d274463171aadad753d851c9f7cc7ce4`.
- Data fork revision inspected: `4bef44cd5622f834df0b9afdb20c0d1f1183f013`.
- Production changes: none. Tests added or executed: none. No RED/GREEN claim.
- Complexity: no production changes to measure; 400 physical lines/file, 300 logical syntax units/file and 50/function remain the implementation gate.
- Review: independent financial/architecture review pending; no acceptance claimed.

## Evidence and consequence

The approved design requires `x-qopenbb-financial` extensions and metadata schema components to come from the query/data declarations used by fetchers. It explicitly prohibits a handwritten parallel financial schema registry.

- `FMPKeyMetricsQueryParams.limit` already declares 1-1000 and default five; these constraints can be projected directly.
- `FMPKeyMetricsData` does not carry the full financial field metadata. Currency categories, fraction units, financial bases and limitations live in `key_metrics.py` module constants and `_fields`/`_metadata` helpers. Reading a field name or docstring cannot establish those semantics safely.
- `FMPEquityHistoricalQueryParams.calendar_window` enforces the five-calendar-year rule procedurally. The returned-row cap of 5000 is also runtime logic, rather than projection-safe schema/class metadata.
- The financial sidecar guarantee and baseline versus explicit-provider selection policy have no common approved declaration annotation that the projection can consume. Unknown annotations must remain unknown; inventing replacements in this module would introduce the prohibited second registry.

Installed associations are available: `RegistryMap.original_models` supplies standard model to provider to query/data classes, and installed routes carry `openapi_extra['model']`. The blocker concerns declarative semantics, not inability to resolve those associations.

The existing typed `FinancialResultMetadata` can generate a reusable schema component. Its response location is `OBBject.extra.results_metadata.__qopenbb_financial__`. A schema reference in an operation extension would document that location; it would not make unrestricted `extra` enforce that schema. Fetcher and envelope validation remain separate acceptance evidence.

## Reproduction

Read-only inspection used PowerShell `Get-Content` and `rg -n` against the approved specification, `RegistryMap`, route association code and the accepted FMP/FRED query/data modules. `git rev-parse HEAD`, `git -C vendor/data-api rev-parse HEAD` and `Get-FileHash -Algorithm SHA256` identified the inspected sources. Successful inspection commands returned zero; two early discovery commands reported a PowerShell brace-expression parse error and absent paths respectively, corrected by explicit paths. Missing default steering files `product.md`, `tech.md` and `structure.md` were reported to the controller; available complexity/testing/documentation/delegation guidance was read.

| Source relative to data fork | SHA-256 |
| --- | --- |
| `openbb_platform/providers/fmp/openbb_fmp/models/key_metrics.py` | `ceb8dfb49a9f59a9080413baea0680cbc1a64dcd897be11b1ed3d7c9cb48463a` |
| `openbb_platform/providers/fmp/openbb_fmp/models/equity_historical.py` | `a9d43baaba1cf04fa32b6ea0ed081759d3bbc0f957318feabe00e653b237af42` |
| `openbb_platform/core/openbb_core/provider/registry_map.py` | `521432dee0bffd49cdf657f6c89be0171b8686237008b75d6a0c7487bfb149d9` |

## Required next action

The controller should route a bounded declaration-contract repair to the upstream metadata/adapter owner, preserving accepted runtime values and compatibility. Freeze its annotation shape and verification before redispatching task 4.1. Alternatively, explicitly authorize a partial projection that exposes absent annotations as unknown; that draft would still leave full task acceptance open.

After repair, write fixture tests before production code, request the serialized pytest slot, and verify deterministic/idempotent nonmutating projection, installed associations, resolvable schema references, query/provider semantics, the actual nested metadata location and structural safe response contracts for 422/400/502/204/500. Runtime error sanitization and provider guards require their owning task's separate tests.
