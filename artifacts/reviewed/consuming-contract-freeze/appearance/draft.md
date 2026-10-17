# Project source appearance into the existing Cartesian renderer

Freeze the source-consuming interfaces below for design synthesis. The boundary is selected baseline + generated source options + the actual selected theme -> accepted composition/color helpers -> `resolveApplicationAppearance` -> extended existing `ResolvedCartesianStyle` -> existing `translateCartesian` -> existing ECharts host. Required unresolved fields return `unresolved` without style/options; they block the dependent rendering case. Named source rules can be implemented after approval, but the complete candidate render awaits the capture gates below. This is not complete B2, application activation, editor acceptance or renderer parity.

The [finite manifest](field-manifest.json) has 131 rows: 127 observed field groups covering 908 reviewed observations, plus four supplemental capture gates. It records exact raw values, original capture paths and SHA-256 provenance, as well as the four saved-composition inputs/combined/effective projections and eight proxy color/collision cases. [Proposed interfaces](proposed-types.ts) separate background, captions, category axis, number axis, legend, per-stable-ID bar/line/marker channels and tooltip. [Locked target inspection](locked-echarts-targets.json) establishes public member existence against installed 6.0.0 and the repository package/bun lock. Member existence is not evidence of visual equivalence.

## Boundary and dependencies

This artifact owns appearance contract inputs for requirements 4.8 and 4.9. It imports the accepted `OptionBaseline`, `RuntimeOptions`, `composeAppearanceOptions`, `deriveAppearanceColors`, snapshot and trusted `ChartDisplayPolicy`. It extends the existing mapper and host call, with the session remaining responsible for revisions and latest baseline selection. There is no new state store, theme interpreter, persistent schema, control predicate, package, feature flag or parallel renderer. Unknown rows are excluded from readiness claims, not from the product obligation.

Current Workspace is frozen at `ea02ec15956dee8d2c8a06825387a570757db12d`. Original observations identify `38dffc33389aca0e4a87e0e88d42f7067aa220df`; earlier candidate IDs inside evidence remain historical. Only this artifact directory was written. No browser, suite, TypeScript build, image build, install, dependency change or network call ran.

The local Kiro extension/design-principles and synthesis guidance was applied: freeze seams, adopt existing owners, distinguish source rules from proposals, and carry precise unresolved dependencies. Core product.md/tech.md/structure.md are absent; complexity.md, documentation.md and delegation.md were read. This draft does not alter phase approval metadata or authorize runtime tasks.

## Exact input ownership

`resolveApplicationAppearance(input: AppearanceInput): AppearanceResult` is the sole appearance entry. It is called by the planned application session once per selected baseline/theme/render revision. Inputs are application source values, never captured effective fixtures:

| Input | Actual source and invariant |
| --- | --- |
| `baseline` | The accepted session baseline selection. Compose `baseline.options`; do not independently read model.chartOptions or storage. Preserve original model/options for the reducer and save. |
| `generated` | The original generated data-only option projection from createDefaultSeries/createDefaultAxis/getDefaultChartOptions plus the owned common legend/navigator generation. Trusted callbacks are omitted here and supplied as display policy. Reconstituting this original generator is a session/options integration prerequisite; a test constant is not its production replacement. |
| `theme.name/base/params/overrides/palette` | Select the actual `chartThemes[0]` entry from the existing theme source; project its data properties, retaining unknown JSON in its source owner. The current loop's final `themePalette` is not the active theme selector. Selected custom base/params replace their source values as observed. |
| `mode` | Existing session/theme source dark/light mode. The ledger's effective.mode is this value, not a ThemeSelection.name. Theme name is selected separately through actual chartThemes[0]; dark alone cannot distinguish openbb-dark from custom-dark. Reject a name suffix inconsistent with supplied mode. |
| `theme.colorTokens` | Source-resolved explicit foreground/background/text/chart-background tokens for accepted color derivation. Explicit alias values may differ. Alias graph resolution is open; the caller must not supply guessed tokens to obtain a resolved result. Record the token paths. Unsupported opaque-color domain is an engineering diagnostic, not a product restriction. |
| `series` | Ordered stable descriptor IDs, source keys and labels from the snapshot selection. Join each effective-reference yKey to its source key for assertions; yName/label is not identity. No modulo palette allocation or label-keyed map is inferred. |
| `categoryColumnId/chartBarFillEnabled` | Actual selected category and original category-fill source state. Enabled category fills require their own source/effect contract; ordinary palette projection cannot pretend to implement them. |

Runtime boundary inspection is descriptor-safe, exception-contained and data-only, preserving absent/own undefined/null distinctions. Reject malformed input with a field diagnostic; return unresolved for structurally valid behavior that is not established. Never execute saved callbacks/getters. The proposed types are precise design contracts, not compiled production declarations. Per-leaf evidence status and origins belong to the manifest, not a runtime resolution graph.

## Source resolution rules that can be frozen now

The resolver must call `composeAppearanceOptions({baseline, generated})`, then read named leaves from its detached result. It must call `deriveAppearanceColors(theme.colorTokens)` for derived grid/subtitle colors. These outputs must reach the mapper in the same candidate call; implementing another unused helper does not satisfy this boundary.

| Rule | Evidence and status | Concrete expected result |
| --- | --- | --- |
| Replace saved common wholesale with generated common before lodash merge | Accepted helper, original useChartOptions 406-434, four saved cases. Source-observed. | Saved common title `SAVED COMMON/#123456` does not reach effective title; generated common legend top remains in common. Preserve saved original common for persistence. |
| Saved family branch survives composition | Accepted helper + bar-family/line-family. Source-observed finite composition. | bar title `SAVED BAR`, line title `SAVED LINE`, both `#654321`; legend right; `axes.number.left.label.color=#abcdef`. |
| Named family title enabled/text/color/fontSize leaves | Finite saved cases support source values for these fields. No universal family-over-common law. | Family enabled true; text above; fontSize remains 12 in captured cases. A conflict on an untested typography/spacing leaf remains unresolved. |
| Grouped bar family series fill/stroke/strokeWidth | bar-family compared with bar-common. Finite source-observed. | Both selected series fill `#abcdef`, stroke `#fedcba`, width 3. Common.series.fill `#123456` does not beat generated stock fills. |
| Line series stroke/width and marker channels | line-family/line-common. Finite source-observed. | Stroke `#fedcba`, width 5; marker enabled true, fill `#789abc`, stroke `#cba987`, width 2, circle, size 7. Supplied line.series.fill `#abcdef` is absent effective and is not mapped to stroke. |
| Line connection/disabled marker retention | Existing theme source plus stock/saved observations. Source default is known; general collision rule is open. | connectMissingData true; disabled markers retain circle/7 and independent fill/stroke values. Disabling never drops these source values. |
| Derived grid/subtitle colors from explicit tokens | Accepted normalized color helper and eight proxy cases. Source-observed derivation only. | Stock dark grid `#515153`, subtitle `#7a7a7b`; changed dark background gives `#5e6c79/#838e98`; normalized edge `#000000/#9b0000` at literal `1-.1` gives `#8b0000`. |
| Explicit grid/subtitle token override | Original token semantics accepted in prior design; direct/collision context must stay identified. | An explicit resolved `gridLineColor`/`subtleTextColor` is the field input; do not derive over it. Its precedence against additional saved axis/subtitle leaves is open until captured. |
| Selected theme background/palette source | Six stock + two custom grouped cases and theme source. Mode selection is source-observed, allocations are finite observations. | Dark background `#151518`, light `#FFFFFF` (case-normalization only at derived-color boundary). First stock fills `#5090dc/#ffa03a`; strokes `#74a8e6/#ffbe70`. Custom fills/strokes use the selected custom theme, never the other mode's last-loop palette. |

The finite selector reads only the named paths above and applies rules only where their source-domain preconditions are met. It does not check a fixture ID, observation label or hardcoded number of selected series. Beyond proven allocation, saved collisions or unsupported aliases, the result is unresolved with exact field diagnostics; no partial style/options reaches the host. Proven leaf rules remain usable for isolated verification but do not imply a renderable source configuration. A general `merge(common, family, position)` is prohibited: composition is known; original library inheritance after composition is a separate question.

Stock-default values in the manifest are observations, not a new default algorithm. A profile of those constants may be used as an explicit test oracle. It may not be passed by the application as magic effective style or installed as an arbitrary inheritance fallback. A full candidate render is blocked until its required source-resolution and geometry rows close; implementation tasks must identify that complete required row set before acceptance.

## Public projection and assertions

`AppearanceResult` is `{status:"resolved", style:ResolvedCartesianStyle}` or `{status:"invalid"|"unresolved", diagnostics}`. `resolved` requires every applicable field in the declared consuming render coverage and any joined editor field to be established for that source configuration; absence of diagnostics is not enough. Inapplicable bar/line branches retain source state and are not fabricated as active styles. Existing `background`, `title/titleEnabled`, `legend`, palette and per-ID series fields remain their owners; explicit role extensions add subtitle, independent axes, padding, typography, geometry and tooltip mode. The initial admitted source rules alone do not meet full required coverage.

| Role | Public ECharts 6.0.0 target | Projection decision and acceptance |
| --- | --- | --- |
| Visible background fill | `backgroundColor` | Exact explicit fill; hidden-background compositing remains open. Enabled images need separate implementation/effect evidence. |
| Title and subtitle | Two entries in `title[]`, each `show/text/textStyle` | Proposed independent entries preserve subtitle visibility when title is disabled. ECharts has one show for text+subtext in a single title, so a single title/subtext mapping is inadequate. Separate positions and spacing require layout evidence. Title/Subtitle strings remain when disabled. |
| Four-sided chart padding | `grid.outerBounds` plus explicit caption/legend layout | Public grid bounds exist; they are not AG chart padding. All four dimensions remain distinct. A direct grid.left=20 claim would confuse plot/label/caption insets. Capture geometry before accepting this projection. |
| Category and number axes | `xAxis/yAxis.position`, `name/nameTextStyle/nameGap`, `axisLabel.show/color/fontFamily/fontSize/fontWeight/margin` | Roles remain separate. Axis-title enabled maps to rendered empty name while retaining text in projection. Name spacing/margins require geometry comparison. Generated source title formatting must be joined explicitly. |
| Axis line | `axisLine.show/lineStyle.width/color` | Line color is absent from the old ledger. Do not substitute grid stroke or allow ECharts default equality to count as parity. |
| Grid | `splitLine.show/lineStyle.color/width/type/opacity` | Distinguish gridLine.width from style.strokeWidth and style fillOpacity; their differing-value meaning is open. Numeric dash-array member exists; pattern and alternating-style projection require effect evidence. |
| Legend | `show`, position/orient, textStyle, icon, itemWidth/itemHeight | Source 11px square marker maps to rect 11x11 as a design proposal. Original spacing 20, maxHeight 50, paddingX 32, paddingY 8, marker padding 5 are independent. They are not equivalent to ECharts itemGap/height/text padding. Multirow/overflow layout remains open. |
| Grouped/stacked bar | series stable id + itemStyle.color/borderColor/borderWidth/opacity | Grouped finite explicit fill/stroke/width is admitted. Stacked/custom/opacity conflicts need named source evidence; no default-match claim. |
| Line | series.lineStyle.color/width/opacity/type and connectNulls | Separate from marker and fill. Source numeric arrays/nulls remain untouched. Nondefault opacity/dash unresolved. |
| Marker | showSymbol/symbol/symbolSize and itemStyle.color/borderColor/borderWidth | `enabled=false` retains shape/size/colors in projection. ECharts accepts more symbols than the current circle-only validator; original enabled-shape semantics still need evidence. No new shape restriction is authorized. |
| Series labels | label.show and label typography/formatter | Use trusted display.seriesLabel; never infer title/legend/axis typography from one global font. Enabled label placement/visibility is open. |
| Tooltip | tooltip.trigger/formatter plus hovered stable-ID event bridge | Content and invocation are separate contracts. Current axis/all-series formatter cannot satisfy single mode. Do not derive hovered identity from label or first series. |

Every option assertion checks exact role/ID-target value before ECharts normalizes options. Every visual assertion checks matched viewport/mode/DPR output, settled geometry and financial values; comparison of public options alone cannot establish layout parity. Numeric observations, units, scales, nulls and stable row/series identity remain snapshot-owned.

## Mapper and display-policy join

### Canonical style migration within the existing mapper

The source resolver emits one canonical role style. The proposed `Omit` definitions replace overlapping legacy fields in the existing style contract; they do not add a normalizer, store or mapper. The existing validator has two explicit input branches: an omitted display-policy argument permits only the accepted legacy shape, preserving existing isolated tests; a supplied policy requires the complete canonical application shape. Canonical roles without policy, legacy style with policy, or a mixture of canonical fields and forbidden legacy aliases is invalid with exact paths. Unknown original source behavior remains unresolved before mapper invocation. Validation does not synthesize a canonical style from legacy fallback values.

| Channel | Canonical owner and legacy migration/rejection rule |
| --- | --- |
| Numeric formatting | Trusted `ChartDisplayPolicy` owns formatting. Canonical input rejects any own `precision`, including undefined; the resolver does not invent an unused precision value. Legacy three-argument input retains its existing precision behavior. |
| Marker fill/stroke/width | `series[id].marker.fill/stroke/strokeWidth` only. Canonical input rejects own `markerFill`, `markerStroke`, `markerStrokeWidth` fields, even if equal or undefined. Source resolution writes nested values directly; it does not copy mapper aliases. Legacy three-argument input keeps existing alias behavior. |
| Marker enabled/shape/size | Per-ID nested `series[id].marker` only, including retained values when disabled. Canonical `line` contains only connectMissingData; any own `line.markers` is invalid. Enabled and disabled line series both require complete nested marker values. No precedence between global and per-ID marker representations is invented. |
| Bar/line color and width aliases | Canonical `series[id].fill/stroke/strokeWidth` and optional opacity/dash fields are the owners. Canonical input rejects `color` and `lineWidth`. A bar requires its admitted fill/stroke/width; a line requires stroke/width plus marker channels. Palette is retained source information, not mapper fallback allocation. Unestablished allocation returns unresolved in the resolver. |
| Title/legend typography | `typography.title` and `typography.legend` only, each complete including weight. Existing title text/visibility retain `title/titleEnabled`. Subtitle owns its complete separate typography. There is no global font/color fallback on the canonical path. |
| Category/number axis typography | `categoryAxis.label/title.typography` and `numberAxis.label/title.typography` only. Canonical input rejects any own `typography.axis` and global `textColor/fontFamily/fontSize`. These legacy fields remain accepted only by the legacy branch; even matching duplicate values are rejected in canonical input. |
| Series labels and ECharts global textStyle | `series[id].label` owns label typography. The canonical mapper sets role targets explicitly and does not use ECharts global textStyle as a fallback for owned roles. A required unresolved role prevents the resolved result; it cannot borrow another role's font/color. |

No second representation remains authoritative on the canonical path. Implementing the migration means updating existing validation/projection branches together and preserving the legacy behavior only in its explicit compatibility branch. After all accepted callers migrate, removal of that branch is a separate reviewed change. Required verification includes conflicting and equal duplicate aliases, own undefined aliases, global/per-ID markers, global/role typography, omitted required roles, and unchanged existing three-argument behavior.

Extend the existing `TranslateCartesian` signature to `(snapshot: ChartSnapshot, family: string, style: unknown, display?: ChartDisplayPolicy): CartesianTranslationResult`. The application always supplies its trusted display policy and only a resolved canonical style under the migration rules above; accepted isolated three-argument fixtures retain their previous formatting behavior. There is one mapper entry/implementation and the existing supported/unsupported/invalid result contract. The session does not call it after appearance invalid/unresolved; no partial options reach the host. Successful rendering remains insufficient for application parity. The existing host owns render/export/disposal.

Use `display.category` with the source category value, `display.numericAxis` with the unscaled numeric tick, `display.crosshair` with the original raw value, `display.legend` with the stable-ID label, `display.seriesLabel` with source label value and `display.tooltipNumber` only for present numbers. Convert callback results to ECharts-required strings at the mapper boundary, without changing source policy fallback behavior. Never keep `toFixed(style.precision)` beside the joined policy. Trusted callbacks stay in memory and never enter RuntimeOptions or saved state.

`TooltipInvocation` contains stable row ID, hovered series ID and pointer/keyboard source. ECharts item-trigger is a proposed bridge for single mode; axis-trigger cannot supply hover identity by itself for shared/compact. The final policy is owned by the joined display/tooltip contract, not inferred here. Finite grouped reference Single content is `2024-Q1 Revenue (USD millions) 100`; Multiple/Compact raw text is retained in the manifest. Null, ties, order, keyboard and missing hovered identity remain named capture gates. Escape provider text at the final HTML boundary. A null is not numeric zero and never reaches tooltipNumber.

## Bounded files and planned verification

Paths below are relative to `terminalpro/src/components/General/Table/Chart/`. These are responsibility proposals, not created production modules or approved tasks.

| File | Responsibility and dependency |
| --- | --- |
| `application/appearanceTypes.ts` (new) | AppearanceInput/Result and role fields; imports accepted data contracts only. Keep large role definitions here instead of growing existing 181-line application/types.ts. |
| `application/effectiveAppearance.ts` (new) | Descriptor-safe source projection, accepted composition/color calls, named selector rules and unresolved paths. No store, React, AG runtime import or duplicated persistence. |
| `echarts/cartesianTypes.ts` (modify) | Extend existing resolved style role fields and mapper signature; import display policy. Keep the existing mapper result contract. |
| `echarts/cartesian.ts` (modify) | Existing shared series/snapshot mapping; accept trusted optional display argument and apply joined fields. One entry, no second mapper state owner. |
| `echarts/cartesianAxes.ts` (new if needed by measured growth) | Category/number axis public projection and layout-boundary diagnostics. |
| `echarts/cartesianCaptions.ts` (new if needed) | Independent captions/legend projection; owns their shared layout decisions. |
| `echarts/cartesianTooltip.ts` (join with display lane) | Trusted content, escaping and invocation bridge; parent freezes interface first. |
| Existing `application/useApplicationChartSession.ts` and chart entry (controller join) | Produce source inputs and consume result into mapper/host in the real original journey. This artifact does not claim that hook exists today. |

Whole modified/new production files must pass 400 physical/300 logical units and 50/function caps with the accepted inventory and explicit source scope. Split cohesive axes/caption/tooltip responsibilities before exceeding caps. No policy-only enforcement or exception is proposed. Test fixtures and this design directory are nonproduction exclusions; that exemption cannot hide hand-maintained runtime logic. No physical/logical measurements or checker success is claimed here.

After design and task approval and closure of the required capture rows, planned finite verification uses real accepted helpers and source-generated input, then the existing mapper/host in one render. Change baseline family title/color, selected light/dark/custom palette and explicit tokens; assert the changed exact public targets and captured output while original baseline/generated/theme inputs remain unchanged. Assert bar and line colors remain independent, disabled marker state remains circle/7, interior null and numeric arrays remain unchanged, and invalid/unresolved source configurations produce diagnostics without options. The test cannot import effective capture JSON as its resolver input or branch on fixture IDs. Source observation JSON is an oracle only. No rendering task is ready solely because the narrow source rules are specified.

The later real application journey remains selection -> original editor -> edits/theme -> fresh export -> table -> explicit save/reopen/restart. Candidate-only source projection is preparatory and does not satisfy that journey. Full C, original predicates and all control/family obligations remain required.

## Exact captures that still block dependent readiness

| Capture gate | Required input and discriminating assertion |
| --- | --- |
| Theme alias and collision gate | Original selected stock/custom dark/light theme name/base/params; generated data-only input; nonempty saved family/common leaves under one action. Vary text vs foreground and chart-background vs background separately; explicit grid/subtitle params compete with axis/subtitle saved fields. Record source token paths, combined projection and effective leaves. |
| Caption/layout gate | Independently enabled title/subtitle with retained texts, unequal fonts/weights/spacing; unequal top/right/bottom/left padding; title-off/subtitle-on and inverse. Record original control event, saved path, effective values and bounding boxes. |
| Axes/grid gate | Category/number title and labels with unequal roles; explicit line color different from grid stroke; position vs generic color conflict; unequal grid width/style strokeWidth, opacity and nonempty dash; hidden -> shown retains all values. |
| Legend gate | Four positions; multirow/overflow at fixed width; distinct horizontal/vertical item padding, marker padding, maxHeight and spacing. Record item/marker/text/panel geometry, not only option names. |
| Series/allocation gate | Source-selected 1/2/more-than-palette series, selection reorder, repeated/duplicate labels, saved family fill/stroke plus independent marker overrides; custom line/stacked; nondefault opacity/dash; enabled supported original marker shapes; category-fill on/off. Record stable source key/ID ordering and financial data unchanged. |
| Tooltip invocation gate | Actual pointer on each grouped series, keyboard path, null/missing/ties, shared/compact order and source identity; separate line/stacked observations. Capture invocation, settled content and stored mode under one action. |

All captures must retain exact original revision/image, fixture digest, action ID, original saved input, generated/combined projection, settled effective fields, diagnostics and scoped cleanup. Public-proxy experiments remain identified as synthetic; they do not supersede saved application reachability. No fresh capture was performed here. The parent can freeze the named source rules and mapper interfaces now while keeping these dependent readiness rows open.

## Reproduction of this artifact

Run only the offline extraction with the existing Python environment and installed dependency tree:

```text
wsl -d Debian -u mc -- /mnt/d/Source/QOpenBB/pipeline/.venv/bin/python /mnt/d/Source/QOpenBB/artifacts/consuming-contract-freeze/appearance/extract_manifest.py
```

The script reads an explicit allowlist, verifies repository and installed ECharts 6.0.0 identity, records local public declaration/source matches, and writes finite raw data plus input/output hashes only inside this directory. It does not read runtime accounts, credentials, diagnostics, private caches or arbitrary theme objects. Its output validates extraction and target provenance only; it is not runtime verification.
