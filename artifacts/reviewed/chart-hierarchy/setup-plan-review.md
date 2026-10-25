# H1c setup and prepared-node plan review

VERDICT: APPROVED for implementation of the five-module inactive H1c plan. The owner grouping decision and explicit Average initialization resolve the previous blocker. This is plan approval, not implementation or runtime acceptance.

Reviewed `artifacts/chart-hierarchy/h1c-plan.md`, final SHA256 `e666341913dba00bdadab1896daed3310d69772d3ae2dba0966f0f628699ff5b`, against accepted H1a/H1b APIs and directly inspected pinned AG Grid source. The initial reviewed revision was `b06a84bad7438e315eaa9b14e1eda122a3148a3576c179356c9b5e54c62caa11`; the final policy, arithmetic and verification-command changes were directly reread and rehashed. No implementation, test, browser or build ran in this reviewer lane.

## Resolved numerical distinction

The original explicit aggregation stage G42701 onward indexes a plain object using each raw category cell (`currentMap[key]`). A null category and the literal string "null" therefore fall into the same aggregate bucket. The later hierarchy builder canonicalizes nullish values to null and other values to String, using a Map, so without explicit aggregation those two category paths remain distinct.

The canonical-array Map keeps null and "null" separate. The owner approved this correction on 2026-10-25, as relayed by the controller after explicitly presenting the recommended interpretation. The final plan labels it as a deliberate correction to original aggregation, distinct from the earlier approved missing-size correction. Safe Map storage avoids prototype hazards. Tests of null-versus-literal-null aggregation must be described as approved-correction regressions, not original observed parity.

## Other findings

- Directly inspected G24495 onward: all-missing Sum, Average, Min and Max yield null. First/Last retain endpoint missingness. Count counts every admitted scalar row, including missing/null. Sum initializes from the first number; Average accumulation starts at positive zero. The final plan now states that Average initialization explicitly for signed-zero tests.
- Canonical numeric/string 1 and boolean/string true equivalence is otherwise consistent. Structural tuples avoid delimiter collisions; no-category rows bypass aggregation and retain independent row identity. No-size count weighting remains distinct from selected missing-size zero weight.
- Count relabels selected numeric descriptors as observation-count/scale 1 only when aggregation executes; no-category saved Count cannot relabel financial amounts. Original labels/units and raw observations remain available through detached source provenance.
- Winning representative and all bucket candidate sourceRowIds are clearly distinguished. Keeping zero-weight leaves and raw color values preserves information needed by H2 color-domain decisions; the renderer must not infer a positive-weight-only domain without its own source-backed contract.
- Fixed-depth rows prevent internal own-value ambiguity. Synthetic root/internal own weights are zero, and finite overflow diagnostics prevent partial or nonfinite output. This safety boundary is explicit rather than claimed as original runtime behavior.
- Multi-category source onValueChange updates selection/order without clearing aggFunc, while default-category clearing is in a separate single-select branch. Preserving an inactive aggFunc after removing the last hierarchy category is source-backed and consistent with inactive-option preservation; it remains unobserved in the browser probe.
- Exact new ownership is cohesive and capped; H1a types are imported, no prepared output is written into ordinary snapshots, and transitions remain detached pure results. H3 alone owns stamps, recapture checks, storage writes and atomic live union integration.

The two planned suites cover meaningful numerical, identity, finite-failure, retained-FMP reconciliation and transition behavior. Runtime/geometry/browser acceptance remains H4. No extra framework or further task subdivision is required. Final commands use the existing application Vitest configuration with one worker and the repository's TypeScript toolchain. No remaining blocking plan finding was identified; implementation must still supply RED/GREEN, inherited-static-diagnostic comparison, independent review and inventory-backed 400/300/50 size evidence.
