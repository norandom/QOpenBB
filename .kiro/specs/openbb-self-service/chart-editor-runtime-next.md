# Nested editor contracts from the focused original capture

Selected nested editor paths now have runtime evidence. Full editor/application readiness remains blocked by the explicit gaps below. This 2026-10-17 evidence extends [the prior failed probe](chart-editor-runtime-contract.md) and [the editor inventory](echarts-editor-contract.md); it does not replace their untouched scopes or approve implementation.

Original owned source `38dffc33389aca0e4a87e0e88d42f7067aa220df`, unchanged image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`. The focused headless disposable-runtime journey exited 0 with 18 successful UI actions, zero action failures and 22 offline evidence assertions. One earlier action attempt failed and remains preserved. [Report](../../../artifacts/parity/editor-runtime-next/report.md), [patch ledger](../../../artifacts/parity/editor-runtime-next/patch-ledger.json), [control ledger](../../../artifacts/parity/editor-runtime-next/control-ledger.json), [domains](../../../artifacts/parity/editor-runtime-next/domains.json) and [verification](../../../artifacts/parity/editor-runtime-next/verification.json) own the detailed evidence.

## Contract boundary

The previous Horizontal Axis failure was whitespace in the title-bar textContent, not an absent control or incorrect class. The successful collector waits for the editor and accepts surrounding whitespace. It reads named original chart/grid references with a bounded parent walk, then finite field projections. No generic recursive runtime inspector is used.

| Control | Runtime contract |
| --- | --- |
| Horizontal label Padding | UI 9 writes `bar.axes.category.top/bottom.label.spacing = 9`; effective bottom-axis spacing is 9. Preserve the difference between the UI word and stored field. |
| Horizontal Auto Rotate | Off writes `bar.axes.category.top/bottom.label.autoRotate = false`; effective false is retained. |
| Vertical line Thickness | UI 3 writes `bar.axes.number.left/right.line.enabled = true` and `.width = 3`; effective left-axis width is 3. Grid Lines owns a different Thickness input. |
| Vertical label Size | Dropdown 14 writes `bar.axes.number.left/right.label.fontSize = 14`; effective 14. |
| Column Labels and Stroke Width | `bar.series.label.enabled = true`; `bar.series.strokeWidth = 3`; both effective series match. Enabled labels reveal Font/Weight/Size/Color. |
| Legend Weight/Size | Bold writes `bar.legend.item.label.fontWeight = "bold"` plus `.fontStyle = "normal"`; Size 14 writes `.fontSize = 14`. |
| Legend marker/spacing | Marker Size 15 writes `bar.legend.item.marker.size`; Horizontal Spacing 40 writes `bar.legend.item.paddingX`. Effective values match. |
| Line markers | Enable writes `line.series.marker.enabled = true`; Diamond and 9 write `.shape = "diamond"` and `.size = 9`; both effective series match. Shape/Size/Stroke Width appear conditionally when enabled. |
| Aggregate | Root model `aggFunc = "sum"`; duplicate Q1 revenue 100+120 becomes 220, operating income 20+25 becomes 45. Off removes aggFunc and restores four ordered rows. |
| Switch Category / Series | Root model flag changes both ways. On has xKey `AG-GRID-DEFAULT-CATEGORY` and yKeys `period:0` through `period:3`; off restores the two original series. Numeric transposed data was not fully projected. |

Actual `chartOptionsChanged` events accompany these edits. The event/model ledger retains original family and position namespaces. Weight emitted two events for the observed edit; do not replace this with an assumed one-event contract.

Tooltip Mode has an observed Single/Multiple/Compact menu and a successful UI change to Single with an event. Its changed model/effective leaf is outside the captured projection, so no patch namespace or tooltip result is accepted from that action. The 18-action count includes this limited observation.

## Evidence limits and next decision

The final line screenshot shows diamond markers at the original values. Aggregate numerical assertions use effective chart data; its immediate screenshot caught intermediate animation heights. No settled aggregate pixel geometry is claimed. One final explicit save produced an outgoing synthetic dashboard POST with line markers enabled/diamond/9 and series count 2. [Finite outgoing projection](../../../artifacts/parity/editor-runtime-next/outgoing-storage-projection.json) does not prove backend readback or intermediate-edit persistence.

The known original datafeed error remains. Cleanup removed the owned container, state and generated credentials with exit 0. [Publication allowlist](../../../artifacts/parity/editor-runtime-next/publication-allowlist.json) excludes private state, raw diagnostics and raw request metadata; its hashes refer to selected completed artifacts pending independent review.

Still required before full C acceptance: tooltip namespace/rendering, nested titles, colors/shadows, remaining axis/legend fields and conditional controls, aggregate functions beyond Sum, numeric transpose output, range/reorder, stackedBar and other families, light/detached/forecast and keyboard paths, stable geometry and save/reload. These gaps must remain visible in task sizing. This is a bounded discovery result, not an application implementation or whole-renderer acceptance claim.
