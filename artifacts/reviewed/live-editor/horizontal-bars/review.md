# Horizontal-bar design review

Independent Astra review approved the scoped UI-10 design for ordinary `groupedBar` and `stackedBar`. This is design review, not owner approval or implementation evidence.

The design reuses existing capture, appearance, controls, session and persistence owners. Sol research identified hardcoded family admission, initial axes, physical axis/title bindings and section ordering. No production code or dependencies changed.

Two review corrections were applied: the existing Customize composition owns Horizontal-before-Vertical section order using current binding direction, and a controller-owned prerequisite records original category ordering, signed-stack endpoints and navigator/miniature behavior before dependent renderer work starts. Task generation must assign exact test files and any required cohesive extraction paths before fan-out.

Whole-file caps remain 400 physical lines, 300 logical units and 50 units/function. The plan reuses existing checks, isolated browser fixtures and the complexity inventory. It does not introduce a new harness, hidden feature reductions or invented saved axis fields. Visible deviations require an owner decision before acceptance. Other Cartesian families, advanced callers and release acceptance remain pending.

Reviewed Workspace source: `aa2e0bfe4253edf6bf6ef2f18822d4304f07fdd8`. Design SHA-256: `97e58b19b22ebfb32deac18d234eaefe42f5514ddfae5f05bc7436de2e9b7a69`. Final reviewer verdict: APPROVED. No runtime tests were run for this documentation-only amendment.
