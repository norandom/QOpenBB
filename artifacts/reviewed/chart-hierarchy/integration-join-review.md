# H3 application integration review

**VERDICT: APPROVED for the frozen H3 application join.** No unresolved blocking finding remains in this scope. This accepts the source integration and its bounded unit/integration evidence; it does not establish H4 packaged/browser acceptance, financial examples, release or deployment.

Reviewed against the [canonical integration design](../../../.kiro/specs/analyst-workspace/hierarchy-integration-design.md) and [renderer design](../../../.kiro/specs/analyst-workspace/hierarchy-renderer-design.md), including the immediate-control stamp amendment and narrowly approved lifecycle/Histogram owner amendments. Independent reviewer inspected evolving source, requested concrete corrections, then verified the frozen result without editing production or maintained tests.

## Frozen scope and ownership

Base Workspace revision: `15db313febfda9d9a30b2b2f442daed54183d447`. `artifacts/chart-hierarchy/h3-join/frozen-files.json` contains all 35 changed/new paths: 29 production owners and six changed tests. Its SHA-256 is `e11c23bd25aad29decf4bbcc72e62f8e344856fd38082387c87afd5682ebf90c`.

The reviewer compared the production manifest with the actual tracked diff plus untracked Chart source: no missing or surplus production owner. All 35 content hashes matched before and after independent checks. Evidence: `artifacts/chart-hierarchy/h3-join/reviewerlogs/freeze-before.json` and `freeze-after.json`. Unrelated Perspective/financial files are outside this review.

The parent combined inventory gate covers all 29 production owners with zero errors/violations. Largest measured file: 394 physical lines; maximum logical file size: 229; maximum function: 50. These satisfy 400/300/50 whole-file caps. Evidence: `artifacts/chart-hierarchy/h3-join/combined.json`, `reviewerlogs/combined-summary.json`. Worker final lint exits 0 over 36 paths, including the unchanged hover test dependency.

## Contract findings and resolution

Paths below are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/`.

- **Capture and transaction boundaries:** `application/applicationSessionGuards.ts`, `applicationSessionCapture.ts`, `applicationChartProjection.ts`, `applicationSessionDispatch.ts` and `applicationSessionRecapture.ts` discriminate the own hierarchy kind and family before entering ordinary contexts. No fabricated scalar snapshot or fake category alias remains. Grid recapture completes before `owner.transact`; accepted H1 transitions are rerun against current storage. Recapture must match its full originating command stamp, ordered category request and required numeric fields, then pass current generation/data freshness. Immediate appearance controls allow render-only drift, preserving same-turn control behavior; asynchronous error/export/hover checks remain strict.
- **Ranges and family transitions:** `caller/chartInputs.ts` and the shared hierarchy range route preserve explicit saved empty/category-only/number-only ranges. Initial numeric membership uses public collection order, with roles following candidate range order. Gallery normalization remains distinct from invalid saved over-cap selections and removes the synthetic default category. The draft regression in `application/familyTransition.ts` globally preferring numeric collection order was repaired: ordinary `familyColumns` again uses its descriptor semantics; only hierarchy gallery normalization receives selected order followed by unselected public numeric order. The ordinary caller regression is green.
- **Live editor and empty selection:** `caller/LiveChartEditor.tsx` and `editor/ApplicationChartEditor.tsx` branch to hierarchy Setup/Customize before ordinary controls. `AgChartView.tsx` retains active no-size hierarchy sessions. Real-hook tests cover ordered category recapture, removing all categories/numbers, persisted empty range and Treemap → Sunburst → groupedColumn → Treemap with capture-kind assertions. An independent real editor probe removes both numeric fields through visible Setup buttons and the actual hook/Widget transaction owner.
- **Theme/generated precedence:** `caller/themeInputs.ts` now distinguishes Treemap group text color/base font from contrasting tile/sector background color and source-specific font/minimum ratios. A draft generic typography override and subsequent group-ratio error were corrected. Generated label/tooltip defaults and explicit overrides remain data-only, with effective hierarchy appearance layered through accepted H2 selectors. Maintained tests exercise light/dark/custom group, tile and Sunburst behavior.
- **Hover and lifecycle:** `echarts/EChartsHost.tsx` transports the plan. `lifecycle.ts` installs hierarchy subscriptions only when needed, invalidates plans before render/resize, keeps accepted plans on stale requests, and detaches ownership before cleanup/native errors become observable. `application/useApplicationChartSession.ts` refreshes hierarchy render revision even for same-size positive resize; this repairs the draft case where expired coordinates could never receive a new plan after same-size or zero-size recovery. Zero-size cleanup failure releases the instance and invalidates export. The new `lifecycleHierarchyHover.ts` owns only binder/expired-plan state; main generation/revision/export ownership remains in lifecycle.
- **Ordinary preservation and caps:** `projectLifecycleOptions` in `echarts/lifecycleLegendProjection.ts` retains the original legend → retained navigator → navigation-window → Histogram-axis order and prior-pending semantics without unconditional native reads. `application/histogramEditorTransaction.ts` only adds explicit rejection of three hierarchy panels. Existing ordinary test changes are narrowing guards and a `satisfies` fixture declaration; no behavioral assertions were removed.

## Independent verification

Checks ran in WSL Debian as `mc`, using the pinned Node 24 binary and existing dependencies, bounded to one Vitest worker. No image build, installation or browser runtime was started.

| Independent check | Result | Raw evidence under `artifacts/chart-hierarchy/h3-join/reviewerlogs/` |
| --- | --- | --- |
| Hierarchy session/owner, actual callerRoute and Histogram production join | 65 tests, exit 0 | `maintained-application.log`, `.exit` |
| Existing lifecycle and hierarchy hover binder | 38 tests, exit 0 | `maintained-lifecycle.log`, `.exit` |
| Additional actual editor/hook and native lifecycle boundary probes | 7 tests, exit 0 | `boundaries.log`, `.exit` |

The seven additional probes exercise actual editor dispatch, tooltip-off hover, same-size revision refresh, no-size persistence, both-direction family capture replacement, stale/resize/zero-size plan handling, hierarchy-to-ordinary expiry and native hover error/export cleanup. The first artifact run failed before tests because its external test location needed JSX-runtime aliases and a partial ECharts mock. A subsequent editor fixture called resize before Widget-owner registration; moving that explicit action after registration resolved the empty DOM. These were reviewer-harness corrections only; final sources still match every frozen hash. Prior output is retained in `boundaries-initial.log` and `boundaries-prior.log`.

Worker evidence was also inspected: 159 application regression tests, 19 additional Histogram tests and 38 hover/lifecycle tests all exit 0. Their final raw logs/exit files are in `artifacts/chart-hierarchy/h3-join/`. Early development RED logs were overwritten during iteration; the observed failures and controller corroboration establish their provenance, but this review does not claim separately retained raw RED artifacts or failure hashes.

## Compiler limitations and acceptance boundary

Both actual TypeScript 6 projects exit 2 before and after. Application diagnostics remain 3480; compatibility rises from 3489 to 3490. Full-message comparison, allowing line movement, finds no new changed-owner logic/type error. It is not a clean or byte-identical compilation.

The one newly exposed compatibility diagnostic is TS2882 at unchanged accepted `editor/hierarchy/HierarchySetupPanel.tsx:10`, importing `../setup/chartSetupPanel.css`. The ready union makes that module reachable; the broad compatibility configuration lacks the Vite CSS declarations. The import already exists in the accepted UI and application baseline. This is newly exposed inherited configuration debt, not a newly introduced source import or missing stylesheet.

Six external diagnostic messages change at identical file/line/column/code locations in both scopes. `Widget.context.tsx:16:37` and `MonacoEditor.tsx:247:16/30` retain the same missing `params`/`sqlParamDefs` failures; only the displayed `Omit` union order changes. `src/lib/state/app.ts:664:13`, `1215:13` and `2122:13` retain TS2345 and the same terminal optional `data.name` versus required string incompatibility; their truncated union display order changes. Exact before/after blocks are retained in `reviewerlogs/static-classification.json`, alongside the worker `static-comparison.json` and raw baseline/final compiler logs. No upstream configuration expansion was required for this bounded join.

H4 remains necessary for real browser rendering, visible controls, packaged resize/export, real-FMP financial examples and fresh-session persistence. This approval makes none of those claims.
