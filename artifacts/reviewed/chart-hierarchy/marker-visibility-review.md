# First-hover marker repair review

## Review Verdict

- VERDICT: APPROVED
- TASK: H4 bounded first-hover marker visibility repair; source acceptance only.
- BASELINE: Workspace `99e6878920cf586b94bcf9c59c3177373126d1cf`.
- MECHANICAL_RESULTS:
  - Independent native regression: PASS, four tests, exit 0. Ran pinned Node with `node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/hierarchyHoverBinding.render.test.ts --maxWorkers=1` from `vendor/workspace/terminalpro`.
  - Implementer affected checks: PASS, 74 tests across five files, exit 0.
  - RED phase: VERIFIED. Final native regression fails all four first-hover assertions against baseline, observing zero painted polygons instead of one. Earlier draft-oracle diagnostics are excluded from acceptance evidence.
  - Scoped Biome: PASS, both files, no fixes.
  - Strict types: baseline and candidate both exit 2 with the identical inherited `typography.ts(1,1) TS2578`; no added or owned diagnostic. This is baseline-relative acceptance, not a clean application compile.
  - Whole-file complexity: PASS, 130 physical lines, 70 logical units, maximum callable 16; limits 400/300/50. The combined inventory report has no errors or violations. The new test is explicitly excluded from production caps.
  - Placeholder/secret scan: CLEAN. Boundary: WITHIN the assigned production binding and new native regression. Source/test hashes remained unchanged during independent verification.

## Findings

No blocking finding remains. The production diff adds only `invisible: false` to the existing marker update in `src/components/General/Table/Chart/echarts/hierarchyHoverBinding.ts`. This explicitly clears the hidden placeholder state retained by native ECharts graphic merging. Financial preparation, marker identity, tooltip visibility, clearing and lifecycle ownership remain unchanged.

The new `tests/unit/chart-compatibility/hierarchyHoverBinding.render.test.ts` exercises real ECharts SVG output through production translation, hover projection and binding. Both families paint exactly one marker on initial hover and after a full tooltip-off replacement, before any recovery mouseout. Missing-color leaves, parents, mouseout and globalout clear it; subsequent valid hover restores it. The effective tooltip state is checked after painting.

Frozen source SHA256: `0eda9296a2dec60a8d910e8569f61706550c4ca98caaf980aa90b4a20ed2feb3`. Frozen test SHA256: `57637f8b6a103e9bc6089ac63711d7d91f8303b45cca63618190f0aa8e5a0a15`. Independent command, exit and before/after hashes are retained in `artifacts/chart-hierarchy/h4/reviewerlogs/marker-native-result.json`; native output is in `marker-native.log` beside it.

SUMMARY: Approve the minimal source repair; H4 remains open until a rebuilt identified image passes the unchanged packaged synthetic journey, including the first hover with Tooltips Off.
