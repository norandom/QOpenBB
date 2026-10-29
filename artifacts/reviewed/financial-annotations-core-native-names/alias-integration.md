# Native output names require a bounded contract correction

2026-10-29. Do not accept the key-metrics alias remapping workaround. Native OpenBB emits Python field names for this route, while the annotation binder and proposed projection currently assume alias serialization. Preserve the original isolated core review; this is new integration evidence requiring a small core/projection correction before adoption acceptance.

## Evidence

- `openbb_core/provider/abstract/data.py:77` configures separate generated validation and serialization aliases. The two explicit FMP fields override that generator: `ev_to_ebitda` has alias and serialization_alias `evToEBITDA`; `net_debt_to_ebitda` has both `netDebtToEBITDA`.
- `openbb_core/app/router.py:143` explicitly defaults `response_model_by_alias` to `False`. The `KeyMetrics` command in `extensions/equity/openbb_equity/fundamental/fundamental_router.py:278` does not override it.
- `openbb_core/api/router/commands.py` retains those APIRoutes when installing command wrappers. Its ordinary response path returns validated output for FastAPI serialization; results-only serialization also calls `model_dump` without enabling aliases.
- A read-only probe against actual FMPKeyMetricsData confirmed `model_dump(by_alias=False)` and `model_json_schema(mode="serialization", by_alias=False)` use `ev_to_ebitda` and `net_debt_to_ebitda`. With `True`, both use `evToEBITDA` and `netDebtToEBITDA`.
- The current projection `_model_schema` explicitly uses `by_alias=True`. The current annotations likewise use the camel-case keys. The worker's conversion back to Python names preserves runtime metadata but leaves projected fields/row schema inconsistent with actual native rows.

The probe's final attempted template rendering failed because a current, actively edited model field lacks a description. Its process exit was 1; the alias observations above preceded that failure. This is not represented as a passing suite. No heavy suite, application startup, network call or source edit was performed.

## Recommended minimum correction

Keep `bind_query_annotation(model)`, `bind_data_annotation(model)` and `render_field_templates(model)` signatures unchanged. Define class-owned template keys and references as canonical Python field names, excluding fields declared `exclude=True`. Validate these names directly against `model_fields`; input aliases remain input concerns. Render the same canonical keys. This preserves accepted runtime metadata and the native false-alias row contract without a route-dependent ClassVar declaration.

Projection must inspect the actual route's `response_model_by_alias`. For supported native routes with `False`, generate serialization schemas with `by_alias=False` and use canonical rendered templates. Explicitly reject `True` with `InvalidFinancialAnnotation` before publication in this bounded slice; none of the approved native operations inspected requires it. Supporting a true-alias route later requires an explicit projected-name mapping for keys and references, with the runtime metadata relationship tested. Do not silently assume a mode or change provider aliases to hide the mismatch.

Required regressions: an actual-style model with canonical declaration `ev_to_ebitda` and input/serialization alias `evToEBITDA` binds and renders canonical metadata; false-mode serialization and schema agree with those names; alias-only declarations and references fail; excluded-field references fail; projection reads a false route flag and agrees with real metrics; a true flag fails explicitly. Remove the provider workaround that converts alias-keyed templates back to canonical names after the core correction.

This correction changes declaration ownership to match existing public behavior. It does not authorize changing rows, response aliases, accepted metadata, shared Data configuration or the native route defaults.
