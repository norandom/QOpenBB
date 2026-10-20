# Combination chart port verification

C1, C2, C3 and the C4a/C4b source integration are accepted. Combination charts now connect to the existing Table/File editor in source. Image/browser acceptance and real-FMP application acceptance remain open. No alpha has been published for this milestone.

C1 Workspace source: `99e3f8637960d4981695e73bb8fedd974215c113`.

Independent Sol review inspected both complete files against the retained original ComboChartModel and approved with no blocking findings. The reviewer reran 21 focused Vitest tests and strict scoped TypeScript checking successfully. Coverage includes builtin splits, custom ordering, first duplicate wins, missing/unsupported assignments, primary-only coercion, immutable state and malformed input.

From `vendor/workspace/terminalpro`, using the pinned Node 24.22.0 in WSL:

```sh
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/comboAssignments.test.ts
node node_modules/typescript/bin/tsc --noEmit --strict --skipLibCheck --target ES2022 --module ESNext --moduleResolution Bundler --types node,vitest/globals tests/unit/chart-compatibility/comboAssignments.test.ts src/components/General/Table/Chart/compatibility/comboAssignments.ts
```

The controller independently measured 118 physical lines, 109 logical units and 17 maximum units/function. The portable complexity gate passed with explicit C1 fork changes and no data-api changes. Local scope inputs and raw report remain under ignored `artifacts/chart-combo/`.

The initial RED run failed because the implementation module did not exist; no assertions ran at that stage. Its output remains in tool history, not a persisted log. Broader compatibility TypeScript checking reports existing errors in `typography.ts:1` and `cartesian.geometry.test.ts:42`; the scoped check above does not establish whole-project compilation.

Fresh FMP annual AAPL statements were retrieved for subsequent financial verification. Provider payloads and credentials are excluded from publication. No application runtime, visual parity, save/reopen, export or provider integration is accepted by this report.

## C2a: admission and independent numeric axes

Workspace source: `d5334ae2011ddb8c2875c01143b7d92fbd3f5767`.

Independent Astra review first rejected malformed-row admission and numeric-axis spacing based on raw rather than rounded ticks. Thirteen regression failures reproduced those gaps before repair. A second independent review approved the fixes and reran all 40 focused tests successfully:

```sh
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/combo.admission.test.ts tests/unit/chart-compatibility/combo.axes.test.ts
```

Coverage includes declared units per axis, separate same-unit secondary axes, all-secondary inputs, stable indexes, duplicate labels/selections, signed stack domains, zero/null values, malformed observations and rounded/rotated tick spacing on either side. Original axis placement controls remain valid inputs.

The portable complexity gate passed with explicit C2a source scope. Production physical/logical/max-function measurements are: types 74/42/no functions, admission 302/131/33 and axes 152/83/24. Scoped strict checking reports only the existing `typography.ts:1` unused directive; this is not a passing whole-project typecheck. Full-project attempts also encounter existing project-reference/compiler configuration errors.

C2a does not assemble mixed series or connect the application. Nonfinite derived geometry throws internally; the C2b public mapper must translate it into diagnostics without partial options. The independently accepted C1 root commit `d60835a` also passed the portable GitHub checks in run 39389836206; image building and alpha publication were skipped as intended.

## C3a: session transactions

Workspace source: `5d74f94bb4423a19891a19b61404e221e0f3b785`.

Independent Sol review approved the inactive assignment/family transactions and reran six combo tests plus 22 existing ordinary-session tests. The transactions use the existing local session owner, rehydrate latest storage, reject stale or removed targets, retain live custom assignments locally and serialize current assignments only. Unknown model fields remain intact. No hook, gallery or editor routing was added.

The portable complexity gate passed for all six touched production modules. Maximum measurements were 171 physical lines/file, 117 logical units/file and 19 units/function.

An isolated checkout of the preceding committed Workspace source and the same checkout with only these six source changes produced identical diagnostics under `tests/unit/chart-application/session.tsconfig.json`: both exited 2, with no added or removed diagnostic lines. This supports absence of new compiler diagnostics in that comparison; it does not establish passing project compilation. Raw logs, the exact comparison script and temporary checkout identity remain under ignored `artifacts/chart-combo/c3a/`.

The focused commands, from `terminalpro`, are:

```sh
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/comboSessionAssignments.test.ts
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs tests/unit/chart-application/applicationSession.test.tsx tests/unit/chart-application/applicationSessionTransactions.test.ts
```

Initial RED was a missing-module failure, not assertion execution.

## C2b: mixed renderer

Workspace source: `11515eee1d4f4c7e9bcc3bc59b0df537b5fd02d9`.

Independent Astra review approved the mapper and reran 52 tests: eight mixed-geometry cases, three actual ECharts SVG rendering cases and 41 existing area regressions. Rendered geometry covers category/number/time alignment and independent financial scales. Other checks cover separate stacks, raw tooltip values, global palette positions, reserved public/internal IDs, style isolation and area fragment axis bindings.

From `terminalpro`:

```sh
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/combo.geometry.test.ts tests/unit/chart-compatibility/combo.render.test.ts tests/unit/chart-compatibility/cartesian.area.test.ts tests/unit/chart-compatibility/cartesian.area-contract.test.ts tests/unit/chart-compatibility/cartesian.area-values.test.ts
```

The portable complexity gate passed. Physical/logical/max-function measurements: mapper 88/41/14, series assembly 96/45/21 and the modified area helper 236/76/9. The scoped compiler still reports the inherited typography directive diagnostic. Initial RED was a missing mapper import.

SVG rendering establishes engine geometry, not the live Workspace editor or full application journey. Navigator, refresh, save/reopen and actual FMP application checks remain open. The C3a root commit's ordinary pipeline runs checks only; no new image has been published for this incomplete milestone.

## C4a: independent navigator scales

Workspace source: `ec9128827b71d656bdf5c7c32b1e2458035f626c`.

Independent Sol review approved the navigator and reran 84 tests across seven files: `cartesian.navigator`, `cartesian.area`, `cartesian.area-contract`, `cartesian.area-values`, `cartesian.normalized`, `cartesian.horizontal` and `lifecycle`, using the same chart-compatibility Vitest config. Nine navigator tests include actual combo output and ECharts SVG/grid binding checks.

Checks cover independent main/overview axis mapping, index/ID conflicts, private area fragments, stack and name collisions, full-overview separation from hidden main geometry, immutable inputs, slider targets and retained ranges. The portable complexity gate passed; navigator metrics are 135 physical/45 logical/15 maximum function units, and overview helpers 99/52/9. Scoped TypeScript remains limited by the inherited typography diagnostic.

The initial RED run failed on a fixture theme issue. After implementation, the corrected regression was run against an isolated copy of the preceding navigator: one case failed and one passed. This establishes regression sensitivity but is not evidence of a successful tests-before-code sequence. Raw logs remain local. Combination-chart routing, real application lifecycle and FMP acceptance are still open.

## C3b: geometry appearance and axis transactions

Workspace source: `ed5d8de2748a4b05547c3b01a93a1c175361afeb`.

Independent Astra review initially rejected stale concrete axes after assignment/gallery changes. A composed edit-then-assignment regression reproduced the failure; the repair rebuilds transient axes, preserves saved numeric styling and assignment category type, and applies the original gallery category reset. Review then approved 15 focused combo tests and 55 ordinary appearance/setup/session regressions.

Run `comboAppearance.test.ts`, `comboEditorTransactions.test.ts` and `comboSessionAssignments.test.ts` under the chart-compatibility Vitest config. Run `effectiveAppearance.test.ts`, `setupProjection.test.ts` and `applicationSession.test.tsx` under the chart-application config. All tests reside under their corresponding `tests/unit/` directories.

The ten-file portable complexity gate passed: maxima 379 physical lines/file, 136 logical units/file and 24 units/function. An isolated committed baseline and the final ten-file candidate again produced identical session TypeScript diagnostics, both exiting 2. The baseline source was `11515eee`; the unrelated navigator changes were excluded from that comparison. This is baseline-relative evidence, not a passing project compile.

Appearance remains independently resolved by geometry. Combo setup defers cross-column unit comparison to actual numeric axes while retaining validation and aggregation provenance. Existing ordinary defaults remain unchanged. Actual editor routing and source-refresh hooks are not accepted by this task.

## Retrieved FMP data: engine check

An independent Astra reviewer reran the ignored real-data probe successfully: one test passed with no skips. It used the existing five annual AAPL income-statement records, verified their provenance hash and CSV headers, and compared all 15 unscaled revenue/net-income/EPS values with actual ECharts series output. Checks also covered date labels, grouped-column alignment, raw tooltips, finite SVG and independent USD versus USD/share axes.

The exact command and probe remain local under `artifacts/chart-combo/fmp-engine/`. No new provider request was made. The initial probe assumed positional CSV fields; a header-based correction and the original failure are retained locally. Font measurements are mocked, so this proves neither visual parity nor Workspace integration. Raw data and rendered financial values are excluded from publication. The public sanitized summary contains provenance, units and check counts only.

## C3c/C4b: existing editor and caller integration

Workspace source: `74254b6dc037277449d3a89c69d265aa61412eec`.

Independent Astra review approved the 24-file production join and reran 51 application tests plus 24 compatibility tests. Actual Table/File components now expose combo assignments in Set Up and geometry-specific Customize controls. Tests cover live custom-cache recovery, restored builtins, external replacement and stale edits, mixed-unit setup/count, concrete-axis refresh defaults and unchanged full navigator overview during main legend filtering.

Run the five chart-application suites `callerRoute`, `comboEditorControls`, `comboProductionJoin`, `applicationSession` and `applicationSessionTransactions` using their existing Vitest configuration. The independently repeated compatibility suites are recorded in local `review-contracts.log`. The new `tests/e2e/live-chart/combo-charts.spec.ts` is maintained but unexecuted.

The reviewer identified and verified fixes for Custom Combo gallery reachability, pending-family reconciliation, restored-builtin editing and stale external-assignment caches. A restored-builtin failure was captured before its correction. A separate ordinary-line test mismatch was reproduced on clean baseline `ed5d8de`; its stale expectation was corrected to retain both coordinate and raw-value assertions.

The committed source passed the explicit 24-file portable scope/complexity gate. Maximum measurements are 383 physical lines/file, 136 logical units/file and 39 units/function. An isolated baseline comparison added no TypeScript diagnostic lines and removed an existing chart-family registration error. Both runs still exit 2 because unrelated project diagnostics remain.

This accepts source integration and component behavior. It does not establish browser console/network cleanliness, actual FMP dashboard behavior, image rendering, save/reopen or export in a running application.

## Candidate source pin repair

Source staging correctly rejected the stale Workspace pin in `contracts/sources.json`. The policy now matches the source lock at `74254b6`; source allowlists and the data API revision are unchanged. A repository-level regression exercises the existing `source_scope` validation for both sources. The initial run failed on the Workspace mismatch (1 failed, 9 passed); the repair and independent review each passed all 10 tests. This accepts source coherence, not image or runtime acceptance.

## Historical checkpoint: local packaged candidate and C4 readiness

The canonical `qopenbb_ci.image_cli` acquire/stage/export/load sequence completed with exit 0 through Dagger 0.21.8. Source staging used the committed Workspace `74254b6dc037277449d3a89c69d265aa61412eec` and data API `49cc413e6ab67eaa0444e07485b0f9243c786f7b`. The frontend bundle compiled; the archive passed the loader's identity and re-export checks.

- Loaded Linux/amd64 image: `sha256:46917e184c07578f1d054fedfa64de8a9fbf07886f6502198327ba46cbb3258a`.
- Image config digest: `sha256:283013c961dd4a4099a351f14a047cab585aaa7db3c5efaf9ec214fc00dff950`.
- Archive SHA-256: `0933d8a7fa9f1d7d346c93e584267ab6a2e6c136193074701a5c1ee350735a8c`.
- Local build reports: `/home/mc/qopenbb-work/combo-candidate-20261020-74254b6/`.
- Root `9422d28` checks passed in GitHub run `39397678391`; publication was skipped as intended.

A separate test-only Workspace commit `40426db` adds `tests/e2e/live-chart/combo-fmp.spec.ts`. It received independent source review after stale drawing evidence and line-width assertions were repaired. Syntax and captured fixture consistency were checked; the browser scenario is unexecuted. The production source lock intentionally remains at the exact candidate revision above.

The opt-in `QOPENBB_COMBO_FMP_EVIDENCE` directory must contain the ignored `raw.json`, `annual.csv` and `provenance.json`. The scenario verifies provenance, all 15 unchanged observations, separate axis drawing, an actual line-width change, saved assignments/style, reopen and PNG structure. Browser output may contain licensed data and must remain ignored. Missing evidence skips the scenario and does not count as acceptance.

Automatic approval review previously rejected the isolated runtime start with only `blocked by policy`. No equivalent runtime start was retried. This candidate has not been booted or browser-verified. C4/C5, real-FMP application acceptance and milestone publication remain open.

## Packaged application checks and refresh repair

The owner started the exact `46917e18` candidate in packaged-image-only mode at loopback port 55530. The shell/login check passed. The synthetic combination journey passed gallery changes, saved custom assignments, reopen and PNG export. The captured FMP journey passed on the same image: the actual File response retained all 15 original observations; tooltips before and after reopening matched all five fiscal periods, correctly rounded USD billions and USD/share values. Separate numeric-axis drawing, rendered line width, saved assignments/style and console/network diagnostics passed. Parent and independent reviewer privately inspected the exported financial PNG. Source-only approval is superseded by this runtime evidence for those journeys.

Browser evidence stays local in `browser-run-1`, `browser-run-2` and `browser-run-6` beneath `artifacts/chart-combo/`. The failed intermediate runs identified test assumptions about gallery labels, imported header title-casing, automatic date-tick thinning and compact number formatting. Corrections preserve all 15 input-value and formatted-display checks. Financial screenshots, response data, tooltips and raw browser results are not public artifacts. The accepted test corrections are committed at Workspace `c4702b0`.

The lifecycle check exercised Area & Column, hidden main-series/full-miniature behavior, a changed navigator range and theme retention. After correcting stale pointer coordinates and selecting the supported dashboard Refresh data action, it exposed a real defect: successful File refresh reset the navigator range. `browser-lifecycle-5` retains that failure. File widgets do not expose the navbar timer; the dashboard refresh action was used, with the actual completed File GET and its returned data verified.

C4c corrects the source defect at Workspace `61239915182fe409e517b70c81c68fc085e68b94`: the File query retains previous successful data only for matching source/parser identity while refreshing. This keeps the existing chart mounted without adding persisted interaction state or another chart owner. Four focused tests using the real File component, query hook and query client pass; independent review repeated them. The preceding RED run failed the same-source mount-retention case and passed the other three. Initial loading, changed source/parser and visible failed-refresh behavior remain covered.

The two production files pass the portable scope/complexity gate: 293/16 physical lines, 114/5 logical units and 26/2 maximum function units. A new optional-endpoint type error found during review was corrected. Final isolated baseline/candidate comparison reports the same 2,713 inherited TypeScript diagnostics, both exit 2, with no added diagnostics after normalizing line shifts. This is not a passing project-wide compilation.

The repair is source-reviewed; it still needs the lifecycle and FMP journeys on its rebuilt packaged image. C4/C5 and milestone publication remain open.

## Corrected candidate ready for runtime verification

Dagger build/export and portable image load completed with exit 0 for Workspace `61239915182fe409e517b70c81c68fc085e68b94`. Loaded Linux/amd64 image: `sha256:ddb58fb80a4eb4e13ab7bd6b6a0d600a6849baca6be771b7fe1832d8f9d972a0`; config digest: `sha256:c5b3a698745597581fba228a7c20bf4640ec819b99ab676006c6911f30f23a3c`; archive SHA-256: `dce49d0f6a5f2220dceb8a1090241398df74034fb05dcb7a39fa4849289fd33f`. Source-policy checks passed (10 tests), and root `54d61cb` CI run `39407716346` succeeded without image publication. The corrected candidate has not yet passed its browser acceptance gate.

## Corrected packaged-image acceptance

The owner started the corrected image `sha256:ddb58fb80a4eb4e13ab7bd6b6a0d600a6849baca6be771b7fe1832d8f9d972a0` at loopback port 55531. The runtime descriptor confirms packaged-image-only mode, no source overlay and ready Full configuration/login. The final batch passed the shell, synthetic combination save/reopen/export and captured-FMP journeys. Its lifecycle case stopped at login with HTTP 429 before exercising a chart. An isolated lifecycle run then passed in 17.4 seconds, with zero retries/skips.

The 429 was a test-scheduling failure: login allows five requests per minute per client IP. Startup consumes one login and the first two journeys consume four, including reopening. A later shell login succeeded; the lifecycle rerun used the normal login route after the window cleared. Neither headers nor rate limits were changed. Future runs must budget these logins and separate batches by a full minute plus a margin.

On the corrected image, actual FMP checks again verified all 15 unscaled File observations, all five fiscal categories and compact-formatted tooltip values before/after reopen, separate USD/USD-share axes, rendered width, saved assignments/style and PNG export. The lifecycle check verified both builtins, hidden-main/full-miniature behavior, changed navigator extent, theme retention and the completed dashboard-triggered File refresh with unchanged response data and retained interactions. All four journeys include their applicable console/network assertions. Raw reports, financial PNGs and failure captures remain ignored under `browser-final-6123991` and `browser-final-lifecycle-6123991`.

These results concern the bounded combination-chart milestone. They do not certify other unfinished renderer families, production-server deployment, all provider endpoints or a clean project-wide TypeScript compile. The previous refresh failure is resolved by source `6123991` in the identified packaged image.

Independent Astra feature review approved C4/C4c and the C5 review gate for this exact source/image. No blocking combination-chart gaps remain; publication is the outstanding delivery step.
