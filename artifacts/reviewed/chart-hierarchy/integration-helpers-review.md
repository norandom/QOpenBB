# H3 inactive helpers independent review

APPROVED for the frozen H3 step 1 helper/extraction slice. The implementation preserves ordinary routing and supplies inactive hierarchy range, session, palette and hover prerequisites. It does not activate hierarchy charts, complete H3, or establish browser/H4 acceptance.

- VERDICT: APPROVED.
- TASK: H3 step 1 under the [integration design](../../../.kiro/specs/analyst-workspace/hierarchy-integration-design.md), including the approved capture-free frame and immediate-command stamp amendments.
- SOURCE: Workspace base `a5112cb3312c85524b32fe6bba7c35e1bb23e0b9` plus the 20 frozen file hashes in local `artifacts/chart-hierarchy/h3-helpers/frozen-files.json`. The reviewer independently matched all 20 before execution and again after execution; no mismatch or source mutation occurred.
- BOUNDARY: 17 maintained production files and three test files. The two hierarchy UI components and their test were accepted separately and are not accepted again here. The reviewer changed only local review/check artifacts, not production code.
- FINDINGS: No unresolved blocking finding within this inactive slice.

## Contract assessment

The reviewer read all 17 complete production owners, all three tests, and the six existing-file diffs. The shared changes are cohesive extractions: family dispatch moves to `applicationChartProjection.ts`, ready-editor composition to `LiveChartEditor.tsx`, and native legend selection projection to `lifecycleLegendProjection.ts`. Existing family branches, callbacks and persistence behavior are retained. `ApplicationSessionFrame` removes an unnecessary capture requirement only from baseline/reducer helpers. Ordinary capture-bearing contexts and retained state still use `ChartSnapshot`; no hierarchy family or retained union is activated. The standalone hierarchy state interface is a structural input view, not another runtime state store.

`hierarchyRange.ts` preserves saved `[]`, category-only and numeric-only vectors, row bounds and unknown range metadata. It rejects explicit saved numeric counts above two before visibility filtering. Fresh membership follows numeric collection order before assignment follows candidate order. Gallery reduction remains a separate operation, discards the ordinary synthetic category and confines the no-selection numeric fallback to the source maximum-reduction case. The shared session selector preserves saved empty/single selections without requiring an existing local frame key and expires the accepted local override after configuration identity changes. Independent checks exercised those session-level paths, beyond the implementer's pure range cases.

Session selection reuses H1 financial preparation and H2 appearance/translation. Only actual aggregated Count changes units; no-category Count retains raw units and no Size retains equal observation weights. Grid capture occurs outside replayable reducers. Setup validates the latest frame without requiring current arithmetic to succeed, reruns the transition, verifies exact recapture origin and current data identity, checks category order and retained/requested numeric fields, then projects prospective arithmetic before returning a commit. Full model replacement removes `aggFunc` when disabled while preserving unknown fields. A failed prospective projection returns no partial commit.

The stamp correction is implemented: immediate commands may survive an option-only render advance, while earlier data/generation changes remain stale. Recapture must match the original command's complete stamp before current synchronous freshness checks. Appearance maps current style/assignments against latest storage, so two same-origin edits compose. Export/render/hover freshness is not relaxed by these helpers.

The palette helper uses the same selected theme as the existing caller and preserves pinned light/dark/custom hierarchy tokens. Source inspection confirmed the default light/dark diverging color values are identical in the pinned AG Charts package; the different hierarchy and stroke arrays are retained. Native hover uses own plain data IDs plus series identity, finite marker geometry, one silent graphic, and exact listener cleanup. Independent checks also verified cleanup after partial subscription failure and continued removal after an unsubscribe throws. The binder invalidates itself before cleanup and remains idempotent.

The approved [setup contract](../../../.kiro/specs/analyst-workspace/hierarchy-setup-design.md) and [renderer contract](../../../.kiro/specs/analyst-workspace/hierarchy-renderer-design.md) remain the numerical and appearance authorities. No duplicate tree preparation, alternate persistence owner, feature flag or fallback renderer was introduced.

## Mechanical evidence

Independent checks ran serially with pinned Node 24.22.0, Vitest 4.1.11 and existing one-worker configurations. The reviewer entry point was `wsl -d Debian --cd /mnt/d/Source/QOpenBB -- pipeline/.venv/bin/python artifacts/chart-hierarchy/h3-helpers/reviewer-verify.py`. Its subprocess exit codes were all zero and its before/after source hashes matched.

| Check | Result | Local raw evidence |
| --- | --- | --- |
| Hierarchy session/owner plus ordinary transaction and range suites | 27 tests in four files passed, exit 0 | `artifacts/chart-hierarchy/h3-helpers/reviewer-application.log` and `.exit` |
| Hierarchy binder and existing lifecycle suites | 36 tests in two files passed, exit 0 | `artifacts/chart-hierarchy/h3-helpers/reviewer-hover.log` and `.exit` |
| Independent session-range and listener-failure cases | Six tests passed, exit 0 | `artifacts/chart-hierarchy/h3-helpers/reviewer-boundaries.log` and `.exit` |
| Independent Biome lint | All 20 owned production/test files passed, exit 0 | `artifacts/chart-hierarchy/h3-helpers/reviewer-lint.log` and `.exit` |
| Frozen bytes | All 20 match the worker freeze before and after checks | `artifacts/chart-hierarchy/h3-helpers/reviewer-source-before.json`, `reviewer-source-after.json`, `reviewer-results.json` |
| Maintained inventory and combined caps | Controller gate exit 0; reviewer verified all 17 owners included, zero errors/violations | `artifacts/chart-hierarchy/h3-helpers/combined.json` |
| Placeholder/credential spot scan | No TBD/TODO/FIXME/HACK/XXX or concrete scanned key patterns in the 17 production owners | Reviewer read-only `rg` scan |
| RED-before-implementation | Four meaningful missing-export/import failures inspected | `artifacts/chart-hierarchy/h3-helpers/red-session.log`, `red-transactions.log`, `red-owner.log`, `red-hover.log` |

The controller's combined whole-file gate reports maximum 377 physical lines and 216 logical units in `lifecycle.ts`; the largest callable is 38 units in `applicationSessionEdit.ts`. The largest new helper is `hierarchySessionTransactions.ts` at 226 physical lines. All changed files satisfy 400 physical/300 logical/50 per function. Eleven new production owners are registered; no size exception was used.

The implementer also supplied a passing broader ordinary/caller regression run: 137 tests in nine files, exit 0, plus the 36 binder/lifecycle tests. The reviewer inspected that evidence rather than rerunning the same broad suite. Some passing JSDOM application cases emit the inherited unavailable-canvas-context diagnostic; these tests are not browser rendering evidence.

## TypeScript evidence and limits

The broad TypeScript 6.0.3 scopes do not compile cleanly. Final measured compiler exits are 2. Application diagnostics change from 3,476 to 3,480; compatibility retains 3,489. The original pre-edit logs are retained, but their wrapper did not preserve compiler exit status, so this review does not assign a baseline exit code.

Application adds four newly reachable TS2882 CSS declaration errors in separately accepted files: one in `HierarchySetupPanel.tsx`, two in `HierarchyGradientLegendPanel.tsx`, and one in `HierarchySpacingControls.tsx`. The broad application configuration lacks the Vite CSS declarations and now reaches these imports through the new editor tests/props. The separately accepted UI scope includes `vite-env.d.ts` and retained its four unrelated inherited diagnostics unchanged. These are real new exposures in the broad diagnostic output, not helper-owned source errors, and must not be described as an identical or clean typecheck.

Both broad comparisons also contain three changed TS2345 diagnostic text blocks at unchanged `src/lib/state/app.ts` positions 664:13, 1215:13 and 2122:13. Their leading assignability statements, locations and terminal optional `data.name` versus required string failure are unchanged; the truncated inferred union display order differs. No helper-owned diagnostic was added. Local `artifacts/chart-hierarchy/h3-helpers/static-comparison.json` retains the full differing blocks and the `application-*.log`/`compatibility-*.log` files retain raw compiler output. This classification is narrower than a repository compile pass and does not waive future integration diagnostics.

## Remaining integration gate

Step 2 must still activate the retained union and validated capture contexts, actual caller range/order transport, family/gallery transactions, generated/theme layering, hierarchy editor routing and live-family dispatch together. The new hover binder is not yet wired into host lifecycle; actual resize plan invalidation, render/error/export handling and generation cleanup remain mandatory join checks. No packaged build, browser journey, financial screenshot comparison, fresh-session application persistence or deployment was performed or accepted by this review.

Verification status: VERIFIED for this frozen inactive helper/extraction task only. H3 and H4 remain open.
