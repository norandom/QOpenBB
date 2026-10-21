# Pie and donut verification

P1 assignments were independently accepted at Workspace `0a2dd8659c89cc6368ce3d6359cf05c0e632b69a` as inactive foundation code. P2 rendering is now independently accepted as described below. Original controls, application/image acceptance and publication remain open; the published alpha is unchanged.

## P0 design and fixture

Independent Astra review matched the [assignment design](../../../.kiro/specs/analyst-workspace/pie-design.md) to the retained original `PieChartProxy`: first selected field for pie; all selected fields for donut; pixel ring offsets and conditional title participation; saved `doughnut` spelling preserved separately from canonical renderer family.

The candidate FMP fixture derives exactly four AAPL fiscal-2025 quarters from the previously captured income-statement response, with no new provider request. Raw capture SHA256 `390dc8cbfc8302720a203bd9782d5e3b1f7363a4f762bdfcef079dbbe4c72f6b`; derived CSV SHA256 `5a19cf332d9896f111d4400cab18e949db4bc345037990aed234db2e4d096669`. Revenue totals USD 416,161,000,000; gross profit totals USD 195,201,000,000. Independent review matched all rows, dates, periods, values and hashes. Separate rings will have separate denominators. This is fixture readiness, not a rendered example; raw provider data remains ignored.

## P1 source

Only `compatibility/pieAssignments.ts` and `tests/unit/chart-compatibility/pieAssignments.test.ts` were added. They cover first selected pie field, ordered donut rings, alias preservation, empty selections, exact original offsets, malformed/duplicate/sparse inputs, failed reads and independent output objects. No runtime routing, editor, dependency or flag changed.

RED captured a missing-module failure before implementation. The focused existing Vitest configuration then passed 30 tests; an independent rerun also passed 30. Scoped strict TypeScript passed. The independent review's initial launch failed before execution because default WSL PATH lacked Node; using the established pinned Node toolchain resolved that environment issue. Logs remain under `artifacts/chart-pie/p1-*.log`.

The explicit maintained-scope checker passed: 85 physical lines, 67 logical units and maximum 17 per function, within 400/300/50. Inventory scope is `p1-workspace-scope.json` plus the unchanged data-API scope. Source commit `dc83f53` was followed by line-ending-only cleanup `0a2dd86`; independent review confirmed an empty diff ignoring end-of-line whitespace and a clean whitespace check. No semantic changes followed the verified tests.

Commands used pinned Node with `node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/pieAssignments.test.ts`, scoped `tsc -p artifacts/chart-pie/p1-tsconfig.json`, and the existing `tools.quality.complexity --check` with both explicit repository manifests. No candidate build or release was dispatched for this inactive task.

## P2 inactive mapper

Independent Astra review accepted Workspace `300c231a00e106eba3e3f019b35b8fd0f1b3560b` on 2026-10-21 against the [renderer design](../../../.kiro/specs/analyst-workspace/pie-renderer-design.md). Six mapper modules plus an explicit empty-selection snapshot policy preserve per-ring raw values, independent observation legends, palette gaps, pixel ring offsets, both label layers and zero-total outlines. No runtime routing, editor, dependency or feature flag changed.

The original source probe establishes finite-negative/zero retention without slice area, null/invalid omission, independent ring selections and collapsed radii. The replacement uses native ECharts sectors with a transparent label companion. Original labels format before field-name prefixes; tooltips retain raw locale formatting. The prepared FMP quarterly values are checked arithmetically, not yet through the application.

The implementer and independent reviewer each passed 93 focused tests across four files, including 13 actual SVG engine tests. These exercise fractions/radii, native legend dispatch and reprojection, labels/leaders, restoration, empty outlines, collapsed/reversed rings, rotation and both palettes. RED recorded missing mapper modules and the new snapshot-policy failure before implementation; its first wrapper returned zero incorrectly, while the captured Vitest output shows the failures. Subsequent validation captured the actual exit status.

Scoped strict TypeScript reports only the inherited `src/components/ds/plugins/typography.ts:1` TS2578 unused directive; no changed-file diagnostic. Scoped Biome lint passes after declaration-style corrections. The full explicit-scope checker passes all eight changed production files: maximum 252 physical lines, 122 logical units and 29 per function. New mapper modules alone reach at most 252/86/14. No exception is needed.

Reproduction uses the established one-worker `chart-compatibility/vitest.config.mjs` with `pieAssignments.test.ts`, `pie.test.ts`, `pie.render.test.ts` and `snapshot.test.ts`; scoped `p2-tsconfig.json` and both explicit `p2-*-scope.json` manifests feed the existing tools. Detailed logs and independent review remain local under `artifacts/chart-pie/`. Shared application integration, original/candidate visual comparison (including thick-stroke inset), FMP image acceptance and release remain P3-P5. No image build was dispatched for P2.
