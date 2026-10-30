# Company selector source progress

Tasks 1 and 3 are source-accepted on 2026-10-30. The owner approved the bounded design, tasks and implementation. The versioned company-selection contract now decodes saved metadata, identifies the eight eligible FMP widgets, preserves source-qualified listing identity and rejects known ambiguity. It introduces no widget UI or provider route.

Independent Astra review passed 49 focused tests, strict TypeScript, scoped Biome and the missing-scope regression. The new production module measures 200 physical lines, 190 logical units and a maximum 12 units per function. The scoped portable gate passed 80 files with no errors or violations. Existing exception files are byte-identical; only their source-revision binding moves with the accepted fork commit.

The search task uses the frozen interfaces; group safety is now source-accepted. The selector is not shipped: lifecycle, controls, host integration and real-FMP browser/persistence acceptance remain open. No images were built or published for this foundation task.

See [independent review](task1-review.md), [source identity](source.json) and [task plan](../../../.kiro/specs/analyst-workspace/company-selector-tasks.md).

CI found premature inventory entries for the unchanged parameter host and group hook. The correction removes those two future targets until their integration tasks modify them; the contract remains maintained. The corrected full gate passed 673 maintained files, with zero errors or violations. [Independent correction review](task1-inventory-review.md) supersedes the initial scope conclusion. The initial CI run41063840201 failed; corrected CI is pending.

Task 3 adds the pure group guard: all current members must have compatible FMP source/bindings; preview and detached contexts cannot write a live group. Existing multi-symbol values can be explicitly replaced, and ungrouped local editing stays available. Independent Sol review passed 60 cases, strict TypeScript and Biome; production measures83 physical/67 logical/max27. The scoped portable gate passed80 files. The host must still supply actual fresh dashboard membership at integration. [Group review](task3-review.md).

The second CI attempt passed the full size gate and209 portable tests, but exposed an unsynchronized build-source policy. The policy now follows the same accepted Workspace revision as the source lock; its focused two-source regression passes. Corrected CI remains pending. This changes no runtime or build allowlist.
