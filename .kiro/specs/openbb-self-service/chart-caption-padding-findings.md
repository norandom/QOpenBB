# Preserve independent captions, paired typography and layout padding

The original dark grouped-column capture establishes independent title/subtitle/axis-title controls, all eight Weight bindings and four-sided chart padding. These findings constrain the replacement editor and mapper; they do not establish candidate parity or authorize activation.

The [capture report](../../../artifacts/reviewed/ui-parity-captions/capture/report.md) records nine cases against original Workspace `38dffc33389aca0e4a87e0e88d42f7067aa220df`, image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`. The four quarterly revenue and operating-income observations retain their values and USD-million units. Candidate `ea02ec15956dee8d2c8a06825387a570757db12d` was not executed.

| Original behavior | Consuming contract consequence |
| --- | --- |
| Each of four caption toggles removes only its own text; the other captions and tick labels remain. Disabled text survives and returns on enabling. | Represent each caption independently and preserve disabled details. Do not use one combined title block with shared visibility. |
| Horizontal title edits write both category top/bottom branches; vertical title edits write both number left/right branches. | Preserve the original model namespaces, including inactive positions; distinguish stored values from the currently rendered axis. |
| Weight choices update both `fontWeight` and `fontStyle`, emitting two ordered events. All eight role bindings reached their expected raw, effective and scene values. | Keep the original combined Weight menu. The draft `RoleTypography` needs a reviewed `fontStyle` correction before implementation. |
| Baseline weight is numeric `400` with absent style. Selecting Predefined restores numeric `400` but writes explicit `normal` style. | Preserve numeric/string and absence/explicit-value distinctions. Retention is not byte-identical restoration to the untouched baseline. |
| Swapping left/right padding 13/67 to 67/13 preserves plot width and shifts it right by 54 chart units. | Bind each side separately; plot position also includes axis/title/label occupancy. Do not equate plot x with left padding. |

In the captured 584 x 346 canvas, disabling the chart title or subtitle releases different vertical space. All four chart-padding values stay at 20 through the title toggles because the integrated original chart has no AG toolbar. The report retains measured rectangles; these are fixture observations, not universal spacing constants.

The corrected fifth attempt completed 164 interactions, 51 field edits and 100 settled snapshots. Its offline verifier checks 13 assertion groups, including nonempty `parentNode` chains with actual visibility/opacity values. Earlier attempts and their diagnoses remain recorded: the fourth run's empty ancestor projection did not satisfy that measurement even though its browser journey completed. All five attempts have owned-resource cleanup evidence.

Light mode, other families, font-family/size/color menus, persistence and candidate comparisons remain open. Use these results with the [navigation findings](chart-ui-navigation-findings.md) when revising the [consuming contract draft](chart-consuming-contract-draft.md); neither capture replaces the full application journey or the implementation gates.
