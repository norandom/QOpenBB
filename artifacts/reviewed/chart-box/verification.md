# Box Plot verification

B0 numerical design and B1 inactive numerical helper are independently accepted. Rendering, application appearance/behavior and publication remain open. The existing published alpha is unchanged.

The original Grid 34.1.1 `BoxPlotChartProxy` calculates each category/field independently: sorted minimum and maximum, with quartiles at `(n - 1) * q` and the original interpolation expression. It does not use IQR fences or separate outlier points. The reviewer checked the retained bundle SHA-256 `1a195685c473488defe1ce535e3115c26a42b2be94ad6ccc7fefa351eac7094f` and the actual source around lines 9664-9820. Original Workspace: `38dffc33389aca0e4a87e0e88d42f7067aa220df`.

The [frozen B1 design](../../../.kiro/specs/analyst-workspace/box-plot-design.md) accepts the existing normalized finite-number/null domain. Empty groups produce no summary; nonfinite inputs or derived arithmetic overflow return diagnostics. This is explicitly bounded behavior, not equivalence for the original proxy's admitted infinities. B1 is one inactive numerical helper plus focused tests; no renderer, editor or saved-state change is accepted yet.

Independent source/design review: `artifacts/chart-box/b0-review.md`. Read-only integration tracing confirms the existing Box Plot gallery item and identifies shared session/host boundaries. No tests, builds, browser checks or provider requests were run for B0. Preliminary mapper/fixture suggestions are not approved interfaces. Later contracts and executable evidence belong to the [milestone](../../../.kiro/specs/analyst-workspace/box-plot-milestone.md).

## B1 numerical helper

Workspace `85ca9ea247cc0c97add941b5007661b75941e734` adds only `compatibility/boxSummary.ts` and its focused compatibility test. Missing-module RED was captured before implementation. The final focused Vitest run and independent rerun each passed 31 tests; scoped strict TypeScript passes. Combined complexity passes with no errors or violations: helper 60 physical lines, 48 logical units and maximum 22 per function.

Tests cover original odd/even/two-value/decimal quartiles, minimum/maximum rather than outlier fences, singleton/empty/all-null groups, repeated/signed values, omitted nulls, immutable input, malformed/sparse/throwing input and nonfinite derived arithmetic. The helper has no renderer, grouping, provider, editor or persistence effects. Existing browser tests were not rerun for this inactive addition. Source review and logs remain under `artifacts/chart-box/b1-*`; application acceptance is explicitly pending.

## B2 renderer design

Independent review approved the [inactive renderer design](../../../.kiro/specs/analyst-workspace/box-plot-renderer-design.md) after corrections to category alignment, numeric domains, typing acceptance and engine-time errors. A bounded installed-ECharts 6 SVG experiment verified public numeric slot coordinates with explicit custom labels/ticks in both directions, including singleton categories and the original custom-padding counterexample. Coordinate, label/tick, pointer identity and clipping assertions passed. This establishes the coordinate mechanism, not application or Box Plot appearance acceptance.

Original source inspection also confirmed that numeric nicing can expand fractional constant domains and explicit bounds. The inactive mapper separates semantic and transport domains; B3 must reconcile original effective nicing/ticks before activation. The existing broad TypeScript scope has inherited diagnostics (compiler exit 2); B2 requires zero new diagnostics and zero diagnostics in its own files against the captured baseline, not a claimed clean application build. Design review and spike inputs remain local under `artifacts/chart-box/b2-*`. Renderer implementation, real-FMP application acceptance and publication are still open.
