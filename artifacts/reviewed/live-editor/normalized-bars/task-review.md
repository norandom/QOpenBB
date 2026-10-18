# Normalized-bar task graph review

Verdict: PASS for task-phase owner review. Implementation remains unapproved.

Reviewed 2026-10-18 against artifacts/live-editor/normalized-bars/tasks-draft.md, the normalized-bar design, parent requirements/design/tasks, task-generation and parallel-analysis rules, and project delegation/complexity policies. Merge assumption: insert the draft after the existing introduction and preserve every historical task and acceptance record.

- Dependencies are executable: accepted 1.4 and 2.81 precede 2.82; independently reviewed 2.82 freezes shared contracts and reference/runtime details; 2.83 and 2.84 may then run concurrently; 2.85 joins both accepted outputs. The explicit execution sequence governs this prepended amendment rather than historical display order.
- Ownership is disjoint during fan-out. Lifecycle interface edits transfer from 2.82 to 2.84 before parallel work; renderer arithmetic and host interaction have separate production/test files. Application guards, callback composition and shared metadata remain controller-owned. Extraction paths must be agreed before edits.
- Prerequisites are visible: reuse the accepted checker and installed reference/toolchain, settle formatter/fallback/legend/miniature observations before dispatch, freeze native-key mapping and immutable callback inputs, and stop on contradictory observations or additional visible deviations. The approved working horizontal overview is preserved.
- Every new task has observable completion, focused verification, independent review and whole-file 400/300/50 gates. The final task is explicitly integration work and reuses the existing journey infrastructure. Its stated scope limit requires escalation if the join cannot remain bounded; it does not authorize an expanding regression matrix.
- Coverage includes signed normalization, raw financial values, enabled membership, independent overview, physical-X crop, current-request lifecycle, errors/disposal/export, exact family/range restoration, original controls, themes and fresh backend reopen. Earlier aggregation/restart/save-failure evidence is reusable only while changed ownership introduces no concrete regression risk.
- Mechanical document inspection found 141 unique task identifiers in the proposed merged text, no duplicate identifiers, no missing new dependency targets, all 69 active criteria still mapped, and no invalid requirement references in the draft. These are traceability checks, not completed implementation tests.

No corrections required. Broader UI-10, release acceptance and Anthropic-before-Excel remain gated. Historical superseded renderer clauses do not override the approved normalized amendment. No production/spec files changed and no tests or builds ran for this review.
