# Area chart design review

PASS for the scoped design amendment after one local repair round. This verdict is independent design review, not owner design approval, task approval, financial validation or runtime acceptance.

Reviewed on 2026-10-18 using `kiro-spec-design/rules/design-review-gate.md`. Draft SHA-256: `0cb461aee254c8985ef1a481b02b2dbb3cbc014c8eeaedd49f0dd5d2acbc9422`. Current Workspace source: `375fe8990c698ef5e9d4c972f92e6b77c242dae3`.

Mechanical checks pass: all scoped criteria 4.7, 4.8, 4.9 and 10.1-10.6 appear in the traceability table with concrete validation obligations. Boundary commitments, exclusions, allowed dependencies and revalidation triggers are populated. File ownership now gives explicit production, test and delivery paths without placeholders. Introduced area projection/types and existing integration components have corresponding owners. Other requirements remain governed by the main design.

The existing normalized-bar design and current family, mapper, series, appearance, eligibility and application projection code support the proposed seams. Area arithmetic must be separate from the existing signed-bar normalization. Raw observations remain authoritative for labels, tooltips and persistence; the native host retains transient selection ownership. Renderer and editor lanes have disjoint paths; the controller owns shared contracts and serializes activation. Whole-file 400/300 and per-function 50 caps, inventory registration and the combined audit are explicit.

The repair prevents premature caller activation: both `isCartesianFamily` and its transitive normalization admission remain unchanged until the join. It also removes ambiguous relative paths from the ownership table.

Arithmetic, signed fill boundaries, missing values, original controls, axis formatting and miniature semantics remain explicit prerequisites. The `[7,-6,5]` example is labeled an inference, not accepted numerical evidence. Native geometry failure blocks dependent work and requires a concrete adapter design review; it does not approve approximate stacking, changed financial values or a visible deviation. Removing a default does not establish connect-missing control eligibility.

No blocking design issue remains. Generate tasks only after owner design approval; freeze the numerical contract and typed seam before implementation fan-out. Native geometry mismatch or contradictory source/runtime evidence reopens the affected design decision. No browser, installation, test execution or production edit was performed for this review.
