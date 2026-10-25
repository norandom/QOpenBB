# Treemap/Sunburst renderer and controls

Implement the inactive renderer and controls against the accepted shared declarations at Workspace `fc0f02f`. H1c alone owns financial preparation. The [independent join review](../../../artifacts/reviewed/chart-hierarchy/renderer-final-design-review.md) accepts the readiness decisions dated 2026-10-25. Live integration remains H3 and packaged visual/financial acceptance remains H4.

## Shared contract and scope

The executable declaration owners supersede earlier draft types: `application/hierarchyPaintTypes.ts`, `hierarchyAppearanceTypes.ts`, `hierarchyEditorTypes.ts`, and `echarts/hierarchyModel.ts`, `hierarchyHoverTypes.ts`, relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/`. Their [independent review](../../../artifacts/reviewed/chart-hierarchy/renderer-types-review.md) establishes type shape, not runtime behavior.

Reuse the [hierarchy contract](hierarchy-contract.md), [setup design](hierarchy-setup-design.md), existing ECharts host, option baseline composition, reducer, theme and typography owners. Preserve all existing hierarchy controls, field paths and saved preferences. No fake axes, categorical legend, alternate persistence owner or feature flag. Renderer data and editor state are detached projections; neither writes the baseline.

The immediate paint route is the actual Workspace generated/public-control/string-palette workflow. Preserve all four source wrapping policies and source-valid saved paint data. Advanced object fills are a retained compatibility obligation, not a claim of implemented rendering: do not silently flatten an active advanced fill or misclassify a valid saved chart. A concrete active advanced-fill configuration needs a narrow reviewed adapter before acceptance. Do not expand this milestone into a standalone AG Charts API rewrite.

## Finite gradient behavior

The original Treemap and Sunburst were observed with equal Color50 and with all selected Color values missing. The latter uses a numeric anchor row excluded through the original public table filter, retaining the numeric field type. Public canvas text, screenshots and saved model identify the states. The original still emits its previously documented script/CSV diagnostics; these observations do not establish a clean application baseline or persistence.

| Prepared observations | Display and hover contract |
| --- | --- |
| Distinct finite color minimum/maximum | Original sampled gradient, finite numeric scale labels, marker located from the observed legend domain |
| Equal finite colors | Keep the gradient bar; the observed value has one centered label. Original scale conversion maps the hover marker to the midpoint of the bar |
| Color assigned, all observations missing | Keep the unlabelled gradient bar and its existing controls. Use palette fallback for marks; no fabricated labels or hover marker |
| No Color assignment | Preserve saved legend preference but retain original control applicability; no color legend is rendered |

Collect color extent before omitting zero-area nodes. Paint fallback `[0,1]` for degenerate/absent extent is separate from measured legend labels and marker positions. Never pass Infinity/NaN to ECharts. Equal50 label behavior is observed; detailed fractional equal-domain tick nicening remains a source-backed formatting concern, not a reason to invent a range. The original equal-domain scale explicitly converts to `(rangeStart + rangeEnd) / 2`.

## Renderer lane

Exclusive new owners: `echarts/hierarchy.ts`, `hierarchyData.ts`, `hierarchyColor.ts`, `hierarchyChrome.ts`, `hierarchyTooltip.ts`, `hierarchyLabels.ts`; tests in `tests/unit/chart-compatibility/hierarchyEngine.test.ts`. The label helper owns wrapping, overflow and label-box adaptation to keep translation owners within caps. Further helpers require an ownership review.

Consume prepared root children without exposing the synthetic root. Native values are subtree weights; raw tooltip observations remain separate. Exclude zero-area geometry only after resolving palette identity and color extent. Treemap uses a stable descending sibling sort with native `sort:false`, squareRatio1, visibleMin0 and childrenVisibleMin0. Sunburst keeps source order, starts at90 degrees and uses equal depth bands. Disable native drilldown, roaming and breadcrumbs. Native layout owns coordinates; no custom squarifier or sector engine.

Preserve original root-index/depth palette identity and missing-color fallback. Use Culori4.0.2 with the original achromatic/shortest-hue/nonpremultiplied-alpha wrapper and source-reference samples; types pin4.0.1. Retain explicit endpoint colors and sampled0.05 gradient stops. The protected dependency operation must pass before this lane's executable color verification.

Map spacing, captions, background, labels and continuous legend to native ECharts options/graphics. Original tooltip text uses observed size/color semantics, not geometric weights or invented parent totals. All-zero geometry is blank. Native Treemap partition/title fitting and Sunburst spacing/label fitting require H4 comparison; these are not pixel-parity claims.

The renderer also projects `HierarchyHoverPlan` from the same selection, node IDs and viewport as the legend. Unknown/parent/missing-color nodes return no marker. H3 owns the native event binder and one silent triangle graphic update; no hit-test subsystem. Resize must discard the old plan until fresh viewport selection, not merely hide the current marker. Revision/generation guards, error/export invalidation and exact cleanup remain mandatory.

## Controls lane

Exclusive new owners: `application/hierarchyAppearance.ts`, `hierarchyAppearanceDefaults.ts`, `hierarchyAppearanceValues.ts`, `hierarchyEditorState.ts`, `hierarchyEditorTransaction.ts`, `editor/hierarchy/HierarchySpacingControls.tsx`, `HierarchyGradientLegendPanel.tsx`; tests in `tests/unit/chart-compatibility/hierarchyAppearance.test.ts`. The values helper owns validated paint/label/gradient resolution. Shared declarations and existing session/editor files are not worker-owned.

Use `composeAppearanceOptions` with the selected baseline and generated options. Resolve finite family defaults, theme common/family overrides, then composed common/family options. `themePalette` is the single hierarchy paint-token input; no competing store. Preserve explicit false/zero, saved inactive preferences and unknown model fields.

Reuse titles, background, padding, tooltips, typography and existing numeric/choice primitives. Treemap exposes Group Padding/Spacing and Tile Padding/Spacing, defaults4/2/3/1. Sunburst exposes tooltips only under Series. Continuous legend maps its exact original `gradientLegend` paths, defaults enabled/right/thickness16/length200/spacing20/reversefalse. Color assignment determines applicability, including when all Color observations are missing.

The intent mapper accepts only the declared correlated field/value union, validates runtime input without getters, and emits one family-root leaf patch. It never writes storage or stamps. H3 derives fresh context from style/assignments after stamp/family/baseline checks and uses existing reduction/commit. The two custom groups reuse the existing shell, labels, keyboard flow and theme.

## Join and evidence

Each lane starts from the frozen declarations, has RED-before-implementation behavior tests, independent review, affected strict/lint checks and whole-file inventory caps400 physical/300 logical/50 per function. Reuse two focused suites; no duplicated harness or broad test matrix. Serialize installs, heavy verification, shared integration and commits.

H3 integrates capture/setup unions and renderer/editor routing atomically, with cohesive extraction before near-cap shared files grow. H4 exercises the retained eight-leaf FMP AAPL FY2025 USD fixture, original comparisons, representative spacing/gradient/tooltip effects, hover, light/dark, resize/refresh/export and fresh-session reopen. H5 publishes selected FMP images and one verified image milestone. No image rebuild is required for these inactive foundation commits.
