# Sankey shared implementation contract

Status: SK0 ready for independent review, 2026-10-27. This freezes the bounded ordinary Table/File implementation described in [the milestone](sankey-milestone.md). It establishes no implementation or application acceptance. Implement SK1 and SK2 only after the controller accepts this contract and installs its shared declarations; integrate in SK3.

## Scope and observed seams

Add the persisted family `sankey` and gallery label `Sankey`. The existing ordinary capture keeps only one category, so use a distinct immutable edge snapshot. Reuse `GridCaptureInput`, `SessionStamp`, `ResolvedRange`, public AG Grid capture guards, `CartesianTranslationResult`, existing appearance resolution and `EChartsHost`. The host already imports full ECharts; no new host or chart registration is needed.

`caller/chartInputs.ts` supplies no unit/scale metadata for ordinary definitions. Never infer units, currencies or provenance from a column label. Blank metadata is allowed and visibly unknown. The core product/tech/structure steering files are absent in this checkout; the existing delivery, delegation, complexity and documentation amendments govern this bounded contract.

## Shared declarations

All paths below are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/`. The controller owns `compatibility/sankeyContracts.ts` and `application/sankeyTypes.ts`, seeds the following declarations before fan-out, and serializes any change. Existing imported types retain their original modules.

```ts
// compatibility/sankeyContracts.ts
import type {
  ChartSnapshot, SnapshotDiagnostic, SnapshotJson,
} from "./snapshotTypes";

export type SankeyRawId = string | number | boolean;
export type SankeyMetadataKey = "unit" | "currency" | "scale" | "period" | "measure";
export interface SankeyMetadata {
  readonly unit: string | null;
  readonly currency: string | null;
  readonly scale: number | null;
  readonly period: string | null;
  readonly measure: string | null;
}
export interface SankeySelection {
  readonly sourceColumnId: string | null;
  readonly targetColumnId: string | null;
  readonly valueColumnId: string | null;
  readonly metadata: SankeyMetadata;
  readonly metadataColumnIds: Readonly<Partial<Record<SankeyMetadataKey, string>>>;
}
export interface SankeyRow {
  readonly id: string;
  readonly source: SankeyRawId | null;
  readonly target: SankeyRawId | null;
  readonly value: number | null;
  readonly metadata: SankeyMetadata;
  readonly provenance: SnapshotJson;
}
export interface SankeySnapshot extends Omit<ChartSnapshot,
  "categoryColumnId" | "rows" | "rangeCategory" | "sourceMode"> {
  readonly kind: "sankey";
  readonly sourceMode: "flat";
  readonly selection: SankeySelection;
  readonly rows: readonly SankeyRow[];
}
export interface SankeyDiagnostic extends SnapshotDiagnostic {
  readonly severity: "error" | "warning";
  readonly rowIds: readonly string[];
  readonly nodeId?: string;
}
export interface SankeyNode {
  readonly id: string;
  readonly raw: SankeyRawId;
  readonly label: string;
  readonly role: "source" | "internal" | "sink";
  readonly incoming: number;
  readonly outgoing: number;
  readonly residual: number | null;
  readonly tolerance: number | null;
  readonly balanced: boolean | null;
}
export interface SankeyLink {
  readonly id: string;
  readonly source: string;
  readonly target: string;
  readonly value: number;
  readonly rowIds: readonly string[];
}
export interface SankeyGraph {
  readonly snapshot: SankeySnapshot;
  readonly nodes: readonly SankeyNode[];
  readonly links: readonly SankeyLink[];
  readonly metadata: SankeyMetadata;
  readonly reconciliation: "declared-units" | "unspecified-units";
}
export type SankeyGraphResult =
  | { readonly status: "ready"; readonly graph: SankeyGraph;
      readonly diagnostics: readonly SankeyDiagnostic[] }
  | { readonly status: "empty"; readonly reason: "no-rows" | "zero-only";
      readonly diagnostics: readonly SankeyDiagnostic[] }
  | { readonly status: "invalid"; readonly diagnostics: readonly SankeyDiagnostic[] };
export type ValidateSankeySnapshot = (input: unknown) =>
  | { readonly valid: true; readonly snapshot: SankeySnapshot }
  | { readonly valid: false; readonly diagnostics: readonly SankeyDiagnostic[] };
export type BuildSankeyGraph = (snapshot: SankeySnapshot) => SankeyGraphResult;
```

```ts
// application/sankeyTypes.ts
import type { GridCaptureInput, SessionResult, ChartDisplayPolicy } from "./types";
import type { ResolvedApplicationAppearance } from "./appearanceModel";
import type { SnapshotColumn } from "../compatibility/snapshotTypes";
import type { SankeySelection, SankeySnapshot, SankeyGraph,
  SankeyMetadataKey, SankeyDiagnostic } from "../compatibility/sankeyContracts";
import type { CartesianTranslationResult } from "../echarts/cartesianTypes";

export interface SankeyGridCaptureInput extends Omit<GridCaptureInput,
  "categoryColumnId" | "snapshotPolicy"> {
  readonly selection: SankeySelection;
}
export type CaptureDisplayedSankey =
  (input: SankeyGridCaptureInput) => SessionResult<SankeySnapshot>;
export type SankeySetupEdit =
  | { readonly kind: "mapping";
      readonly field: "sourceColumnId" | "targetColumnId" | "valueColumnId";
      readonly value: string | null }
  | { readonly kind: "metadata"; readonly field: SankeyMetadataKey;
      readonly value: string | number | null }
  | { readonly kind: "metadata-column"; readonly field: SankeyMetadataKey;
      readonly value: string | null };
export interface SankeySetupPanelProps {
  readonly columns: readonly SnapshotColumn[];
  readonly selection: SankeySelection;
  readonly diagnostics: readonly SankeyDiagnostic[];
  readonly onEdit: (edit: SankeySetupEdit) => void;
}
export interface SankeyRenderInput {
  readonly graph: SankeyGraph;
  readonly style: Readonly<{
    application: Pick<ResolvedApplicationAppearance,
      "title" | "subtitle" | "padding" | "background" | "tooltip">;
    palette: readonly string[];
    textColor: string;
    fontFamily: string;
    fontSize: number;
    linkOpacity: number;
    nodeWidth: number;
    nodeGap: number;
    labels: boolean;
  }>;
  readonly context: Readonly<{
    display: ChartDisplayPolicy;
    viewport: Readonly<{ width: number; height: number }>;
  }>;
}
export type TranslateSankey = (input: SankeyRenderInput) => CartesianTranslationResult;
```

Export `validateSankeySnapshot`, `buildSankeyGraph`, `captureDisplayedSankey`, `translateSankey` with these types. Export the named React component `SankeySetupPanel(props: SankeySetupPanelProps)`. No lane may change these declarations unilaterally.

## Capture, identity and metadata

Capture displayed flat client-side rows through `getCellValue({ rowNode, colKey, useFormatter: false })`. Honor selected range, filtering and row order, validate stamps and reject unsupported grouped/pivot/remote models through existing guards. Preserve row ID, data revision, state address, original model and range. Deep-copy/freeze retained JSON; no grid/store/row references enter the snapshot. Missing mappings and missing selected columns yield row/column diagnostics, with selection retained by the session owner.

Source and target accept nonblank strings, finite numbers and booleans. Whitespace-only strings are invalid; other strings keep every original character. Node identity is `JSON.stringify([typeof raw, raw])`; numeric negative zero normalizes to zero. Thus `1`, `"1"` and `true` differ, and a display formatter never merges identities. Labels default to `String(raw)`; identical labels remain distinct and tooltips expose raw type/identity. Link identity is `JSON.stringify([sourceId, targetId])`. Do not use plain object keys for uncontrolled identities. SK3 caller projection must retain descriptors for both mapped identifiers and every bound metadata column, bypassing the ordinary one-category filter; category descriptors support textual metadata and numeric descriptors support scale.

Values must be unformatted finite numeric cells; null/missing, strings, negative values and nonfinite values are errors. Invalid primitive cell types return capture diagnostics rather than throwing through the UI. Null IDs/values can be retained to produce precise validation errors. Row IDs and column IDs must be unique; all mapping IDs must reference the captured range. Source, target and value mappings are distinct. Capture each optional metadata column even when it is not a numeric descriptor. No automatic selection from column labels.

The metadata editor contains explicit Unit, Currency, Scale, Period and Measure fields, with optional column bindings under a collapsible Metadata section. Defaults are all null and no bindings. A bound row cell overrides no conflicting declared value: disagreement is an error. Blank bound cells remain unknown and cause a warning; no fill-forward. The scale binding accepts finite positive numbers only. Other bound fields accept nonblank strings only. Currency, when present, is an uppercase three-letter code; use unit `currency` with a currency code for monetary amounts. Nonmonetary units require null currency. Positive finite scale expresses base units per stored numeric amount; calculations retain stored amounts and label scale explicitly.

For each key, differing non-null metadata among rows or between a row and a declaration is an error; even zero-valued rows participate. Do not infer period compatibility from dates. Period denotes a common allocation scope such as `AAPL FY2025`; quarterly statement dates belong to provenance/labels, not conflicting period identities. The common measure may be `income-allocation`, allowing revenue to allocate into costs and gross profit; it must not mix unrelated measures such as assets or share counts. Unknown metadata is allowed with the persistent warning `Units or allocation scope unspecified; numerical balance is not financial reconciliation`. Any incomplete row metadata keeps that warning. Reconciliation is `declared-units` only when unit, scale, period and measure are known on every row, plus currency for monetary units. It means a user/source declaration, not independently verified provider truth.

Ordinary capture provenance records row ID and mapped column IDs only. It must not claim FMP origin. The live-data fixture retains richer endpoint/retrieval/hash/date evidence externally and in its explicit CSV labels. No credentials enter persisted provenance.

## Aggregation and numerical decisions

Validate the entire snapshot before producing geometry. Reject self-links and directed cycles, including zero links, with affected row IDs. Never discard invalid rows to render a partial graph. Aggregate identical directed pairs by compensated Sum in captured row order, retaining every contributing row ID. Check every aggregate and node total for finite overflow. Zero links remain in the retained snapshot but have no rendered width; nodes with no positive incident links are omitted from geometry. No rows gives `no-rows`; all valid zero rows gives `zero-only`.

Use compensated sums for incoming and outgoing positive links. Internal residual is `incoming - outgoing`; source-only and sink-only nodes have `residual`, `tolerance` and `balanced` null, distinguishing absence of counterpart links from an observed zero. For internal nodes use the stored-value tolerance:

`tolerance = max(1e-9, 1e-12 * max(abs(incoming), abs(outgoing)))`

`balanced = abs(residual) <= tolerance`

Tolerance addresses floating-point arithmetic, not accounting materiality. Keep residuals unrounded and display the exact tolerance in the internal-node tooltip. An imbalance produces a warning with node ID, contributing row IDs, incoming, outgoing and residual, but still renders. Do not add balancing edges or normalize totals. Node geometry may use `max(incoming, outgoing)`; never sum both sides as economic value. Do not expose a sum-of-all-links "total" because it double-counts internal transfers. Missing metadata never converts a numerical equality into a financial reconciliation claim.

## Renderer, recovery and persisted behavior

Use native ECharts Sankey options, left-to-right orientation, stable node/link IDs, no draggable financial mutation and animation disabled for reproducible refresh/export. Default nodeWidth 20, nodeGap 12, linkOpacity 0.45, labels true; use the resolved application font and plain-color palette. Reject invalid style numbers/colors with diagnostics, never partial options. Escape all tooltip HTML from labels, units and provenance. Tooltips show source/target, aggregate value, unit/currency/scale, period/measure and contributing row IDs. Internal-node tooltips show incoming/outgoing/residual/tolerance and `Balanced within numerical tolerance` or `Incomplete or imbalanced flow`; source/sink tooltips identify their role without a fictitious counterpart observation.

The controller resolves existing chart chrome, title/subtitle, background, padding and tooltip controls. Saved explicit options override generated defaults and theme tokens through the existing option baseline machinery. Theme changes affect palette/text only; metadata and values never change. Node spacing/width and link opacity are fixed defaults for this bounded slice, not hidden or disabled controls. Do not expose Cartesian axes/legend controls on this new family. Existing family controls remain intact when switching away.

Persist selection under `storage[stateKey].sankey.sankeySetup` as `{ version: 1, ...SankeySelection }`, and range under the usual `cellRange`. `chartModel.chartType` is `sankey`. Version 1 fields are validated on every read; absent setup opens an unmapped editable state. Unknown versions or malformed persisted fields show a diagnostic and permit replacing mappings/metadata; never reinterpret another family's saved options or silently overwrite invalid storage. Store the user's next valid edit through the existing stamped transaction and latest-storage owner. Mapping/metadata/range changes advance data revision and recapture; appearance edits advance render revision only. Preserve all other chart partitions. Refresh and reopen reconstruct snapshots, not serialized ECharts instances.

The setup panel and chart-family selector stay mounted in waiting, invalid, empty and ready states. Invalid input clears obsolete geometry and presents actionable diagnostics beside the mappings. Empty state explains `No rows in selected range` or `All selected links are zero`. Warnings remain visible above the chart and in accessible diagnostic text, not hover-only. Corrections recapture without switching family or reloading the widget. Do not reuse a context helper that requires an already valid capture: selection, columns, stamp and grid inputs remain available independently of graph validity. Sankey setup bypasses ordinary multi-series, transpose and aggregation controls; Sum is fixed. Export uses existing lifecycle PNG ownership for ready graphs; invalid/empty states must not export an old graph. No feature flag, hidden gallery entry, disabled replacement or synthetic balancing result satisfies completion.

## Exact lane ownership and join

Each worker is not alone in the codebase and must preserve others' edits. No worker may add unlisted files without controller reassignment. Prefix all source paths with the Chart directory defined above; test paths below are relative to `vendor/workspace/terminalpro/`.

| Owner | Exclusive writable paths | Output / prerequisite |
| --- | --- | --- |
| Controller SK0 | `compatibility/sankeyContracts.ts`; `application/sankeyTypes.ts` | Frozen declarations above, reviewed before SK1/SK2 dispatch. |
| SK1 data | `application/sankeyCapture.ts`; `compatibility/sankeySnapshot.ts`; `compatibility/sankeyGraph.ts`; `compatibility/sankeyValidation.ts`; `compatibility/sankeyAggregation.ts`; `tests/unit/chart-application/sankeyCapture.test.ts`; `tests/unit/chart-compatibility/sankeyGraph.test.ts` | Inactive capture/validation/aggregation exports. Focused invalid, duplicate, metadata, cycle, zero, precision and fixture assertions. No UI/routing edits. |
| SK2 presentation | `echarts/sankey.ts`; `echarts/sankeyTooltip.ts`; `editor/sankey/SankeySetupPanel.tsx`; `editor/sankey/SankeyMetadataFields.tsx`; `tests/unit/chart-compatibility/sankeyEngine.test.ts`; `tests/unit/chart-application/sankeySetupPanel.test.tsx` | Inactive options translator and controlled setup components; construct literal graph fixtures from shared types. No capture/storage/routing edits. |
| Controller SK3/SK4 | All existing integration files; new `application/sankeySession.ts`, `application/sankeySelection.ts`, `application/sankeyProjection.ts`, `application/sankeyTransactions.ts`, `application/sankeyAppearance.ts`; `tests/e2e/live-chart/sankey-fixture.ts`, `tests/e2e/live-chart/sankey-chart.spec.ts`; owning docs/inventory/breadth | Join only reviewed lanes; extend capture union and guards explicitly, including `RetainedApplicationCapture` in `hierarchyTypes.ts` and `isOrdinaryCapture`. Add gallery/thumbnail, session dispatch/projection/transactions/recapture and persisted family vocabulary. |

Parent integration paths include `editor/chartTypeGalleryCatalog.ts`, `editor/ChartTypeGallery.tsx`, application session modules, caller input/render modules and existing setup/customize routing. They are intentionally inaccessible to both workers. The controller may split its own integration responsibility to meet whole-file limits; shared contract changes stop affected lanes and receive review first.

Every production file must pass 400 physical lines, 300 logical units/file and 50/function. The controller registers all new paths in `.kiro/complexity-budgets.json` before acceptance. Reuse the implemented checker foundation; no new verification framework. From the root Linux/WSL toolchain use `pipeline/.venv/bin/python -m tools.quality.complexity --check --changes workspace=artifacts/chart-sankey/workspace-changes.json --changes data_api=artifacts/chart-sankey/data-api-changes.json --output artifacts/chart-sankey/complexity.json`. The controller creates actual scope manifests using the schema and pinned bases in [complexity checks](../../../docs/complexity.md); the data API manifest explicitly has no changes. This milestone-specific command is planned, not yet exercised. Retain focused test commands/exit codes and scoped typing/lint evidence; run the existing affected shared integration suite once at join.

## Financial fixture and acceptance boundary

Reuse `tests/e2e/live-chart/hierarchy-fixture.ts` and its `retainedHierarchy()` validation without editing that shared fixture. Require raw SHA256 `390dc8cbfc8302720a203bd9782d5e3b1f7363a4f762bdfcef079dbbe4c72f6b`. The four revenues are 124300000000, 95359000000, 94036000000 and 102466000000 USD; cost/gross-profit pairs are (66025000000,58275000000), (50492000000,44867000000), (50318000000,43718000000), (54125000000,48341000000). Verify each identity using BigInt before generating edges.

Generate 12 explicit CSV edges: `FY2025 revenue (derived sum)` to each `FY2025 Qn revenue (statement date)` using reported quarterly revenue, then each quarter to the shared `Cost of revenue` and `Gross profit` sinks. Dates are 2024-12-28, 2025-03-29, 2025-06-28 and 2025-09-27. Root outgoing is 416161000000 USD, a derived sum; it is not an independently reported annual observation. Use unit `currency`, currency `USD`, scale 1, period `AAPL FY2025`, measure `income-allocation`. The test-only `retainedSankey()` returns `{ csv, edges, total, provenance, hashes }`; edges retain quarter/date/measure/valueOrigin metadata and the CSV retains quarter/date labels. Reuse retained endpoint, parameters, retrieval and provenance hashes. Never describe this as cash flows or provider-supplied links.

SK4 performs one bounded application journey using this retained real FMP input and existing isolated browser fixtures: select mappings/metadata, independently compare all edges and four internal reconciliations, inspect an imbalance then correct it, remove/restore an invalid mapping, change supported theme, refresh, save/reopen and inspect actual PNG export. Capture all console/network diagnostic arrays before asserting. A fixture mismatch, changed raw hash or failed revenue identity blocks this example; synthetic fallback cannot establish live-data acceptance. Keep local source behavior, identified-image behavior, owner appearance acceptance and publication separately recorded. Selected sanitized real-FMP screenshots, milestone checkboxes, README/docs summaries, breadth and sync manifest are controller completion work. Anthropic-before-Excel remains unchanged.
