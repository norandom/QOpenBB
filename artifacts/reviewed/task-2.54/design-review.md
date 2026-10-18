# PASS: Background and Tooltips design and task plan

Independent bounded review on 2026-10-18. Tasks 2.54 and 2.55 can proceed after accepted 2.53, with controller integration at 2.56. No design or task-plan blocker found. This verdict covers the proposed controlled UI slice, not implemented behavior or renderer acceptance.

The original Chart Style capture places Background after Padding. The Series capture places Tooltips before Stroke Width, inside Series. The design preserves both parent groups and field order, including the collapsed Series parent. Original installed AG source at lines 48043-48077 confirms background.visible and background.fill; lines 48776-48827 confirm tooltip.enabled and tooltip.mode. The captured menu and source agree on Single=single, Multiple=shared, Compact=compact.

The contracts preserve caller-owned booleans and hidden fill/mode values, forbid mount edits and normalization, retain unknown modes, and reuse CaptionColorInput for alpha, correctable drafts and picker keyboard behavior. No extra opacity or tooltip settings are introduced. These are explicit implementation obligations, not tests already passed.

Ownership is disjoint: each worker owns its panel, focused test and individual story; shared accepted controls remain read-only. The controller owns combined-story composition and delivery metadata. Interpret worker task bullets to register files as supplying their inventory entries to the controller, who serializes shared inventory and breadth edits. Task 2.56 explicitly depends on both accepted panels and checks retained edits across dock and tab lifecycle in both themes.

All six cited criteria are represented within the bounded slice: 4.8/4.9 through original controls and scoped evidence; 10.1/10.4 through isolated verification with one browser lane; 10.5 through the controller breadth update; 10.6 through explicit evidence limitations. Existing complexity foundation is reused and 400/300/50 caps apply to complete maintained production files. The tasks have observable completion conditions and an explicit integration join. Full renderer parity and other requirements remain outside this incremental plan and are not declared complete.

Reviewed bytes (SHA-256):

- `.kiro/specs/openbb-self-service/chart-background-tooltip-design.md`: `5BBEF64DF51FA4B49F2F905ACA73DE9272370A00988788351ECC7C014E28AF18`
- `artifacts/task-2.54/tasks-draft.md`: `783B5D0B32C1BD37666B18CB44F022268A9E243483F35DBD423DF76FD5F46986`
- `.kiro/specs/openbb-self-service/requirements.md`: `3200AFA4A8412CF097CB2479A1E969F50225748E6903BA9D7405807534A0D43B`

Reviewed task-generation rules, complexity, delegation, workspace-experience and documentation steering, and the existing cited JSON/source evidence. No new browser capture or production edits were made. Implementation acceptance still requires independent review and fresh focused evidence; the unresolved historical tooltip-toggle runtime effect must remain disclosed.
