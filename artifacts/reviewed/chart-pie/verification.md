# Pie and donut verification

P4 application acceptance passed on 2026-10-21. The owner accepted the disclosed appearance differences, and independent feature review approved all seven final-image browser journeys. P5 published [alpha-39584871538-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-39584871538-1); both public image identities and six anonymous pulls are verified. Scope is the ordinary Table/File chart journey; other families and callers remain open.

## P4 final image acceptance

- Workspace production: `9d1883849f480f45c89c53867554590d45b12428`.
- Image: `sha256:2459fc315b735cb2f66083bb11a10bacaed2b0fdad7f11f46191937661591d81`.
- Release source: `9e0f2eea031048fe882178eb7af6851e4b596124` adds only the four reviewed browser-harness files; production bytes are unchanged from the tested source.
- Owned runtime: packaged image only, without source overlays; configuration and login ready.
- Actual isolated browser results: FMP 1, synthetic 1, ordinary/combination 2, scatter/bubble 2 and histogram 1 passed, with no skipped/flaky acceptance checks. The first XY batch passed its first journey but hit HTTP 429 at scatter reopen because batches were scheduled too closely. After the login window cleared, only that blocked scatter journey was rerun; the original failure remains recorded.

The FMP journey checks raw tooltips and separate ring proportions, both themes, existing style controls, side-legend ellipsis/full tooltips, canvas paging and independent selection, refresh, save/reopen and PNG export from the second legend page. Unfiltered browser diagnostics pass. The synthetic journey retains duplicate/signed/missing observations, aggregation, empty recovery and saved `doughnut` controls. The shared lifecycle repair also passes all five prior-family journeys on this same image.

Run commands use `bash artifacts/chart-pie/run-pie-browser.sh PRIVATE ORIGIN EVIDENCE fmp|synthetic` and `bash artifacts/chart-pie/run-prior-browser.sh PRIVATE ORIGIN EVIDENCE ordinary-combo|xy|histogram`, with pinned Node and one isolated headless browser worker. Final local evidence directories are `p4-browser-fmp-8`, `p4-browser-synthetic-5`, `p4-final-ordinary-combo`, `p4-final-xy`, `p4-final-scatter` and `p4-final-histogram`, all beneath `artifacts/chart-pie/`. Raw logs, disposable account state and intermediate failed captures remain local. Independent review: `artifacts/chart-pie/p4-feature-review.md`.

The three published chart-only samples come from the final FMP run and exactly match the owner-accepted default PNG bytes. Captures use 619 × 284 CSS pixels at DPR 1 (crop width rounds to 620 pixels). The accepted differences are slightly shifted outer labels, no thin slice separators and a Pie diameter about 10 pixels smaller than the original. Styled controls are separately exercised in a larger widget, not presented as a matched-size default comparison.

FMP source: `https://financialmodelingprep.com/stable/income-statement`, symbol AAPL, period quarter, limit 40; retained capture retrieved at `2026-10-20T14:06:05.149732+00:00`. Four FY2025 quarters, reporting dates 2024-12-28 through 2025-09-27, retain original USD values. Revenue denominator is USD 416,161,000,000; gross-profit denominator is USD 195,201,000,000. Each ring independently distributes its own measure; overlapping revenue and gross profit are never combined. The raw capture and derived CSV hashes are retained below. No new provider request was made for these checks.

The historical source reviews below retain the defects and repairs found during P4. Their pending statements describe those earlier checkpoints; final packaged acceptance is established above. Production caps pass. Scoped production typing retains the documented unchanged upstream typography diagnostic; the authored browser files pass scoped typing. This does not claim a globally clean upstream typecheck or complete renderer coverage.

## Historical implementation evidence

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

## P4 paged legend source acceptance

Source `e5e3e36a79fa6c84285d5c8063428680095813a7` implements measured multi-row legend paging, descriptor-derived donut titles and surrounding-ring label containment. The lifecycle owns a transient page anchor and projects keyboard controls; native ECharts remains the selection owner. Session propagation preserves immutable metadata without writing it to saved chart state. The original six-items-plus-two-items layout is covered at the reference canvas size. Insufficient space follows the original conditional minimum-cell rule and recovers when space returns.

Focused checks pass: 25 layout/render/native tests, 29 binding/lifecycle tests and 5 session tests. Independent review reran H and L checks, requested and accepted the bounded no-fit correction, and inspected the controller join. Lint and the combined fourteen-file complexity gate pass (400 physical/300 logical/50-function caps). Scoped TypeScript still reports inherited application errors; none are attributed to the changed production files. This is not a globally clean typecheck. Local review: `p4-v2-review.md`; lane records: `p4-layout.md`, `p4-paging.md`.

The browser adaptations are source-reviewed, including passive initial reopen, native mouse paging, keyboard interaction and noninitial-page export. They have not yet passed against the rebuilt image. Real-FMP visual/interaction acceptance, selected image publication and P5 release remain open. The previous alpha remains unchanged.

## P4 image findings and side-legend repair

The Dagger candidate from `e5e3e36` built and loaded successfully as `sha256:e87cb9c72039ca71b364920c489691dd54828abc7dee4e5f14d2441bde3ce9b1`; it runs image-only without a source overlay. The owner accepted the default appearance after disclosure of the smaller Pie diameter, shifted outer labels and missing thin separators. Those differences are retained deliberately.

Six browser journeys pass on that image: synthetic pie/donut (30.1 s), ordinary and combo (2 tests, 1.5 min), XY (2 tests, 41.3 s), and histogram (52.1 s). The synthetic journey covers independent selection, saved family order, aggregation, empty recovery and legacy saved-alias controls. These successes do not close the FMP journey or certify a later image.

Earlier FMP attempts exposed test-harness assumptions: omitted runner identity variables before login, a 15 px observer cutoff that omitted a visible small ring, and hover targets smaller than one CSS pixel after styling. Source-reviewed harness corrections preserve financial assertions, use normal widget resizing after matched default captures, and retain passive initial reopen. A synthetic test also incorrectly assumed Pie edits should replace Donut's saved field selection, then toggled an already-restored editor closed; both expectations were corrected and the journey passes. Raw diagnostics remain local.

The FMP styled right-legend check found a real product defect: at 619×593 the legend consumed plot width and no sectors were drawn. Source `cdb1684ae14ba93f4e0bad9895035238c775420b` restores the original automatic side-width aspect-ratio rule, preserving explicit bounds and the accepted top/bottom behavior. Independent source review, nine final layout tests and combined complexity checks pass; the preceding 27 focused layout/render/native checks also passed before the adjacent horizontal fallback was removed from scope. Local evidence: `p4-side-legend.md`, `p4-side-legend-review.md`. The corrected candidate still requires the FMP browser journey; P4/P5 and publication remain open.

## P4 tooltip replacement source repair

The corrected side-legend image `sha256:4efd6c3ea6633a9407aad6aae8af99f625c986a9056ba1edadeed4c8f6024d77` runs source `cdb1684` without overlays. FMP7 passes the right-legend placement/full-caption tooltip checks, style controls, native paging, independent selection and refresh, then fails unfiltered console diagnostics before reopen. The synthetic journey passes separately on this image (29.9 s). These are partial FMP results, not P4 acceptance.

The real ECharts regression reproduces the exact null-content exception: resize queues a tooltip refresh, then notMerge replaces its view while the engine remains active. Source `9d1883849f480f45c89c53867554590d45b12428` issues public `hideTip` inside the existing applying guard before replacement. This clears the old target so the callback becomes harmless; it does not cancel the engine timer or disable later tooltips. Actual visible HTML tooltip recovery, selection retention, transitions without next tooltip options, action ordering and failure cleanup are covered. The final focused run passes 34 tests; independent review reruns the affected real-engine and lifecycle checks. Combined caps pass (lifecycle: 289 physical/219 logical/32 per function). Scoped typing reports only the unchanged upstream typography TS2578, with no changed-file diagnostics.

The repair is two production lines plus focused tests. No dependency patch or private engine API was added. Local evidence: `p4-tooltip-repair.md`, `p4-tooltip-design-review.md`, `p4-tooltip-source-review.md`. The next identified image must pass the full FMP journey and affected shared lifecycle regressions. Publication remains pending.

## P5 published alpha

[CI run 39584871538](https://github.com/norandom/QOpenBB/actions/runs/39584871538) passed hosted checks, both Dagger builds and publication. The tagged prerelease points to root `455eceb5c537a192dcfb27694caf05beaba78a42`. Release Workspace `9e0f2eea031048fe882178eb7af6851e4b596124` differs from the locally tested production source only in the four reviewed browser-harness files. Data API remains `49cc413e6ab67eaa0444e07485b0f9243c786f7b`.

| Service | Manifest digest | Config digest |
| --- | --- | --- |
| workspace | `sha256:d4ea3d5d7f92c7b14461e2ea5d0fde774a6ce2a2611165e10557a920d0bff010` | `sha256:3b8d21e63ebeed7f7b9cf7f37dc7e02e24a0309126e44baf06132bcf966c8163` |
| data-api | `sha256:317594d49ce67726373011c8e670a43576d1224e9dd1fe58dfb7f5ae28275dbc` | `sha256:ebc2897c8322d2f801152ae8d488b15fdfabd85c148caa34622de83721979550` |

Both services passed anonymous Docker pulls by immutable digest, alpha release tag and `latest`, using a fresh empty Docker configuration. Remote manifest/config digests, Linux/amd64 platform, source/service labels and local repository digests match the completed release manifest. Six pulls passed. Manifest SHA-256: `497d5ed7c5c14bc79b9c77884dcb5bf656fc5f52dfe9d17746002115b98f99ec`; local pull-record SHA-256: `7cbce7e24a09b15e9e90ad113b930453dc5c95b75a53a0512d72c8a13063a186`. The public manifest is a [release asset](https://github.com/norandom/QOpenBB/releases/download/alpha-39584871538-1/manifest.json). Raw pull logs and registry responses remain local under `artifacts/chart-pie/release-39584871538/`.

CI-built publication identities are verified separately from the local packaged image used for browser acceptance. No browser run against the CI-built bytes or assembled Compose/server deployment is claimed. Pie/Donut completion covers the ordinary Table/File journey; other chart families, callers and deferred analyst capabilities remain open.
