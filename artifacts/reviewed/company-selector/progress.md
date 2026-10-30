# Company selector source progress

Tasks 1, 2, 3 and 4.1 are source-accepted on 2026-10-30. The owner approved the bounded design, tasks and implementation. The versioned company-selection contract now decodes saved metadata, identifies the eight eligible FMP widgets, preserves source-qualified listing identity and rejects known ambiguity. It introduces no widget UI or provider route.

Independent Astra review passed 49 focused tests, strict TypeScript, scoped Biome and the missing-scope regression. The new production module measures 200 physical lines, 190 logical units and a maximum 12 units per function. The scoped portable gate passed 80 files with no errors or violations. Existing exception files are byte-identical; only their source-revision binding moves with the accepted fork commit.

Search and group safety are now source-accepted; selection lifecycle and the paired UI follow. The selector is not shipped: lifecycle, controls, host integration and real-FMP browser/persistence acceptance remain open. No images were built or published for this foundation task.

See [independent review](task1-review.md), [source identity](source.json) and [task plan](../../../.kiro/specs/analyst-workspace/company-selector-tasks.md).

CI found premature inventory entries for the unchanged parameter host and group hook. The correction removes those two future targets until their integration tasks modify them; the contract remains maintained. The corrected full gate passed 673 maintained files, with zero errors or violations. [Independent correction review](task1-inventory-review.md) supersedes the initial scope conclusion. The initial CI run41063840201 failed; corrected CI is pending.

Task 3 adds the pure group guard: all current members must have compatible FMP source/bindings; preview and detached contexts cannot write a live group. Existing multi-symbol values can be explicitly replaced, and ungrouped local editing stays available. Independent Sol review passed 60 cases, strict TypeScript and Biome; production measures83 physical/67 logical/max27. The scoped portable gate passed80 files. The host must still supply actual fresh dashboard membership at integration. [Group review](task3-review.md).

The second CI attempt passed the full size gate and209 portable tests, but exposed an unsynchronized build-source policy. The policy now follows the same accepted Workspace revision as the source lock; its focused two-source regression passes. Corrected CI remains pending. This changes no runtime or build allowlist.

Task 2 adds connected-source name/ticker search with native result/provenance validation, distinct public financial errors, bounded per-selector TanStack caching, cancellation and source/authentication race protection. Independent Sol review passed35 focused cases and scoped Biome. Adapter size218 physical/79 logical/max14; hook198/99/max21; scoped combined gate81 files passed. [Search review](task2-review.md).

Full native TypeScript/build acceptance remains unverified: the reused local dependency cache cannot build the existing runtimeConfigSchema composite because of three pre-existing Zod type errors. The test uses the actual source-request helper with two unrelated chart-import mocks. No dependency or configuration changes were made; the three generated attempt outputs were removed. These focused source checks do not establish packaged integration.

CI on806a9f0 passed both Prototype41065288631 (210 portable tests) and CodeQL41065288531 after the source-policy correction. Current source progress is3/10; no selector UI or new image publication is claimed.

Task 4.1 adds the selection lifecycle: explicit current-result choices, same-symbol metadata-only updates, fresh compatible-group writes, saved-record validation and exact-symbol name resolution. Auto-resolution changes no financial symbol and never writes a group. Partial local-write failure stays unresolved through later blocked choices until actual reconciliation. The first Astra review found that guard could be downgraded; the focused repair passed independent Sol re-review after Astra was unavailable at capacity. [Lifecycle review](task4.1-review.md).

The current selection suite passes88 cases, including the original49 contract cases; these are not additive totals. Scoped Biome and the80-file portable gate pass, and new production size is307 physical/134 logical/max22. Current progress is4/10 source tasks; paired controls, host wiring, full native graph and real-data acceptance remain open.
