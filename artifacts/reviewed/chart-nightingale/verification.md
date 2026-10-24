# Nightingale contract verification

N0 Workspace source `5fd57cf6d22893b5a26510a6ba3f25726a4386d5` is independently accepted: original observations, retained financial fixture and inactive interfaces are frozen for the two implementation lanes. No replacement renderer, live routing, packaged financial browser acceptance or new image publication is claimed. The [contract](../../../.kiro/specs/analyst-workspace/nightingale-contract.md) separates observed behavior from source-derived numerical semantics.

- Original frontend: `38dffc33389aca0e4a87e0e88d42f7067aa220df`; image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`. The disposable comparison used a backend-only source overlay, 43 files with hash `23b6323e40a2edaa7267e25f72d032da8e92ccef09cc09545cb749fe2d2a15de`. It is not an unmodified image-only release test.
- One isolated original Playwright journey passed in 44.5 seconds, one worker, no retries. The retained run is `artifacts/chart-nightingale/original/run-20261024T120528Z-sl2tbb`. Probe SHA256: `dbbaebd66ee91c0af9734b0c9173273a1df8f3183bee92134c2d4aebb7fa69be`.
- Native tooltips identify every compact single/grouped/stacked/normalized datum and preserve raw amounts. Legend hiding, aggregation/inversion, axis controls, navigator actions and saved-model reload were exercised. Interior hover targets are source-informed, not independent measurements of exact sector geometry. Mixed data has screenshot/model coverage, not exact negative/missing tooltip acceptance.
- Original normalized missing data hides the whole affected series. On 2026-10-24 the owner approved correcting this: retain valid observations and omit only the missing observation. This is a documented behavior difference, not a strict parity claim.
- Diagnostics are not clean: the routed original retains an `Unexpected token '<'` error and a failed CSV request during reload. Behavioral test success does not certify clean transport. The final saved chart still renders.
- The retained FMP AAPL FY2025 fixture contains four quarterly cost-of-revenue/gross-profit pairs in USD, plus revenue reconciliation references. All 12 amounts, four dates and four additive totals match the hash-verified 40-record response, SHA256 `390dc8cbfc8302720a203bd9782d5e3b1f7363a4f762bdfcef079dbbe4c72f6b`, retrieved 2026-10-20. Revenue is not a third stacked component. No new provider request was made.
- The inactive declaration measures 177 physical lines and 110 logical units, with no executable functions. The combined checker exits 0 with no errors or violations. Scoped Biome lint and syntax parsing pass. Strict TypeScript current/baseline logs are identical: four existing dependency diagnostics, no new declaration diagnostics. This is comparative checking, not a clean application compile.

## Commands and limits

The existing isolated Playwright configuration runs `nightingale-original.spec.ts` with the qualified original descriptor and a uniquely allocated evidence directory. Credentials, state, raw provider responses and raw browser logs remain local. Earlier failed runs are retained: context arcs did not observe native Path2D; exact tooltip text uses newline fields; stacked series render offscreen. The final probe removes path instrumentation and retains fresh-paint provenance, visible screenshots and exact native tooltip checks.

Scoped static commands use pinned Node 24.22.0, the existing Biome CLI, TypeScript 6.0.3 and `tools/quality/syntax_units.ts`. The combined gate was:

```sh
pipeline/.venv/bin/python -m tools.quality.complexity --check --changes workspace=artifacts/chart-nightingale/interfaces/workspace-changes.json --changes data_api=artifacts/chart-nightingale/interfaces/api-changes.json --output artifacts/chart-nightingale/interfaces/combined.json
```

The source characterization and inactive declarations do not require a feature RED/GREEN claim. N1/N2 must add focused numerical, native-engine and mutation regressions before activation. N4 still owns identified packaged real-FMP checks, light/dark appearance, refresh, fresh-session reopen and export. Real-data milestone screenshots remain pending; synthetic reference screenshots are not published as FMP samples. The previously published Radar alpha and local Compose data are unchanged.

## Inactive implementation acceptance

N1 and N2 passed independent review on 2026-10-24, committed separately as `f6f6c1721248b1b4e201a96f7dc8bd1c992787c1` and `7cffa0894c494ebe59769d4df9a055135a72d65f`. Both remain inactive until N3 connects the existing Table/File application. No packaged image or UI acceptance is inferred from these checks.

- N1: ten focused tests pass (six mapping, four actual native ECharts SVG engine). The tests cover signed/normalized geometry, centered category bands, grouped widths, sparse missing/negative observations, duplicates and the owner-approved missing-value correction. Native polar bars render the sectors; a bounded graphic layer handles category labels. Five production modules pass caps, maximum 179 physical lines, 52 logical units and 19/function. Scoped lint passes eight files; the controller's combined gate exits 0. [Independent renderer review](n1-review.md).
- N2: eight focused tests pass, including a mounted control emitting its orientation intent. Group Type mutations remain at model root; appearance edits map only applicable polar axes and preserve inactive options. Five production modules pass caps, maximum 147 physical lines, 58 logical units and 21/function. Scoped lint passes six files; the controller's combined gate exits 0. [Independent controls review](n2-review.md).
- Both scoped strict TypeScript comparisons retain the same four inherited diagnostics without additions. Reviewers independently reran the focused tests and lint and verified frozen source hashes. RED evidence includes missing implementation and concrete grouping/angle failures before correction.

N3 must preserve model-root Group Type during setup and reject stale root edits, connect the existing state owners and controls, and supply original background strokes for inbuilt palettes through caller palette provenance. Custom palette strokes must remain intact. N4 still owns real-FMP browser, theme, refresh/reopen/export and appearance acceptance; one publication follows the accepted milestone.

## N3 application integration

N3 at Workspace `716cd1a95087d9c1d3755b8192671a48f48b2192` passed independent integration review and the combined complexity gate on 2026-10-24. The existing Table/File owner now routes Nightingale data, setup and customization to native polar bars. Root Group Type is persisted with stale-command protection; built-in palette strokes use background colors while custom strokes remain supplied values. The approved sparse normalized behavior keeps valid observations visible.

Fresh independent owner/editor checks pass all 11 tests; scoped lint passes all 29 present files. The 24 production files fit the 400/300/50 caps (maxima 357/140/42). Strict TypeScript has 2680 inherited diagnostics on both baseline and candidate, with no normalized delta; this is not a clean application compile. Packaged real-FMP rendering, export and fresh-session persistence remain N4. See n3-review.md.

## N4 first packaged checks and layout correction

The original FMP reference passes (original-run-2, 29.6 seconds). Candidate image `sha256:5beffd2ad3136b8a7d478c3b72c334d4ecbaf029cba261990414e5851604f130` from Workspace `716cd1a` reaches grouped/normalized geometry, raw tooltips, native legend hide/restore and count aggregation checks. The complete journey is not accepted: retained runs exposed test selectors that must follow displayed title-case labels and region roles, plus an inappropriate Pie-only legend helper. Export and fresh reopen remain unverified.

Matched captures exposed extra radial lines and diagonal value labels. A bounded layout correction removes those lines, moves values to the top ray and adjusts spacing while preserving the native numerical scale. Independent review, 11 focused tests, scoped lint and the combined complexity gate pass; limits are 205 physical lines, 49 logical units and 12/function. Rebuilt appearance remains unverified. See n4-layout-review.md.

## N4 accepted packaged evidence

The refined candidate passes the complete one-worker journey (candidate-run-4, 1.2 minutes) against retained FMP AAPL FY2025 quarterly cost of revenue and gross profit in reported USD. The original reference passes in 29.6 seconds. Candidate image `sha256:6edd63b48c0c265a18d8c06315a037691ab98d9fe332bfeac8efc7a850c60604` has source `596a5234f7dec5c672dd97b09e365bfb90aac755`; actual Docker labels and the sole disposable data bind are verified.

Checks cover exact component values, grouped/stacked/normalized geometry and raw tooltips, native legend hide/restore, count aggregation, stroke and axis effects, nonzero inner radius, orientation, refresh, PNG export and fresh-session save/reopen. Candidate diagnostics pass. The original retains known transport diagnostics. The owner accepted the refined light appearance in qView on 2026-10-24. Light/dark captures are published; canvas heights differ by one CSS pixel at DPR 1, so these are matched-view comparisons, not pixel-identical claims. Independent review: n4-review.md. Local acceptance does not certify future CI-built image bytes.
