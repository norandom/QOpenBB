# Review: retain this package as a concrete contract draft

The repaired package is an accurate, coherent draft for the next design decision. It is **not an implementation-ready design**. The Kiro architecture/executability gate remains NO-GO until the source-resolution, complete-editor, widget-transaction and settled-export contracts below are closed. No activation task or phase approval follows from this review.

Independent review date: 2026-10-17. Candidate Workspace: `ea02ec15956dee8d2c8a06825387a570757db12d`. Original reference: `38dffc33389aca0e4a87e0e88d42f7067aa220df`. Review used source inspection, local hash comparison and finite evidence comparison only. No browser, test suite, compilation, build, installation or network operation ran in this review. Separately produced captures or transaction research are outside this verdict and publication set.

## Scope and repaired findings

The review compared the [controller draft](../controller/draft.md), [appearance contract](../appearance/draft.md), [proposed types](../appearance/proposed-types.ts) and [session contract](../session/draft.md) against actual candidate types, mapper/style code, grid capture, theme selection, reducer helpers, widget updater and host/lifecycle. The application integration design, appearance/editor amendment, consuming-readiness note and Kiro design-review gate supplied the controlling boundaries. Two bounded repair passes were used.

The [spec navigation wrapper](../../../../.kiro/specs/openbb-self-service/chart-consuming-contract-draft.md) and its docs-index entry were also checked. They preserve the draft-only verdict, identify the actual updater defect and remaining gates, and make no new runtime, task or phase-approval claim. They are maintained documentation, not copied artifact outputs in the publication allowlist.

| Finding | Final disposition |
| --- | --- |
| New per-series markers overlapped inherited marker aliases and global `line.markers`; separate axis typography overlapped global/axis fallbacks. | Repaired in the proposed canonical shape and migration rules. Canonical validation rejects overlapping aliases even when equal or own undefined. Legacy three-argument callers retain their explicit compatibility branch in the same mapper. |
| Canonical style still required legacy `precision` despite mandatory trusted display policy. | Repaired in pass 2: omit/reject canonical `precision`; preserve it only for legacy callers. No invented formatting value is needed. |
| `buildRender` could not supply root bar-fill state without a hidden closure; source-key construction was unspecified. | Repaired: immutable `chartBarFillEnabled` explicitly invalidates rendering; ordinary selected numeric IDs supply `id = sourceKey = column.id`. Different source-key/transformed bindings require an explicit reviewed map. Enabled category-fill effects remain unverified. |
| One pending write until the next view could drop continuous edits or wait forever after rejection/no-op. | Withdrawn. Admission, ordered completion, rebase and cancellation are explicit blocked interfaces. No freeze or implementation claim remains for that scheduler. |
| A pure session callback was treated as sufficient for the actual existing widget updater. | Corrected to an explicit predecessor. `Widget.hooks.tsx:260` mutates the captured request from function to object; replay can reuse the first result. Persistence/context effects also occur inside state calculation. The existing owner must be adapted and verified; the draft does not claim this defect is fixed. |
| Evidence counts and mode identity overstated or conflated different records. | Repaired: 127 observed appearance pointer groups plus four supplemental gates; 290 editor capture rows plus five command rows; dark/light mode is distinct from selected stock/custom theme name. |

These dispositions repair the draft's claims and handoffs. They do not establish runtime correctness of proposed code.

## Source-backed conclusions

- Appearance uses the accepted composition/color helpers, a single canonical style and the existing Cartesian mapper. Invalid/unresolved appearance cannot yield partial host options. Selected theme, generated source options, mode, root bar-fill state and formatting are explicit inputs; effective reference output is an oracle, not a production input.
- `SessionResult<ChartRenderRequest>` can carry the supplied session stamp while the render request uses its render revision. Selection remains unstamped until the session captures it. Baseline options remain the reducer input; composed styles and ECharts options never become saved options.
- Accepted reducer code supports exactly the five stated events and keeps valid stacked tooltip edits unresolved. That union is an implementation fact, not permission to ship a five-control editor, hide original controls or alter original entry predicates.
- The current host discards lifecycle applied/deferred/stale/disposed results, and export returns only a data URL. The proposed additive receipt addresses revision application, not animation settlement. Remounting the existing host at address/generation changes prevents reset revision counters from colliding with its previous lifetime.
- The planned file ownership includes the existing widget owner and preserves one reducer, store and chart engine owner. Whole-file complexity caps remain 400 physical lines, 300 logical units and 50/function, with inventory/checker enforcement required for later production work.

## Mechanical evidence

The [verification record](verification.json) records checks performed during this review.

| Check | Result and limit |
| --- | --- |
| Appearance manifest | 131 rows: 127 observed pointer groups and four supplemental gates. All 908 case/pointer/raw-value observations compared equal to the prior reviewed leaf ledger. Four saved-composition and eight proxy cases remain separately identified. |
| Editor ledger | 295 total rows: 202 runtime capture rows, 88 inventory capture rows, five supported-command rows; 13 unresolved query groups. Repeated captures and paired controls do not establish 295 independent controls. |
| Appearance input hashes | All 30 explicit input files matched. |
| Session references | All 26 unique ledger reference files matched. The final session allowlist's 51 source/output hashes also matched. |
| Appearance output hashes | All six listed output hashes matched after the final repair. The output allowlist itself is additionally included in the publication set. |
| Locked ECharts targets | All 11 target-group hashes matched the installed local files; there are ten unique files because global and symbol groups share one declaration file. Package/lock inspection identifies ECharts 6.0.0. This establishes member availability, not projection equivalence or animation behavior. |

## Prerequisites before task readiness

1. Complete original source resolution for required appearance fields: selected-theme tokens/aliases, generated inputs, saved family/common/position conflicts, allocation/reorder and custom-family behavior. Finite known leaves do not form a complete renderable configuration by themselves.
2. Establish independent caption, asymmetric padding, axis/grid, legend overflow, line/marker/label and tooltip invocation effects. In particular, an available ECharts option is not evidence that AG geometry, alternate styles or pointer/keyboard behavior is reproduced.
3. Finish the original control/event/domain/predicate ledger and full docked props, family changes, Set Up/transform bindings and close/reopen/focus/scroll rules. Preserve original controls and return-to-table behavior; unknown units, source modes and other families remain product obligations.
4. Freeze an actual transaction completion port in the existing widget owner together with admission/rebase/ticket types. Verify replay against distinct previous widgets, continuous edits, no-op/rejection completion, generation cancellation, once-only effects and failure recovery before session write tasks.
5. Freeze a settled-frame export acknowledgement correlated with the current host lifetime, revision and resize/animation state. Applied revision equality alone cannot certify fresh final pixels. Preserve external export menu, filename and download ownership.
6. Obtain independent consuming-design review and human design approval, then generate bounded tasks with explicit joins and complexity checks. Application acceptance still requires matched original/candidate light/dark journeys, financial values, fresh export and real save/reopen/restart evidence.

The [safe publication allowlist](safe-publication-allowlist.json) lists only the new frozen controller, appearance, session and review outputs with SHA-256 digests. Referenced historical evidence and production source remain references; they are not duplicated into this package. It excludes separate capture/research lanes and private/runtime/environment data. Its own digest must be recorded by the parent publication manifest rather than through a circular self-hash. Links in this report target its final `artifacts/reviewed/consuming-contract-freeze/review/` location.
