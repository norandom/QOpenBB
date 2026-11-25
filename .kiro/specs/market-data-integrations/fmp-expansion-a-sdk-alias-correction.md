# SDK supplied-value normalization correction

This bounded task 2.1 correction restores the approved `quarterly` to `quarter` behavior. It changes no financial schema, query bound, task count or live-request budget. The original Batch A design and explicit-route admission amendment remain unchanged; this document supersedes only the amendment's read-only restriction on `filters.py`. Independent architecture review is required before the production repair.

The [public-entry finding](../../../artifacts/reviewed/fmp-expansion-a/sdk-period-followup.md) applies to analyst estimates, both revenue-segment variants and all three growth variants. At API `0c544ace4d177cc6ff833619ad520bf806b90d91`, supplied validation accepts the alias but discards its normalized result. Native enum filtering then rejects the raw value before Container can normalize effective parameters. Independent diagnosis reproduced twelve canonical successes, twelve alias failures and twelve safe invalid-period rejections across explicit and omitted FMP selection.

## Bounded repair

Retain the existing supplied validation result only when validation succeeds. Store normalized canonical values only for financial fields actually supplied by the caller in the invocation-owned frame. Do not inject model defaults, replace raw membership, or validate the full query again at the filter boundary. Missing-only validation retains its existing deferred behavior with an empty normalization cache. All six periodic native signatures require symbol before filtering; nonperiodic configured-symbol behavior must remain unchanged.

Add one cohesive hook immediately before native filtering. It uses only the current owner-matched strict frame after pinned native selection, with matching provider and authoritative selected-query identity, before Container consumption. Pending, baseline and absent frames retain ordinary behavior. Invalid selected frame state fails safely. Copy parameter mappings before projecting cached supplied values; preserve controls, omitted fields, caller dictionaries and the raw snapshot used for defaults precedence. Clear the normalization cache after projection without consuming the admission frame. Original native enum and multiplicity filtering still runs. Clear the cache on baseline activation and all synchronous/asynchronous cleanup paths.

Omitted providers still resolve exactly once at the generated native resolver call. Explicit FMP remains identifiable before validation; unresolved omitted-provider pre-body failures retain native ordering without guessing a provider. No global normalization, native-validation bypass, parallel registry or runtime fixture dependency is introduced.

## Exclusive repair ownership

All paths below are in the API fork beneath `openbb_platform/core/openbb_core/`:

- `app/parameter_admission.py`: retain successful supplied normalization and project it into copied mappings.
- `app/static/utils/admission_context.py`: invocation-local normalization cache with existing owner and lifecycle checks.
- `app/static/utils/decorators.py`: clear the cache alongside existing raw-state cleanup.
- `app/static/utils/filters.py`: call the scoped projection before original native filtering.

Container, emitter, standards, routers, maps, Query and CommandRunner remain read-only for this repair. Root regression ownership is `tests/providers/test_fmp_parameter_admission.py`; controller ownership includes this correction, task notes, `.kiro/complexity/data-api.json`, acceptance metadata and reviewed evidence. The five frozen HTTP files belong to task 2.2 and must not be staged, edited or reverted by the repair.

The authoritative filter baseline is 91 physical lines, 42 logical units and 38 units for `filter_inputs`. All four changed files must pass whole-file 400/300/50 caps; no filter exception is proposed. Existing emitter exceptions remain restricted to identical bytes, metrics and positions, with actual-revision rebinding under their recorded approval.

## Required evidence before re-acceptance

Use actual generated SDK methods, native descriptors, Container/CommandRunner/Query and offline Fetchers. Cover all six periodic variants with explicit FMP and omitted selection resolving to FMP. Verify both `quarter` and `quarterly` reach the actual Fetcher as `quarter`, once, without changing caller data. Cover omitted period with annual schema defaults and configured quarter/quarterly; supplied quarter/quarterly must beat configured annual. Prove no omitted model defaults are inserted prematurely.

Retain safe zero-extraction rejection for invalid/null/unsupported periods, null/bool bounds, unknown fields and alias collisions. Preserve nonperiodic missing-only/configured-symbol behavior, explicit or omitted baseline-provider behavior, native filter checks and provider-mismatch rejection. Check normalization cleanup through nested calls, threads, async tasks, inherited child contexts, failures before/inside filtering and subsequent baseline calls. Frozen schemas remain unchanged.

Independent review, affected SDK/freeze regressions, exact source metrics and the combined executable scope gate must pass before task 2.1 is accepted again. Then resume task 2.2's frozen HTTP implementation and run its final regressions. Adapter fan-out remains gated by task 2.3. No live requests are required for this repair.
