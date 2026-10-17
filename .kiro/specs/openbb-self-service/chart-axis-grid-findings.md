# Match original axis and grid behavior using actual rendered fields

The bounded original-runtime capture resolves the missing axis stroke field and several grid-width/dash questions. It does not prove candidate rendering or the complete axis editor. The reference is original Workspace `38dffc33389aca0e4a87e0e88d42f7067aa220df`, image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`.

## Observed results

| Input | Original processed/rendered result | Limit |
| --- | --- | --- |
| Baseline grouped columns | Both axes have `line.stroke = #c1c1c2`; `line.color` is absent. Bottom scene width is 1; disabled left axis has scene width 0 despite its node's visible flag. | Earlier collectors read the wrong field. Node visibility alone does not establish a visible line. |
| Real UI: vertical-axis thickness 3 | Left/right model namespaces retain enabled line width 3; live left-axis width is 3. | One original family, theme and fixture. |
| Real UI: grid thickness 4 | Left/right model grid width is 4; processed style width and five live line widths are 4. | No arbitrary style-inheritance rule inferred. |
| Real UI: grid dash 5 | Model style retains `stroke: #515153` and `lineDash: [5]`; live grid lines use `[5]`. | This is the actual scalar UI action's result. |
| Synthetic: general width 3/style width 1, then general width 1/style width 4 | Live widths follow style width: 1 and 4 respectively, with dash `[2,7]`. | Public-proxy experiments; no UI reachability or persistence claim. |
| Synthetic: style `strokeOpacity` 0.25 and 1 | Original library reports an unknown option; the property is absent from processed style and live nodes retain opacity 1. | No supported original opacity control/effect is established. Do not add an opacity feature from an available ECharts property. |

The [capture report](../../../artifacts/reviewed/consuming-axis-grid-capture/report.md) links exact action/model/processed/scene records, screenshots, source identities, diagnostics and cleanup. Three UI edits and four synthetic cases completed after a diagnosed onboarding-navigation harness correction. The first failed attempt is retained. Onboarding, candidate rendering, provider access and save/reopen were not accepted by this run; diagnostics must be read with the report rather than described as clean.

Independent [review](../../../artifacts/reviewed/consuming-axis-grid-review/report.md) accepts these finite observations, with 231 offline checks and inspection of all eight screenshots. This is acceptance of original-reference evidence, not candidate parity.

## Effect on the consuming design

This evidence supplements the [contract draft](chart-consuming-contract-draft.md). Correct the source collector to use `line.stroke`; do not borrow grid color as an axis-line default. Preserve the distinction between model grid width and effective per-style width. The draft's opacity field is still a proposal, not a supported control or proven source projection. These probes target `gridLine.style[0].strokeOpacity`; they do not settle the earlier ledger's `fillOpacity` or every possible opacity mechanism.

The matching installed source distinguishes these channels: `calculateGridLine` reads stroke, strokeWidth and lineDash, while `calculateGridFill` reads fill and fillOpacity. Treat the earlier fill-opacity observation as grid-fill behavior requiring its own effect evidence. The proposed ECharts split-line opacity target is not an established mapping for that field.

Explicit color edits/conflicts, alternate axis roles/positions, multiple grid styles, retained hidden values, other themes/families and candidate geometry remain open. Use the finite results above as reference assertions in the eventual mapper/editor join, without restricting the product to these captured cases.
