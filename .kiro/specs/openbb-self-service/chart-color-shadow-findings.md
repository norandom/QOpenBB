# Preserve color alpha and retained Series Shadow controls

The original dark grouped-column editor accepts alpha within color strings and renders the retained Series Shadow tuple. The [nine-case capture](../../../artifacts/reviewed/ui-parity-color-shadow/capture/report.md) supplies concrete original behavior for the replacement contract. Candidate rendering, light mode, other families and backend persistence remain unverified.

The reference is Workspace `38dffc33389aca0e4a87e0e88d42f7067aa220df`, image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`, with four quarterly revenue and operating-income observations in USD millions. No provider account or owner state was used.

| Original control/effect | Contract consequence |
| --- | --- |
| Spectrum Right, hue Right and alpha Left change the category-axis line. Enter and a later no-edit Escape dismiss the picker and return focus to the Color wrapper. | Preserve keyboard interaction, dismissal and focus as well as color values. The Escape observation does not establish rollback after edits. |
| Invalid grid text produces a validity error and no options event. Hex8 `#27C6A080` becomes `rgba(39, 198, 160, 0.502)` in model, processed style and live nodes. | Retain valid color-string alpha and invalid-input behavior. This does not introduce a separate grid opacity property. |
| First picker opens normalize axis, grid and Shadow colors and emit events; a later axis reopen emits none. | Opening a picker is not necessarily read-only. Transaction handling must account for the observed normalization and presence changes. |
| Shadow color, blur 12, X offset -7 and Y offset 9 reach both series and all eight bar rectangles, with matching visible halo changes. | Represent Shadow explicitly, including enabled, color, blur and both offsets. A generic series-opacity field cannot substitute for it. |
| Shadow off hides nested controls without disabling them, removes the halo and retains details. On restores the tuple and identical sampled halo pixels. | Preserve the original conditional controls and disabled-value retention. This is off/on retention, not save/reopen persistence. |

Axis writes affect both category top/bottom line-stroke branches; grid writes affect both number left/right first-style strokes. Width and dash survive the tested grid edit. Only a one-style baseline was exercised, so multiple-style retention and general precedence remain open. Sampled bar interiors are unchanged across the color/Shadow actions; halo effects are measured separately.

The capture completed 51 UI actions and 24 screenshot checkpoints. Its instrumented mutation counter omitted picker opens; conservative evidence-based accounting includes all four opens and remains within the approved bound at 17 of 20. The raw counter and correction remain published. Both attempts cleaned their owned browser, container, state and credentials; the initial onboarding setup failure and original diagnostics are retained.

Use this evidence with the [axis/grid findings](chart-axis-grid-findings.md) and [caption findings](chart-caption-padding-findings.md) to revise the [consuming contract draft](chart-consuming-contract-draft.md). Its missing Shadow representation remains a design gap. The reference capture does not alter the frozen contract, activate the renderer or prove the complete application journey.
