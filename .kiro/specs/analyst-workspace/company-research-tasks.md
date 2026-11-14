# Company Research implementation tasks

Status: task plan for owner review, 2026-11-14. Requirements and design are approved. Task execution and implementation are not yet approved. This is the bounded Company Research increment, not completion of the analyst-workspace umbrella or full IA-B readiness.

The [design](company-research-design.md) owns contracts and file responsibilities; [requirements](company-research-requirements.md) own acceptance. Deliver a useful App with linked company statements and price context, independent editable peers, inspectable evidence and saved configuration. No financial modeling service or house calculations are introduced.

## Execution contract

Each executable item is a 1-3 hour work unit, not a guaranteed elapsed-time estimate. If a unit exceeds its responsibility boundary, split it before dispatch. Use `gpt-6.1-sol` implementers and routine reviewers; use `gpt-6-astra` for financial/integration review. Every task follows implement, independent review, fresh focused verification, selective commit. Controller owns joins, shared artifacts and pushes. Do not run implementation from this unapproved plan.

All new/modified production files must pass 400 physical lines/file, 300 logical units/file and 50/function. Generated artifacts, tests and documentation are excluded with recorded generators/reasons; generator logic is not excluded. Task 1 extends the existing executable inventory/checker; it does not rebuild the framework. Existing oversized import/state/schema/QueryParams/data-processor files stay unchanged. No size exception is granted. Export serialization and table-query extraction must reduce complete touched files to the caps, not just move an oversized function elsewhere.

Run from the relevant native Windows repository; use Podman Compose for owned runtime and the pinned Dagger path for image builds only. Reuse pinned uv/uvx and pnpm/Safe Chain, Node 24.22.1 or the separately accepted newer pin. Keep temporary outputs under `D:/BuildArtifacts/QOpenBB/company-research`, secrets outside published evidence, helpers hidden and browsers isolated. Never restart WSL or unrelated containers as a prerequisite.

Use the existing `python -m tools.quality.complexity --check` entry point with explicit `--repository-root`, `--changes` manifests for both forks and `--output` under the external artifact directory, as documented in [complexity checks](../../../docs/complexity.md). Task 1 resolves the actual interpreter, pinned tool versions, inventory base, snapshot identities and complete invocation; each later task reuses that receipt with its updated changed-file manifest. Do not reuse historical heads or pass empty manifests for changed code.

## Ownership and parallel schedule

After tasks 1 and 2 freeze shared contracts, core items may skip ahead only according to the explicit dependencies below. This project delegation schedule overrides generic sequential ordering. At most two implementers run alongside the controller and one reviewer. Each worker owns only the listed production paths and task-specific tests; it may read other lanes but must not revert their changes. Shared test files, inventories, source locks, generated outputs and commits are controller-serialized.

Workspace paths are relative to `terminalpro/` in the owned fork. A slash-separated module list is shorthand for separate files in that directory.

| Tasks | Exclusive production ownership |
| --- | --- |
| 1, 2 | Controller: clean source snapshots, complexity inventories; `src/lib/companyResearch/config.ts`, `financialEnvelope.ts`, `eligibility.ts` and frozen contract definitions |
| 3.1 | Root catalog lane: `pipeline/qopenbb_ci/catalog_research.py`, `catalog.py`; controller integrates `catalog_cli.py` hash registration and generated contracts |
| 3.2 | Workspace query lane: `src/components/General/Table/useTableData.ts`, `tableQueryOptions.ts`, `AgGridTable.tsx`; `src/lib/companyResearch/useEvidenceLifecycle.ts` |
| 3.3 | Workspace identity lane: `src/lib/companyResearch/selectionReconciliation.ts`; `src/components/General/Table/NavBar/useCompanySelection.ts` |
| 3.4 | Workspace template lane: `src/lib/utils/exportTemplate.ts`, `researchTemplateState.ts`; `src/components/General/ExportTemplatePopup.tsx` |
| 3.5 | Workspace peers lane: `src/components/Widgets/CompanyResearch/PeerEditor.tsx` |
| 4.1 | Inspector lane: `src/components/Widgets/CompanyResearch/ObservationInspector.tsx`, `observationPresentation.ts`; table mount edit serialized after 3.2 |
| 4.2 | Peer observation lane: `src/components/Widgets/CompanyResearch/usePeerObservations.ts`, `PeerObservations.tsx` |
| 4.3 | Controller join: `src/components/Widgets/CompanyResearch/PeerResearch.tsx`, `src/components/Widgets/index.ts`, catalog artifacts and source locks |
| 5.1, 5.2, 5.3 | Controller acceptance: existing browser/contract runner files, reviewed evidence, breadth, README/docs and release inputs |

Suggested dispatch: 3.1 + 3.2, then 3.3 + 3.4, then 3.5 + 4.1; 4.2 may overlap another disjoint ready task after its dependencies. Task 4.3 waits for all feature lanes. There is only one heavy build/suite at a time; shared fixture mutations and acceptance runs are serial. Unit checks remain scoped, xdist at most two workers and browser workers one for the stateful journey. No new harness or exhaustive per-commit reruns.

## Tasks

- [ ] 1. Establish an isolated, measurable implementation baseline
  - Resolve accepted root/Workspace/API revisions and existing native tools; create isolated checkouts where unrelated dirty work would overlap. Preserve current unrelated catalog generator and inventory changes rather than incorporating or reverting them.
  - Extend the existing inventory for the design's maintained paths and explicit fork manifests; measure complete integration-file baselines. Freeze a runnable quality invocation and focused test commands from the installed toolchain.
  - Confirm the existing Compose/Playwright runner can address an owned local project and retained data directory. Record setup gaps as concrete prerequisites, not a request to rebuild the infrastructure.
  - Done: exact source/tool identities and writable ownership are recorded, the existing checker accepts the explicit scope, and no lane depends on unrelated unaccepted edits.
  - Inventory/config files satisfy the 400-line cap; no new checker is planned. Baseline measurements are not feature acceptance.
  - _Boundary: Controller foundation_
  - _Requirements: 6.1, 6.4_

- [ ] 2. Freeze research configuration and financial evidence contracts
  - Implement versioned configuration validation, the adapter to existing source-qualified company identity, supported financial-envelope narrowing and evidence-only status/reason contracts.
  - Retain nullable facts, original row/source ordinals, duplicate/signed observations and separate acquisition/observation dates. Unknown metadata versions fail to explicit unknown evidence, not fabricated fields.
  - Freeze the peer renderer ID, its declaration shape, query context/lifecycle interface, safe export projection contract and eligibility interface before workers start. These interfaces have one owner and no duplicate persistent state.
  - Done: focused contract cases cover config limits, unknown versions, missing/zero/negative/duplicate evidence and no valid-comparable state; downstream lanes can consume stable types without editing this ownership scope.
  - All maintained contract/parser/status files pass 400/300/50 and independent financial review; tests are excluded from production size caps.
  - _Boundary: Research contracts_
  - _Depends: 1_
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 4.3, 4.4, 4.5, 5.6, 6.1_

- [ ] 3. Build independent research capabilities
- [ ] 3.1 (P) Generate the curated research App
  - Compose profile, Income/Balance/Cash, price context and the frozen peer widget declaration using accepted catalog IDs and the existing grid layout.
  - Declare only eligible primary tables in the Symbol group; link only statements by period. Price dates remain independent and peers/macros stay outside the primary group. Use the explicit Apple example, no silent fallback.
  - Done: focused catalog checks validate layout, declaration and group membership; the App is emitted directly without losing storage through provider-App adaptation. Final runtime mounting waits for 4.3.
  - Generator files pass 400/300/50. Generated catalog files are excluded with generator hashes; controller alone updates hash registration and generated artifacts.
  - _Boundary: Catalog generation_
  - _Depends: 2_
  - _Requirements: 1.1, 1.2, 2.1, 2.3, 2.4, 2.5, 6.1_

- [ ] 3.2 (P) Preserve table evidence through refresh and identity changes
  - Cohesively extract table query/options from the existing component, preserving rows/columns and using the existing authenticated query adapter.
  - Expose original envelope and context-bound lifecycle to consumers. Disable empty/unresolved company queries; discard previous-context views and ignore late responses.
  - Retain only same-context successful data on failed refresh, visibly separating acquisition/observation dates and failed-attempt time; initial failure remains empty with its inline state.
  - Done: focused lifecycle cases prove clear/change race isolation, same-context stale retention and no stale data attributed to a new company. Existing table row rendering remains unchanged.
  - Entire extracted and touched files pass 400/300/50; API adapter, oversized processors and QueryParams remain unchanged.
  - _Boundary: Table query and evidence lifecycle_
  - _Depends: 2_
  - _Requirements: 1.3, 2.2, 3.3, 5.3, 5.4, 6.1_

- [ ] 3.3 (P) Preserve unresolved saved company identities
  - Add the narrow selector reconciliation guard using saved source identity and current source, without a second persisted flag.
  - Prevent automatic same-symbol replacement across sources; retain the unresolved saved name/symbol and reason until explicit current-source reselection. Preserve normal same-source group changes and initial defaults without saved metadata.
  - Done: focused selector checks cover foreign-source/ambiguous/malformed saved identity, normal group changes, absent initial metadata and explicit recovery. The later persistence journey verifies unresolved save/reopen.
  - Hook and helper pass 400/300/50; use existing error presentation and leave QueryParams unchanged.
  - _Boundary: Company identity reconciliation_
  - _Depends: 2_
  - _Requirements: 2.1, 2.2, 5.1, 5.6, 6.1_

- [ ] 3.4 (P) Preserve research choices in safe template export
  - Extract pure export serialization into cohesive capped functions, retaining existing template behavior and group references.
  - Add only validated company selection and research configuration to the allowlist. Exclude provider payloads, credentials and session/request secrets; refuse credential-dependent identities rather than leaking URL components.
  - Reuse the existing import storage merge unchanged and the frozen consumer decoders. Invalid/unknown research versions remain unresolved and retain their original imported configuration.
  - Done: focused serialization roundtrips retain identity, period, price dates, peer order/rationales, layout/groups and unrelated existing allowlisted fields; negative cases demonstrate secret exclusion.
  - Popup and extracted serializers pass 400/300/50 as whole files; existing oversized import/state/schema files remain unchanged.
  - _Boundary: Template serialization_
  - _Depends: 2_
  - _Requirements: 5.1, 5.5, 5.6, 6.1_

- [ ] 3.5 (P) Edit an independent candidate peer set
  - Reuse company search and existing themed UI primitives for add/remove/reorder and rationale editing. Display readable names, symbols and available listing/exchange facts.
  - Keep the peer array in its single widget-owned configuration, independent of primary selection. Candidate suggestions are not automatic membership or financial validation.
  - Done: component checks preserve peer identity/order/rationale through edits and reject invalid/oversized configuration without silently discarding input. Search absence or entitlement failure leaves existing choices intact.
  - Editor passes 400/300/50; it consumes frozen contracts and does not modify other lanes' state or selectors.
  - _Boundary: Peer editor_
  - _Depends: 2_
  - _Requirements: 1.2, 1.3, 2.5, 4.1, 4.6_

- [ ] 4. Integrate the research experience
- [ ] 4.1 (P) Make original financial observations inspectable
  - Present the original-observation selector and financial metadata using existing frame actions/theme controls, independent of grid transpose/grouping.
  - Show source, definition, unit/scale/currency, origin, actual dates, fiscal labels, coverage evidence and explicit unknowns. Keep duplicate rows individually selectable; do not infer period duration or historical availability.
  - Done: inspector checks match original row ordinals and display unknown/provider-calculation limitations; mount through the table evidence seam without per-cell requests. Keyboard navigation and existing controls remain usable.
  - Inspector/helpers and the final table integration pass 400/300/50; controller serializes the table mount after 3.2.
  - _Boundary: Observation inspector integration_
  - _Depends: 2, 3.2_
  - _Requirements: 1.2, 3.1, 3.2, 3.3, 3.4, 3.5, 6.1_

- [ ] 4.2 (P) Show provider peer observations with explicit limits
  - Request periodic metrics/ratios separately per selected listing, `ttm=exclude`, using the existing adapter and no more than two concurrent requests. No automatic polling; count bounded retries in request receipts.
  - Expose dataset/field and original-observation choices with dates, units, currency and provider origin. Keep duplicate rows available and each failed peer/dataset inline.
  - Use the frozen evidence-only statuses; unknown denominators never become validated, explicit zero/negative evidence is not meaningful, and apparent matches remain unverified for aggregation. Retain generic controls with the persistent valuation limitation notice.
  - Done: focused orchestration checks demonstrate cancellation/removal/unmount, partial failure, refresh and no cross-context reuse; display has no financial formulas, inferred joins or validated ranking.
  - Query/view files pass 400/300/50; shared evidence/eligibility contracts remain frozen.
  - _Boundary: Peer observations_
  - _Depends: 2, 3.2_
  - _Requirements: 1.3, 3.4, 3.5, 4.2, 4.3, 4.4, 4.5, 4.6, 5.3, 5.4, 6.1_

- [ ] 4.3 Join the App, peer widget and saved state
  - Compose the peer editor and observations in the existing widget frame; register the frozen renderer and bind validated configuration to existing widget persistence.
  - Join catalog generation and template serialization, verifying group references after import and independent statement/price/peer parameters. Reconcile only reviewed source changes into exact fork/root revisions.
  - Done: installed catalog opens the complete App, all sections are reachable and no section failure blanks unrelated widgets. Saved configuration carries choices, not provider payloads or a frozen valuation snapshot.
  - Run affected contract/type checks and final shared-module size audit; all maintained join files pass 400/300/50. Generated contracts are regenerated and hashed, not hand-edited.
  - _Boundary: Explicit Workspace/catalog integration_
  - _Depends: 3.1, 3.3, 3.4, 3.5, 4.1, 4.2_
  - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.3, 2.4, 2.5, 4.1, 5.1, 5.5, 5.6, 6.1_

- [ ] 5. Verify and deliver the bounded milestone
- [ ] 5.1 Verify the packaged analyst journey with real FMP observations
  - Build the accepted candidate through existing Dagger definitions and run it in owned native Compose with the existing financial browser runner. Tests/publication remain outside Dagger.
  - Use a primary company and two peers; check displayed values against source evidence, readable identity changes, annual/quarter changes, independent price dates, peer edits, inspector and refresh behavior.
  - Cover missing/incompatible evidence and failure recovery with clearly labelled deterministic cases where live data cannot safely reproduce the condition. Inspect owned browser console/network diagnostics; preserve current theme and controls.
  - Done: focused browser/contract evidence and independent financial review pass against exact source/image identities. Record actual request counts, skipped cases and any unresolved issue; no automatic whole-suite reruns.
  - Test/evidence files are excluded from production caps; any implementation repair returns to its owning task and 400/300/50 checks before acceptance.
  - _Boundary: Packaged browser acceptance_
  - _Depends: 4.3_
  - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4, 3.5, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 5.3, 5.4, 6.1, 6.2_

- [ ] 5.2 Verify retained research configuration and template portability
  - Extend the same existing journey to fresh authenticated reopen, template export/import and container recreation retaining the owned data directory.
  - Verify primary identity, period, price window, peer order/rationale, layout and group references. Test unresolved foreign-source identity through save/reopen and explicit recovery, without silently substituting a company.
  - Done: the restored App retains all analyst choices, exports contain no secrets or provider payloads, and evidence explicitly distinguishes retained-data recreation from backup/restore or owner-server deployment.
  - Test/evidence-only work is outside production caps; fixes return to their code owners and the full applicable gates. Reuse the same candidate image unless source changes require rebuilding.
  - _Boundary: Persistence acceptance_
  - _Depends: 5.1_
  - _Requirements: 5.1, 5.2, 5.5, 5.6, 6.2, 6.3_

- [ ] 5.3 Verify milestone publication and close evidence mappings
  - Run the existing release pipeline once for the accepted feature, including its Dagger image build and portable publication steps. Verify immutable image/manifest/source identities and prebuilt pullability; do not rebuild for every task commit.
  - Synchronize only completed sanitized evidence into the reviewed artifact mirror, validate hashes and obtain independent acceptance of the publication set. Update actual test paths/evidence and completed checkboxes in breadth, README and docs.
  - Done: a tagged milestone and its image receipts identify the accepted feature and limitations. Planned/skipped checks stay distinct; full IA-B and owner-server acceptance remain open unless separately evidenced.
  - Release evidence/generated-only work is excluded from production caps; any pipeline code change is a separately reviewed capped repair, not implicit scope expansion. This release verification is required by project delivery policy and criterion 6.4; it does not deploy to the owner's server.
  - _Boundary: Controller release verification_
  - _Depends: 5.2_
  - _Requirements: 6.4_

## Review and approval boundary

Thirteen executable tasks cover all 29 criteria. Existing unit/contract checks are attached to their owning tasks; the two browser acceptance tasks share the existing runner and candidate. No optional tests replace required acceptance. A dependency or frozen-contract change stops affected lanes for controller reconciliation.

Task approval authorizes this bounded implementation workflow only. House modeling, broader IA-B readiness, new providers, AI/Excel and server deployment are not included.
