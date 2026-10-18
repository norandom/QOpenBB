# Restore axis Grid Lines and Ticks

Continue the approved original-UI restoration with the Grid Lines and Ticks subsections. Requirements 4.8, 4.9, 10.1, 10.4, 10.5 and 10.6 apply. These controlled components preserve the existing design system; option mapping, axis eligibility and persistence stay with the caller.

## Independent component boundaries

Task 2.63 owns `Chart/editor/axis/ChartGridLinesPanel.tsx` and `tests/unit/chartGridLinesPanel.test.tsx`. Export ChartGridLinesState with enabled:boolean, color:string, thickness:number and lineDash:number, a discriminated field/value edit union, and props value/onEdit. Render Grid Lines switch, then Color, Thickness, Line Dash while enabled. Numeric minima are zero, default maxima 10 and 30 respectively, expanded to the current value; range step1 and number step any. Preserve raw alpha colors and correctable invalid drafts while enabled; retain accepted controlled values across disable/re-enable without mount edits.

Task 2.64 owns `Chart/editor/axis/ChartTicksPanel.tsx` and `tests/unit/chartTicksPanel.test.tsx`. Export ChartTicksState with enabled:boolean, color:string, width:number and length:number, discriminated field/value edits, and value/onEdit/showLength props. Render Ticks switch, then Color, Width and optional Length. Width default maximum10 and Length30, minima0, maxima expand to current values, range step1/number any. showLength is required and caller-owned; hiding Length must retain it without emitting an edit. The original stored length path is tick.size. Do not invent an Axis Line toggle.

Both tasks depend on accepted 2.62 and may run concurrently in disjoint files. Reuse DS Switch, CaptionColorInput, ChartNumberInput and accepted CSS read-only. No new generic control layer, dependencies, option normalization, flags or storage. Each maintained file must pass 400 physical lines, 300 logical units and 50/function, registered in the existing executable inventory. Tests are excluded from production caps.

## Join and eligibility

Task 2.65 composes the panels in the existing ChartEditorControls story under Horizontal Axis and Vertical Axis after Series, in Grid Lines then Ticks order. Keep independent state per axis, surviving dock and tab remounts. Use ordinary Cartesian bar/line preview conditions only; showLength=true. Default fixture values must come from existing original captures or be explicitly described as synthetic examples outside the controls. Other axis controls (type, time format, position, color/thickness and Labels), family-specific axis conditions, live chart binding and persistence remain pending; this preview does not claim a complete axis editor.

The original grouped-category category axis hides Length; other ordinary category/number axes show it. Original Ticks is absent for radarLine/radarArea/rangeBar/boxPlot/waterfall; Grid Lines is absent for heatmap. Components must not decide these conditions. Grid style-array projection belongs to the future mapper; the controlled color/dash fields must not rewrite saved arrays themselves.

Existing `editor-runtime-next/focused/*-Axis-default.json` captures establish horizontal Grid Lines off, vertical Grid Lines on, grid color #515153, thickness1/dash0, both Ticks off and tick width1/length6. Inherited tick color is not present in the capture; use a disclosed synthetic theme-appropriate color in the preview rather than claiming an observed default.

## Evidence and delivery

Original source: `artifacts/task-2.1/frontend/terminalpro/node_modules/ag-grid-enterprise/dist/package/main.cjs.js`, Ticks47424-47451, Grid Lines47471-47527, order47614-47616, Ticks eligibility47762-47783 and grouped-category47859-47864. Shared numeric factory46394-46409 establishes expanding maxima and decimal input. Existing reference captures and accepted primitives are the baseline; no new reference collection is needed.

Run selected tests through `tests/unit/chart-editor/vitest.config.mjs`, scoped Biome and known-baseline TypeScript checks. One isolated light/dark joined browser/CDP check verifies exact edits, alpha, decimal correction and independent retained axis values. Independent review precedes each acceptance and commit. Publish concise reviews and one useful joined screenshot; keep runners, raw logs and measurements local. Sync reviewed artifacts before commits and push. Existing DS typography.ts TS2578 is disclosed; no full compiler or deployment acceptance is implied.
