# Labels and Markers design/task review

PASS. No blocking findings in the reviewed design and task draft. This is a source-based design review, not implementation acceptance or phase approval.

- Contracts and ownership are disjoint: 2.60 owns Labels, 2.61 owns Markers, and 2.62 owns composition and delivery metadata. Shared accepted controls and styles are read-only; edit events, state, choices and caller responsibilities are explicit.
- Original installed FontPanel/Labels source confirms Font, Weight and the grouped Size/Color row. The existing Labels capture confirms Verdana, Predefined, size 12 and #FFFFFF. Ordinary Labels excludes text, placement, padding and format controls.
- Original Markers source confirms Shape, Size and Stroke Width, caller shape order square/circle/cross/diamond/plus/triangle/heart, and default maxima 60/10. There is no invented Color control. Retained unknown values, invalid drafts and disabled values have explicit acceptance criteria.
- Original family ordering confirms bar Labels before Shadow and line numeric controls before Markers before Labels, with no line Fill Opacity/Shadow. Family eligibility stays with callers; scatter/bubble and other special label groups remain explicitly deferred. The story selector is bounded preview input and introduces no production feature flag or full-family claim.
- Task 2.59 is checked complete in tasks.md and independently APPROVED in its existing review. The graph is accepted 2.59 -> parallel 2.60/2.61 -> joined 2.62; controller ownership of shared metadata and the serialized browser lane prevents overlapping worker writes.
- The existing checker/inventory foundation is reused, new maintained production files must meet 400 physical lines / 300 logical units / 50 units per function, and inventory registration is required. Focused component tests/static checks plus one combined isolated light/dark browser/CDP join satisfy the bounded verification plan. No new harness copy or broad repeated suite is requested.

Inspected existing original source ranges: main.cjs.js 47233-47420, 48532-48584, 48931-48953 and 49084-49115. Existing reviewed JSON captures were read; no captures, tests or implementation edits were made for this review.

Exact reviewed SHA256 identities:

| Path | SHA256 |
| --- | --- |
| .kiro/specs/openbb-self-service/chart-labels-markers-design.md | 75052111c0539d1d863f00d6e56a7997882438cc1043eda21ece3d42c5c98601 |
| artifacts/task-2.60/tasks-draft.md | ee23127fea69a326bf3124bd81b5ccd413ac8ecbaaf2a2b11b6bb76001e7c87d |
| artifacts/task-2.1/frontend/terminalpro/node_modules/ag-grid-enterprise/dist/package/main.cjs.js | ff634fef7612738444a1618604ea88c0625328f271382f2fb3aaf9a26926d30c |
| artifacts/reviewed/parity/editor-runtime-next/focused/Series-labels-enabled.json | 7ad46dbe140d791328ed99a8a3635b581feab830400e1d568f12f0c36dc67271 |
| artifacts/reviewed/parity/editor-runtime-next/focused/line-markers-on.json | 843c14636f1b8140f285388173a9e8365da6f9270f78f2be068ad2d7d78d9032 |
| artifacts/task-2.59/review/verdict.md | 490eb1c5178f30eb88aced9fd583c475e586adcb4f7de659cc90664cbfefa428 |
