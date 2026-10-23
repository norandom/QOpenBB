# Keep Waterfall editable with no selected series

The first packaged FMP run on 23 October exposed a recovery failure: removing the last value series saves an empty selection, then the Waterfall selector rejects it. The editor disappears and its Add a series action cannot recover the chart. This repair implements the existing requirement to preserve the original editor flow; it adds no analyst-facing feature or flag.

## Reviewed repair

Independent integration review approved this bounded design after the owner authorized continued verification tonight. Introduce a Waterfall observation policy that admits category-only selection while retaining ordinary finite raw values, aggregation and single-axis unit checks. Do not borrow Histogram/Pie coercion or statistical grouping semantics.

Represent an absent selected field explicitly. After validating source, context and axes, an empty renderer returns the existing chart chrome with no series, pointer or navigation callbacks. Do not synthesize a placeholder field, zero movement or missing observation. Keep the complete retained capture available for re-addition; a fresh empty saved chart must also recapture current values correctly. Editor changes with no selected field retain a zero series count.

Production scope under the chart directory:

- compatibility: snapshotTypes.ts, snapshot.ts.
- application: histogramCapture.ts, setupProjection.ts, waterfallSessionSelection.ts, waterfallTypes.ts, waterfallEditorTransaction.ts.
- echarts: waterfall.ts, waterfallInteraction.ts.

The existing capture, setup transition, editor and host owners remain authoritative. No AgChartView or lifecycle rewrite is planned. Every modified whole production file must pass 400 physical lines, 300 logical units and 50 units per function, with explicit inventory scope.

## Completion checks

- [x] Actual session hook: remove the last series, retain ready empty editor state, edit appearance with series count zero, then re-add the original values and recover cumulative bars.
- [x] Fresh saved-empty capture and refresh retain usable controls; adding a field uses current captured values.
- [x] Explicit policy permits empty Waterfall selection while default strict admission, single-axis unit checks and malformed nonempty data remain enforced.
- [x] Empty renderer has no invented data or interactive callbacks; selected-field mismatches remain invalid.
- [x] Independent implementation review, focused regressions and combined complexity pass.
- [ ] An identified rebuilt image passes the original packaged remove/re-add journey with retained real-FMP data.

Evidence begins at artifacts/chart-waterfall/candidate-run-1. Implementation and review records belong under artifacts/chart-waterfall/empty-selection. An isolated initial-field diagnostic is explicitly not acceptance of this recovery requirement.
