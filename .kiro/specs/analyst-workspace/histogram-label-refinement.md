# Histogram endpoint labels and control order

H4's default FMP comparison found a clipped final X label and Bin count above Tooltips. Correct these within the existing visual-parity obligation. Independent source investigation supports the following three-file scope; source implementation is independently accepted at Workspace `b18082dad1243cb04a7b07c4ec221c818e99e7c4`. Corrected-image acceptance remains open.

## Original behavior

The retained AG Charts bundle under `artifacts/task-2.1/frontend/terminalpro/node_modules/ag-charts-enterprise/dist/umd/` enables overflow handling for horizontal continuous axes with collision avoidance (21907-21922). With more than two ticks, it suppresses the last label when its coordinate plus half its measured text width exceeds the range end plus chart right padding (21245-21254). It also suppresses the first label only at the full visible range `[0,1]`. Measurement uses formatted, unrotated text width. Native tick and grid lines remain.

The retained AG Grid Enterprise bundle orders histogram controls as Tooltips, bins, stroke and remaining series styling (13972). Move Bin count after the existing tooltip panel.

## Bounded implementation

One worker owns these paths relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/`:

- New `echarts/histogramAxisLabels.ts`: a guarded public ECharts `afterupdate` extension reads actual native main-X ticks and coordinates. Apply the source condition to endpoint text in the public component view, matching both formatted text and the native tick's global coordinate. Restore only text hidden by this extension before reevaluating; preserve native overlap suppression. Read current zoom state rather than retaining another range owner.
- `echarts/histogramAxes.ts`: import the extension and attach transient histogram main-X metadata for the original formatter, resolved font and chart right padding. Y and overview axes remain outside the policy.
- `editor/ApplicationSeriesEditor.tsx`: move the existing histogram control below Tooltips.

The first implementation used `axisLabel.customValues` in a layout hook. Actual SVG tests disproved it: ECharts builds its native axis view during coordinate-system update, before that hook, so updated label options did not change drawn text. The revised public `afterupdate` hook uses `getViewOfComponentModel` and public graphic text/coordinate APIs; it does not access internal axis-builder caches or identifiers. No domain, interval, tick/grid, financial observation, saved setting or series data changes are authorized. No recursive `setOption`, event listeners, new dependencies or feature flags.

## Acceptance and ownership

Extend the existing `histogram.render.test.ts`, `histogramNavigator.test.ts` and `histogramEditorControls.test.tsx`. Verify actual rendered labels and unchanged tick/grid counts and rectangle geometry; short labels, sufficient padding, two ticks, top/rotated axes, zoom/reset and overview isolation; and DOM control order. Use RED/GREEN, independent review, baseline-relative static checks and the explicit inventory checker with whole-file limits of 400 physical lines, 300 logical units and 50 units per function.

The browser lane owns only the three H4 browser files and may inspect its current candidate while source work proceeds. Heavy checks remain serialized. Controller owns inventory, pins, documentation, commits and the next Dagger image. Final H4 acceptance requires the corrected image's FMP and synthetic journeys plus prior-family regressions; source tests alone do not close it.
