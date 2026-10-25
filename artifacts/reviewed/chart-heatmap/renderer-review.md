# HM2c independent renderer review

**APPROVED** for the inactive renderer slice after local remediation. This does not accept application routing, browser typography, all-missing native parity, public-grid undefined admission or HM3/HM4 delivery.

Reviewed 2026-10-25 using `kiro-review`, against [the renderer design](../../../.kiro/specs/analyst-workspace/heatmap-renderer-design.md), accepted HM1 matrix semantics and frozen `application/heatmapTypes.ts`. Its SHA-256 remains `729ba59722dfae0bc315219aef8ce3f2c81edbc9ade32c572e0f185261f94bb1`. All five reviewed source/test files match `artifacts/chart-heatmap/hm2c/frozen-hashes.json`.

## Mechanical evidence

- Independent focused run: `vitest run tests/unit/chart-compatibility/heatmapRenderer.test.ts tests/unit/chart-compatibility/heatmapData.test.ts --maxWorkers=1`, through the existing Node 24.22.0 WSL toolchain, **exit 0: 12 renderer + 8 data tests**. Exact output: `artifacts/chart-heatmap/hm2c/reviewer-green.log`. Actual ECharts SVG SSR is exercised, including signed/zero labels, constant paint, no-series text and transparent missing borders; it uses the existing canvas measurement mock and does not establish real-browser typography.
- Exact-file Biome check: five files, no fixes, exit 0; `artifacts/chart-heatmap/hm2c/lint-final.log`.
- Final baseline-relative TypeScript: 44 baseline/44 candidate inherited diagnostics, zero added or owned diagnostics, comparison exit 0; `artifacts/chart-heatmap/hm2c/typecheck-final.log` and `artifacts/chart-heatmap/hm2c/typecheck.json`. This is no-new-errors evidence, not a clean upstream compile.
- Controller's final combined inventory-backed gate has zero errors/violations: `artifacts/chart-heatmap/hm2-join/combined.json`. Renderer physical/logical counts are 105/48, 207/94, 143/51 and 251/96; whole-file and function caps pass. The working inventory includes unrelated existing root mappings; this approval covers only the frozen renderer slice.
- Placeholder and credential-pattern inspection is clean. Four new renderer modules and their focused test remain within HM2c ownership. No session, router, storage, host lifecycle, HM1 adapter or frozen contract edits are included.

Initial RED was a missing-module failure. The later `artifacts/chart-heatmap/hm2c/red-behavior.log` demonstrably catches three deliberate mutations to constant palette selection, tooltip suppression and gradient reversal; it is mutation evidence, not chronological implementation-first failure evidence. Reviewer-requested layout regressions independently failed before their fixes: `artifacts/chart-heatmap/hm2c/review-red.log`, two failures. The final focused run passes both regressions.

## Findings resolved

1. Multiline ellipsis could leave earlier lines wider than the cell. Every returned line is now bounded; hyphen width participates in wrapping. The new regression checks each measured line and retains hide behavior.
2. Axis allocation reserved unrotated font height and the y title gap ignored row-label width. Layout now reserves projected rotated extents and full y-label clearance; its regression failed against the previous implementation.
3. The reverse-marker test used an invalid ID on one side, weakening the assertion. Both sides now use the same JSON row/column ID; label coordinates and missing-cell marker exclusion are checked explicitly.
4. Cell rounding now matches pinned AG Charts 12.1.1 source: floor the origin and ceil the size, then clip. Independently inspected `ag-charts-enterprise@12.1.1/dist/package/main.esm.mjs` lines 18672-18676; the test checks the corrected fractional-boundary result.

No remaining blocking findings within this slice. The renderer uses finite HM1 cells for color extent and hover identity, retains duplicate rows through numeric category indices, and draws missing borders without numeric values or tooltip content. Shared OKLCH interpolation preserves source palette ordering; constant domains select the middle stop. Both axes remain categorical, and legend reversal changes gradient and labels together without modifying cell colors. Disabled tooltips return no content as well as disabling the native tooltip option. The gradient hover plan reuses the existing structural contract without hierarchy weighting or new lifecycle ownership.

Application acceptance must still demonstrate real native hover, visible controls, retained-FMP values, refresh, fresh reopen and export through the existing host. These are the planned integration boundary, not missing pure-renderer work.
