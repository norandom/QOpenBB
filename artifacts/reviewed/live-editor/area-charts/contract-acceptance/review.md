# Area contract acceptance

Task 2.86 and its native-span/processed-label design refinements are APPROVED for downstream implementation. This accepts the frozen seam and demonstrated native representation, not an implemented area renderer or application parity.

## Review verdict

- VERDICT: APPROVED
- TASK: 2.86
- Reviewer: independent financial/architecture review; actual diff, new files, requirements 4.8/4.9/10.1-10.6, task boundary, amended design, retained source and evidence inspected.
- Tests: PASS, independently reran pinned Node with `node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/cartesian.area-contract.test.ts`; four tests, exit 0, 1.34 seconds.
- Static checks: scoped Biome lint PASS, independently rerun after labelValues addition; three files, exit 0. Compiler evidence reports only existing typography.ts TS2578; full compiler success is not claimed.
- Placeholders/secrets: CLEAN in scoped changes.
- Boundary and boundary audit: WITHIN/CLEAN. New immutable area types and type-union extension only; runtime admission remains seven Cartesian/two normalized families. No flags, dependencies, persistence owner or renderer activation added.
- RED phase: VERIFIED in red.log; missing new contract module prevents test collection before implementation.
- Complexity: current contract-complexity.json has no errors/violations; cartesianTypes.ts 156 physical/105 logical, cartesianAreaTypes.ts 46/29; each function is one logical unit. Whole-file 400/300/50 caps pass.

## Findings and limits

No blocking findings. Signed negative deltas, null termination and duplicate-X split endpoints are exercised in native SVG rendering, including cumulative coordinates, pixel positions and polygon return edges. These tests demonstrate that isolated baseline/delta spans can express the required geometry; they do not implement or validate original span generation. Task 2.87 must reproduce the pinned neighbor-stack/phantom-span algorithm and independently test its outputs, including hidden, zero, missing and single-series cases.

The processed-label refinement is justified: retained original source applies invalidValue to yValueRaw, and the inspected original screenshot shows a zero label for Gamma/First missing data and the overlapping Delta/Second zero. Separate labelValues preserves this presentation without rewriting raw snapshots or tooltip lookup. Native probe geometry and the new label seam have distinct responsibilities.

Original browser evidence is source-overlaid and records one CSV 401. Custom-theme combinations and standalone zero-only/all-missing displayed domains remain unobserved. Source-derived contracts are identified as such; area application acceptance, clean diagnostics, save/reopen and broader UI-10 remain pending. The existing baseline compiler diagnostic remains reported, not suppressed.

## Reviewed source identity

Original Workspace: `38dffc33389aca0e4a87e0e88d42f7067aa220df`; retained AG Charts 12.1.1 and AG Grid Enterprise 34.1.1 hashes are frozen in the fixture. Pinned executable: `/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node`, WSL Debian user mc.

SHA-256 of reviewed files (Workspace terminalpro-relative):

| File | SHA-256 |
| --- | --- |
| src/components/General/Table/Chart/echarts/cartesianTypes.ts | e93d2d5b2cbde48b7ee5dfbbf11662b917eadeb6a3ccab70fb63d3916061d1d0 |
| src/components/General/Table/Chart/echarts/cartesianAreaTypes.ts | f0276cbdff610b20b95fdf7fc5877d13f5db368ae78965a2422e7d972f057462 |
| tests/unit/chart-compatibility/cartesian.area-contract.test.ts | f1649ebd12c721907a6aa156f29218d01a7e3c222bd70874d2e7dbb3fd7ffebb |
| tests/unit/chart-compatibility/fixtures/area-charts.json | c31885c480b18aeb374119c09026bd3c9390b23b913d92d0dcdd586fc4a0ad4d |

REMEDIATION: None required for the scoped prerequisite. Downstream acceptance remains governed by tasks 2.87-2.90 and the frozen contract.
