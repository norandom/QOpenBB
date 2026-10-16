# Next chart integration boundary

## Overview

Owner-approved design for the next isolated chart slice, following accepted tasks 2.13-2.18. It establishes lossless resolved data snapshots and three Cartesian render mappings. It does not enable a reduced chart experience in Workspace. Original controls, themes, flags and outcomes remain the release target under requirements 4.8-4.9.

Source baseline: Workspace `042ba87e3208a51857da4ae2d1c3109a680716d9`; original behavior reference `38dffc33389aca0e4a87e0e88d42f7067aa220df`. This amendment supplements the parent design; all other requirement coverage stays with that design. The owner approved this design and the bounded tasks 2.19-2.23.

## Boundary Commitments

### This slice owns

- An immutable, validated copy of already resolved chart observations, selected columns, captured state address and provenance.
- Pure ECharts mapping for flat, unaggregated `groupedColumn`, `stackedColumn` and `line` snapshots.
- Isolated composition with the accepted EChartsHost, including settings-only render revisions and family replacement.

### Out of Boundary

Actual grid capture, provider fetching, financial transformations, aggregation, pivot/grouping, remote-page completeness, editor field mapping, storage writes, SQLite repair and application activation remain separate work. These exclusions bound development, not the final feature set. No existing control, feature flag, rejection guard or application caller changes in this slice.

### Allowed Dependencies

Use locked ECharts 6.0.0, current TypeScript tooling, existing compatibility JSON types and the accepted EChartsHost. Snapshot code must not import GridApi, React, ECharts, dashboard stores or providers. Translators depend on snapshots and ECharts types, never on grid/store internals. Add no runtime dependency or generic renderer framework.

### Revalidation Triggers

Changes to input values/order, type definitions, source revisions, theme projection, supported settings, ECharts lock or lifecycle revision rules require affected unit/browser checks to rerun. Actual grid adoption requires new original-source capture evidence and a separately reviewed integration boundary.

## Architecture

The original `Chart/utils.tsx:603` returns `rowData:null` for ordinary integrated charts. The grid owns those observations. Transformed paths use displayed/filter/sort traversal and custom transpose rules. Therefore this slice takes explicitly resolved rows; it must not pretend that `createRangeChart` options are a universal data source.

Flow: resolved synthetic input -> snapshot validation/copy -> family translator -> EChartsHost. A fixture controller issues a strictly increasing render revision for each accepted options change. The snapshot keeps its data revision separately. Neither data revision nor active dashboard partition is used to infer render ordering.

### Data contract

`ResolvedSnapshotInput` contains: string stateAddress; finite dataRevision; opaque original JSON chart model; source mode; unique ordered selected column IDs; categoryColumnId; column descriptors (stable ID, display label, category/number role, unit metadata); ordered rows (stable ID, string/number category, per-column finite number/null/missing values); and original selected-range bounds retained as JSON. categoryColumnId must be included in the selection. Each row.category is the value of that descriptor; per-column values contain numeric descriptor IDs only. Category observations are explicit ordered rows, not a map keyed by label. Repeated labels remain separate observations.

The validator returns a discriminated success/error result with field paths. It rejects duplicate column/row IDs, unknown selected IDs, anything other than exactly one category descriptor matching categoryColumnId, no selected numeric series, nonfinite values/revisions and invalid JSON provenance. Missing cells remain missing and null remains null in the snapshot; neither becomes zero. It clones nested structures, never mutates inputs, and exposes deeply readonly types. Source mode records flat, transformed, grouped, pivot or remote-page inputs; only flat is renderable in this slice. Valid opaque model fields are preserved without claiming semantic support.

`ResolvedCartesianStyle` is an explicit render input, not an AG options decoder: background, ordered palette, text color/font family/font size, optional title text, legend visibility/position, per-series color/line width, and value display precision. Series overrides use column IDs. All colors are strings, dimensions finite nonnegative numbers, precision integer 0-20, legend position top/bottom/left/right. Input validation rejects invalid values. This slice accepts resolved styles from fixtures only; it must not infer original saved-option paths or introduce production defaults.

`translateCartesian(snapshot, family, style)` returns supported options or an explicit unsupported/invalid result. Exact family names are `groupedColumn`, `stackedColumn`, `line`; no fallback. Grouped columns have separate bar series; stacked columns share one stack; line has line series and no bar/stack residue. Selected numeric columns determine series order; descriptor IDs determine identity; labels are display-only. Categories preserve supplied order, including descending dates and duplicates. Values keep original numeric precision; rounding affects display only. Missing/null values produce gaps rather than zero. Negative stacks require numeric/visual verification. All selected numeric descriptors must carry the same explicit unit and scale for this single-axis boundary (including an explicit dimensionless unit where appropriate). Missing or incompatible unit/scale metadata returns unsupported; no conversion or secondary-axis inference occurs. This isolated restriction does not add a production rejection guard. Multi-axis and mixed-unit original behavior needs its own resolved contract before adoption.

Axis categories use ordinal positions internally and label formatting from the corresponding observation, preventing duplicate labels from merging. Export/tooltip labels must display the observation label, not the ordinal. No aggregation, sorting, resampling, percent conversion or currency conversion occurs. Financial metadata survives unchanged. Unknown opaque model options are retained but are not interpreted by this translator; its supported result describes only this explicit resolved-input contract, not full legacy-model support.

### Failure behavior

Invalid snapshots and unsupported families/source modes return structured errors without constructing partial options. The isolated fixture displays the diagnostic and does not submit a render request. This is not a proposed production error UX. Rendering failures use the accepted host error/recovery contract. No snapshot or original model is rewritten after failure.

## File Structure Plan

All frontend paths below are under `vendor/workspace/terminalpro/`.

| Path | Responsibility |
| --- | --- |
| `src/components/General/Table/Chart/compatibility/snapshotTypes.ts` | Snapshot and validation result contracts |
| `src/components/General/Table/Chart/compatibility/snapshot.ts` | Validation and immutable copy |
| `src/components/General/Table/Chart/echarts/cartesianTypes.ts` | Resolved style and translation result contracts |
| `src/components/General/Table/Chart/echarts/cartesian.ts` | Three family option construction and style projection |
| `tests/unit/chart-compatibility/snapshot.test.ts` | Input fidelity and failure cases |
| `tests/unit/chart-compatibility/cartesian.test.ts` | Values, identity, styles and family mapping |
| `tests/e2e/chart-compatibility/cartesian.html` and `cartesian.tsx` | Isolated host composition and revision owner |
| `tests/e2e/chart-compatibility/cartesian.spec.ts` | Render/update/export/recovery observations |
| Existing chart fixture Vite/Playwright configuration | Register the isolated fixture only |

Controller owns root complexity inventory, breadth mapping and verification documentation. Existing reducers and host remain unchanged unless a demonstrated contract defect returns this design for review. Every new production file must pass 400 physical lines, 300 logical units and 50 units/function; split only by demonstrated responsibility. No exceptions proposed for this slice.

## Requirements Traceability and Testing Strategy

This slice contributes evidence to 4.8 and 4.9; it cannot complete them. Original UI and complete legacy behavior require later integrated comparisons. Requirements 10.1-10.2 require headless isolation and sanitized CDP diagnostics. Requirement 10.3 is supported by reproducible isolated browser checks; 10.4 by one browser worker and separate fixture outputs; 10.5-10.6 by explicit breadth status separating foundation results from unverified product parity. Requirements 4.2 and 4.7 remain blocked on separate real persistence acceptance.

- Snapshot tests: selected/series order, duplicate display labels with distinct IDs, repeated categories, descending dates, zeros/null/missing, negative and fractional values, immutable copies, unknown JSON retention, invalid/nonfinite inputs and unsupported source modes.
- Translator tests: exact raw numeric values; reordered series retaining ID-bound styles; negative stacks; label/tooltip ordinal substitution; display-only precision; title/legend/palette changes; unsupported families; all three families' exact series/stack properties.
- Browser: render all three families with labelled synthetic Revenue/Costs in the same currency and scale; verify settings-only update at unchanged data revision, stacked-to-line replacement, resize, PNG export and host recovery. Record numeric option evidence and image evidence; screenshots alone do not prove numeric correctness. Use one isolated background browser, sanitized CDP diagnostics and owned cleanup.
- Run existing foundation units and isolated browser regressions, strict TypeScript and maintained-module complexity checks. Register actual new tests in breadth only once implemented; passing this slice never marks renderer parity passed.

## Delivery Sequence

After design approval, generate bounded tasks. Controller freezes snapshot/style contracts first. Sol snapshot and translator workers can then run concurrently with exclusive paths and shared frozen fixture definitions. Astra reviews the financial mapping and join. Controller serializes browser/build work and the final shared-module audit. Implementation is authorized only within approved tasks 2.19-2.23.

## Remaining Discovery

Update after this slice's acceptance: seven outgoing original-editor payloads were subsequently captured using the verified save shortcut. See [option discovery](chart-option-discovery.md) and the [approved option-state design](chart-option-state-design.md). The capture gap described below is historical; effective styling and real persistence remain open.

Capture actual original editor save payloads before designing a legacy-field registry. Current capture waited eight seconds; both inspected revisions dispatch state at 30 seconds and dashboard saves at 60 seconds. Observe that schedule or verify an explicit save action before repeating capture. An observed outgoing body is not proof of successful persistence.

SQLite is a separate proposed repair: six dialect-specific string expressions plus real CRUD tests. Source review also found an entity-sharing creator query missing its User join. Neither concatenation probes nor engine recreation establish service restart/reopen acceptance. Keep this work separately reviewed, without introducing another database or adapter service.
