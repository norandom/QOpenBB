# Theme preview baseline and contract review

The bounded replacement contract passed independent review on 2026-10-27. Implementation and replacement appearance remain open. The owner explicitly approved making the existing Padding control affect the preview while preserving its saved format.

Reference: Workspace `e12713d29a9572599c7482d293f37cc040eba12f`, packaged image `sha256:b18d296f007935dc40c8b329939e15cdd27120e2e573bbca20d7b84ff200d523`. Runtime qualification confirmed no source overlay and only disposable data. The unchanged Theme Settings preview uses AG Charts Community 12.1.1.

Six existing theme-state tests passed. The corrected original browser probe passed in 16.4 seconds with one worker at 1600 x 1000; console, page-error, request-failure and HTTP-failure arrays were all empty. No theme was saved or reset. The original sample is synthetic Dolphin Interaction Data, not financial or FMP evidence.

Observed behavior: plot focus and legend form two chart-region tab stops. Left/right move between categories; up/down move between series. The focused bar has an outline and tooltip. Legend arrows move roving focus, and Enter toggles visibility and regroups the bars. Escape does not dismiss the focused tooltip or alter selection. Ten default legend entries fit two rows. Pointer hover shows category, series, integer value and swatch.

The corrected clean light/dark captures precede all interaction. Their SHA-256 hashes are `a8c36d043060c643ead1a9c2bb21168551a810741ec76ffda7b699293089495e` and `bf9e07b24dacb2d0891711b56290e50c1afda09d02ba12776d69c45546a392a6`. The corrected probe hash is `31d636dc537a4f3e586d19b35b51d2da6d61155bd81a23b62ad12d60559ff442`. Raw captures remain local until selected comparisons are published. An earlier dark capture followed a legend toggle and is not a clean default comparison.

Double-click isolation and overflow paging are source-derived, not runtime-verified. Padding effects, replacement controls, save/reopen, real-FMP propagation and export remain pending. Independent review found no blocking design defect; it requires actual native bar/focus geometry checks after toggle/resize, lifecycle cleanup and preservation of existing Pie behavior before accepting the shared foundation. Public coordinate conversion alone does not establish per-series offsets.

See the [implementation contract](../../../.kiro/specs/analyst-workspace/theme-preview-milestone.md) and [control map](../../../.kiro/specs/analyst-workspace/theme-preview-controls.md). This report establishes the original baseline and planning approval only.
