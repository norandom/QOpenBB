## Review Verdict

- VERDICT: APPROVED
- TASK: Area zero-category repair, owning pure projection from task 2.87.
- MECHANICAL_RESULTS:
  - Tests: PASS. Independently ran cartesian.area-values.test.ts: 18/18, exit 0. Worker zero-green.log records numerical/native/contract suites: 36/36.
  - TBD/TODO and secrets: CLEAN in the narrow diff.
  - Static checks: PASS. Independent one-file Biome lint and scoped git diff --check, exit 0.
  - Boundary: WITHIN. cartesianArea.ts and its existing numerical test only; renderer assembly unchanged.
  - Boundary audit: CLEAN. Contract correction records original typed-stack semantics; no new state or fallback renderer.
  - RED phase: VERIFIED. zero-red.log records the new six-row regression failing with final fill endpoints incorrectly zero, before repair.
- FINDINGS: Original typed-array coercion was omitted from the numerical model. The narrow correction restores it while retaining scalar cumulative nulls, raw missing values and labels.
- REMEDIATION: No code remediation required. Controller retains fresh whole-file complexity gate and actual application journey acceptance.
- SUMMARY: The pure projection now supplies the source-backed zero valley and following nonzero boundaries for native rendering.

## Source proof and review

Read the retained AG Charts Community main.cjs.js under /home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules/ag-charts-community/dist/package/. groupStackAccFn around line 29270 constructs Float64Array stack entries. normaliseFnBuilder around line 29063 maps those typed arrays; its normalise2 returns null at zero extent. Float64Array.map coerces that result to zero. Scalar cumulative values retain null. getSeriesSpans around line 40184 therefore sees finite zero stack entries and continues fill/stroke boundaries through that category.

Independent pinned-Node witness: Array.from(new Float64Array([0,0,0]).map(()=>null)) returned [0,0,0]. This is why globally replacing missing data or changing native gap behavior would be incorrect. The repair only changes zero-extent stack coordinates when processed values contain a finite observation. All-missing single-series inputs retain missing markers/strokes; nonzero-extent missing values remain missing.

Reviewed the updated chart-area-contracts.md distinction. For Third across Delta/Epsilon/Zeta, the regression verifies upper [100,0,100], lower [37.5,0,50], corresponding stroke edges, and unchanged raw Gamma missing observation. The existing single-series test now correctly retains the zero-to-negative stroke. No unrelated gap expectation changes remain.

## Commands and identity

From vendor/workspace/terminalpro in WSL Debian user mc, NODE=/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node:

```text
$NODE node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/cartesian.area-values.test.ts --maxWorkers=1
$NODE node_modules/@biomejs/biome/bin/biome lint src/components/General/Table/Chart/echarts/cartesianArea.ts
```

Workspace base HEAD b523f1455b632e42711de5e6193045fee6d3987c. Frozen working-tree SHA-256:

| File | SHA-256 |
| --- | --- |
| terminalpro/src/components/General/Table/Chart/echarts/cartesianArea.ts | e45810be8018b885f68711300b396f7e0e8db3ff44c557bfdd11e968e3224d20 |
| terminalpro/tests/unit/chart-compatibility/cartesian.area-values.test.ts | 94f1d74ecc6fd1a372db171dcaf43d4dfb1c58c9e004854c9a3d78b2253f1e63 |

This review establishes the numerical repair and its source ownership. It does not claim a fresh browser comparison, full compiler success or release acceptance. Earlier renderer acceptance remains bounded to native assembly; the actual application join exposed this prerequisite numerical defect.
