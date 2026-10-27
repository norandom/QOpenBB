# Theme preview shared foundation

TP1 source support is accepted at Workspace `fd5c43e31570f177e3441539c2209e76118ba380`. The Theme Settings preview still uses its original renderer; replacement appearance, controls, persistence and publication are not accepted by this checkpoint.

The existing Pie legend layout now has a neutral item-based adapter. Optional preview interactions add roving legend focus and grouped-bar keyboard navigation through the existing ECharts lifecycle. The host still exposes only image export. Pie callers retain their existing policy and layout.

Independent review approved all 20 frozen source/test files. Five focused Vitest files pass 53 checks, including actual rendered bar bounds after hiding a series and resizing, real HTML tooltip contents during keyboard navigation, and stale/error/zero-size/disposal behavior. Read-only Biome passes for 15 production files. Actual-import baseline/current TypeScript diagnostics are identical at 31, with none introduced; application-wide typing is not claimed clean.

The combined size checker passes for all 15 changed production files: maximum 385 physical lines, 209 logical units and 31 units per function. It measured the live fork with an exact task inventory and accepted-root production snapshot, excluding unrelated local catalog edits. The inventory is 393 lines. No code-size exception was added.

The independent reviewer verified all frozen hashes and repeated the focused tests and lint. No browser, image build or publication was run for this source-only checkpoint. Next: [TP2 preview integration and TP3 application checks](../../../.kiro/specs/analyst-workspace/theme-preview-milestone.md).
