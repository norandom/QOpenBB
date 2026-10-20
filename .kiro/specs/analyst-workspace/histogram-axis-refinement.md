# Histogram automatic-axis refinement

Independent design review approved this bounded correction on 2026-10-20. H4's authentic original reference shows that the replacement retains the right bins but omits viewport-dependent automatic axis rounding. This addresses the existing visual-comparison obligation; H1 membership, saved controls and financial observations remain unchanged. Implementation and candidate-image acceptance remain open.

## Source evidence and policy

References below are line numbers in retained `artifacts/task-2.1/frontend/terminalpro/node_modules/ag-charts-enterprise/dist/umd/ag-charts-enterprise.js`:

- Histogram raw X uses the first/last calculated bin endpoints (45000-45008). NumberAxis applies supplied bounds without adding zero (30524-30543, 32086-32089).
- Defaults are `nice=true`, target count five and minimum tick spacing 50px (19414, 14130, 20025). Pixel length bounds the tick count (20530-20549); step selection uses `[1,2,5,10]` and nearest permitted interval count (20404-20426).
- LinearScale rounds outward, recomputing the step up to four times until stable (32051-32073). Original label-collision handling can further reduce ticks (21154-21243); reproducing that entire layout engine is outside this correction.

The authentic default revenue screenshot has approximately 295px X and 224px Y plot lengths. Raw X `[40B,150B]` chooses a 50B step and displays `[0,150B]`; raw Y `[0,9]` chooses step five and displays `[0,10]`. Zero on X is an outcome of rounding, not a new zero-inclusion rule. A wider viewport can retain a positive X minimum. Source facts and this measured comparison do not establish parity at every size.

## Exact production ownership and interfaces

Paths are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/echarts/`. One implementer owns these seven paths after approval; all other production files remain read-only.

| Path | Bounded change |
| --- | --- |
| `cartesianAxes.ts` | Export existing `niceNumberExtent(min,max,pixels)` without changing its body or ordinary/area call sites. Its one-pass behavior stays unchanged. |
| New `histogramNiceExtent.ts` | Histogram-only wrapper over that export, returning finite `{min,max,interval?}`. Iterate at most four times, retaining original unrounded endpoints as the rounding operands. Preserve explicit sides. Do not copy the existing step-selection algorithm. |
| `histogramLayout.ts` | Export a pure `histogramAxisPixels(input,grid,domains)` budget helper, using existing `measureText`; keep current layout generation unchanged. |
| `histogramAxes.ts` | Apply the wrapper to nonempty automatic axes using supplied pixel budgets; set the resulting native interval as well as min/max. Keep domain exclusion checks before rounding. |
| `histogram.ts` | Resolve existing domain and layout once, derive budgets, then assemble axes. Keep the single H1 admission call and existing retained projection. Returned `domain` remains the pre-nice resolved domain; rendered axis bounds are in `options`. Replace its stale inactive-projection comment with the pure caller-owned projection rationale. |
| `histogramNavigator.ts` | Compute the main Y budget from the decorated main grid, including existing navigator reservation. Retain it as `openbbHistogram.yPixels` alongside existing explicit Y bounds. Keep full overview data and its label-free renderer. |
| `histogramNavigationWindow.ts` | Apply the same wrapper to the visible frequency domain and retained Y budget. Mount, legend, zoom, pan and reset therefore preserve the same rounding policy without H1/aggregation calls. |

Grid padding alone is insufficient near the 300px step threshold: numeric Y labels consume part of X's usable span. The budget helper subtracts existing numeric grid margins, measured perpendicular endpoint-label footprint (including rotation and label margin), and applicable tick/title space from the viewport. Use the resolved fonts and display callbacks; measure endpoint labels from a provisional domain. This is a bounded estimate, not a second layout owner: do not change grid padding or subtract these estimates from ECharts layout a second time. Clamp exhausted budgets to zero. A bounded second budget pass may use the provisional nice endpoints if their formatted width changes; no unbounded collision search. Navigator decoration must measure its actual main grid so its vertical reservation is counted once. Overview geometry remains full-data; it does not inherit the visible-window Y range.

## Bounds, finite output and acceptance

Keep supplied min/max exact. For mixed supplied/automatic bounds, only the automatic side rounds outward. Retain existing direction-specific exclusion, empty-axis behavior, endpoint-equality repair and outward extensions. Never zero-seed X, change interval membership, synthesize empty observations or overwrite saved bin settings. A nonfinite/zero step, overflow, collapsed result or unusable pixel budget must not produce invalid options: retain the already validated finite nondegenerate extent and omit `interval`; preserve existing diagnostics if that extent itself is invalid. Empty/fallback navigation output must remove any inherited interval from the retained Y options. The original special one-tick/collision cases remain explicit comparison limits, not a claim of universal pixel identity.

Extend only existing `tests/unit/chart-compatibility/histogram.test.ts`, `histogram.render.test.ts`, `histogramNavigator.test.ts` and, if needed, `tests/unit/chart-application/histogramProductionJoin.test.ts`. Cover narrow/wide budgets; the authentic default revenue distribution and independently calculated four-bin distribution; positive and signed domains without forced X zero; actual-engine tick/rectangle output; supplied min/max and excluded-bound recovery; tiny/zero/extreme finite inputs; zoom/legend/reset using retained data; and unchanged H1/aggregation call counts. Run the existing ordinary navigator/axis regressions to establish unchanged shared-helper behavior. Candidate-image comparison against the authentic default reference decides visual acceptance; source/unit checks cannot close it. The original four-bin input did not repaint within the reference run, so it supplies no four-bin visual acceptance evidence.

Every changed production file must satisfy 400 physical lines, 300 logical units and 50 units/function through the existing combined checker. Controller owns inventory, source pins, broader checks, candidate build, H4 evidence and publication. No new dependency, framework, editor control or milestone is authorized by this draft.

