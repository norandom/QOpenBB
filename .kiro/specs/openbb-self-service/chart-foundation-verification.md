# Chart foundation verification

The approved foundation has working state reducers and a React/ECharts lifecycle host. It remains isolated from Workspace application controls. This record covers tasks 2.13-2.18; it does not accept the whole renderer or a deployable release.

## Source and verification scope

- Workspace: `042ba87e3208a51857da4ae2d1c3109a680716d9`, owned `qopenbb/baseline` branch.
- Foundation comparison base: `48e3f59cc48e0ae7aa6f6ce92069fc5b10ee3e86`.
- Original behavior reference: `38dffc33389aca0e4a87e0e88d42f7067aa220df`.
- ECharts 6.0.0 and zrender 6.0.0 are pinned through the existing protected Bun lock. Safe Chain interception, the 48-hour minimum age and an empty-cache frozen restore passed. Licenses and notices retain their package integrity and recorded hashes.
- Current committed branch files match the independently tested host stage. Package/lock identities match its shared, protected dependency stage. The initial joined comparison assumed the lock existed in the fixture stage; the corrected check follows the actual dependency-stage location and passes.

## Observed results

| Check | Result | Evidence |
| --- | --- | --- |
| Shared contracts and reducers | 10 contract and 16 reducer cases; unknown fields, arrays, null/undefined, original write ordering and repeated edits preserved | `artifacts/task-2.14/review/`, `artifacts/task-2.15/review/` |
| Lifecycle and React ownership | 13 lifecycle and 6 host cases; stale revisions/observers, hidden recovery, errors and disposal | `artifacts/task-2.16/review/`, `artifacts/task-2.17/review/` |
| Joined focused suite | 46 tests passed, including one real-library tooling test; strict TypeScript and scoped lint pass | `artifacts/task-2.17/review/check.log`, `lint-pinned.log` |
| Real browser | Fresh production build; two one-worker cases pass; zero CDP diagnostic errors, owned server/browser cleaned up | `artifacts/task-2.17/review/browser-results.json`, `browser.log`, `identity.log` |
| PNG and displayed data | 640 by 400 PNG independently inspected; visible USD observations 123.45 and 67.89; pixel contents, numeric options and changed output asserted | Actual-host browser case and PNG attachment |
| Existing Perspective runtime | 10 unit cases, strict TypeScript, production build and four browser cases pass | `artifacts/task-2.18/perspective-*.log`, `perspective-browser.json` |
| Complexity | Current dirty-fork gate passes; supplementary measurement of all five registered foundation modules passes 400/300/50 | `artifacts/task-2.18/complexity.json`, `joined-module-quality.json` |
| Source and scope | All changed branch files match tested stage bytes; no application call-site, guard, feature-flag, catalog, editor, provider or Excel changes | `artifacts/task-2.18/joined-source-hashes.log`, `scope-audit.md` |

Sol workers implemented bounded tasks; independent Astra reviewers accepted each production leaf. A Luna mechanical audit checked scope and documentation links. State and lifecycle implementation ran in parallel after the contracts froze. The controller serialized dependency changes, builds, browser checks and commits. Existing unrelated financial/catalog work was preserved and is outside this acceptance.

Run the maintained commands in [chart foundation verification](../../../docs/chart-foundation.md). The same portable verification commands run outside Dagger. The source lock identifies the acquired/adapted fork; `validated_release` remains null.

## Remaining application obligations

Requirements 4.8 and 4.9 remain open. The next integration design must connect these modules through the original controls and verify editor field mapping, chart families, light/dark styling, table capabilities, selection/zoom continuity and original export behavior. Actual save/restart/reopen still requires the separately identified SQLite query repair and application persistence tests.

No live FMP/FRED request, Anthropic acceptance, Excel implementation or release image is established by this fixture suite. Whole-application TypeScript retains its recorded upstream TS6305/TS5103 blockers; focused strict checks cannot be reported as whole-application success.

Independent Astra joined review returned APPROVED for task 2.18 and GO for tasks 2.13-2.18 only. Fresh verification reproduced all 46 focused tests, strict TypeScript, all 24 changed-file identities and the five-module cap audit. The full report is retained in ignored `artifacts/task-2.18/review/verdict.md`; acceptance is recorded in [tasks](tasks.md) and [phase status](spec.json).
