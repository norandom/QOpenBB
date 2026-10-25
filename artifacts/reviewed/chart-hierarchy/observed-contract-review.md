# H0 observed-contract review

The bounded numerical/control evidence is approved for the H0 contract join after the completed follow-ups and explicit policy decisions below. Exact typed interfaces and ownership still require controller freeze. This is not production implementation, H4 acceptance or clean application diagnostics. Earlier findings below remain the review history; the final disposition resolves their H0 scope.

This independent review inspected run 2 observations and the edge-size/no-size screenshots under `../original/run-2/browser-output/hierarchy-original-origina-f1047--bounded-hierarchy-contract/`. The reviewed probe is `8deb7da0c073eec3dc1799c635f13c7315f9133346b394b2e3e7b2e275139ee6`. The worker reports one passing characterization test; the reviewer did not execute browser/tests/builds. Run 1's Shared-versus-Multiple selector failure is explained in the pre-execution review. It is not an application failure.

## Observed numerical distinctions

| Observation | Treemap evidence and consequence |
| --- | --- |
| Duplicate West/Alpha | Native Size/Color values are 6/20 with aggregation off, 8/10 with sum, 4/5 with average, and 2/2 with count. Two numeric fields have separate roles; aggregation operates on both. |
| Missing Color | Gamma has Size 4 and no Color tooltip field with aggregation off, sum or average. Count displays Color 1 and Size 1 despite the original missing Color. Count must not be described as a count of measured nonmissing color values. |
| Parent tooltip | West/East display their labels only. Derived parent totals are not displayed by these observed tooltips. Do not add totals while claiming exact tooltip parity. |
| Ordered categories | Saved columns change from Region,Desk,Size,Color to Desk,Region,Size,Color; observed parent labels become Alpha/Beta/Gamma with child West/East. |
| Numeric reorder | Saved columns become Region,Desk,Color,Size and the layout changes; Beta has no successful label hit. Missing hover alone does not prove absence. |
| Missing size | Missing is visibly a narrow tile beside Valid, whose native tooltip displays Size 8. Missing tooltip has no amount. Screenshot proportions are consistent with the proposed 1:8 weights, but this visual review is not an exact geometric calculation. |
| No selected size | Saved columns contain Group,Leaf only. Screenshot shows four equal-sized tiles, including Zero and Negative. Native tooltips contain labels without amounts. Restore/reload brings back Missing and Valid tiles with the preceding labels/amounts. |

The owner approved excluding missing sizes on 2026-10-25, as relayed by the controller: when Size is selected, missing contributes zero weight/no area while valid values remain; deliberate no-size equal count weighting, zero/negative handling and duplicates remain unchanged. Preserve raw missingness rather than reporting an imputed financial zero. A fallback geometric weight is not an observed financial amount.

## Observed controls and unresolved findings

Treemap Series defaults are group padding 4, group spacing 2, tile padding 3 and tile spacing 1. The four changed captures serialize respectively to `chartOptions.treemap.series.group.padding`, `.group.gap`, `.tile.padding` and `.tile.gap`. This confirms the index-selected inputs' identities. Saved paths alone do not certify each visible spacing effect; inspect the relevant screenshots before closure.

Multiple serializes to `chartOptions.treemap.tooltip.mode = shared`; Compact serializes to compact. These paths are directly beneath the family options, not `series.tooltip`. The observed tooltip strings are unchanged across modes.

Important: the tooltips-disabled record saves `chartOptions.treemap.tooltip.enabled = false` yet retains all six native parent/leaf tooltip hits. Do not call the off control functional. One settled off/re-hover observation should distinguish an inert original control from timing before freezing the replacement policy.

Important: run 2 diagnostics contain `Unexpected token '<'` and a failed `/api/pro/files/...csv` request. They remain recorded; attribute the error and its effect on the observed scope before claiming a clean run. A characterization test's passing exit code does not mean clean application diagnostics.

The initial probe does not close title/theme, third-numeric-selection, parent click, quick actions/common panels, nondefault-control reload, no-category or all-zero-total behavior. Complete only minimal targeted transitions. Equal/all-missing color-domain cases may remain explicitly unobserved until needed by the implementation contract. The final capture/setup/control interface contract is still awaiting review.

## Sunburst run 3

Independently inspected run 3 observations and edge-size/no-size screenshots. Sized Missing is visibly a small sector beside Valid=8, consistent with the source's 1:8 weighting; zero/negative have no visible sized sectors. No-size shows four equal outer sectors. The observer records zero sectors/outlines because Path2D is not decoded, so exact angular measurement is not claimed.

Sunburst size tooltips confirm duplicate off/sum/average/count values 6/8/4/2. Numeric reorder displays Color values 20 and 10 as sizes. Default parent tooltips repeat the label without a derived amount. Compact removes the size text from leaf tooltips, unlike Treemap's equivalent text across modes. Tooltip disablement still retains hits and the same diagnostic classes recur; the settled follow-up remains necessary. These are original characterization findings, not replacement acceptance.

## Final H0 evidence disposition

APPROVED for the bounded numerical/control contract join. Independently read completed runs 5/6 follow-up JSON and inspected both families' no-category and all-zero PNGs. Both save tooltip enabled=false and produce six native hits in each of three traversals after explicit no-visible-tooltip checks; true also produces six each. This establishes the inert original toggle beyond stale text. The controller authorized honoring the existing toggle intent in replacement: false hides, true restores, using observed family-root paths and preserving family mode effects.

No-category selects Size,Color and visibly retains five unlabeled root marks; zero-category identity therefore uses individual source row IDs, not an empty-path duplicate collapse. All-zero charts are blank. At two numeric selections the Add Series combobox is absent. These observations close the small prerequisite gaps without another framework or exhaustive common-control traversal.

Independently read pinned G42254-42316 and rehashed the installed AG Grid source to `76831274e5f22060913871da1e756d5269e71b87ea9a601ecac05baca4504286`. Category canonicalization is null for nullish values, String(value) otherwise; no-category rootValues keeps each row. Retain raw string/number/null categories separately from canonical string/null paths; undefined normalizes to null, empty string stays distinct. These scalar cases are source-backed, not runtime observations. Do not group by raw typed identity and thereby silently change original numeric/string collisions.

Remaining common title/gradient/navigation mutations, precise layout/spacing, packaged financial data, export and fresh-session persistence are explicitly H4 candidate gates per the controller's bounded scope decision. Their absence does not block this numerical/control contract, and they must not be claimed as completed tests. Baseline diagnostic errors remain unattributed; run 4 establishes only the fresh-reopen upload-route limitation. Follow-ups retain a CSV failure despite no page errors. H0 approval therefore does not assert clean diagnostics or persistence.

Reviewed worker join report: `../original/probe-report.json`, supplied SHA256 `da45217f91b307c04d0f0783411d8d0f475ceba712086b16f1f063c3daf410f2`. Its scope and failure distinctions agree with the inspected evidence. The reviewer ran only source/artifact reads and hashes; reported browser/lint/typecheck exits belong to the worker's evidence.
