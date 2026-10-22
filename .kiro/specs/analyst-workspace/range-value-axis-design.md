# R4c: Range numeric axis foundation

Implement one inactive, shared Range value-axis planner and extract the already accepted linear tick arithmetic into a neutral module. This gives both Range families their raw scale/tick input without coupling their financial domains to Box Plot. It is the smallest coherent next dependency: continuous category geometry also needs caller provenance, calendar selection, Bar bandwidth and Area hit/path changes, which cannot honestly be covered by a tick-only change.

2026-10-22 proposal, controller approved for bounded implementation. Workspace baseline: `912f97e1732bfd1b8d91c110e8e37b19a559233c`. This follows [R4b axis findings](range-chart-plan.md#r4b-series-appearance), the [Range plan](range-chart-plan.md) and [appearance contract](range-series-appearance-design.md). Trust their retained-source evidence; no original-bundle research is required. English is the owning specification language.

## One task and exact ownership

One implementer owns only the following paths relative to `vendor/workspace/terminalpro/`. Other agents may be working; preserve their changes. No commits, dependencies, application activation, provider work or browser/build jobs belong to this task.

| Path | Responsibility |
| --- | --- |
| `src/components/General/Table/Chart/echarts/linearTicks.ts` | New single owner of the existing density, linear nicing and raw tick algorithms. |
| `src/components/General/Table/Chart/echarts/boxPlotTicks.ts` | Replace implementation with direct compatibility export aliases. |
| `src/components/General/Table/Chart/echarts/rangeValueAxis.ts` | New pure Range domain/window/raw-scale planner. |
| `tests/unit/chart-compatibility/rangeValueAxis.test.ts` | Focused domain/tick tests and actual renderer handoff checks using existing Range fixtures. |

The compatibility facade preserves four production callers and the existing Box test API without churn. It contains no wrappers or second algorithm. This is compatibility ownership, not a size-cap workaround. Existing renderers, projections, financial summaries, capture, appearance, caller, session, editor, navigation and all Box tests remain read-only. The controller owns inventory, breadth, maintained status/evidence and acceptance updates. Existing complexity foundation is accepted; use it rather than rebuilding it.

## Frozen interfaces

Move the contents of `boxPlotTicks.ts` into `linearTicks.ts` with neutral identifiers only:

```ts
export interface LinearTickDensity {
  readonly tickCount: number;
  readonly minTickCount: number;
  readonly maxTickCount: number;
}
export function linearTickDensity(span: number, fraction?: number): LinearTickDensity;
export function niceLinearExtent(domain: readonly [number, number], density: LinearTickDensity): [number, number];
export function linearRawTicks(domain: readonly [number, number], density: LinearTickDensity, visible?: readonly [number, number]): number[];
```

Preserve algorithm behavior and existing error text in this extraction. `boxPlotTicks.ts` directly re-exports these as `BoxTickDensity`, `boxTickDensity`, `niceBoxExtent` and `boxRawTicks`. Source equivalence is already established at M18683-18701/M30262-30284 in the prior findings. Do not import any Box module from Range.

```ts
export interface RangeValueAxisInput {
  readonly dataExtent: readonly [] | readonly [number, number];
  readonly bounds: { readonly min?: number; readonly max?: number };
  readonly span: number;
  readonly density?: LinearTickDensity;
  readonly visibleRange?: readonly [number, number];
}
export interface RangeValueAxisPlan {
  readonly semanticExtent: readonly [] | readonly [number, number];
  readonly fullExtent: readonly [] | readonly [number, number];
  readonly visibleExtent: readonly [] | readonly [number, number];
  readonly rawTicks: readonly number[];
  readonly density: LinearTickDensity;
  readonly span: number;
  readonly valueScale: ResolvedRangeBarScale | null;
}
export function planRangeValueAxis(input: RangeValueAxisInput): RangeValueAxisPlan;
```

Import `ResolvedRangeBarScale` as a type from the accepted Range core. Range Area already inherits the same scale contract. The caller supplies `projectRangeBar(...).projection.dataExtent`, which already reflects enabled fields; this planner must not regroup rows or rerun statistics. `span` is the actual numeric plot span, not the whole viewport. Optional density permits the later collision/layout loop to choose a candidate without changing this API. Optional `visibleRange` defaults to `[0,1]` in normalized axis space; this is a pure crop primitive, not application navigator wiring. Report the final density used for ticks in `density`.

## Observable behavior

1. Validate finite bounds, finite nonnegative span, dense extent/window tuples, ascending input data extent, and `0 <= start <= end <= 1`. Supplied density counts are finite nonnegative integers with `minTickCount <= tickCount <= maxTickCount`. Invalid input or nonfinite derived arithmetic throws a descriptive Range axis error; never return a partial plan. Do not change neutral helper admission during extraction.
2. Resolve semantic endpoints by applying each explicit bound to the corresponding data endpoint. With no data, both explicit bounds are required; zero or one bound yields an empty plan. Effective `min > max` also yields empty. Empty has all three extents and ticks empty and `valueScale: null`. Preserve finite raw endpoints and avoid mutation. Do not force zero into the semantic extent. Original linear nicing may naturally reach zero; that is different from inserting a zero datum.
3. Use supplied density or `linearTickDensity(span)` and source linear nicing for nonconstant domains. Reject nonfinite span differences or nice extents rather than producing Infinity geometry. An equal semantic domain bypasses nicing and stays `[c,c]`, even at tiny spans. Keep semantic, full niced and visible domains distinct.
4. Crop the full domain using the normalized window. For a positive fraction below one, use `linearTickDensity(span, fraction)` for tick density, matching the existing Box window mechanic; otherwise retain the base density. A zero-width window must avoid division by zero, produce equal visible endpoints and retain only a full-domain tick matching that point, if any. Zero span always emits no ticks, even if a caller supplied a positive density. Finite derived-domain and tick checks remain mandatory.
5. Return raw ticks for the visible domain using the neutral algorithm, then strictly filter to the closed visible raw interval. The neutral helper rounds its crop boundaries outward; Range's accepted mapper requires every supplied tick inside its raw scale. For full `[-5,10]` cropped to `[-1.25,6.25]`, retain `[0,2,4,6]`, excluding the helper's outward `-2`. Keep the neutral algorithm unchanged. Build `valueScale` directly from visible raw endpoints and those raw ticks. In particular, equal `[c,c]` remains `{min:c,max:c,ticks:[c]}` when a tick is present; it never becomes Box's `{min:0,max:1,constant:c}` transport. Range's existing mapper owns the engine-only `[0,1]` coordinate transport. Empty and constant are distinct.

## Verification and completion

Use one focused new test file, unchanged accepted fixture helpers, and existing Box/Range regressions. Assert fixed independent source expectations, not expected results computed by the new helper. Reuse the retained linear-oracle cases in `boxPlotValueAxis.test.ts` as reference; do not copy its harness or create another source-probe artifact.

- Cover strictly positive `[4.53,6.47] -> [4,7]` at 49 pixels, its negative mirror, mixed data, decimals, explicit/one-sided bounds, empty, both-bound explicit empty, reversed effective bounds, singleton/equal at zero/tiny/normal spans, finite extremes and derived overflow. Distinguish natural nicing from a forced zero baseline.
- Cover nonuniform raw ticks, density override, crop, zero-width crop, zero span and malformed/nonfinite/negative/fractional/out-of-order density, invalid windows, immutability and errors. Exercise legend-dependent data extent through `projectRangeBar` using existing fixtures.
- Feed returned `valueScale` into the existing Bar mapper in both directions and the Area mapper. Use ECharts SVG rendering to inspect numeric tick text/positions and constant raw callback values; retain actual raw extrema in labels. Do not claim category-axis parity from these ordinal fixture checks.
- Run unchanged Box value-axis, category-plan, navigator and integrated rendering regressions plus the existing Range unit/render tests. They must establish no extraction regression. No browser or FMP milestone claim is made by these tests.

Run from `vendor/workspace/terminalpro` with the existing pinned Node toolchain and one-worker configuration:

```sh
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs \
  tests/unit/chart-compatibility/rangeValueAxis.test.ts \
  tests/unit/chart-compatibility/boxPlotValueAxis.test.ts \
  tests/unit/chart-compatibility/boxPlotCategoryPlan.test.ts \
  tests/unit/chart-compatibility/boxPlotNavigator.test.ts \
  tests/unit/chart-compatibility/boxPlotIntegration.render.test.ts \
  tests/unit/chart-compatibility/rangeBar.test.ts \
  tests/unit/chart-compatibility/rangeBar.render.test.ts \
  tests/unit/chart-compatibility/rangeArea.test.ts \
  tests/unit/chart-compatibility/rangeArea.render.test.ts
```

Run scoped Biome and strict typing using existing project conventions; identify inherited diagnostics separately. Every new/modified production file must pass 400 physical lines, 300 logical syntax units and 50 per callable. Controller adds the two new owned paths to `.kiro/complexity-budgets.json`, supplies current explicit manifests for both forks, and runs the established gate from repository root:

```sh
pipeline/.venv/bin/python -m tools.quality.complexity --check \
  --changes workspace=artifacts/chart-range/r4c-workspace-scope.json \
  --changes data_api=artifacts/chart-box/b3d-data_api-scope.json \
  --output artifacts/chart-range/r4c-complexity.json
```

One heavy gate at a time. Capture actual commands, source identity, exits and local results in the existing Range evidence workflow. A fresh independent review must inspect the extraction and attempt to disprove Range domain/raw-scale behavior before acceptance. Controller reconciles the owning Range plan, breadth and README/docs checkboxes, leaving controls, axis/layout integration and real-FMP acceptance open. This document and tests are excluded from production caps. No image build is justified by this inactive slice.

## Next integration dependency

R4c completes only the numeric value-axis arithmetic dependency. Before either family activates, freeze category/number/time coordinates while retaining `groupSlot` identity, raw Date inference at caller capture, calendar ticks, continuous Bar width/padding, Area path and hit lookup, and final label/chrome/navigation layout. The accepted findings already identify those source contracts. Category-only application activation, hidden controls or a permanent flag are not valid substitutes. The next contract should consume R4c directly instead of introducing a second value-scale planner.

Disproof conditions: Range imports Box financial types/helpers; tick algorithms are duplicated; empty becomes constant; equal raw bounds become transport bounds; Box regressions change; or the slice activates a family. Any one prevents acceptance.

## Completion

- [x] Freeze the reviewed neutral tick and Range raw-scale contract.
- [x] Implement and independently review the numeric planner and compatibility extraction.
- [x] Pass affected tests, formatting, typing comparison and complexity; reconcile evidence and status.
