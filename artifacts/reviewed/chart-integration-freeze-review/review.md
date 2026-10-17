# Chart integration design freeze review

## Decision

GO for human design review and a bounded task plan covering controller contract freeze, A1 source range/session state, and B1 financial display helpers. These lanes have source-proven responsibilities and can run independently after the explicit design and task approvals. NO-GO for activation or acceptance of the whole application journey: A2, unresolved mapper projections and full C retain precise runtime prerequisites; this does not require completing every chart family before an unreleased ordinary-journey milestone.

Reviewed 2026-10-17 against candidate Workspace HEAD `f23cb786a946a6a996deedbe87be9c7ca86b221e`, original pin `38dffc33389aca0e4a87e0e88d42f7067aa220df`, and application design SHA-256 `68d5f72b74435a8547ddcb2c83fa8822244d02ce9e9cf58d7f75fdfc98bd4fe2`. Review is source inspection, not executed application verification. The latest completed editor probe remains exit 1 before edits; a retry in progress provides no accepted evidence yet.

## Critical issues

1. **One capture interface has two incompatible definitions.** Frozen session contracts specify `CaptureDisplayedChart -> SessionResult<ResolvedSnapshotInput>` with `ready/stamp/value`; Displayed-grid capture specifies `GridCaptureResult` with `captured/input` and no stamp. The controller must retain one canonical signature and reference it throughout before creating shared types or dispatching A2. This is a local freeze correction, not an AG research dependency. Requirements 4.8/4.9; evidence: application design, Frozen session and state contracts / Displayed-grid capture.

2. **The remaining library seams cannot be implemented as guessed controls or data transformations.** A2 still needs the exact ordinary fixture category, selected range and raw/valueGetter results. Full C needs per-field conditional visibility, value domain, event path and rendered effect; mapper joins need formatter invocation and effective nested leaves. Freeze each consuming task's finite ledger before dispatch. Missing controls stay unfinished defects in an unreleased candidate; they cannot be hidden, disabled or accepted as unavailable. Requirements 4.8/4.9; evidence: control ledger, range contract and completed failed editor-runtime report. This blocks affected joins, not A1/B1.

## Strengths

The proposed address/stamp ownership, exact four column patches and reuse of the existing option baseline/reducer match current source. The design preserves addressed storage, inactive-family options, top-level theme stripping and host-only disposal, with explicit stale-render/export handling.

The file allocation separates pure state/range and formatting work from React activation. Whole-file 400 physical / 300 logical / 50 per-function caps, manifest-based checks and a final shared-module audit are required. Existing checker foundations are reused rather than promised again.

## Executable handoff boundaries

- Controller owns `application/types.ts`, inventory and breadth. Resolve issue 1; define A1 callable inputs/outputs from the documented precedence and existing reducer types. Keep original storage keys unchanged. Record the actual working-tree manifest, not HEAD alone.
- A1 owns `chartRange.ts`, `sessionState.ts` and corresponding units. Assert stored/configured/generated range precedence and intersection, stale address/generation/revision rejection without writes, current-storage merging, inactive-family preservation and current reducer semantics. No AG interpretation or activation.
- B1 owns `financialFormatting.ts` and corresponding units. Assert threshold boundaries, zero precision, fiscal/date distinctions and integrated-versus-detached scaling separation using source helpers. No claim about AG invocation. A1/B1 may run concurrently after contracts and approvals.
- B2 may later implement only reviewed finite stock/custom leaves. Freeze typed AppearanceInput/Result and per-leaf precedence before that task; prose placeholders are not a worker API. No extrapolated custom-family inheritance.
- Before D, freeze ChartSessionInput/ChartSession and editor props/events; A2/B1/B2 and required mapper projections must be reviewed. D exclusively reconnects callers and removes chart guards. A1/B1 must actually be consumed at this join.
- Real-app acceptance requires the original shell/editor, financial observations, theme/export, table restoration and explicit save/reopen/restart with SQLite. A smaller unreleased milestone may exercise known controls; it cannot certify full C or renderer/release parity.

Before task approval, replace superseded Perspective dependencies and acceptance wording in tasks 3.8, 4.3, 4.5 and the top-level lane table. Preserve the Anthropic-before-Excel dependency. No spec approval state was changed by this review.

## Inspection scope

Read the project AGENTS guidance; workspace-experience, delegation, complexity, documentation, testing and CI steering; kiro-validate-design and its review rules; requirements/spec metadata; application, range and formatting contracts; current snapshot/legacy/option-state types, integrated reducer and host lifecycle. Core product/tech/structure steering files are absent. No browser, heavy build, test, secrets or production edits were used. This review artifact is documentation and outside production size caps.

## Correction disposition and current scoped verdict

Verified revised design SHA-256 `ba3b27321e624ecb2fff7cca0e6ae3cc917f7cdd28e0f37579e30691a45f9d69` on 2026-10-17. The Displayed-grid capture paragraph now explicitly implements `CaptureDisplayedChart` and its `SessionResult<ResolvedSnapshotInput>` envelope: successful output is `ready` with `stamp` and `value`; waiting/stale/diagnostics use that same envelope. Critical issue 1 is closed. The historical review above records the earlier hash and is not the current defect list.

**Current verdict: GO for human design review and task generation of the controller contract-freeze, A1 and B1 boundary.** These concrete source-safe lanes can execute after explicit design and task approval, with the ownership and acceptance bullets above. No remaining architectural blocker prevents that bounded task plan. B2 may be planned against its finite reviewed leaves with its exact typed input/output freeze prerequisite.

**NO-GO remains for dispatch/acceptance of A2, unresolved mapper projections, full C and D activation until their named contracts are frozen.** The runtime retry is still in progress; finite projection debugging does not establish category selection, editor events or formatter invocation. The eventual real-app join remains necessary to accept the application milestone. Neither this scoped GO nor A1/B1 completion certifies renderer/release parity or changes approval metadata.
