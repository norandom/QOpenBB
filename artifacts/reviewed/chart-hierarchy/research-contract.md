# Treemap and Sunburst original-contract research

Proceed to an original browser probe before freezing implementation. The shared hierarchy engine has financially consequential missing-size and duplicate-path behavior. A flat chart adapter cannot carry the required ordered category paths. This is source research dated 2026-10-24, not observed hierarchy application behavior, implementation approval or acceptance.

Only this ignored report is written. No WSL command, build, test, browser, install, provider call or production mutation ran. Dependency files were read through the Windows UNC filesystem. The direct successor authorization is `.kiro/specs/analyst-workspace/radial-milestone.md`; the spec language is English. Delegation, complexity, testing, documentation and delivery-workflow steering were read.

## Source identity

`W` means `vendor/workspace`, original commit `38dffc33389aca0e4a87e0e88d42f7067aa220df`, inspected with `git show` and `git grep`. W source references below are relative to `terminalpro/src/`. The current replacement inspected is `f9b29ddd4e2d1367f08eafe67e82e2a8a357f320`.

Installed source references below use physical lines of `dist/package/main.esm.mjs`, beneath `\\wsl.localhost\Debian\home\mc\.bun\install\cache\`. Fresh PowerShell SHA256 checks returned:

| Code | Package directory | SHA256 |
| --- | --- | --- |
| G | `ag-grid-enterprise@34.1.1@@@1` | `76831274e5f22060913871da1e756d5269e71b87ea9a601ecac05baca4504286` |
| C | `ag-charts-community@12.1.1@@@1` | `e9b1b8be8d27ffc1f2c66e715b863b36d5f3aecef0c79e18cc0101a440956df4` |
| E | `ag-charts-enterprise@12.1.1@@@1` | `710be7da26f7b52005f459c1d8fa5d57698a0181c85aac24ff758547476bfe69` |

These pins identify inspected source, not an independently qualified running frontend.

## Source-derived reachability and data rules

- W `components/DataConnectors/WidgetsBuilder/consts.ts:173,177` and `lib/constants.ts:1286,1290` retain `sunburst` and `treemap`. G52263-52264 advertises both under Hierarchical for range and pivot charts, enterprise only. G17138-17139/G17352-17353 also maps pivot/range context-menu commands. The established Table/File route is the target; its actual menus, entitlement, File ingestion and saved models still require a hierarchy-specific original probe.
- G41534-41542 permits unlimited selected category dimensions and at most two numeric fields; G53549-53552 allows zero numeric fields. G42339-42387 creates one series: first numeric field is `sizeKey/sizeName`, second is `colorKey/colorName`. The numeric fields are not independent series or additive siblings. Missing size selection produces equal leaf weights through C51552-51556.
- Flat categories use their selected order as hierarchy levels. Null/undefined labels become null; all other values use `String(value)` (G42254-42269). Each path uses Map insertion order. Repeated complete nonempty paths overwrite the previous leaf datum (`hierarchy.value = item`, G42308-42316); this is not automatic summation. With no category levels, original root rows remain separate (G42287-42290, G42310-42314). String coercion can collapse numeric 1 and string '1'.
- Explicit `aggFunc` is a separate earlier grid transform, before hierarchy construction (G42572, G42701-42762). With no operator or no dimensions it returns rows unchanged. Otherwise it groups by all selected dimensions and aggregates every selected numeric column. Therefore color values are also subject to the selected operator; averaging rates and summing amounts have different financial meanings. The original raw grouping uses object keys rather than the hierarchy Map; prototype-like labels need probing, not blind duplication of an unsafe implementation.
- Grouped rows use reversed auto-group label arrays as category paths (G42271-42284). When color exists, groupData is appended with size removed before tree construction (G42374-42384). This is a distinct capture contract from flat ordinary rows; do not promise it merely because the original gallery lists pivot.
- C51542-51593 constructs tree weights. A finite size is `max(size, 0)`; a missing, null, numeric string or nonfinite size becomes 1 on leaves and 0 on internal nodes. `sumSize = own sizeValue + sum(child.sumSize)`. No absolute-value conversion. Consequently missing financial amounts can occupy visible area. Raw values remain in node data; geometry and tooltip value are separate contracts. An owner decision is needed if observed missing-data behavior is to be corrected.
- Color extent includes `typeof value === 'number'` values; the normal scale domain is min/max, falling back to [0,1] unless min < max (C51560-51592). Node coloring uses the color scale when colorValue is nonnull (E41826-41839). Preserve missing color separately from missing size, and probe equal/negative/all-missing color and any nonfinite values surviving ingestion.

## Distinct geometries and controls

Treemap filters nonpositive effective children and sorts siblings descending by effective size (E42721-42731). It uses a squarified layout (E42733 onward). Effective size is leaf own size, or internal `sumSize - sizeValue` (E42644-42645), so internal own amounts do not occupy a separate tile. Group padding reserves title height in addition to the numeric padding (E42675-42719). Defaults are group padding 4/gap 2, tile padding 3/gap 1 (E43333-43385). These geometry defaults are source-derived; effective Workspace styling still needs observation.

Sunburst assigns child angles in input order using one global scale `2*pi/root.sumSize` (E41776-41783), not Treemap size sorting. It renders equal radial depth bands, radius=min(width,height)/2, top origin at -pi/2 (E41880-41900), with depth-band radii in E42103-42104. Theme sectorSpacing=2 and padding=3 (E42325-42326). Own size on an internal node can therefore leave angular remainder relative to child totals, unlike the Treemap effective-size rule. Do not force an ECharts default root, drilldown, sort or normalization onto this contract.

Source-exposed control matrix:

| Surface | Source contract | Original probe needed |
| --- | --- | --- |
| Setup | Multiple ordered categories, zero to two numeric selections; no inverted category/series support on hierarchy descriptors (G41455-41461, G41546) | Category/series ordering, fallback category, effect of deselection, switch control absence |
| Aggregate | Toggle and sum/first/last/min/max/count/avg; shown with a selected nondefault category (G46954-47000) | Default operator when toggled, displayed effects on duplicate paths and both numeric fields, save paths |
| Treemap series | Tooltips and four spacing sliders: `group.padding`, `group.gap`, `tile.padding`, `tile.gap`, slider default maximum 10 (G49409-49452, G49630) | Exact labels, bounds, defaults, visible inner/outer gap effects and persisted option paths |
| Sunburst series | Tooltips only (G49631) | Absence of unrelated polar controls; saved options still preserved |
| Tooltips | Enabled toggle and mode single/shared/compact (G49469-49504) | Effective placement/content for parent and leaf, mode effects and pointer behavior |
| Common format | Reuse common chart/caption/background/padding/theme machinery; no axes implied by hierarchy | Enumerate actual common and gradient-legend panels; distinguish controls that visibly act from inert retained flags |

W `components/General/Table/Chart/hooks/useChartOptions.tsx:71-100` enables Treemap group/tile labels, Sunburst labels, sets bottom padding 10, and makes Sunburst tooltip pointer-anchored/interactive. W `components/General/Table/Chart/utils.tsx:184-195` has a Treemap-specific tooltip with color/size names and raw datum values; do not infer the same custom formatting for Sunburst. W `useChartOptions.tsx` retains common navigator/mini-chart options and storage flags; these are not proof of visible hierarchy navigator support. The series editor does not expose the extensive style knobs accepted by standalone AG APIs, so separate reachable controls from externally saved fields.

## Current adapter gaps and minimal proposed boundary

All following paths are beneath current `vendor/workspace/terminalpro/src/components/General/Table/Chart/`.

- `editor/chartTypeGalleryCatalog.ts:46-48` and `editor/ChartTypeThumbnail.tsx` already name both families. This is a preview inventory, not live renderer support.
- `application/comboSessionTypes.ts:12-24` excludes both from `ApplicationChartFamily`; there are no hierarchy assignment/appearance/session/renderer owners in the inspected tree.
- `compatibility/snapshotTypes.ts` has one `categoryColumnId` and one row `category`, with numeric values only. It cannot preserve multiple category values or a tree. `application/applicationSessionSelection.ts:70-100` likewise resolves one category and treats remaining noncategory fields as series.
- `application/gridCapture.ts:80-100` supports ordinary client-side rows and rejects pivot/tree/pinned models; subsequent checks also reject grouped ownership. Reuse lifecycle, transaction stamp, row selection, units, serialization and native host; extend capture deliberately rather than disguising hierarchy as an ordinary cartesian snapshot.

Proposed contract to review, not a frozen interface: an ordered `categoryColumnIds[]`; zero/one size field and zero/one color field with independent labels/units; captured rows with stable IDs, ordered raw category values and nullable raw numeric values; explicit aggregation operator; source mode; and provenance for displayed transformations. A hierarchy preparation owner resolves full-path identity/duplicate policy before producing tree nodes with stable identity, display label, raw data, own/effective/subtree size and optional color value. Numerical geometry must not re-aggregate or replace missing amounts. Keep the root synthetic and out of the persisted provider data. Preserve source-path identity even where display labels collide.

A control boundary needs family, option baseline, setup assignment, tooltip state, common appearance and Treemap's four spacing values. Renderer consumes prepared nodes and immutable appearance; existing session owners handle save/reopen and stale-command protection. Gradient legend requires its own continuous-color projection, not a per-numeric-series categorical legend. Freeze exact filenames and types with the controller after the original probe and independent review. Modified maintained production files must pass 400 physical lines/file, 300 logical units/file and 50/function with the existing inventory-backed gate. This document creates no new production scope or size exception.

## Retained FMP candidate with real accounting meaning

Prefer two ordered category levels `Fiscal quarter -> Revenue component`, one `Amount (USD)` size field, and eight leaves for AAPL FY2025. Each quarter has Cost of revenue and Gross profit. This uses reported, nonoverlapping accounting components whose sum equals revenue; it does not place revenue beside gross profit as if they were disjoint. Do not include a revenue subtotal as another leaf or an internal own amount.

Source is `artifacts/chart-histogram/fmp/raw.json`, freshly rehashed as `390dc8cbfc8302720a203bd9782d5e3b1f7363a4f762bdfcef079dbbe4c72f6b`. Retained `provenance.json` identifies `/stable/income-statement`, symbol AAPL, period quarter, limit 40, retrieved 2026-10-20T14:06:05.149732+00:00. Values were read directly from the retained raw rows:

| Quarter / reporting date | Cost of revenue USD | Gross profit USD | Revenue USD |
| --- | ---: | ---: | ---: |
| FY2025 Q1 / 2024-12-28 | 66,025,000,000 | 58,275,000,000 | 124,300,000,000 |
| FY2025 Q2 / 2025-03-29 | 50,492,000,000 | 44,867,000,000 | 95,359,000,000 |
| FY2025 Q3 / 2025-06-28 | 50,318,000,000 | 43,718,000,000 | 94,036,000,000 |
| FY2025 Q4 / 2025-09-27 | 54,125,000,000 | 48,341,000,000 | 102,466,000,000 |

All four rows report USD; the displayed component sums equal each row's revenue and the four-quarter total is 416,161,000,000 USD. This is fiscal FY2025, not calendar 2025. This proposal is a derived tabular reshape of retained data, not a new provider response or a statement of application acceptance. Retain all source dates, units and source hash when generating the fixture. Parent ring/rectangle totals are derived; labels/tooltips must identify that fact. `artifacts/chart-pie/fmp/provenance.json` independently retains the same four revenue/gross-profit values, but is not a hierarchy acceptance record.

An optional second color field should remain a separately labeled measure with explicit aggregation semantics. Avoid adding a fabricated percentage merely to exercise color. Synthetic signed color fixtures are sufficient for the first color-control contract; a real second measure can be selected in a separate financially interpretable layout later.

## Minimal original probe and decisions before implementation

Use the existing isolated original runtime and fixture/login helpers after the controller's heavy-build queue frees. Qualify exact frontend/image/backend overlay first. One compact fixture should contain two category levels, distinct size/color fields, duplicate full paths, repeated leaf labels under different parents, zero/negative/missing size, signed/missing color, and deliberate order differences. A second small empty/all-zero/no-size case distinguishes counting behavior from amount weighting. Do not claim a missing point absent solely because hovering failed.

Observe both families through File and retained Table routing: category reorder/deselect, numeric reorder and two-field cap, aggregate off and sum/avg/count, duplicate-path outcome, saved model changes, visible geometry, parent/leaf tooltip, continuous legend, Treemap spacing, theme and common controls. Probe any missing-size fallback before choosing correction or preservation; current research does not authorize silently applying prior Nightingale/Radial correction policy. Confirm whether the original permits drilldown, and if it does, record interaction and persistence; default ECharts navigation is not an acceptance oracle.

The package acceptance plan later needs the real accounting fixture, original comparison, actual visible transformations, refresh, export and final fresh-session reopen. Source research, source-level controls and a generated fixture do not complete any of these checks. Original grouped/pivot reachability and the existing adapter's unsupported capture path must remain explicitly unresolved until scoped and reviewed.
