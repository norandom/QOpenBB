# Task 2.87 independent financial review

- VERDICT: APPROVED
- Scope: pure area numerical projection and tests only; renderer/application acceptance remains pending.
- Source: frozen contract at Workspace 1d907aff0c6530551bb7e55a805655d743daa058; final files reviewed after parallel editor commit 95fca92. Original AG Charts 12.1.1 bundle identity is recorded in the frozen fixture.

## Mechanical results

- Independent tests: PASS. Initial contract plus values run passed 20 tests. After final single-series predicate/test refinement, affected values suite passed all 17 tests, exit 0; contract source/tests unchanged.
- Command: pinned Node /mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node, Workspace terminalpro cwd, node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/cartesian.area-values.test.ts --maxWorkers=1. Initial run also selected cartesian.area-contract.test.ts.
- Scoped Biome: PASS, exit 0, all three owned files, using the same Node and node_modules/@biomejs/biome/bin/biome lint with explicit paths.
- Placeholder/credential scan and runtime import inspection: CLEAN.
- Boundary audit: WITHIN. No state owner, dependencies, flags, runtime admission or renderer changes introduced by this lane.
- RED: VERIFIED in values/red.log; original missing production import failed suite loading.
- Complexity: inspected controller evidence measures cartesianArea 76 physical/68 logical, largest function 10; cartesianAreaSpans 101 physical/91 logical, largest function 11. Final predicate refinement adds no lines or logical units. Controller confirms final inventory rerun exit 0 against updated fork revision in values-complexity.json.
- Compiler limitation: known upstream typography TS2578 remains; no full compiler success claimed.

## Financial and source review

Signed ordered accumulation and normalization match independent arithmetic: [7,-6,5] uses denominator 7; reordered [7,5,-6] uses 12; [-4,8,-3] uses 8. Normalized multi-series missing entries become processed zero, so previous-row window gating remains finite and does not alter current-row denominators across sign changes. Marker coordinates, processed labels and immutable raw observations remain separate. Hidden values contribute zero independently of raw data.

Reviewed retained getSeriesSpans, split/skip slots, earlier-stack phantom fallback and axis fallback against the cohesive helper. Lower, middle, upper and consecutive gaps preserve distinct marker and stroke behavior. Single-series non-normalized processing now uses the precise original grouping predicate. Large normalized values scale before arithmetic overflow; unrepresentable ordinary cumulative coordinates throw explicitly rather than silently changing the amount.

No blocking findings remain. The reviewer's initial negative-single-series concern was withdrawn: original inequality splitting precedes Math.max, so [-2,-4] correctly retains stroke [-2,-4]. Final regression records that source behavior. review-rejected.md preserves the explicitly withdrawn local reasoning, not a current defect or acceptance blocker.

Final SHA-256: cartesianArea.ts 8aac8e75fbd6b780c21aa98c635e3e14133efa1f707eb0c68e9af71cc22baa5f; cartesianAreaSpans.ts 9a30ffa25f0a164b1ed1bdde3f1f0536674ba34dacadb799ab6705d322dde3c5; values test 9e6d2bb254dd1354fb41dd00f799a7930775eeafc7d5472f0283c4b1e075256a.

Summary: pure projection accepted for task 2.87. No browser, renderer, displayed standalone axis-domain or release acceptance is implied.
