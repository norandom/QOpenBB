# Treemap and Sunburst contract

The bounded numerical/control contract is sufficient for H0 once joined to the reviewed capture interfaces and ownership manifest. The owner approved excluding missing sizes; the controller approved making the existing tooltip toggle functional. This draft records those bounded corrections alongside original observations, not implementation or H4 acceptance.

## Observed boundary

Original frontend `38dffc33389aca0e4a87e0e88d42f7067aa220df`; synthetic File journeys run 2 (Treemap) and run 3 (Sunburst), probe `8deb7da0c073eec3dc1799c635f13c7315f9133346b394b2e3e7b2e275139ee6`. Runtime/image qualification remains the controller's evidence owner. The test's passing status means the characterization journey completed; diagnostics are not clean.

One ordinary File widget per dashboard is asserted before extracting the saved model. This demonstrates the shared Table renderer through File. It does not qualify a separate provider Table caller, grouped/pivot/tree capture, remote/pinned rows, candidate rendering, export or fresh-session persistence.

## Numerical and setup contract

- Preserve `treemap`/`sunburst` model strings and ordered `cellRange.columns`. Region,Desk establishes two hierarchy levels; Desk,Region changes their nesting. Selected numeric order changes the size/color roles; the fields are not additive parallel series.
- Aggregation off retains the last row for a repeated complete category path. Repeated leaf labels beneath different parents remain separate. Preserve this original behavior; users must explicitly choose Sum when they want duplicate rows combined.
- Sum, Average (`aggFunc=avg`) and Count act before hierarchy construction. Observed West/Alpha Size/Color are off 6/20, sum 8/10, average 4/5 and count 2/2 in Treemap; Sunburst size tooltips show 6,8,4,2. Count gives Gamma Color=1 despite its original missing Color. Do not describe Count as a nonmissing-value count.
- Treemap parent tooltips show labels alone. Sunburst default parent tooltips repeat the parent label; neither displays a numeric derived parent total in these observations. Compute parent totals for geometry/reconciliation internally; do not add totals to tooltip UX under a parity claim.
- With Size selected, Missing occupies visible area beside Valid=8, while Zero=0 and Negative=-4 have no visible sized marks in the screenshots. Pinned engine source assigns finite negative/zero sizes weight 0 and a missing leaf weight 1. Screenshots are consistent with a 1:8 ratio, including roughly 40/320 degree Sunburst sectors; exact geometry is not independently measured because the observer does not decode Path2D. Missing tooltips do not display an amount of 1.
- With Size deselected, all four leaves occupy equal tiles/sectors, including the rows whose unselected Size is zero or negative. This deliberate no-size mode is count weighting, not financial amount imputation. Same-session reload after restoring Size restores the observed sized view and column assignments.
- Runs 5/6 observe no-category selection saved as Size,Color and five unlabeled root marks, retaining all source rows rather than collapsing duplicate paths. Leaf identity in this mode is source row identity, with no fabricated category level. Both all-zero fixtures render blank; preserve that behavior without a new message. At two numeric selections, the Add Series combobox is absent.
- Source-backed category scalar contract: retain `string | number | boolean | null`, normalize undefined to null, retain empty string separately. Canonical path components are null for nullish values and `String(value)` otherwise; number 1 and string '1' therefore share the canonical label/path. Preserve raw components for provenance. This is directly inspected pinned source, not runtime coverage of mixed scalar/missing categories. Equal/all-missing color-domain fallback is likewise source-backed and not a claimed runtime pass.

## Owner-approved missing-size correction

Owner decision relayed by the controller on 2026-10-25: "Exclude missing sizes." When a size field is selected, a missing size contributes zero geometric weight and no area; valid observations remain visible. Preserve the raw missing datum as missing, not a measured zero. When no size field is selected, retain equal count weighting for all leaves. Zero/negative size handling and duplicate-path behavior remain unchanged. The later H1c contract separately records the owner-approved category-collision correction below; other numerical semantics remain unchanged.

This deliberately differs from the original missing-leaf weight 1 observed above. The distinction must remain explicit in regression expectations and original comparisons; this approval does not waive the remaining H0 interface/control review.

## Controls and appearance

Treemap defaults observed in Series: group padding 4, group spacing 2, tile padding 3, tile spacing 1. Changed saved paths are `chartOptions.treemap.series.group.padding`, `.group.gap`, `.tile.padding`, `.tile.gap`. Implement the pinned source's spacing intent; H4 verifies visible effects. Saved paths alone are not a completed replacement-control check.

Both families expose Single, Multiple and Compact. Saved mode lives at `chartOptions.<family>.tooltip.mode`; Multiple maps to `shared`, Compact to `compact`. Treemap native tooltip text is equivalent across these modes. Sunburst Compact removes the numeric size content while Single/Multiple display it. Preserve these family-specific effects.

Disabling Tooltips saves `chartOptions.<family>.tooltip.enabled=false` yet native tooltip hits remain. Runs 5/6 independently confirm three traversals of six hits for both false and true, with explicit absent-tooltip checks before each traversal. The original toggle is inert on this route. Controller decision, communicated to the user: replacement honors the existing toggle intent, so false suppresses and true restores tooltips. Retain the original family-root paths and mode effects. Source-derived `series.tooltip` paths are not the observed saved-control paths.

Follow-ups capture common/title/quick-action availability, light/dark state, and a parent click with unchanged painted hierarchy; no drilldown is required from this observed action. Actual title mutation, quick-action visible effects, gradient controls, nondefault-control reopen and precise spacing/layout checks remain H4 candidate gates using pinned source intent and existing shared owners. They are not original runtime passes. Preserve inactive/unknown options; no feature flags or hidden activation routes are authorized.

## Capture and implementation constraints

The current one-category snapshot cannot preserve ordered hierarchy paths. Freeze an explicit hierarchy capture policy before implementation: ordered category IDs and raw values; optional size/color assignments with distinct labels/units; immutable source row identity and provenance; explicit aggregation; prepared path identity and geometric weight separate from raw financial amount. Do not weaken existing grouped/pivot/tree/remote/pinned guards or alter other families' missing-value rules.

Keep original option persistence, application session transactions/stale-command rejection, ECharts host, refresh and export owners. The H1a ownership and type definitions below are frozen for review. Later executable ownership remains a proposal in the capture assessment. New/modified production files require inventory-backed 400 physical lines, 300 logical units and 50/function checks.

The real fixture remains AAPL FY2025 Quarter -> Cost of revenue/Gross profit, eight reported-USD leaves totaling 416,161,000,000 USD; revenue is only the reconciliation reference. No second financial color measure is invented. Real-FMP application rendering and packaged lifecycle acceptance belong to H4.

## Open evidence issues

Initial runs retain `Unexpected token '<'` and failed File CSV requests. A fresh-context reopen failed before canvas because the reused helper installs upload-auth routing only for current-context uploads; its failure is not successful persistence evidence and does not explain every baseline error. Fresh-upload follow-ups have no page errors but retain a failed CSV request whose exact cause is not established. Retain the artifacts and do not claim clean end-to-end diagnostics or fresh-session acceptance. Missing hover hits are not absence evidence, native raw tooltips do not prove effective weights, and screenshots do not establish exact numerical geometry.

Independent evidence: [observed contract review](../../../artifacts/reviewed/chart-hierarchy/observed-contract-review.md). Original diagnostic limitations remain explicit; this contract does not establish replacement acceptance.


## H1a: inactive capture and setup type contracts

This task adds two production declaration owners and one compile-only fixture. It changes no runtime routing, validators, state, controls or saved models. Existing ChartSnapshot and flat snapshot policies remain unchanged. There is no feature flag.

`compatibility/hierarchyContracts.ts` exports:

- `HierarchyChartType = "treemap" | "sunburst"`.
- `HierarchyRawCategory = string | number | boolean | null`.
- `HierarchyCategoryPath = readonly (string | null)[]`.
- `HierarchySnapshotRow`: readonly `id: string`, `rawCategoryValues: readonly HierarchyRawCategory[]`, `categoryPath: HierarchyCategoryPath`, `values: Readonly<Record<string, number | null>>`.
- `HierarchySnapshot`: extends `Omit<ChartSnapshot, "categoryColumnId" | "rows" | "rangeCategory" | "sourceMode">`, with readonly `kind: "hierarchy"`, `sourceMode: "flat"`, `categoryColumnIds: readonly string[]`, and `rows: readonly HierarchySnapshotRow[]`.
- `HierarchySnapshotValidationResult`: `{ readonly valid: true; readonly snapshot: HierarchySnapshot } | { readonly valid: false; readonly diagnostics: readonly SnapshotDiagnostic[] }`.

`application/hierarchyTypes.ts` exports:

- `HierarchyGridCaptureInput`: extends `Omit<GridCaptureInput, "categoryColumnId" | "snapshotPolicy">`, with readonly `categoryColumnIds: readonly string[]`.
- `HierarchySetupSelection`: readonly `categoryIds: readonly string[]`, `seriesIds: readonly string[]`, optional `aggFunc: SetupAggregation`.
- `HierarchyAssignments`: optional readonly `sizeId: string`, `colorId: string`.
- `RetainedApplicationCapture = ChartSnapshot | HierarchySnapshot`, an inactive declaration until the serial application join.

Import ChartSnapshot and SnapshotDiagnostic from compatibility/snapshotTypes, GridCaptureInput from application/types, and SetupAggregation from echarts/cartesianTypes through type-only imports; do not duplicate their definitions. Compatibility declarations must not import application owners. The application declaration file may import compatibility contracts. Do not declare an unreviewed placeholder hierarchy projection or prepared-node type.

Canonical path semantics are source-backed: nullish category input becomes null; other admitted JSON scalars become String(value). Preserve raw scalar types separately, keep empty string distinct from null, and never concatenate path components with a delimiter. Thus numeric 1 and string "1" have the same canonical component. Reject nonfinite/complex category values rather than invoking arbitrary coercion hooks. The original source accepts broader JavaScript values; this JSON-safe Table/File capture boundary is explicit, not a claim of object-cell support.

With zero selected categories, each source row is an independent leaf with path [], identity derived from its stable row ID and no visible category label. Do not merge those leaves as duplicate empty paths or invent a category alias. Optional size/color assignments preserve deliberate no-size counting. Hierarchy raw values remain independent of derived geometry and aggregation.

`tests/unit/chart-compatibility/hierarchyContracts.typecheck.ts` is the only test owner for H1a. Use representative no-category, multi-level, null/boolean/raw-number and zero-numeric selections, with compile-time negative assertions that an ordinary snapshot cannot be consumed as a hierarchy snapshot and missing required hierarchy metadata is rejected. This proves type shape only, not runtime validation, canonicalization, geometry or financial arithmetic.

Completion requires independent declaration/fixture review, scoped strict TypeScript evidence with inherited diagnostics distinguished, formatting and inventory-backed 400 physical/300 logical/50-per-function checks for both complete production files. Add both owners to the maintained inventory with an explicit source revision/change scope before accepting the task. No broad runtime suite or image build is warranted for inactive declarations.

## Subsequent executable boundaries

H1b will freeze and implement hierarchy-specific validation and displayed-row capture with shared grid guard extraction. No live application capture return type changes belong to that inactive foundation task. Default flat validators/capture behavior and client-side/group/pivot/tree/pinned/remote guards must remain intact. Prepared setup/node contracts must be independently reviewed before setup and renderer lanes consume them.

H3 owns the atomic retained-capture union integration: storage/context/result types, own-kind and family-mismatch guards, and narrowing before every flat selector. Audit existing `state.capture as ChartSnapshot` sites in applicationSessionCapture and applicationSessionRuntime; do not widen a shared context and leave flat consumers casting. Preserve range/data-generation stamps and stale-command rejection. No partial union propagation is accepted between tasks.

H2 renderer and controls run in disjoint lanes only after their exact input/appearance contracts are frozen. H4 owns real-FMP examples, visual controls and theme, refresh, export and final fresh-session reopen. Every applicable existing control must remain available; unverified common-control effects remain explicit acceptance work rather than disabled features.

## Owner-approved aggregation identity correction

On 2026-10-25 the owner approved keeping missing categories distinct from literal names such as null during aggregation. The original object-key aggregation can merge a null category with the literal string null; replacement aggregation uses the canonical path tuple instead. This is a deliberate correction, not original parity. Other canonical equivalences remain unchanged. See the [setup design](hierarchy-setup-design.md) and [independent review](../../../artifacts/reviewed/chart-hierarchy/setup-plan-review.md).
