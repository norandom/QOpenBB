# Company selector implementation plan

Status: owner approved tasks and implementation on 2026-10-30, after independent task-plan review. The bounded design and QueryParams size exception were approved earlier that day. This is an amendment to analyst-workspace, not approval of its umbrella backlog.

Read [requirements](company-selector-requirement.md) and [design](company-selector-design.md) before dispatch. Each executable task is a 1-3 hour work unit; elapsed delivery depends on review and runtime availability.

## Implementation tasks

- [x] 1. Establish the selector contract and executable size scope
  - Reuse the pinned Workspace c652b909627d7634241eee2ed13a561fbb4f177b and data API 28423762e8cc3faae978e770899834b41e7cde99 in clean owned checkouts. Confirm Node 24.22.1, installed native Vitest and existing browser prerequisites without adding a framework or changing dependencies.
  - Freeze the design's versioned selection, search, context, group and commit ports; implement strict decoding, eight eligible bindings, source identity and contradictory-listing rules. Metadata stays outside request parameters.
  - Extend the existing controller-owned complexity inventory for the eight production paths and explicit fork scope. Prove missing scope fails and run the existing checker. Do not activate a future candidate exception now; register its exact reviewed revision/measurements at task 5.
  - Completion: focused decoder/eligibility cases pass, the shared ports are importable, and measured new production code passes 400 physical/300 logical/50 per function. No new checker or provider endpoint is introduced.
  - _Boundary: Selection contract, controller foundation integration_
  - _Requirements: 1.2, 1.4, 1.5_

- [x] 2. (P) Deliver connected-source company search
  - Use the frozen ports and existing connected-source request helper; preserve the connector prefix and headers while targeting the owned FMP search route. Validate native results, dataset/provider, effective query/limit and mode-specific source endpoint; retain nullable fields, alternatives and actual retrieval timestamps.
  - Implement name/symbol thresholds, 250 ms debounce, limit 20, no automatic retries, private per-mount cache generation, cancellation and stale-response rejection. Authentication/source changes clear obsolete results without persisting secrets.
  - Completion: focused transport/hook cases distinguish empty, malformed, entitlement, rate-limit and network outcomes; late responses cannot replace current results or commit. New production files pass 400/300/50.
  - _Boundary: Search adapter and search hook_
  - _Depends: 1_
  - _Requirements: 1.1, 1.3, 1.4, 1.5_

- [x] 3. (P) Deliver exact group compatibility decisions
  - Implement the pure group guard against the frozen context contract, validating every member, effective immediate mode, exact Symbol binding, provider/source and competing bindings.
  - Reject mixed/incompatible groups, preview and detached contexts for live group writes. Preserve independent groups and expose an actionable blocked reason without changing membership.
  - Completion: focused pure cases cover compatible groups, source/provider changes, multiple bindings and preview/detached contexts; this module never writes a store. Production code passes 400/300/50.
  - _Boundary: Pure group safety_
  - _Depends: 1_
  - _Requirements: 1.3, 1.4, 1.5_

- [x] 4. Compose the linked fields and explicit selection lifecycle
- [x] 4.1 Preserve a valid company identity through explicit selection
  - Use the accepted search and safety ports to implement guarded local metadata and explicit commits. Re-read context immediately before writes; call the existing group writer once before the origin's compound local commit, without awaiting between guard and write.
  - Preserve valid metadata only for its source/provider/effective single symbol. Same-symbol choices can update metadata without refreshing financial data. Group-write failure leaves origin metadata unchanged; a later local failure produces unresolved state rather than claiming rollback.
  - Resolve a legacy or peer-updated single symbol through an exact-symbol search only when metadata is absent/invalid; zero or contradictory exact matches remain unresolved. Avoid repeat resolution for a still-valid saved record.
  - Completion: lifecycle tests cover explicit choice, metadata invalidation, unchanged symbols, exact-symbol resolution and partial failures; the hook accepts supplied existing operations without a second store. New production code passes 400/300/50.
  - _Boundary: Selection lifecycle_
  - _Depends: 2, 3_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [x] 4.2 Present the paired company controls without losing comparison editing
  - Compose adjacent labelled Company name/Symbol fields, portal suggestions, accessible keyboard/status behavior and responsive wrapping from installed primitives and the accepted lifecycle hook.
  - Retain the original Profile comparison editor and explicit replace-list action; typing or Tab does not choose a listing. Render loading, empty/error and name-unavailable states distinctly from the committed identity.
  - Keep the existing raw Symbol update callback, including its 1250 ms debounce and clearing/validation behavior, separate from resolved listing metadata. A listing choice cancels an obsolete raw draft; name searches never apply a raw symbol, and multiple-symbol typing cannot silently replace the list.
  - Completion: component tests cover keyboard choice/cancel, ambiguous options, null names, failure feedback and reachable multiple-symbol editing. The component passes 400/300/50 and does not write storage directly.
  - _Boundary: Selector presentation_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [x] 5. Integrate the selector into native widget execution and groups
- [x] 5.1 Supply reactive and freshly checked dashboard group context
  - Add reactive local/shared dashboard widget-and-group selection and a fresh imperative context read to the existing group hook; preserve its current writers and permissions. Verify membership changes while suggestions are open affect the next commit.
  - Expose the accepted context/operations to the lifecycle hook without creating a second group store. Preview, override and detached paths cannot call the live writer.
  - Completion: focused group-hook tests show current membership/source changes in both local and shared dashboards, preserve existing writes and reject preview/detached live writes. The modified hook passes 400/300/50.
  - _Boundary: Existing group context integration_
  - _Depends: 4.2_
  - _Requirements: 1.3, 1.4, 1.5_

- [x] 5.2 Integrate paired selection into the existing parameter host
  - Wire only the eight eligible immediate-query definitions through the dedicated auto-height below-navbar row. Retain GroupDropdown, comparison editing, Period/Limit and unrelated controls; manual-run variants and ineligible widgets use their original renderer.
  - Extend the existing local synchronization path for one functional parameters-plus-metadata update, including its unchanged-symbol metadata-only branch. Preserve local refs, stale/copilot/SSRM behavior; avoid duplicate grouped writes and financial metadata leakage.
  - Completion: integration regressions exercise changed and unchanged symbols, legacy dashboards, multiple values, manual-run fallback, shared reactivity and preview isolation. Only QueryParams may use the approved 1000 physical/390 logical/50 function ceiling; all other changed code passes 400/300/50. Bind exact candidate revision, measured source and expiring 2026-11-30 exception to the independently reviewed inventory before accepting this task.
  - _Boundary: Native widget host and group-store integration_
  - _Depends: 4.2, 5.1_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [x] 6. Join the frozen fork source and native catalog contracts
  - Pin the accepted Workspace candidate and retain the unchanged data API pin; reconcile native generated-definition provenance and tests against the eight eligibility bindings without broad regeneration or a new provider surface.
  - Run affected native unit/interaction tests, portable schema/catalog drift checks and the combined size gate with explicit base/head or changed-file scope. Verify retained storage metadata never appears in a financial request.
  - Completion: immutable source identities and scoped reports agree, all maintained selector paths have inventory ownership, and the actual candidate passes its approved ceilings. Existing unrelated working-tree changes remain excluded.
  - _Boundary: Controller source and contract integration_
  - _Depends: 5.2_
  - _Requirements: 1.2, 1.3, 1.4, 1.5_

- [ ] 7. Verify the analyst journey against real FMP data
- [x] 7.1 Extend the existing financial browser cases
  - Author the combined name-to-MSFT/symbol-to-AAPL journey and independent synthetic keyboard/failure case in the existing financial test. Preserve its Income regression, configuration and fixture isolation; add no harness.
  - Include clipped-viewport assertions against captured actual responses, compatible Profile/Income, independent comparison/FRED sentinels, save/fresh-login and retained-bind recreation checkpoints.
  - Completion: browser cases are discoverable through the existing runner and static checks pass; test discovery is recorded as discovery, not live acceptance. Test code is excluded from production caps; any maintained helper changes pass 400/300/50.
  - _Boundary: Browser case authoring_
  - _Depends: 6_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [ ] 7.2 Execute packaged real-data and persistence acceptance
  - Repair the runtime-discovered controlled-value comparison regression in the existing CompareTermsParam before rebuilding: add/remove must start from the latest external values when no local edit is pending, while rapid pending edits retain their local list. Cancel obsolete queued writes after a contradictory external change; own acknowledgements and equivalent values preserve the search draft. Preserve the open editor, 600 ms debounce and original controls. Cover external-value add/remove and rapid edits with the existing native test runner; map the modified control and enforce 400/300/50.
  - Build the packaged candidate with the existing Dagger workflow and start owned disposable Workspace/data runtimes using the current financial browser fixtures. Reuse the existing Playwright configuration, one worker, zero retries and actual isolated CDP diagnostics; serialize builds and respect the login budget.
  - Run one combined name-to-MSFT and symbol-to-AAPL journey with compatible Profile/Income, an independent comparison group and FRED sentinel. Assert displayed names/symbols and clipped-viewport financial values against actual responses, including period/currency provenance.
  - Save and fresh-login reopen; recreate the owned Workspace with its retained bind and reopen again. Run a separate labelled synthetic keyboard/failure/race case; retain the original Income regression. Capture one settled light/dark pair only.
  - Completion: actual responses, visible financial values, untouched sentinels and persisted selection pass; console/network failures are explained. Missing credentials or unavailable runtime are blocked/unverified, never a pass. Tests are excluded from production caps; any helper production changes remain 400/300/50.
  - _Boundary: Packaged browser acceptance_
  - _Depends: 7.1_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

## Ownership and execution

All paths below are Workspace-relative unless marked root. This table assigns ownership rather than adding executable tasks. Workers are not alone in the codebase: preserve other edits and stop if a shared contract must change.

| Task | Exclusive writable scope | Role and join |
| --- | --- | --- |
| 1 | `terminalpro/src/components/General/Table/NavBar/companySelection.contract.ts`; initial `terminalpro/tests/unit/company-selection.test.ts`; root inventory | Controller freezes ports and foundations; fresh Astra review before fan-out |
| 2 | Same NavBar directory: `companySearch.ts`, `useCompanySearch.ts`; `terminalpro/tests/unit/company-search.test.ts` | Sol; independent Sol review; accepted search output joins task 4 |
| 3 | Same NavBar directory: `companyGroupSafety.ts`; `terminalpro/tests/unit/company-group-safety.test.ts` | Sol concurrently with task 2; independent Sol review; accepted safety output joins task 4 |
| 4.1 | Same NavBar directory: `useCompanySelection.ts`; extend `terminalpro/tests/unit/company-selection.test.ts` | Sol; independent Astra lifecycle review; sequential after tasks 2/3 |
| 4.2 | Same NavBar directory: `CompanySymbolSelector.tsx`; `terminalpro/tests/unit/company-selector.test.tsx` | Sol; independent Sol UI review; sequential after task 4.1 |
| 5.1 | `terminalpro/src/components/Widgets/Helpers/useParamGroupBindings.ts`; relevant existing group tests | Sol; fresh Astra integration review; sequential after task 4.2 |
| 5.2 | `terminalpro/src/components/General/Table/NavBar/QueryParams.tsx`; extend existing `terminalpro/tests/unit/components/General/Table/NavBar/QueryParams.test.tsx`; coordinated array normalization in the existing group hook/test and raw recovery in the presenter/test; root candidate exception controlled by controller | One integration owner; fresh Astra review; sequential after task 5.1 |
| 6 | Root source lock/provenance, inventory and affected existing catalog contract checks | Controller; independent source/scope review |
| 7.1 | Root `tests/e2e/financial-workspace.spec.mts`, existing financial fixture/config only if necessary | Sol; independent Sol case review before candidate execution |
| 7.2 | Existing NavBar `CompareTermsParam.tsx` and its focused native unit file for the bounded controlled-value repair; controller-owned source pin/inventory and ignored runtime outputs; freeze source/tests before each actual browser run | Controller or one Sol verifier; independent Astra evidence review |

Tasks 2 and 3 explicitly skip the default sequential dependency on one another. Their distinct unit files specialize the design's proposed contract test grouping, using the same existing Vitest entry point. No additional harness is introduced. All other tasks are sequential. At most controller + two implementers + one reviewer are active; installs, builds, shared fixtures and commits are serialized. Each task retains implement, independent review, fresh verification and a selective commit.

## Closing gate and delivery record

The existing checker entry is `pipeline/.venv/bin/python -m tools.quality.complexity --check`, with current explicit fork scope and pinned Node 24.22.1 as documented in [complexity checks](../../../docs/complexity.md). Resolve exact candidate inputs before each worker handoff; do not reuse a historical head as current evidence. Native tests use the existing `vitest run tests/unit` entry; run focused files during work and the affected joined set once. Browser acceptance reuses `verification/financial-workspace.config.ts`.

Controller completion also updates README/docs checkboxes and `.kiro/breadth.toml` with actual tests/evidence, publishes one concise reviewed record and selected screenshots, and preserves raw/private output in ignored paths. No source or task checkbox is marked complete from planned checks. A meaningful accepted feature triggers both image builds/publication once through the existing milestone workflow; ordinary task pushes run checks without image rebuilding. These are existing delivery obligations, not extra implementation or deployment tasks.

The owner approved this bounded task plan and implementation on 2026-10-30. Neither design approval nor this plan activates a future inventory exception, approves a release, or completes the broader analyst dashboard.

## Implementation Notes

2026-10-30: packaged integration exposed a local comparison-preservation regression: the original editor displayed an externally updated symbol but appended to its stale initial internal list. Independent Astra review classified a controlled-value add/remove repair as necessary within the approved comparison-preservation scope. Keep one state owner and preserve the original editor flow; do not remount it after every value change or weaken the CSV browser check.
