# ECharts: done and open

ECharts renders editable charts created from table data. It supplies the chart engine behind the existing Workspace chart editor; it is not a universal translator for old Highcharts payloads.

Checked items below describe the implemented and reviewed scope, not every feature of the ECharts library. Remaining work belongs to analyst-workspace and does not block the accepted alpha.

## Done

- [x] Render Pie and Donut, including saved `doughnut`, in the ordinary Table/File journey with captured-FMP values, controls, native legend paging, save/reopen and export. See the [published milestone](../.kiro/specs/analyst-workspace/pie-milestone.md).

- [x] Render Histogram in the ordinary Table/File journey with captured-FMP bin/count acceptance, editor controls, navigation, save/reopen and export. See the [published milestone](../.kiro/specs/analyst-workspace/histogram-milestone.md).

- [x] Repair the reported bubble spread and miniature overflow in a packaged image with captured FMP data; see [X6 evidence](../artifacts/reviewed/chart-xy/bubble-correction.md). Closer axis labels and main-marker clipping are also [accepted and published](../artifacts/reviewed/chart-xy/bubble-label-refinement.md).

- [x] Render Column & Line, Area & Column and Custom Combination with per-series axes, saved styling, navigator/theme/refresh retention and captured-FMP application acceptance. See the [accepted milestone](../.kiro/specs/analyst-workspace/chart-port-milestone.md).

- [x] Install ECharts 6.0.0 and provide the React host, lifecycle and chart-state foundation.
- [x] Connect the ordinary Table/File journey to the existing Chart, Set Up and Customize editor.
- [x] Render line, grouped column and stacked column charts in that journey.
- [x] Render grouped and stacked horizontal bars.
- [x] Render normalized columns and bars.
- [x] Render ordinary, stacked and normalized area charts.
- [x] Connect representative title, series, axis, legend, tooltip and theme edits for the accepted ordinary journey.
- [x] Connect ordinary category/series selection, ordering, filtering, Sum/Avg and orientation changes.
- [x] Apply owner-reviewed visual refinements, including line legends, gallery drawings and tab typography.

## Open

- [ ] Complete Box Plot through the [active milestone](../.kiro/specs/analyst-workspace/box-plot-milestone.md). Its inactive numerical helper, renderer, category capture and aggregate setup are independently accepted; axes/navigation and the existing-host adapter join are also accepted; editor/session activation is independently source-accepted; identified-image application acceptance remains open.
- [x] Independently accept inactive Box axes/navigation and the existing-host adapter join (B3c).
- [x] Connect and source-review the Box editor/session and saved settings (B3d).
- [ ] Run the prepared Box browser journeys against an identified image; original comparison remains pending.
- [x] Independently accept inactive Box capture and original aggregate setup (B3b).
- [ ] Complete other distribution and radial families.
- [ ] Complete Range Bar/Area through the [parallel foundation plan](../.kiro/specs/analyst-workspace/range-chart-plan.md). The inactive min/max helper and Range Bar/Area cores are accepted; application acceptance remains open.
- [x] Independently accept the inactive Range Area renderer core (R3).
- [x] Independently accept the inactive Range Bar renderer core (R2).
- [ ] Complete hierarchy, heatmap, waterfall and other specialty families.
- [ ] Complete standalone, AI-chart and theme-preview caller integration.
- [ ] Accept category-axis type/time-format persistence in an identified image; source implementation exists.
- [ ] Complete remaining saved-state behavior, exports and caller-specific controls.
- [ ] Verify the broader renderer inventory in the assembled application without hidden feature reductions.
- [ ] Apply the shared analyst theme and instrument/time-linking contracts as those features are implemented.

## Current combination-chart delivery

- [x] Independently accept the editor and packaged-image journeys with captured FMP data, save/reopen/export and navigator/theme/refresh retention.
- [x] Publish the updated tagged alpha and verify anonymous image pulls.

See the [reviewed evidence](../artifacts/reviewed/chart-combo/verification.md). Publication does not establish acceptance of the unfinished families below.

## Remaining port acceptance

- [ ] Exercise each completed chart milestone with real FMP responses in the application, checking plotted values, units, dates and transformations.
- [ ] Verify the milestone's applicable controls, refresh, save/reopen, theme and export behavior; retain synthetic edge-case checks.
- [ ] Close the former Highcharts caller/configuration gaps with functioning replacements, not unavailable placeholders or hidden features.
- [ ] After independent review, dispatch the image pipeline once for the completed milestone and publish its tagged alpha.

These are completion criteria for the remaining port. Earlier checked source/functionality items above do not imply comprehensive live-FMP acceptance. Ordinary pushes run checks without rebuilding images.

## Scatter/bubble progress

- [x] Repair bubble endpoint spacing and miniature clipping against the original application; replace the real-FMP sample after verification.
- [x] Publish the corrected image milestone.
- [x] Match original axis labels more closely and resolve slight main-marker edge overlap; independently verified in small/wide FMP views after the owner request.
- [x] Publish the label-refinement image milestone.
- [x] Resolve paired/unpaired X/Y/size identities with source-compatible ordering and incomplete-group behavior; independently reviewed focused tests and complexity checks passed.
- [x] Implement the inactive numeric mapper, with independent review and actual ECharts geometry/tooltip checks.
- [x] Connect and source-review the existing editor/application, including original empty-domain behavior for excluded one-sided bounds.
- [x] Accept captured-FMP application journeys, synthetic scatter/bubble edge cases and prior-family regressions.
- [x] Publish and verify the completed milestone.

Source and packaged-image application acceptance passed. The updated alpha is published with both public image identities and anonymous pulls verified. See [task evidence](../artifacts/reviewed/chart-xy/verification.md).

## Histogram progress

- [x] Review the numerical contract and capture 40 quarterly FMP revenue observations.
- [x] Implement and independently accept inactive binning, including boundaries and observation membership.
- [x] Render numeric intervals with independently checked geometry and native legend restoration in the inactive mapper.
- [x] Connect and independently source-review existing editor and application controls.
- [x] Source-review automatic axis rounding and retained zoom/reset scales.
- [x] Source-review endpoint-label overflow and original Bin count control order.
- [x] Source-review miniature height, plot alignment and full-bin labels.
- [x] Accept identified-image FMP journeys, synthetic edge cases and prior-family regressions.
- [x] Publish and verify the completed histogram milestone.

See [verification](../artifacts/reviewed/chart-histogram/verification.md). The updated alpha includes histogram; both public image identities and anonymous pulls are verified.

## Pie and donut progress

- [x] Review original first-field pie, concentric donut assignments and saved alias.
- [x] Implement and independently accept inactive assignment semantics.
- [x] Implement and independently accept inactive rendering.
- [x] Connect and source-review existing controls and application flow.
- [x] Repair title/legend editor transactions found by the first image run; source tests and independent review pass.
- [x] Restore effective pie legend defaults and retain original title/legend appearance; source checks pass.
- [x] Implement and source-review native legend paging, keyboard access and fitted donut titles.
- [x] Accept identified-image FMP, owner-reviewed appearance and lifecycle behavior.
- [x] Publish and verify the completed milestone.

P4 application acceptance passed on the identified pie/donut candidate: captured-FMP values, synthetic edge cases, controls, paging, refresh, save/reopen, export and five prior-family journeys. The owner accepted the disclosed default appearance differences. P5 published `alpha-39584871538-1`; both CI-built public image identities and six anonymous pulls are verified separately from local browser acceptance. See [verification](../artifacts/reviewed/chart-pie/verification.md).

## Evidence and ownership

The [UI worklist](../.kiro/specs/openbb-self-service/ui-parity-worklist.md) records accepted ordinary, horizontal, normalized and area journeys and the remaining UI-10 through UI-16 obligations. The [capability matrix](renderer-capability-matrix.md) records exact families and caller boundaries. These remain the detailed records behind this checklist.

[Renderer roles](../README.md#renderer-roles) · [Perspective](perspective-status.md) · [Plotly](plotly-status.md) · [Roadmap](roadmap.md)
