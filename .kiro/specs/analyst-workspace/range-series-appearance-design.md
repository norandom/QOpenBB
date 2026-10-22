# R4b Range series appearance

Resolve the original Range Bar and Range Area series defaults and saved overrides into the already accepted renderer field types. This inactive slice preserves source styling semantics before axis/layout and editor activation. It does not add controls, alter the shared appearance resolver or activate either family.

Independently reviewed and approved for bounded implementation, 2026-10-22. Workspace baseline is `102b53ad677f057903af50ea315c3c790ee67789`. This is the next bounded slice under [prototype-first delivery](../../steering/delivery-workflow.md) and the [Range plan](range-chart-plan.md).

## Boundary and source

The retained original is Workspace `38dffc3`, its `hooks/useChartOptions.tsx`, `utils.tsx` and `themes.tsx` under the original Chart directory, plus Grid 34.1.1 and Charts 12.1.1 bundles under `artifacts/task-2.1/frontend/terminalpro/node_modules/`. Detailed source locations and hashes remain in `artifacts/chart-range/r4b-appearance-contract.md`. C below identifies enterprise `dist/package/main.cjs.js`; M identifies community `dist/package/main.cjs.js`.

R4b owns detached option composition, finite series defaults, per-selected-field palette assignment and complete `RangeBarFieldStyle`/`RangeAreaFieldStyle` resolution. Existing capture, summaries, renderers, Box helpers, common appearance modules and caller/session/editor files are read-only. Axes, plot bounds, scales, navigation, tooltip financial formatting, highlights and activation remain separate joins. Both Range families need continuous-axis work before activation; an ordinal-only adapter cannot preserve the original inferred time/number cases.

## Frozen option contract

Reuse `composeAppearanceOptions` without changing it: `baseline.options` is the selected saved operand, generated common replaces saved common, and saved family leaves beat generated family leaves. Do not independently reread `baseline.model.chartOptions` as a different saved state. Collapse selected-theme/composed common leaves and selected-theme/composed family leaves independently, then apply family over common. This preserves the original nested family-before-common priority rather than interleaving layers by convenience (M32771-32800, M33718-33730, M33879-33906, M34079-34105).

The main resolver receives already normalized generated options. Export a separate `buildRangeGeneratedSeries` helper for the future caller join: take data-only caller series options, remove generated `marker`, `connectMissingData` and `calloutLabel`, and retain `label` with a disabled default followed by explicit caller label leaves. Original hook lines 41-42 and 124-127 establish this fallback. Filtering applies only here, never to selected-theme or saved family values. Tests compose this helper's result under the dashed Range family key; there is no second optional caller-series operand or invented collision rejection in the main interface.

The integrated proxy supplies assignment/name/key leaves directly, not paint. Original conditional defaults inspect direct engine series options separately from theme overrides (M33306-33316, M33694-33716, M33807-33809). Therefore a generated/theme/saved series stroke does not trigger Bar's direct-user width default of 2: integrated fallback width remains 0 unless width itself is set. Likewise override label spacing does not erase compatibility padding 6/10. R4b does not introduce a direct-series runtime API.

## Source defaults

Explicit valid effective leaves override these defaults. Preserve zeros and false values. All fields use selected-order palette indices; marker palette paint is independent of explicit band paint. Resolve disabled marker/shadow/label values so enabling later retains their settings.

| Leaf | Range Bar | Range Area |
| --- | --- | --- |
| Family key | `range-bar` | `range-area` |
| Fill / stroke | Selected palette fill / stroke | Selected palette fill / stroke |
| Fill opacity / stroke opacity | 1 / 1 | 0.7 / 1 |
| Stroke width / dash / dash offset | 0 / `[0]` / 0 | 1 / `[0]` / 0 |
| Direction | vertical; saved horizontal supported | No horizontal direction |
| Label enabled / placement | false / inside | false / outside |
| Label spacing / compatibility padding | 0 / 6 | 0 / 10 |
| Label color | Selected chart background | Selected text color |
| Marker enabled / shape / size / stroke width | Not applicable | false / circle / 6 / 2 |
| Marker fill / stroke / opacities | Not applicable | Independent palette paint / 1 / 1 |
| Shadow enabled / color / blur / offsets | Not applicable | false / `rgba(0, 0, 0, 0.5)` / 5 / 0,0 |
| Interpolation | Not applicable | linear; smooth tension 1; step position end |
| Connect missing data / visible | Not applicable / true | false / true |

C20826-20848 owns Bar theme defaults; C20017-20048 owns Area theme defaults. Constructors C19160-19194/C20123-20155 and M37159-37207 supply remaining leaves. M21889-21893 gives explicit marker properties priority over inherited band properties. Label typography follows the selected theme's projected series-label leaves; finite fallback is original base font Verdana, sans-serif, size 12, weight 400 (M26226-26239). Do not use unrelated navigator typography as an implicit series-label override. Existing caller `themeInputs.ts` parameterOptions projects fontFamily/fontSize/fontWeight into common series-label overrides (lines 56-64, 94); use those leaves and explicit family overrides.

## Interface and ownership

Two new production modules under `terminalpro/src/components/General/Table/Chart/application/`:

- `rangeSeriesAppearanceOptions.ts`: generated-series filtering, validated detached composition and source defaults/layer priority.
- `rangeSeriesAppearance.ts`: typed public input/result and field-style resolution using existing scalar/font helpers.

One new test: `terminalpro/tests/unit/chart-application/rangeSeriesAppearance.test.ts`. No other writable production path is authorized. If actual cohesion or caps require another module, return the proposed boundary to the controller before editing. Workers are not alone; preserve unrelated changes. Parent owns inventory, evidence, status, commits and shared integration.

`RangeSeriesAppearanceInput` contains `family: "rangeBar" | "rangeArea"`, `baseline: OptionBaseline`, `generated: RuntimeOptions`, `theme: ApplicationThemeInput` and ordered unique nonempty `seriesIds`. Empty selection is valid. `resolveRangeSeriesAppearance` returns either a resolved discriminated family result, or existing snapshot diagnostics with `invalid`/`unsupported` status. The Bar result has direction, fields and configuredVisible; Area has fields and configuredVisible. Fields use the existing renderer types. Results contain no ECharts options or persisted state. `buildRangeGeneratedSeries` returns a validated data-only options result using existing `ValidationResult<RuntimeOptions>` conventions.

Reject malformed data, nonfinite/invalid scalar leaves and unsupported values atomically without mutating input or invoking accessors. Retain existing finite data-only option admission rather than creating a second schema framework. Unsupported paint objects, label box/border/corner extensions or renderer-incompatible label placement must produce an explicit unsupported result, not silent flattening. Also diagnose encountered nondefault Bar cornerRadius/shadow and Area marker lineDash/lineDashOffset, which current core fields cannot represent. Default corner radius 0, disabled default Bar shadow, and solid default marker dash/offset may remain unrepresented; do not silently discard nondefault disabled configuration. This is a bounded style helper, not acceptance of every original option; subsequent integration must implement reachable missing features before activation. No automatic marker/shadow enabling from size or blur overrides: those theme overrides do not have direct-user auto-enable semantics.

## Tasks and evidence

- [x] Independently review source/default/precedence and the generated-input seam before implementation.
- [x] Implement the two inactive modules and one focused test file, with meaningful missing-module RED followed by GREEN.
- [x] Verify light/dark defaults; family/common and generated/saved collisions; selected baseline operand; generated-only filtering; independent marker palette/opacity; explicit false/zero; Bar direction and label placement; Area interpolation/shadow/gap values; selected order/empty selection; malformed/unsupported options and immutability. Use independent constants, not the resolver as its own oracle.
- [x] Run scoped Biome, existing canonical application typing baseline/candidate comparison and explicit-scope complexity. Every new production file must pass 400 physical lines, 300 logical units and 50 units per function. Register both files in the maintained inventory. No suppression, arbitrary forwarding helper or size exception.
- [x] Independent source review, concise evidence, breadth/checkbox updates and per-task commits. No image rebuild for an inactive helper. Original/replacement FMP appearance and full application behavior remain open.

Use the existing one-worker `tests/unit/chart-application/vitest.config.mjs`; run the new appearance test plus an affected existing composition test only if shared import behavior warrants it. No repeat of statistical suites for pure style code. Run the canonical `tests/unit/chart-application/session.tsconfig.json` typing command against the same accepted baseline and candidate; inherited errors remain disclosed. Disproof conditions include changed Box behavior, filtering saved marker/gap settings, inherited band paint overriding marker palette, treating override stroke/spacing as direct-user options, lost saved precedence, mutation or application activation.
