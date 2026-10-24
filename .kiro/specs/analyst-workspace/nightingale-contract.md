# Nightingale adapter contract

This inactive Table/File boundary combines the reviewed original journey with pinned source research. It does not activate Nightingale or accept replacement rendering. The [milestone](nightingale-milestone.md) owns completion. [Independent N0 review](../../../artifacts/reviewed/chart-nightingale/n0-review.md) approved this boundary on 2026-10-24. Workspace source: 5fd57cf6d22893b5a26510a6ba3f25726a4386d5.

## Data and financial meaning

The retained FMP example is AAPL FY2025 quarterly cost of revenue plus gross profit, reported USD. Q1 through Q4 totals reconcile exactly to reported revenue: 124300000000, 95359000000, 94036000000 and 102466000000. Revenue is the reconciliation reference, never a third stacked component. Fiscal periods come from fiscalYear/period, not calendar year of the report date. Raw source SHA256 is 390dc8cbfc8302720a203bd9782d5e3b1f7363a4f762bdfcef079dbbe4c72f6b, retained retrieval 2026-10-20.

The existing setup owner applies filtering, ordering, aggregation and then category/series inversion. The mapper consumes the selected snapshot and must not aggregate again. Repeated category text retains distinct row identity when not aggregated. Missing/nonfinite values remain missing; neither normalization nor ECharts adaptation may turn missing financial observations into zero.

## Source-derived geometry

Nightingale is an equal-angle categorical chart with a linear numerical radius. It does not encode values proportionally to sector area. Category bands are centered on category rays, clockwise from the top; grouped visible series divide a band in selected order, while stacked series share it. One category spans a complete circle.

Group Type is saved at model-root seriesGroupType: grouped, stacked or normalized. An absent root uses the engine's stacked default. The pinned theme validator drops normalizedTo/grouped/stacked from saved theme overrides; retain those inactive stored keys without activating them. Explicit normalized mode uses 100. Direct standalone-series custom normalization is outside this Table/File contract. Group Type is structural state, not a theme override.

Stack positive and negative values separately. Include zero and visible cumulative extents in the radial domain, then apply the existing span-aware 1/2/5/10 nice-tick behavior. Do not inherit Radar's raw-value extrema for stacked data.

For normalized mode, each category's denominator is max(positive stack total, abs(negative stack total)). Geometry is scaled to 100; raw tooltip and series-label values remain the selected post-setup values. Count aggregation uses count display, never currency display. The original normalized radial ticks are plain numbers (0 through 100 in the compact positive example), without a percent suffix. Use a neutral numerical axis formatter separately from raw amount/count tooltip callbacks.

Legend filtering recomputes visible grouping, signed totals, normalization and radial domain without changing category order. Preserve the existing transient legend owner. All-zero and empty edge behavior remains source-derived; do not claim absent hover targets prove absent input values. The original normalized mixed view loses the entire Primary series when D is missing. On 2026-10-24 the owner explicitly approved keeping valid values visible: the replacement omits only the missing observation, preserving valid earlier/later values and all other series. Add focused normalized-missing regression coverage. This is an intentional correction, not strict original parity.

## Appearance and controls

Keep the existing family/option name nightingale, palette, fonts, caption, legend, background, chart padding and tooltip owners. The original has Series stroke width/dash/opacity, fill opacity and labels; no markers or shadow. Polar Axis has color, thickness, inner-radius ratio and font/weight/size/color/orientation. It has no Radar Shape control and no radial Group/Series Padding section. Inner radius is a fraction in [0,1], step 0.05. Orientations are fixed, parallel and perpendicular.

Preserve unedited inactive options. Shared editors must not accidentally route Nightingale through Pie or expose Radar-only controls. Thickness and inner-radius edits apply to angle-category and radius-number axes; label orientation applies only to angle-category. Navigator and mini-chart actions remain reachable and persist their common options, but produce no additional Nightingale drawing or slider. The original screenshots are identical before/after both actions and reload; intermediate saved flags lag, so this does not promise synchronous timing.

Use native ECharts polar bars as the implementation starting point. Adapt explicit category IDs, original domain/ticks and raw tooltip formatting. A bounded graphic text layer may be necessary for category-label orientation. The source investigation found no established stacked-border incompatibility warranting a custom sector engine.

The original inbuilt palette uses chart-background sector strokes; custom palettes retain their stroke colors. Resolved ApplicationThemeInput no longer identifies palette provenance. N1/N2 therefore preserve supplied palette strokes and explicit overrides; N3's existing caller/themeInputs owner must use its selected.palette authority to supply background strokes when a custom palette is absent. Never infer this distinction from theme name alone. Add a caller regression for both paths.

## Shared interfaces and ownership

The controller freezes compatibility/nightingaleContracts.ts and the reconciled shared fixture before N1/N2 fan-out. No runtime registration belongs to these declarations. N1 owns only the new assignment/data/series/layout/mapper modules and focused tests. N2 owns only the new appearance/selection/editor/transaction/control modules and focused tests. Neither edits shared routing or imports the other lane's implementation.

The editor transaction returns either an option patch or a root Group Type mutation. The existing session reducer owns stale-command validation and persistence. Group Type edits clone the current model, change only seriesGroupType, preserve the same capture and request render. Include this root field in stale-baseline checks. Existing ordinary setup transitions preserve the complete model; do not add a second Group Type owner to ordinary setup state.

N3 serially integrates the named capture policy, family unions, setup control, session dispatch, callers and Customize routing. The existing ECharts host owns lifecycle, resize, export and legend callbacks. Every changed production file is subject to 400 physical lines, 300 logical units and 50 units/function, with controller-owned inventory updates.

## Original evidence and remaining acceptance

The original one-worker journey passed in 44.5 seconds at frontend 38dffc33389aca0e4a87e0e88d42f7067aa220df, image sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f with the qualified backend-only overlay. Single, grouped, stacked and normalized views returned exact native raw-value tooltips; hidden Secondary left only the three Primary tuples. Group Type, aggregation/inversion, axis edits and final reload were exercised. Two observation assumptions were rejected: original paths are native Path2D Beziers, and stacked series render through an offscreen layer. The current probe uses visible labels to choose source-informed hover points; actual native tooltip identity is the runtime assertion. These points are not independent exact geometry measurements.

Original diagnostics are not clean: Unexpected token < and a CSV request failure remain recorded on the routed reference journey. The passing behavioral test is not clean transport acceptance. Separate signed accumulation, denominator, precise geometry and degenerate edges remain source-derived. No exact mixed-data tooltip or full-boundary measurement is claimed. N4 still requires an identified packaged replacement with real FMP data, light/dark parity, financial values, refresh, fresh-session reopen and export. No synthetic original probe establishes that acceptance.

## Frozen lane paths and completion checks

N0 declarations are `terminalpro/src/components/General/Table/Chart/compatibility/nightingaleContracts.ts`; the shared fixture is `terminalpro/tests/unit/chart-compatibility/fixtures/nightingaleContract.ts`. Both lanes consume these declarations. The original regression is `terminalpro/tests/e2e/live-chart/nightingale-original.spec.ts`.

Paths below are relative to `terminalpro/src/components/General/Table/Chart/`:

- N1 owns `compatibility/nightingaleAssignments.ts`, `echarts/nightingale.ts`, `echarts/nightingaleData.ts`, `echarts/nightingaleSeries.ts`, `echarts/nightingaleLayout.ts`, plus new `terminalpro/tests/unit/chart-compatibility/nightingaleMapping.test.ts`, `nightingaleEngine.test.ts` and `nightingale.fixtures.ts`. The controller authorized the test-only helper to share inputs without importing a test module and registering its tests twice. Exports are resolveNightingaleAssignments and translateNightingale; pure mapping takes already selected data, resolved appearance, Group Type, viewport and transient legend selection.
- N2 owns `application/nightingaleSessionSelection.ts`, `application/nightingaleAppearance.ts`, `application/nightingaleEditorState.ts`, `application/nightingaleEditorTransaction.ts`, `editor/nightingale/NightingaleControls.tsx`, plus new `terminalpro/tests/unit/chart-compatibility/nightingaleSession.test.ts`. Exports are prepareNightingaleSelection, resolveNightingaleAppearance, projectNightingaleEditorState, mapNightingaleEditorIntent and NightingaleControls. Group Type remains in Set Up, not the Polar Axis Customize panel.
- N3 owns shared joins only after both lanes pass: family/session unions, named capture policy, setup projection/selection, session dispatch/runtime, useApplicationChartSession, AgChartView, caller input/theme/generated-option guards, Customize/Series editor routing, comboEditorMode and ChartSetupPanel. New nightingaleSessionProjection.ts owns composition. Freeze the exact modified list and whole-file measurements at the join; neither parallel lane changes these files.

N1 numerical checks must cover separate signed totals, maximum-absolute-extent normalization, duplicates/order, empty/all-hidden, zero/missing values and the authorized missing-series correction. Verify native polar options using the existing engine test approach; do not create an alternate renderer. N2 checks cover model-root versus option mutation, defaults, applicable-axis paths, unsupported-neighbor intents and raw/count/normalized display separation. Both lanes preserve inactive options and existing state owners.

Use the existing scoped Biome and strict TypeScript baseline comparison, syntax/combined inventory checker and focused Vitest entry points from package.json/vitest configuration. Record actual commands and results in each handoff. Tests and documentation are excluded from production size caps. The controller alone updates inventory, source locks and change manifests. New helper ownership requires an explicit plan amendment before concurrent edits.

With the pinned Node 24.22.0 on PATH, run from `vendor/workspace/terminalpro`:

```sh
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/nightingaleMapping.test.ts tests/unit/chart-compatibility/nightingaleEngine.test.ts --maxWorkers=1
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/nightingaleSession.test.ts --maxWorkers=1
```

Each lane runs only its command and scoped `node node_modules/@biomejs/biome/bin/biome lint` with its explicit changed paths. From the repository root, compare `node verification/node_modules/typescript/bin/tsc --noEmit -p` using a lane-specific config and the unchanged import baseline under `artifacts/chart-nightingale/interfaces/`; four inherited diagnostics currently remain. Measure production paths with `node tools/quality/syntax_units.ts` using an explicit JSON path list on stdin. The controller runs `pipeline/.venv/bin/python -m tools.quality.complexity --check --changes workspace=MANIFEST --changes data_api=MANIFEST --output REPORT` with the actual scoped manifests. This records combined coverage independently of browser and image acceptance.
