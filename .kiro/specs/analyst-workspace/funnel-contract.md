# Funnel-family implementation proposal

Replace the three existing gallery variants through the current Table/File chart session and ECharts host. Native characterization is recorded in [the milestone](funnel-milestone.md). On 2026-10-26 the owner approved the explicit missing/signed-input rules below. Each executable task still requires frozen interfaces, bounded ownership and independent review before acceptance.

## Data and financial meaning

1. Reuse ordinary retained snapshots, source-value provenance and setup projection. Preserve row order and distinct row identity when aggregation is off. Reuse the existing aggregation owner: observed native Sum combines duplicate stage labels. Do not add a second capture or aggregation implementation.
2. Project one category and the first selected numeric field, retaining the saved full range. The native selector can retain several fields, but the observed chart uses the first. Removing the first selected field was not exercised; do not describe the observed Reserve selection as a confirmed application bug.
3. Preserve reported values and units. Labels and tooltips identify the stage and selected field; display formatting must never change geometry inputs. Retained AAPL income-statement levels overlap financially and are not additive components of revenue or conversion counts.
4. Approved missing-value rule: retain the stage identity but draw no value shape or fabricated zero tooltip. Do not connect a Cone or drop-off polygon across a missing endpoint. Genuine zero remains distinct from missing. No nonfinite coordinate may reach ECharts.
5. Approved signed-value rule: Funnel and Cone use centered magnitude cross-sections with explicitly signed labels/tooltips, normalized against the maximum absolute finite value. An all-zero domain must not divide by zero. Pyramid requires finite nonnegative observations with a positive total; use stable scaled normalization to avoid overflow when summing individually finite values. Otherwise show an accessible explanation in the existing chart surface, retaining all controls and source data. Missing stages do not contribute to its total. The owner approved these explicit data rules on 2026-10-26.
6. Empty selection and empty usable data recover through the existing session when fields or data return. Do not rewrite stored payloads to make an unsupported input render.

## Geometry and appearance

Use custom ECharts rectangles and polygons through the existing lifecycle. Built-in funnel stages have equal axial thickness and cannot express the native Pyramid contract by configuration alone.

| Variant | Required geometry | Reachable variant controls |
| --- | --- | --- |
| Funnel | Ordered centered bars with separately styled optional drop-off connectors | Numeric Labels, Stage Labels, Drop-Off, Shadow and common series styling |
| Cone Funnel | Ordered neighboring magnitude cross-sections joined into tapered stages | Numeric Labels, Stage Labels and common series styling; no added Drop-Off/Shadow controls |
| Pyramid | Ordered triangular slices whose axial thickness is value divided by total; do not use equal-area slices | Numeric Labels, Stage Labels, Shadow and common series styling |

Retain Vertical/Horizontal direction, existing palette/theme, Chart Style, Titles, tooltip and series controls. Keep numeric labels separate from stage labels. Native editor observations expose no Axes, Legend or Navigator panels for these variants; do not import Cartesian controls merely because the shared renderer supports them. Keep exact existing gallery entries and editor flow.

The renderer must retain source-row identity for hit testing, clipping, labels and tooltips. Resize and PNG export stay with the existing host; no parallel canvas lifecycle. Native reload metadata changes and visibly absent numeric labels in the Cone/Pyramid reload PNGs are findings, not permission to lose replacement labels, selection or saved appearance. The cause of the original label loss is unresolved.

## Task boundaries and fan-out

- **F1, data contract:** controller freezes types and admission policy; implementer owns new `compatibility/funnelContracts.ts`, focused adapter/projection helpers and tests. Reuse ordinary selection/aggregation. Independent review checks finite geometry inputs, duplicate identity, chosen field, missing/zero/sign handling and financial fixture values.
- **F2, renderer and controls:** freeze render inputs, resolved appearance and edit intents before two disjoint lanes. Geometry owns new `echarts/funnel*` modules and tests. Controls owns new `application/funnel*` and `editor/funnel/*` modules and tests. Names are responsibilities, not a mandate to create unnecessary files. Neither lane edits shared routing.
- **F3, integration:** controller owns family unions, caller/theme routing, setup projection, session dispatch, editor branches, inventory and breadth mapping. Preserve stale-transaction rejection and family transitions. Shared `echarts/lifecycle.ts` is already 394 physical lines; avoid changes or design a cohesive extraction first.
- **F4, application acceptance:** one identified packaged image, retained FMP financial assertions and original/replacement comparisons in qView. Verify selected-field changes, applicable controls, themes, resize, refresh, empty recovery, fresh save/reopen and PNG output with strict candidate diagnostics. Source option equality alone is insufficient.
- **F5, delivery:** independently reviewed examples and checkboxes, per-task source commits, one completed-milestone image build, tagged alpha and anonymous image pulls. Do not rebuild on each implementation push.

Every modified production file must pass the existing scope inventory and caps of 400 physical lines, 300 logical units per file and 50 per function. Independent reviews and focused tests remain mandatory. Only one heavy build/suite runs at a time; background browser work uses one worker and no retries. Research and test artifacts do not count as production modules.

## Acceptance limits

This contract covers ordinary Table/File charts. Other callers, table capabilities, first-login diagnostics and assembled deployment retain separate obligations. Original CSV errors are documented baseline findings and must not be suppressed in candidate acceptance. Raw provider data, accounts and browser traces stay ignored; publish only selected reviewed reports and financial screenshots with exact identities.
