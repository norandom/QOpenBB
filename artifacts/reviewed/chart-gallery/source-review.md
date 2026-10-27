# HG0 native gallery seam review

## Review verdict

- VERDICT: APPROVED
- TASK: HG0 native saved-state fixture and source compatibility, reviewed 2026-10-27.
- MECHANICAL_RESULTS: Final focused Vitest run passes 15/15 cases, exit 0; scoped Biome lint passes, exit 0. Reviewer read the executed logs and independently matched both frozen input hashes. Placeholder and credential-marker scans have zero matches. Static source review and boundary audit are clean. The worker's exact-path whitespace checks pass.
- RED phase: Initial characterization is recorded in `unit-initial.log`: 14 pass and one failure because native schema defaults made whole-object equality inappropriate. The corrected assertion preserves supplied fields and still requires exact model/range equality. This is fixture characterization; production behavior was unchanged.
- FINDINGS: No blocking contract defect.
- REMEDIATION: None for this seam. Controller-owned inventory, generation interface and milestone closure remain separate HG0 responsibilities.
- SUMMARY: The frozen twelve dataset schemas and all 36 chart payloads can feed the existing native template path without changing production helpers.

## Accepted contract

Read the milestone, actual fixture/test and native schema/hydration sources rather than relying on the worker report. The fixture has exactly the twelve named datasets and the native 35 chart IDs plus `customCombo`. Selected fields exist in the ordered typed schemas. The `companies` mapping supplies visible company names while raw symbols remain available for filtering and provenance.

The test resolves the ordinary source widgets through native `createSourceWidget` and `createCustomTemplateTab`. All 36 receive generated instance IDs, their exact saved models and family ranges, and the native `default` storage partition. Schema parsing preserves the supplied state. Untouched template reuse and numbered copies preserve an edited existing dashboard in the tested helper path.

Sankey correctly omits top-level `state.chartModel`. Its model and `sankeySetup` remain in `state.storage.default`; the generic top-level model branch would otherwise replace the family object and delete its bindings. Native `readSankeySetup` accepts the hydrated selection, including USD, scale 1e9 and derived-income-allocation metadata. Hierarchy recovers fiscal year, quarter and component ordering with `sum`. Preset combos omit assignments; Custom Combo explicitly puts revenue and net income on the left and basic EPS on the right. Native XY assignment resolution preserves volatility, return and activity-proxy roles.

Histogram and Range Area use the native `filterModel.default` symbol-equals-AAPL state. Daily observations remain unaggregated. The final Histogram fixture has twelve equal one-percentage-point bins spanning -6% to +6%; native internal-edge and final-edge inclusion pass. The independent financial reference gives 84 Apple daily returns with extrema approximately -4.040% and 3.654%, inside these bounds. Generation must enforce that envelope because the inherited final-bin predicate also accepts remaining values below the first edge. Waterfall keeps five signed movements; no unsupported subtotal bars are introduced.

The schemas support the milestone's financial recipes: wide monthly returns for Heatmap, mutually exclusive cost/gross leaves, signed income movements, conserved allocation links, reported overlapping income levels and separate EPS units. Reviewed `../capture/financial-reference.json` as the independent finite-input reference. This seam does not execute the future financial projections or certify rendered values.

## Evidence and reproducibility

| Input | SHA-256 |
| --- | --- |
| `contracts/gallery/chart-state.json` | `7955103d90990e24a6515074ab44d90bbc513b5425f7cc8fd637026ed221ef9e` |
| `vendor/workspace/terminalpro/tests/unit/chart-compatibility/galleryTemplate.test.ts` | `d9b735e20891b25cc400a6c2ca9a09ccd1789a55c0a924bc24f1470ab981ca16` |

The base revisions are QOpenBB `6c09e0559e139477cb4e9d1a21502ae46a1eec62` and Workspace `cdefb7638c0991281551db66415328e420287009`. The reviewed additions are working-tree files. Retained local worker evidence (`artifacts/historical-gallery/contract/seam-evidence.md`) records the full pinned-Node WSL command and exit codes. Reviewer read retained final Vitest output (`unit-final.log`): 15 passed, start 14:25:26, duration 28.26 seconds; and retained lint output (`lint.log`): one file checked, no fixes. The suite was not duplicated during review.

From `vendor/workspace/terminalpro`, the scoped commands are:

```sh
node node_modules/vitest/vitest.mjs run tests/unit/chart-compatibility/galleryTemplate.test.ts --maxWorkers=1
node node_modules/@biomejs/biome/bin/biome lint tests/unit/chart-compatibility/galleryTemplate.test.ts
```

This is a QOpenBB integration gate. The default fixture path resolves `../../../contracts/gallery/chart-state.json` from that working directory; `QOPENBB_GALLERY_CONTRACT` can supply an explicit path. A missing parent fixture fails collection with a filesystem error rather than skipping the test. No duplicate fixture or standalone-fork CI expansion is required.

Tests and the contract fixture are outside production size caps. The disposable ignored authoring script is not the maintained HG2 generator. HG2 must consume the frozen JSON and implement its own capped generator; its proposed command is explicitly unexecuted. No production helper, runtime, image, installed service or provider input was changed by this review. Required complexity/delegation/testing/documentation steering was read; the configured product/tech/structure steering files are absent.

## Acceptance boundary

Source inspection confirms `openListedApp` selects the first template and the add-backend success toast in `ManageAppDialog` can iterate all templates. The edit-backend branch returns before that toast. HG3 must therefore verify actual gallery navigation for the installed connector, alongside all 36 renders, financial values, filters, controls, persistence and retained-state recreation. Source navigation is sufficient for this fixture gate and makes no browser acceptance claim.

The controller should record this source-only navigation boundary in the milestone and keep actual navigation in HG3. Runtime packaging, generated data/catalog validation, financial calculations, screenshots, publication and owner-server deployment remain unverified by this review.
