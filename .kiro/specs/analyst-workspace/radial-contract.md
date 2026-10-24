# Radial compatibility contract

Status: RC0 numerical and control interfaces are independently frozen. The [renderer design](radial-renderer-design.md) owns exact formulas and lane boundaries. The owner approved retaining valid normalized Column observations when another category is missing; application and visual acceptance remain open.

## Scope and source identity

Restore Radial Column and Radial Bar in the existing Table/File chart workflow. Preserve all reachable controls, flags, theme, labels and saved fields. The original frontend is Workspace `38dffc33389aca0e4a87e0e88d42f7067aa220df`; current replacement baseline is `e29db76041944a368c7dac446c2f894afea05e68`.

The source investigation used AG Charts Community/Enterprise 12.1.1, AG Grid Enterprise 34.1.1 and installed ECharts 6.0.0. Exact bundle hashes and line references are retained in `artifacts/chart-radial/original-contract.md`; these establish inspected-source identity, not runtime acceptance. A maintained final contract will retain only behavior needed by the adapter.

## Family and model contracts

| Property | Radial Column | Radial Bar |
| --- | --- | --- |
| Saved type | radialColumn | radialBar |
| Option namespace | radial-column | radial-bar |
| Category axis | angle-category | radius-category |
| Numerical axis | radius-number | angle-number |
| Absent model-root Group Type | grouped | grouped |
| Primary value encoding | linear radial extent | angular extent |
| Shape boundary | constant-width column, circular clipping | annular sector |

Group Type belongs to model-root seriesGroupType. Grouped, stacked and normalized are supported structural choices; inactive theme copies of those keys must not silently activate. Distinguish root absence from explicit grouped in stale-command checks even though their default visual result matches.

Existing setup owns filtering, series order, aggregation and category/series inversion. The renderer consumes its projection exactly once. Duplicate category text retains distinct row identities. Tooltip and series-label values remain raw post-setup observations; normalized geometry does not turn USD into percentage tooltips. Count aggregation uses count formatting.

## Numerical boundaries

Use separate positive and negative accumulators. Normalization divides by the larger absolute signed cumulative extent per category, rather than the sum of absolute magnitudes or two independent 100 percent sides. For [10,-5], geometry endpoints are [100,-50], while raw values remain [10,-5]. Visible-series filtering recomputes domains, bands and normalized denominators without losing category identity.

Column uses constant-width sides for a given category/group band, not a sector whose width grows with radius. Grouped series split a category band; stacked series share a band. Column width depends on angular span and chart radius, not datum height. Single-category width and circular baseline/outer clipping are explicit spike/probe cases.

Bar swaps those roles: category rings are subdivided by groups, while stacked numerical values accumulate angle. Signed zero location follows the full numerical angular domain; do not start every signed bar at the top. Original LinearAngleScale uses full-circle power-of-two nice-tick behavior. The original installed angle-axis factory gives compact grouped domain [0,20], stacked [0,40] and normalized [0,160]. Thus 100 spans 225 degrees; the last visible normalized tick 140 is not the domain maximum. Mixed signed domains are [-10,30], [-10,70] and [-50,150]. These executable source observations supplement browser tick observations; they do not establish replacement geometry acceptance.

Missing/nonfinite values stay absent. Original run 3 retains a normalized Column failure: the bounded tooltip probe finds no later valid E=30 from Primary, while Bar exposes it and passes the same journey. The independently inspected Column early return explains whole-series suppression when a category is missing; lack of a tooltip hit alone would not prove that cause. The owner approved correcting this on 2026-10-24: omit only the missing observation and keep valid observations visible. Retain the failed original assertion as evidence; do not reproduce the whole-series suppression.

## Effective axis styles and control projection

Do not collapse two distinct axes into one effective polar style. Resolve rendering defaults independently on the applicable category and numerical axes; preserve the original editor's projected defaults separately when its first-axis value differs.

Runtime defaults and source-derived effective values:

- Column numerical inner-radius ratio 0.5; categorical group/series padding zero.
- Bar categorical inner-radius ratio 0.2, paddingInner/groupPaddingInner 0.2, paddingOuter 0.1.
- Both use palette fills and supplied palette strokes, with default series strokeWidth zero unless an explicit user stroke causes the source fallback. Do not inherit Nightingale's background strokes.
- Labels are off. Column label color follows text; Bar follows background.

Polar edits include line color/thickness, inner radius, label typography/orientation and Group/Series Padding. Padding writes only the categorical axis, and orientation only applicable angular labels. Preserve unsupported neighboring-axis keys. Series edits include tooltip, stroke width/dash/opacity, fill opacity and labels; no invented Shape, marker or shadow controls. Preserve unexposed width ratios and inactive corner-radius bytes without adding new controls.

Native legend selection remains transient and flows through the existing host/session projection. Use its actual painted interaction in browser checks; Pie-specific accessibility proxies are not a generic legend contract. Navigator/mini-chart flags require original observation before deciding visible effect.

## Rendering design

Use the existing ECharts host, update/dispose lifecycle, tooltips, legend and export. Radial Bar may use native polar sector series with explicit original axis-domain and ring-band inputs. Radial Column cannot be represented faithfully by native polar sectors; a family-local ECharts custom series is proposed, with mathematically derived constant-width/clipped geometry and original comparison. No generic custom renderer framework or copied upstream path implementation.

The spike must demonstrate actual ECharts output for positive, signed/baseline and one-category cases. Source/API availability alone is not renderer feasibility acceptance. Defer shared arithmetic extraction until semantic equivalence is proven; no cast that falsely identifies Radial as Nightingale.

## Financial fixture

Reuse retained FMP AAPL FY2025 quarterly cost of revenue and gross profit in reported USD. CSV SHA256 `2be4fd02d6aa89ae20b95614fa0d21413db18e75a1b75b3458d1ca9d1e7ca7d8`; raw response SHA256 `390dc8cbfc8302720a203bd9782d5e3b1f7363a4f762bdfcef079dbbe4c72f6b`, retrieved 2026-10-20. The two components reconcile to quarterly revenues [124300000000,95359000000,94036000000,102466000000]. Revenue is a reference, never a third stacked component. Fiscal labels come from fiscalYear/period, not reporting-date calendar year. Retained-data import does not claim a new provider fetch.

Grouped mode compares components; stacked mode shows composition. Neither ring area nor visible Column area is a financial share. Captions and tooltips identify the data and units. Synthetic signed/missing cases supplement, not replace, the real-FMP acceptance journey.

## Freeze and ownership gate

Controller-owned declarations and fixture are materialized at compatibility/radialContracts.ts and tests/unit/chart-compatibility/fixtures/radialContract.ts. Their exact bytes passed RC0C review; the draft header records the earlier inactive checkpoint, before full RC0 acceptance. The [controls review](../../../artifacts/reviewed/chart-radial/controls-contract-review.md) freezes the inactive boundary. The controls and Column geometry helper paths are frozen in the milestone. The pure helper exports buildRadialColumnPath with local pixel input/result types; it is independently accepted as RC0G. The numerical renderer design subsequently froze the renderer paths and exports. RC1 and the serialized RC3 application integration are source-accepted; packaged acceptance remains RC4.

Acceptance requires original observations, numerical/reference expectations, concrete missing-value decision where needed, exact exported types/defaults, source identity and independent RC0 review. Every changed production file must pass 400 physical lines, 300 logical units and 50/function with inventory-backed checks. Do not count source research, a test list or a screenshot as completed packaged acceptance.

## Observed controls boundary

Original run 3 records 19 states per family, including edited options and reload. Series stroke width 3, fill opacity 0.6 and enabled labels survive reload. Inner radius and thickness write both family axes. Group Padding writes paddingInner and Series Padding writes groupPaddingInner on the category axis. Orientation writes the angular axis only. Both editors project zero padding initially, even though Bar effective category padding is 0.2. Color and label typography target both family axes by source inspection; this probe did not edit those fields.

The Column numerical failure does not block the independently reviewed inactive controls lane. It does block claiming full RC0 or visible parity. Current charts, routing and the published alpha remain unchanged.
