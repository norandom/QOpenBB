# Horizontal-bar contract: source settled, miniature decision pending

Task 2.78 remains incomplete. Original numerical behavior and the navigator contract are established; the original grouped-bar miniature fails at runtime. The renderer/control fan-out waits for the owner's repair decision and final independent contract review.

## Numerical and axis contract

Original Workspace `38dffc33389aca0e4a87e0e88d42f7067aa220df` uses AG Charts 12.1.1. The retained Community bundle SHA-256 is `237912c75d2c7e8219fced7bb79e5ed8fca0f620d6f4d259cdfa58748445fcd1`; Enterprise is `dc8e6a2a500d577438dad28a10cfdb30b8524218a9ec617a6a2adf7400cc5f7f`.

Categories preserve input order from top to bottom. Grouped values start at zero; stacked values accumulate positive and negative values separately in selected series order. Labels/tooltips show raw observations. Missing values have no financial label and remain distinct from explicit zero even if their internal geometry has zero size. The source-derived synthetic fixture is prepared at `terminalpro/tests/unit/chart-compatibility/fixtures/horizontal-bars.json`; it is not yet an accepted production input.

Original source anchors: Community `DIRECTION_SWAP_AXES` 25910-25930, `CartesianChart.sizeAxis` 49018-49044, `Axis.setDomains` 17842-17854, `BarSeries.processData` 41394-41437, `buildGroupAccFn` 29201-29221, labels 41630-41637 and tooltip 41856-41880. These are installed bundle line numbers, not stable upstream API identifiers.

Horizontal bars initialize category/y/left and number/x/bottom. Current runtime bindings own physical direction; Horizontal section/title resolves x, Vertical resolves y, and sections render x before y while retaining semantic IDs. Style patches use actual option type and both positions for its direction. Latest-state rehydration prevents a stale control binding from routing an edit to the previous orientation.

Family transitions use the existing range/options/session owners, retain exact family keys and unknown branches, and establish destination orientation. Structural axes remain runtime-only under the original persistence contract; reopen reconstructs them. No saved axis fields or new persistence owner are introduced. Exact transition/reset behavior must be checked at the application join, not inferred from union admission.

## Observed navigator and miniature

Original navigator controls numeric X, not category Y. A native drag reduced the numerical visible extent while Alpha, Beta, Gamma and Delta remained in order. The original source agrees: Enterprise `NavigatorDOMProxy.updateZoom` 15525-15529 updates x only.

Enabling Show mini chart produces `AG Charts - internal config error: keys must come before values` and leaves its overview empty. The error appears after enabling miniature and before switching families; the menu then reads Hide mini chart. This is confirmed for groupedBar. Switching to stackedBar renders its main stacks and removes the navigator strip; it does not establish a separate stackedBar miniature failure.

Enterprise miniature theme code omits bar direction (21955-21960, 22121-22168); Community defaults to vertical bars (40874). That is a source-derived default, not a working original overview. A vertical categorical overview would not align its horizontal positions with the main chart's numeric-X zoom range.

Proposed repair for owner decision: show a full-data horizontal-bar overview in the existing miniature area, retain all selected series and signed-stack semantics, and keep the slider/mask aligned with numeric X. Preserve original controls, flags, theme and dimensions. This would intentionally repair the original empty overview; it must not be reported as pixel-identical original behavior.

## Evidence boundary

The [reviewed reference finding](../../../artifacts/reviewed/live-editor/horizontal-bars/miniature-finding/review.md) includes the original screenshot, exact identities and fixture adaptation. The original frontend's File fetch omits the current bearer; only this run's exact uploaded synthetic CSV request received the same authenticated session's bearer in memory. No data, response or chart state was substituted. This supports the renderer reference, not the original File authentication journey.

Whole-file complexity passes for the prepared shared type/predicate change. Compatibility type diagnostics are identical between HEAD and the candidate: the existing DS typography TS2578 remains. Broader application/session compiler checks fail on existing dependency/alias/type errors and are not claimed as passes. No runtime replacement feature is accepted by this contract record.
