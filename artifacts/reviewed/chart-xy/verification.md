# Scatter and bubble verification

X1 is accepted at Workspace `e343e16499ba2a087a90ee6e4dd1091a3b4e2bc9`. The inactive resolver preserves selected column order, paired/unpaired scatter and bubble grouping, default pairing and incomplete-group behavior. It rejects malformed identities atomically and does not mutate supplied state. No chart routing, editor or geometry has been activated.

Independent Astra review approved the assignment contract against retained AG Grid Enterprise 34.1.1 `getSeriesDefinitions` and `isPaired`. Independent Sol implementation review then inspected the actual module/tests and repeated the focused checks.

From `vendor/workspace/terminalpro`, using pinned Node 24.22.0 in WSL:

```sh
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/xyAssignments.test.ts
node node_modules/typescript/bin/tsc --noEmit --strict --skipLibCheck --target ES2022 --module ESNext --moduleResolution Bundler --types node,vitest/globals src/components/General/Table/Chart/compatibility/xyAssignments.ts tests/unit/chart-compatibility/xyAssignments.test.ts
```

Both commands exited 0; 33 tests passed. The preceding RED run recorded 31 failures and two passes against an empty resolver, including intended grouping failures. Raw logs remain ignored under `artifacts/chart-xy/x1-{red,green,tsc}.log`.

The portable combined complexity gate passed with explicit Workspace/data-API scope manifests: 89 physical lines, 72 logical units and largest function 17. No errors or violations. The maintained inventory includes the module. Independent review approved X1 with no findings. Final Git whitespace checks required normalizing mixed line endings in the two new files; their code was unchanged.

X1 does not establish rendering acceptance. The next section records the separately reviewed inactive mapper.

## X2 numeric mapper

X2 is accepted at Workspace `7e509d323cfb4b659c5071786d78744a9e8338e0`. The pure mapper retains raw X/Y observations, independent bubble-size domains, missing/negative/equal size semantics and point identities. It does not activate application routing or write saved state.

Independent Astra design review resolved explicit axis bounds, appearance precedence, grid-helper compatibility and triangle anchoring before implementation. Independent implementation review found tooltip rows in X/Y/size order rather than the original descending numeric order. The correction sorts raw tuples before formatting, preserving stable ties and duplicate labels.

Using the same pinned Node and Vitest configuration, `xy.test.ts`, `xy.render.test.ts` and `xyAssignments.test.ts` passed 64/64 tests: 31 X2 and 33 X1. Independent review repeated this command successfully. Actual ECharts SVG rendering checks cover numeric coordinates, scatter and variable-size bubble triangle placement, supported bounds, and datum tooltip identity for overlapping points. RED evidence includes the initial absent implementation, derived-layout overflow and three tooltip-order failures. Raw logs remain ignored in `artifacts/chart-xy/`.

Scoped strict TypeScript reports only inherited `src/components/ds/plugins/typography.ts:1` TS2578 and no XY diagnostics; this is not a clean project compile. The final combined complexity gate exited 0 with no errors or violations. Eight production files measure 37-185 physical lines, 14-88 logical units and at most 14 units per function; all are inventoried.

One-sided explicit bounds excluding all observations currently return an invalid diagnostic because ECharts otherwise reverses the extent. Source characterization establishes that the original renderer instead uses an empty domain with invisible points. The inactive contract permits this temporary safety response, but X4 must implement original-compatible empty geometry before feature acceptance.

Independent review approved the bounded mapper after the tooltip fix. Editor integration, original visual parity, actual FMP application/lifecycle checks and publication remain open. No image build was dispatched for these source-only tasks; the published combination-chart alpha remains the development release.

## X3 editor/session integration and X4 source join

Workspace `ea740ce32571cfb70e22baecc5ef38a4cc211188` connects scatter/bubble to the existing Table/File chart session and controls. X3 source acceptance is complete; X4 packaged-image acceptance remains open. The published alpha still contains the preceding combination milestone.

The integration preserves paired field order, labels, mixed units, empty/incomplete selections, stamped edits, refresh and saved XY settings. Numeric navigation retains at least four observations where available. One-sided bounds excluding all observations now produce empty geometry and restore when removed. These are source and component results, not a claim that the candidate browser journey has passed.

Independent Astra review initially rejected two reachable control defects: collapsing appearance layers lost saved-format precedence, and numeric axis position controls were absent. Focused RED tests reproduced both failures. The correction preserves ordered layers and restores X top/bottom and Y left/right choices through the existing transaction owner. Rereview approved the source; actual ECharts SVG checks verify moved axes.

Verification used pinned Node 24.22.0 and `node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs` or the corresponding `chart-compatibility/vitest.config.mjs`, with selected test files:

| Scope | Result |
| --- | --- |
| XY and shared application/setup/caller/editor regression, nine files | 119 passed before final review repairs |
| Final XY session, editor and owner tests after repairs, three files | 15 passed |
| XY mapper and real-engine SVG checks before repairs | 31 passed |
| Final real-engine SVG checks, including restored bounds and top/right axes | 6 passed |
| Existing host, lifecycle and navigator regressions | 35 passed |

The final explicit-scope combined complexity gate passed for all 39 changed production files. A fresh baseline-relative TypeScript comparison used the unchanged baseline test universe: both revisions report the same 2,713 inherited diagnostics, with none added or removed. This excludes new tests from that comparison and is not a clean full compile. Local commands, logs, source hashes and scope manifests remain under ignored `artifacts/chart-xy/join*`.

The three new XY browser files passed syntax checks and independent source review. They assert complete main-plot point geometry, raw captured-FMP coordinates and linear size mapping, lifecycle behavior, and decoded exported-PNG geometry. No browser execution or candidate-image acceptance is claimed here. Bound restoration uses session/mapper/real-engine tests because the existing UI has no bound editor. Raw FMP data and financial screenshots remain private.

## First candidate and empty-selection recovery

The local Dagger image `sha256:81643ec13f83532de0724c43816d307b0116ca7062b80d16a6a1f66efca98d10` identifies Workspace `ea740ce`. Image-only startup at loopback port 55532 passed Full configuration and login readiness, with no source overlay. Root CI run `39425411045` passed checks; this did not publish a new alpha.

The captured-FMP journey passed against that image after correcting the browser observer. It verifies five raw observations and linear EPS diameters, tooltip values, a complete numeric navigator window and reset, both themes, File refresh, save/reopen, decoded exported-PNG geometry, and application/CDP diagnostics. The synthetic journey exposed a product defect: after removing every numeric field, the first Add X did not restore a series. A separate run waited for that first add before attempting another, ruling out a rapid-edit race. X4 remains open.

Observer repairs are committed at `2f4b029`: use accessible heading/chip locators, force an actual resize and restore the original canvas size, remove hover enlargement before geometry measurement, and assert observable numeric zoom with a stricter reset tolerance. Independent review confirmed that complete-point, raw-value, diameter and PNG assertions remain intact. Earlier diagnostic runs and two interrupted launches are not passing evidence; financial attachments remain ignored.

The recovery fix at Workspace `e64ce8c5760703d23cd003ca2c4497a39e90cea1` propagates the existing XY empty-selection policy through two missed setup validations. Ordinary chart validation defaults are unchanged. The owner regression reproduced rejection before the fix and then passed Labels changes and sequential X/Y re-addition after empty-selection refresh. All 25 focused owner/setup/transaction regressions passed; independent review approved the bounded fix. Both production files pass the combined complexity gate, and the repeated baseline-relative TypeScript comparison adds no diagnostics.

README and renderer checkboxes were reconciled: source integration remains checked; rebuilt-candidate acceptance and publication remain unchecked. The next gate is the rebuilt image's synthetic recovery and FMP journeys, followed by previous-family regressions. The first candidate's FMP result does not certify the rebuilt candidate.

## X4 accepted application milestone

Independent Astra review approved X4 on 2026-10-20. The corrected image `sha256:e7cb9923ae29338539dd215378bb8618352e05401b499c15eba16997ce6ca3f4` contains production source `e64ce8c5760703d23cd003ca2c4497a39e90cea1`, without a source overlay. Workspace `17a35f3468452c5ae92cbf9f57de4d7bd92cde12` changes only the two browser test files; application/build inputs are unchanged.

| Final packaged-image check | Result | Local evidence under artifacts/chart-xy |
| --- | --- | --- |
| Synthetic Bubble and captured-FMP Bubble | 2 passed, 42.1s | browser-e64ce8c |
| Multiple-series Scatter | 1 passed, 23.6s | browser-e64ce8c-scatter-innertext |
| Previous combination family | 1 passed, 16.8s | previous-combo-e64ce8c |
| Previous ordinary families, including backend restart | 1 passed, 1.0m | previous-ordinary-fixed-e64ce8c |

All final commands exited zero, with one browser worker, no retries, skips or flaky results. Tests ran through the existing live-chart Playwright configuration on port 55533. The ordinary regression first exposed a test-only absent-class comparison bug; normalizing the missing class to false fixes it without weakening theme assertions. Scatter tooltip checks use rendered innerText to retain visible line breaks. Both test edits received independent Sol source review.

Scatter verifies six complete signed-coordinate observations across two shared-X series, marker diameter, series-specific tooltips, reordered saved fields, themes, refresh, save/reopen, export and application/CDP diagnostics. Bubble verifies raw FMP coordinates and linear EPS sizes, synthetic missing/signed/equal sizes, aggregation, empty-selection recovery and numeric navigation/reset. Captured AAPL annual income-statement data covers 2021-2025; raw SHA256 is `9e0dae1fb5c1d067473f7f9749cb4969afc6d767ebaa4358376215ff4ea42648`. Financial screenshots and raw data remain private.

This establishes the defined ordinary Table/File milestone, not exhaustive visual parity for every marker or interaction permutation, standalone/AI callers, or complete renderer replacement. X5 registry publication and anonymous pull verification remain open.

## X5 published alpha

[CI run 39432626385](https://github.com/norandom/QOpenBB/actions/runs/39432626385) passed checks, both Dagger builds and publication from root `b5feb442312c5ecc4c80bbc94d16ccf4ccc4896f`. [Tagged prerelease alpha-39432626385-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-39432626385-1) includes Compose, the environment template and manifest. Workspace is pinned to `17a35f3468452c5ae92cbf9f57de4d7bd92cde12`; data API remains `49cc413e6ab67eaa0444e07485b0f9243c786f7b`.

- workspace: `ghcr.io/norandom/qopenbb-workspace@sha256:7738ba65854e5d049c9117f27d9549d62007ee4187a31fa1827d7a0d0537d0bb`.
- data-api: `ghcr.io/norandom/qopenbb-data-api@sha256:2d7f8b3daa9e6f5b565725cbe3454002329c6ae7a4371285849f2721c93d099c`.

Six pulls succeeded with a fresh empty Docker configuration: digest, release tag and latest for each service. Registry configuration digest, source labels, architecture and pulled digest matched the release manifest. Local reports are under `artifacts/chart-xy/release-39432626385/`; credentials and image archives are excluded. The registry images were rebuilt by CI; application acceptance was performed on the identified local candidate above, not on the pulled release images. README, renderer checklist, roadmap, install links, spec and breadth records are reconciled. Assembled Compose, owner-server deployment and remaining chart families are still open.

The first anonymous verifier attempt stopped after a successful pull because it assumed Docker image IDs always equal configuration digests. This daemon reports manifest IDs. The corrected verifier accepts either identified storage representation while independently checking registry configuration and manifest digests, labels and pulled references; all six final pulls passed.
