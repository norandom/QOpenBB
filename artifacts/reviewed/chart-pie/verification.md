# Pie and donut verification

P1 assignments were independently accepted at Workspace `0a2dd8659c89cc6368ce3d6359cf05c0e632b69a` as inactive foundation code. P2 rendering is now independently accepted as described below. P3 now connects the original controls and application flow, as described below. Candidate-image acceptance and publication remain open; the published alpha is unchanged.

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

## P3 application join

Independent Astra source review accepted Workspace `2d91255d763b87c6ddbc4a13c7fdcfdb77599e63` on 2026-10-21 against the [integration design](../../../.kiro/specs/analyst-workspace/pie-integration-design.md). Separate Sol workers implemented the shared integration and label controls; the label leaf also passed independent Sol review. The existing caller, Widget transaction, host and dock now admit Pie, Donut and saved `doughnut`. No new state owner or feature flag was introduced.

The join preserves first-field pie and ordered independent donut rings, ordinary numeric-wrapper capture, once-only aggregation, donut transpose and empty recovery. Common appearance and family-transition logic were extracted for reuse. The existing editor gains independent Callout Labels/Sector Labels and original numeric controls; pie omits the original-inapplicable axis/navigation panels. Switching back restores applicable navigation without changing retained flags. Latest-state typography and saved option paths remain in the shared reducer. Compact tooltips omit the category heading; single/shared retain the hovered item heading and raw value.

Independent final verification passed 36 caller/session/editor tests and 26 mapper tests. Separate leaf verification passed six new and three existing label tests. The implementer also passed affected common appearance/setup, prior-family/caller and root editor/gallery regressions; these runs overlap and are not summed as unique tests. All 45 changed production files pass nonmutating Biome lint and the explicit-scope complexity gate: maxima 293 physical lines, 143 logical units and 39 per function, with no new exception.

Final baseline-relative TypeScript reports 2,714 diagnostics at the unchanged source and 2,713 for the candidate. One setup-policy mismatch is removed. Four remaining diagnostic headlines change only their union spelling/order at existing icon, Zod and combo-test errors; review found no new diagnostic defect. The candidate includes three reviewed existing-test adaptations for the new pie/editor union, recorded with hashes; the four new P3 test files are checked separately and have no diagnostics. This is not a clean whole-app compilation. Local comparison: `artifacts/chart-pie/p3-static-final/comparison.json`.

The lifecycle unit suite fails before collection because its existing ECharts mock lacks `ComponentModel`. A clean baseline archive reproduces the same failure (`p3-static/baseline-lifecycle.log`); it is not reported as a passing regression. Host/mapper/join checks pass, but packaged lifecycle/export remains an explicit P4 gate. The initial new context-property error found by type comparison was corrected before final review.

Reviewed source/test commands and byte hashes remain in `artifacts/chart-pie/p3-source-review.md` and local logs. P4 still requires an identified candidate image, real retained FMP quarterly values, matched original/candidate screenshots in both themes, refresh, save/reopen and export. No candidate build or release was dispatched for this source-only task; the real-data chart sample remains pending.

## P4 first image and control repair

On 2026-10-21, the local Dagger build of Workspace `2d91255d763b87c6ddbc4a13c7fdcfdb77599e63` completed and loaded image `sha256:a001a8e200ed8f5e9f2bbe13832b7148e78cf5640245827eda5acac8c1b55399`. Its disposable Full runtime used the packaged image without a source overlay. WSL briefly rejected new commands during the build and recovered without a restart. The build completed with exit 0.

The retained FMP CSV and raw capture hashes match the P4 fixture contract. The candidate produced four default pie/donut captures and passed the quarterly angle fractions and raw tooltip checks, with separate revenue and gross-profit denominators. The run then failed on enabling a title; save/reopen/export, synthetic cases and prior-family regression acceptance are not claimed. Early test-helper failures in angle ordering and original gallery/capture selectors were diagnosed and corrected, not counted as application passes.

The production failure came from passing the entire resolved caption or legend into a font context that accepts only `fontWeight` and `fontStyle`. Repair `ff8878cc0a811d6ac082b7db16ce4c1b5da7023e` projects those two fields from the latest selected appearance. The shared validator, saved-state owner and stale-event guards remain unchanged. Independent Sol review reran `pieProductionJoin.test.ts`: 19/19 pass, including real title/subtitle and legend transactions for all three saved family spellings, consecutive font edits and stale rejection. Scoped Biome lint and the explicit-scope complexity gate pass: 72 physical lines, 69 logical units and largest function 22. This is source acceptance; the repaired image has not yet been built.

The isolated original reference passed its focused scenario with the same FMP CSV and actual canvas size (619 by 284, DPR 1), including independent ring legend selection and label controls. Its scoped new-chart diagnostics are clean; restored dashboards from earlier reference attempts caused separate startup CSV errors, which are retained locally and excluded from that scoped claim. Original saved state confirms pie legend disabled and donut legend enabled, with a 50-pixel paged legend. Candidate legend defaults, donut pagination/markers, ring title and surrounding-ring label fitting still differ. P4 remains open, and the published alpha is unchanged.

Local reproducibility inputs: `artifacts/chart-pie/p4-control-fix.md`, `p4-control-review.md`, `p4-candidate-findings.md`, and `p4-reference/report.md`. Raw browser output and authentication state remain ignored. No unaccepted chart sample is published as a finished milestone.

## P4 V1 effective appearance repair

Independent source review accepted Workspace `008fbd1668121dab9a33bb11c9db6e8c789309ca`. Pie's default legend visibility now uses the resolved assignment count, so two selected fields do not imply two rendered pie rings. Explicit common/family/generated/saved legend settings still override the fallback. The pie-specific style also retains legend bounds/marker shape and source-derived series-title typography through immutable admission. V1 does not implement the paged legend or draw ring titles; those remain V2 work.

The independent reviewer reran 42 application/default/control tests and 49 mapper/admission/actual-engine regressions, all passing. The explicit-enabled one-field pie test still verifies slice selection and immutable reprojection. Scoped production lint passes; maximum measured production size is 184 physical lines, 78 logical units and 15 per function, with the combined explicit-scope checker passing. Scoped TypeScript still exits 1 on imported baseline dependencies; no diagnostic names any of the eight changed paths after the new fixture was corrected to use immutable construction. This is not a clean whole-application compile.

Review inputs and commands are retained locally in `p4-appearance.md` and `p4-appearance-review.md`. The [repair design](../../../.kiro/specs/analyst-workspace/pie-appearance-repair-design.md) separates the accepted V1 source contract from proposed V2 layout/lifecycle work. The repaired image and matched visual/lifecycle acceptance remain pending, and the published alpha is unchanged.

## P4 native legend foundation

Source `ab50456d73243a0c0b9a45eaa5e2b397ca8c0e0c` retains the native-ECharts selection proof and the reviewed immutable paging metadata types. The independent reviewer reran the final formatted proof: 3/3 pass. A generated visible legend hit target receives a native click, emits exactly one selection event and synchronizes the hidden canonical and visible components. Equal-caption keys in the other ring remain independent. Two test pages preserve off-page selections, separate ring fractions, aligned companions and zero-total recovery. Hidden components do not contribute visible text or hit targets.

This proves the engine seam, not the application pager. No production paging, keyboard access or PNG-export claim is made. The type-only foundation is 31 physical lines and passes the explicit-scope cap gate. The [frozen V2 design](../../../.kiro/specs/analyst-workspace/pie-appearance-repair-design.md) assigns disjoint layout and lifecycle lanes; only the existing lifecycle owns a transient page anchor. Native ECharts remains the slice-selection owner. Local proof/review: `p4-legend-probe.md`, `p4-legend-probe-review.md`, `p4-visual-design-review.md`.
