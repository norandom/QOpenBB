# Scatter and bubble chart milestone

Restore scatter and bubble in the ordinary Table/File journey, preserving the existing Workspace controls, themes and saved options. This follows the published combination-chart milestone under the owner's autonomous chart-port direction. Standalone and AI callers remain open separately.

## Acceptance

Selected numeric columns must retain their original X/Y/size assignment, order and observations. Both axes are numeric. Pairing, labels, marker appearance and applicable navigator/editor controls must work through the existing widget state owner. No hidden controls, replacement editor or silent data transformation counts as parity.

Verify the application with captured FMP annual data: revenue as X (USD), net income as Y (USD), EPS as bubble size (USD/share), fiscal period as label. Check actual coordinates, sizes, tooltips, both themes, refresh, save/reopen and export. Synthetic regressions cover incomplete groups, multiple series, missing values and size-scale edge cases. Publish images once the complete milestone passes independent review and application acceptance.

## Tasks

- [x] X1. Freeze and implement the inactive numeric-field assignment contract, with focused tests for paired/unpaired scatter/bubble, selected order, incomplete groups, defaults, malformed input and immutability. Own `compatibility/xyAssignments.ts` and its unit test only. No gallery activation, state writes or geometry. Independently accepted at `e343e16`; see [evidence](../../../artifacts/reviewed/chart-xy/verification.md).
- [x] X2. Implement the [independently reviewed numeric mapper contract](xy-mapper-design.md), including bubble-size, marker, axis and appearance behavior, and focused real-engine checks. Ownership is new `echarts/xy*.ts` and focused XY mapper tests; no shared helper or production routing edits. Independently accepted at `7e509d3`; the documented excluded-bound diagnostic remains an X4 parity obligation.
- [ ] X3. Connect pairing and XY field roles to the existing editor/session through the [reviewed production join](xy-production-join.md). Preserve option paths and inactive settings.
- [ ] X4. Complete that same cohesive join: family routing, caller defaults, appearance, navigator and refresh behavior. Preserve original empty geometry for one-sided bounds that exclude all observations; the inactive mapper's safety diagnostic is not final parity. Verify captured-FMP application journeys and prior-family regressions.
- [ ] X5. Independent feature review, breadth and README/docs checklist reconciliation, reviewed evidence sync, commits/push and one tagged alpha publication with anonymous pull verification.

Task X1 is independent of the unresolved geometry questions in [source research](xy-chart-research.md). X2 and X3 may run in parallel only after an independently reviewed interface and exclusive file ownership are recorded. Shared production integration and commits remain serialized.

X2 is now accepted. Independent review approved one cohesive X3/X4 implementer because session, editor and caller wiring share contracts. Source review and focused tests precede the packaged-image application gate; neither alone closes X4.

Each production task must pass the existing whole-file complexity gate: 400 physical lines, 300 logical units per file and 50 per function. Extend maintained inventory for additions; tests and documentation are excluded. Keep per-task independent review and commits. Retain unrelated Perspective work.
