# Box Plot verification

B0 numerical design, B1 numerical helper and B2 inactive renderer are independently accepted. Application integration, appearance/behavior and publication remain open. The existing published alpha is unchanged.

The original Grid 34.1.1 `BoxPlotChartProxy` calculates each category/field independently: sorted minimum and maximum, with quartiles at `(n - 1) * q` and the original interpolation expression. It does not use IQR fences or separate outlier points. The reviewer checked the retained bundle SHA-256 `1a195685c473488defe1ce535e3115c26a42b2be94ad6ccc7fefa351eac7094f` and the actual source around lines 9664-9820. Original Workspace: `38dffc33389aca0e4a87e0e88d42f7067aa220df`.

The [frozen B1 design](../../../.kiro/specs/analyst-workspace/box-plot-design.md) accepts the existing normalized finite-number/null domain. Empty groups produce no summary; nonfinite inputs or derived arithmetic overflow return diagnostics. This is explicitly bounded behavior, not equivalence for the original proxy's admitted infinities. B1 is one inactive numerical helper plus focused tests; no renderer, editor or saved-state change is accepted yet.

Independent source/design review: `artifacts/chart-box/b0-review.md`. Read-only integration tracing confirms the existing Box Plot gallery item and identifies shared session/host boundaries. No tests, builds, browser checks or provider requests were run for B0. Preliminary mapper/fixture suggestions are not approved interfaces. Later contracts and executable evidence belong to the [milestone](../../../.kiro/specs/analyst-workspace/box-plot-milestone.md).

## B1 numerical helper

Workspace `85ca9ea247cc0c97add941b5007661b75941e734` adds only `compatibility/boxSummary.ts` and its focused compatibility test. Missing-module RED was captured before implementation. The final focused Vitest run and independent rerun each passed 31 tests; scoped strict TypeScript passes. Combined complexity passes with no errors or violations: helper 60 physical lines, 48 logical units and maximum 22 per function.

Tests cover original odd/even/two-value/decimal quartiles, minimum/maximum rather than outlier fences, singleton/empty/all-null groups, repeated/signed values, omitted nulls, immutable input, malformed/sparse/throwing input and nonfinite derived arithmetic. The helper has no renderer, grouping, provider, editor or persistence effects. Existing browser tests were not rerun for this inactive addition. Source review and logs remain under `artifacts/chart-box/b1-*`; application acceptance is explicitly pending.

## B2 renderer design

Independent review approved the [inactive renderer design](../../../.kiro/specs/analyst-workspace/box-plot-renderer-design.md) after corrections to category alignment, numeric domains, typing acceptance and engine-time errors. A bounded installed-ECharts 6 SVG experiment verified public numeric slot coordinates with explicit custom labels/ticks in both directions, including singleton categories and the original custom-padding counterexample. Coordinate, label/tick, pointer identity and clipping assertions passed. This establishes the coordinate mechanism, not application or Box Plot appearance acceptance.

Original source inspection also confirmed that numeric nicing can expand fractional constant domains and explicit bounds. The inactive mapper separates semantic and transport domains; B3 must reconcile original effective nicing/ticks before activation. The existing broad TypeScript scope has inherited diagnostics (compiler exit 2); B2 requires zero new diagnostics and zero diagnostics in its own files against the captured baseline, not a claimed clean application build. Design review and spike inputs remain local under `artifacts/chart-box/b2-*`. At design review, renderer implementation was still open. B2 implementation is recorded below; real-FMP application acceptance and publication remain open.

## B2 inactive renderer

Workspace `95188eb3ac92188e62f32b8ba9d4897a6c8cc176` adds ten mapper modules and two focused test files. Independent review freshly reran the canonical focused suite: 40 tests pass (31 numerical helper, six mapper and three grouped real-ECharts SVG tests). Scoped Biome passes all 12 files. Combined complexity passes with zero errors or violations. No application routing, gallery, editor, provider or persistence code changed.

The engine checks cover vertical/horizontal box geometry, original band/group padding, null-category pointer identity, singleton/cap/median/whisker styles, native legend hide/remap, resize and SVG export, constant/empty/clipped data and renderer-error propagation through the existing lifecycle. Raw USD and B1 statistics remain unchanged. Missing-module and throwing-callback RED evidence preceded their fixes. Synthetic engine checks establish the inactive boundary only; real-FMP application evidence remains pending.

Final typing reports no diagnostics in B2 files. Both baseline and candidate retain 3,427 inherited diagnostics and compiler exit 2. Raw diagnostic comparison differs only at unchanged TableSettings.tsx(185,38), TS2769, where union members render in reversed order; independent review accepted that exact semantic-equivalence case. The raw comparison remains marked false and is retained locally, rather than presented as a clean TypeScript build. Initial checker execution lacked the pinned Node PATH; the corrected pinned-tool run passed.

Source review and reviewed-file hashes are retained in `artifacts/chart-box/b2-source-review.md` and `b2-source-reviewed-files.json`; focused test, lint, typing and complexity logs stay local. B3 must reconcile original effective numeric nicing/ticks and preserve existing capture, controls and host failure behavior before activation. B4 real-FMP image acceptance and B5 publication are still open.
