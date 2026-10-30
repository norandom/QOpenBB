# Company selector source progress

Task 1 is source-accepted on 2026-10-30. The owner approved the bounded design, tasks and implementation. The versioned company-selection contract now decodes saved metadata, identifies the eight eligible FMP widgets, preserves source-qualified listing identity and rejects known ambiguity. It introduces no widget UI or provider route.

Independent Astra review passed 49 focused tests, strict TypeScript, scoped Biome and the missing-scope regression. The new production module measures 200 physical lines, 190 logical units and a maximum 12 units per function. The scoped portable gate passed 80 files with no errors or violations. Existing exception files are byte-identical; only their source-revision binding moves with the accepted fork commit.

The two downstream search and group-safety tasks can now use the frozen interfaces. The selector is not shipped: lifecycle, controls, host integration and real-FMP browser/persistence acceptance remain open. No images were built or published for this foundation task.

See [independent review](task1-review.md), [source identity](source.json) and [task plan](../../../.kiro/specs/analyst-workspace/company-selector-tasks.md).
