# Pie and donut verification

P1 assignments are independently accepted at Workspace `0a2dd8659c89cc6368ce3d6359cf05c0e632b69a` as inactive foundation code. Pie/donut rendering, original controls, image acceptance and publication remain open. The published histogram alpha is unchanged.

## P0 design and fixture

Independent Astra review matched the [assignment design](../../../.kiro/specs/analyst-workspace/pie-design.md) to the retained original `PieChartProxy`: first selected field for pie; all selected fields for donut; pixel ring offsets and conditional title participation; saved `doughnut` spelling preserved separately from canonical renderer family.

The candidate FMP fixture derives exactly four AAPL fiscal-2025 quarters from the previously captured income-statement response, with no new provider request. Raw capture SHA256 `390dc8cbfc8302720a203bd9782d5e3b1f7363a4f762bdfcef079dbbe4c72f6b`; derived CSV SHA256 `5a19cf332d9896f111d4400cab18e949db4bc345037990aed234db2e4d096669`. Revenue totals USD 416,161,000,000; gross profit totals USD 195,201,000,000. Independent review matched all rows, dates, periods, values and hashes. Separate rings will have separate denominators. This is fixture readiness, not a rendered example; raw provider data remains ignored.

## P1 source

Only `compatibility/pieAssignments.ts` and `tests/unit/chart-compatibility/pieAssignments.test.ts` were added. They cover first selected pie field, ordered donut rings, alias preservation, empty selections, exact original offsets, malformed/duplicate/sparse inputs, failed reads and independent output objects. No runtime routing, editor, dependency or flag changed.

RED captured a missing-module failure before implementation. The focused existing Vitest configuration then passed 30 tests; an independent rerun also passed 30. Scoped strict TypeScript passed. The independent review's initial launch failed before execution because default WSL PATH lacked Node; using the established pinned Node toolchain resolved that environment issue. Logs remain under `artifacts/chart-pie/p1-*.log`.

The explicit maintained-scope checker passed: 85 physical lines, 67 logical units and maximum 17 per function, within 400/300/50. Inventory scope is `p1-workspace-scope.json` plus the unchanged data-API scope. Source commit `dc83f53` was followed by line-ending-only cleanup `0a2dd86`; independent review confirmed an empty diff ignoring end-of-line whitespace and a clean whitespace check. No semantic changes followed the verified tests.

Commands used pinned Node with `node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/pieAssignments.test.ts`, scoped `tsc -p artifacts/chart-pie/p1-tsconfig.json`, and the existing `tools.quality.complexity --check` with both explicit repository manifests. No candidate build or release was dispatched for this inactive task.
