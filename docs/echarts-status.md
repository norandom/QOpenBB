# ECharts: done and open

ECharts renders editable charts created from table data. It supplies the chart engine behind the existing Workspace chart editor; it is not a universal translator for old Highcharts payloads.

Checked items below describe the implemented and reviewed scope, not every feature of the ECharts library. Remaining work belongs to analyst-workspace and does not block the accepted alpha.

## Done

- [x] Render Box Plot in the ordinary Table/File journey with retained-FMP raw-USD summaries, controls, navigation, lifecycle, save/reopen and PNG export. Owner appearance acceptance and B5 publication are complete; see the [published milestone](../.kiro/specs/analyst-workspace/box-plot-milestone.md).

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

- [ ] Complete other distribution and radial families.
- [x] Accept Radar Line and Radar Area locally (RD4). The [bounded milestone plan](../.kiro/specs/analyst-workspace/radar-milestone.md) separates original-behavior confirmation, parallel adapters, integration and packaged FMP acceptance. Radar source integration and packaged behavioral checks are independently accepted; the owner approved the current Line/Area appearance on 2026-10-24. Publication is verified as alpha-40086673952-1.
- [x] Accept Radar's original-behavior contract, retained-FMP fixture and inactive interfaces (RD0); [review](../artifacts/reviewed/chart-radar/rd0-review.md). Source integration and bounded packaged application acceptance are recorded below.
- [x] Independently accept inactive Radar editor/session adaptation (RD2): nine focused checks, validated Polar edits and preserved appearance composition. Source routing, packaged behavior and owner appearance approval are recorded below.
- [x] Independently accept the inactive Radar renderer (RD1): fifteen focused checks including eight ECharts SSR cases cover geometry, retained FMP values and appearance options. Source routing and bounded browser acceptance are recorded below; pixel identity is not claimed.
- [x] Accept Radar capture/setup (RD3a) at Workspace `eb74a5e7a0ee48b395efa8cf2a113cfdd5cb5933`: 172 focused regression tests, eight-file Biome and combined complexity pass; four inherited typing errors remain unchanged. [Evidence](../artifacts/reviewed/chart-radar/verification.md).
- [x] Independently accept source integration (RD3/RD3b) at Workspace `af226971c53922de5925d9b068fbfbd81df02527`: 88 distinct tests, 14 independently rerun, 18-file Biome and combined complexity pass. The 2,680 inherited typing errors are unchanged; historical pre-implementation RED evidence is missing.
- [x] Independently accept RD4 packaged behavior: two candidate family tests pass (2.0 minutes), with 15 retained FMP amounts, controls, refresh, fresh reopen, PNG export and candidate diagnostics. Original comparison passes one test (35.1 seconds), with a recorded CSV request failure. [Evidence](../artifacts/reviewed/chart-radar/verification.md#rd4-application-accepted).
- [x] Accept current Radar appearance, including the pictured visual differences (RD4). [Paired samples](../.kiro/specs/analyst-workspace/radar-milestone.md#fmp-samples).
- [x] Publish the accepted Radar milestone (RD5) as [alpha-40086673952-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-40086673952-1); both CI jobs, release assets and six anonymous pulls pass. [Publication evidence](../artifacts/reviewed/chart-radar/verification.md#published-radar-alpha).
- [x] Complete the ordinary Table/File Range Bar/Area journey with retained-FMP extrema, controls, navigation, fresh reopen and export. See the [accepted application milestone](../.kiro/specs/analyst-workspace/range-chart-plan.md); the accepted image pair is published.
- [x] Independently accept inactive Range capture/setup and Box regression checks (R4a).
- [x] Independently accept inactive Range series appearance and option precedence (R4b).
- [x] Independently accept inactive Range numeric value-axis planning and Box regression checks (R4c).
- [x] Independently accept numeric/time category geometry in both inactive Range renderer cores (R4d).
- [x] Preserve Range category type and native-Date evidence through capture and setup (R4e).
- [x] Compose Range Bar/Area with continuous axes, saved styling, measured chrome and reverse geometry (R4f).
- [x] Connect live Range sessions, retained controls, navigation and pointer lifecycle (R4g); [source evidence](../artifacts/reviewed/chart-range/verification.md#r4g-live-range-integration-accepted). Integrated Range zoom defaults are restored (R4h). Both packaged real-FMP journeys pass; publication is verified.
- [x] Implement and independently review the requested Range axis and legend refinements (R4i); default Area appearance accepted; navigator spacing and corrected default behavior pass both packaged FMP journeys; the accepted image pair is published.
- [x] Independently accept the inactive Range Area renderer core (R3).
- [x] Independently accept the inactive Range Bar renderer core (R2).
- [x] Implement and accept the bounded [Waterfall](../.kiro/specs/analyst-workspace/waterfall-milestone.md) application journey: retained-FMP financial geometry, default sign legend, controls, navigation, tooltips, refresh, fresh reopen and export pass; owner accepts the appearance.
- [x] Publish and verify the accepted Waterfall milestone images as alpha-40002594897-1; both source pins, release assets and six anonymous pulls are verified separately from local browser acceptance.
- [ ] Complete hierarchy, heatmap and other specialty families.
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

## Box Plot progress

- [x] Independently accept inactive Box axes/navigation and the existing-host adapter join (B3c).
- [x] Connect and source-review the Box editor/session and saved settings (B3d).
- [x] Run both Box browser journeys against the identified candidate image.
- [x] Source-review Box appearance refinements; see [verification](../artifacts/reviewed/chart-box/verification.md#b4-visual-refinement-source-accepted-image-comparison-pending).
- [x] Repair Box collision and duplicate layout handling at source level; [repaired-image browser checks pass; owner visual acceptance is recorded](../artifacts/reviewed/chart-box/verification.md#b4-runtime-layout-repair-source-accepted-new-image-required).
- [x] Complete the Box original/replacement and default miniature comparisons; owner approved on 2026-10-22.
- [x] Independently accept inactive Box capture and original aggregate setup (B3b).
- [x] Publish `alpha-39757904293-1` and verify both public service identities and six anonymous pulls.

B4 accepted Workspace `da5979c` and local image `4b7c12f0` after two browser scenarios and owner appearance approval on 2026-10-22. B5 publication passed CI run `39757904293` and independent anonymous-pull verification; published bytes and browser-candidate bytes are recorded separately. See [verification](../artifacts/reviewed/chart-box/verification.md).

## Evidence and ownership

The [UI worklist](../.kiro/specs/openbb-self-service/ui-parity-worklist.md) records accepted ordinary, horizontal, normalized and area journeys and the remaining UI-10 through UI-16 obligations. The [capability matrix](renderer-capability-matrix.md) records exact families and caller boundaries. These remain the detailed records behind this checklist.

[Renderer roles](../README.md#renderer-roles) · [Perspective](perspective-status.md) · [Plotly](plotly-status.md) · [Roadmap](roadmap.md)
