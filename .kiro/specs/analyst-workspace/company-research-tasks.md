# Company Research implementation tasks

Status: owner-approved task plan and implementation, 2026-11-14 (amended 2026-11-14 for financial validation seams, spec-trap guards, installed-library reuse and extensible accounting-optimization provenance). Requirements and design are approved. Owner approved execution and implementation with the project subagent model on 2026-11-14. This is the bounded Company Research increment, not completion of the analyst-workspace umbrella or full IA-B readiness.

The [design](company-research-design.md) owns contracts and file responsibilities; [requirements](company-research-requirements.md) own acceptance. Deliver a useful App with linked company statements and price context, independent editable peers, inspectable evidence and saved configuration. No financial modeling service or house calculations are introduced, but evidence contracts and the observation inspector must preserve raw accounting-optimization inputs (such as stock-based compensation, operating/free cash flow, reported/provider EBITDA, share counts and buybacks) and transformation/limitation metadata as an extensible seam for downstream house-modeling lenses.

## Execution contract

Each executable item is a 1-3 hour work unit, not a guaranteed elapsed-time estimate. If a unit exceeds its responsibility boundary, split it before dispatch. Use `gpt-6.1-sol` implementers and routine reviewers; use `gpt-6-astra` for financial/integration review. Every task follows implement, independent review, fresh focused verification, selective commit. Controller owns joins, shared artifacts and pushes. Execute the approved dependencies and retain independent review before accepting each task.

All new/modified production files must pass 400 physical lines/file, 300 logical units/file and 50/function. Generated artifacts, tests and documentation are excluded with recorded generators/reasons; generator logic is not excluded. Task 1 extends the existing executable inventory/checker; it does not rebuild the framework. Existing oversized import/state/schema/QueryParams/data-processor files stay unchanged. No size exception is granted. Export serialization and table-query extraction must reduce complete touched files to the caps, not just move an oversized function elsewhere.

Run from the relevant native Windows repository; use Podman Compose for owned runtime and the pinned Dagger path for image builds only. Reuse pinned uv/uvx and pnpm/Safe Chain, Node 24.22.1 or the separately accepted newer pin. Keep temporary outputs under `D:/BuildArtifacts/QOpenBB/company-research`, secrets outside published evidence, helpers hidden and browsers isolated. Never restart WSL or unrelated containers as a prerequisite.

Use the existing `python -m tools.quality.complexity --check` entry point with explicit `--repository-root`, `--changes` manifests for both forks and `--output` under the external artifact directory, as documented in [complexity checks](../../../docs/complexity.md). Task 1 resolves the actual interpreter, pinned tool versions, inventory base, snapshot identities and complete invocation; each later task reuses that receipt with its updated changed-file manifest. Do not reuse historical heads or pass empty manifests for changed code.

## Ownership and parallel schedule

After tasks 1 and 2 freeze shared contracts, core items may skip ahead only according to the explicit dependencies below. This project delegation schedule overrides generic sequential ordering. At most two implementers run alongside the controller and one reviewer. Each worker owns only the listed production paths and task-specific tests; it may read other lanes but must not revert their changes. Shared test files, inventories, source locks, generated outputs and commits are controller-serialized.

Workspace paths are relative to `terminalpro/` in the owned fork. A slash-separated module list is shorthand for separate files in that directory.

| Tasks | Exclusive production ownership |
| --- | --- |
| 1, 2 | Controller: clean source snapshots, complexity inventories; `src/lib/companyResearch/config.ts`, `financialEnvelope.ts`, `eligibility.ts`, pure `selectionReconciliation.ts` classifier/request predicate and frozen contract definitions |
| 3.1 | Root catalog lane: `pipeline/qopenbb_ci/catalog_research.py`, `catalog.py`; controller integrates `catalog_cli.py` hash registration and generated contracts |
| 3.2 | Workspace query lane: `src/components/General/Table/useTableData.ts`, `tableQueryOptions.ts`, `AgGridTable.tsx`; `src/lib/companyResearch/useEvidenceLifecycle.ts` |
| 3.3 | Workspace identity lane: `src/components/General/Table/NavBar/useCompanySelection.ts`; consumes frozen controller-owned `selectionReconciliation.ts` |
| 3.4 | Workspace template lane: `src/lib/utils/exportTemplate.ts`, `researchTemplateState.ts`; `src/components/General/ExportTemplatePopup.tsx` |
| 3.5 | Workspace peers lane: `src/components/Widgets/CompanyResearch/PeerEditor.tsx` |
| 4.1 | Inspector lane: `src/components/Widgets/CompanyResearch/ObservationInspector.tsx`, `observationPresentation.ts`; table mount edit serialized after 3.2 |
| 4.2 | Peer observation lane: `src/components/Widgets/CompanyResearch/usePeerObservations.ts`, `PeerObservations.tsx` |
| 4.3 | Controller join: `src/components/Widgets/CompanyResearch/PeerResearch.tsx`, `src/components/Widgets/index.ts`, catalog artifacts and source locks |
| 5.1, 5.2, 5.3 | Controller acceptance: existing browser/contract runner files, reviewed evidence, breadth, README/docs and release inputs |

Suggested dispatch: 3.1 + 3.2, then 3.3 + 3.4, then 3.5 + 4.1; 4.2 may overlap another disjoint ready task after its dependencies. Task 4.3 waits for all feature lanes. There is only one heavy build/suite at a time; shared fixture mutations and acceptance runs are serial. Unit checks remain scoped, xdist at most two workers and browser workers one for the stateful journey. No new harness or exhaustive per-commit reruns.

## Tasks

- [x] 1. Establish an isolated, measurable implementation baseline
  - Explicitly resolve the accepted Workspace revision (`e1a12c3a031a23598f41166a0f91b8fb24ac2387` at `D:/BuildArtifacts/QOpenBB/native-join/workspace`) and accepted Data API revision (`a965f70c164fe477ce9c99654b9be48e2f1bc9fd` at `D:/BuildArtifacts/QOpenBB/statement-period-provenance/data-api`) rather than running against the lagging `vendor/workspace` (`c652b90`) or `vendor/data-api` (`2e60c0a7`) checkouts; create isolated checkouts/worktrees where unrelated dirty work (`pipeline/qopenbb_ci/catalog_cli.py`, `catalog_renderers.py`, `.kiro/complexity-budgets.json`, `.kiro/complexity/workspace.json` and untracked Workspace test files) would overlap. Preserve current unrelated catalog generator and inventory changes rather than incorporating or reverting them.
  - Extend the existing inventory for the design's maintained paths and explicit fork manifests; measure complete physical, logical (`project-syntax-units-v1`) and per-function baselines for all touched integration files (`AgGridTable.tsx`, `useCompanySelection.ts`, `ExportTemplatePopup.tsx`, `src/components/Widgets/index.ts`, `catalog.py`, `catalog_cli.py`) before fan-out. Freeze a runnable quality invocation and focused test commands from the installed toolchain.
  - Confirm the existing Compose/Playwright runner can address an owned local project and retained data directory. Record setup gaps as concrete prerequisites, not a request to rebuild the infrastructure.
  - Done: exact source/tool identities and writable ownership are recorded, the existing checker accepts the explicit scope, and no lane depends on unrelated unaccepted edits.
  - Inventory/config files satisfy the 400-line cap; no new checker is planned. Baseline measurements are not feature acceptance.
  - _Boundary: Controller foundation_
  - _Requirements: 6.1, 6.4_

- [x] 2. Freeze research configuration and financial evidence contracts
  - Execution split (2026-11-14 sizing check): subunit 2a owns `config.ts`, `selectionReconciliation.ts` and identity/config tests; subunit 2b owns `financialEnvelope.ts`, `eligibility.ts` and financial-evidence tests. These disjoint responsibilities join at task 2 acceptance; no downstream lane starts until both pass independent review and the shared exports are frozen. Controller owns inventory and shared interface reconciliation.
  - Implement versioned configuration validation, the adapter to existing source-qualified company identity, supported financial-envelope narrowing and evidence-only status/reason contracts. Reuse installed `zod` (`^4.4.3`) and `dayjs` (`^1.11.10`) in `config.ts` and `financialEnvelope.ts` rather than hand-rolling verbose recursive type guards that consume the 300-logical and 50-per-function budgets.
  - Retain nullable facts, original row/source ordinals, duplicate/signed observations and separate acquisition (`retrieved_at`), observation (`observation_date_field`), valuation (`valuation_date_field`) and publication (`publication_date_field`) dates. Resolve row-level `currency_field` against the exact `originalRows[row_index]` datum rather than assuming table-wide or Profile trading currency; flag currency conflicts as `incompatible` only for a stated comparison requiring matching currencies. Currency differences alone do not invalidate a dimensionless provider ratio. Unknown metadata versions fail to explicit unknown evidence, not fabricated fields.
  - Define explicit denominator and EV-bridge evidence rules in `eligibility.ts`: when a provider endpoint (`metrics`/`ratios`) returns a numeric multiple without raw denominator evidence or, for an enterprise-value measure, applicable dated EV-bridge evidence (`share_count`, `debt`, `cash`, `market_date` as relevant), keep it `unverified` and name the missing evidence; reserve `not_meaningful` for explicitly evidenced zero or negative denominators.
  - Preserve an extensible accounting-optimization and trend-evidence seam in `financialEnvelope.ts` and `eligibility.ts`: keep field/provenance structures open to any returned statement or metric field (including `stock_based_compensation`, `operating_cash_flow`, `free_cash_flow`, `ebitda`, `common_stock_repurchased` and basic/diluted share counts) alongside `financial_basis`, `transformations` and `limitations`, and disclose SBC treatment only when supplied definitions or reconciliations establish it. Never infer an SBC add-back from an EBITDA/OCF/FCF field name; unavailable treatment stays unknown. Preserve supplied measures without economic adjustments.
  - Freeze the peer renderer ID, its declaration shape (aligned with `NonAgGridComponents` in `src/components/Widgets/index.ts`), query context/lifecycle interface, shared request-eligibility predicate, safe export projection contract and eligibility interface before workers start. Implement and test the pure shared identity classifier/request predicate in controller-owned `selectionReconciliation.ts` before fan-out, covering raw malformed/unknown saved metadata, source/effective-symbol reconciliation, absent metadata and deliberate linked-company changes. Tasks 3.2 and 3.3 consume this frozen implementation. Shared-helper changes return to the controller, pause dependent lanes and require renewed focused verification. These interfaces have one owner and no duplicate persistent state.
  - Done: focused contract cases cover config limits, unknown versions, missing/zero/negative/duplicate evidence and no valid-comparable state; include evidenced SBC add-back, evidenced retained expense and unknown treatment; stated monetary currency conflicts versus dimensionless observations with different reporting currencies; and EV-based versus equity-based missing-evidence reasons. Unknown measure definitions retain unknown applicability rather than an inferred classification. Downstream lanes consume stable types without editing this ownership scope.
  - All maintained contract/parser/status files pass 400/300/50 and independent financial review; tests are excluded from production size caps.
  - _Boundary: Research contracts_
  - _Depends: 1_
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 4.3, 4.4, 4.5, 5.6, 6.1_

- [x] 3. Build independent research capabilities
- [x] 3.1 (P) Generate the curated research App
  - Compose profile, Income/Balance/Cash, price context and the frozen peer widget declaration using accepted catalog IDs and the existing grid layout. Ensure the peer widget declaration's `widgetId` and `type` match the frozen renderer registration so `Widget.tsx` mounts the peer component directly rather than falling back to `AgGridTable` via `widget?.endpoint`.
  - Declare only eligible primary tables in the Symbol group; link only statements by period so raw accounting-optimization inputs across Income (`ebitda`, weighted-average shares), Balance (cash, debt, equity) and Cash Flow (`stock_based_compensation`, `operating_cash_flow`, `free_cash_flow`, `common_stock_repurchased`) align by period selection. Price dates remain independent and peers/macros stay outside the primary group. Use the explicit Apple example, no silent fallback.
  - Done: focused catalog checks validate layout, declaration and group membership; the App is emitted directly without losing storage through provider-App adaptation. Final runtime mounting waits for 4.3.
  - Generator files pass 400/300/50. Generated catalog files are excluded with generator hashes; controller alone updates hash registration and generated artifacts.
  - _Boundary: Catalog generation_
  - _Depends: 2_
  - _Requirements: 1.1, 1.2, 2.1, 2.3, 2.4, 2.5, 6.1_

- [x] 3.2 (P) Preserve table evidence through refresh and identity changes
  - Cohesively extract table query/options from `AgGridTable.tsx` (reducing the 347-line file and 152-line `useGetTableData` hook with sufficient physical and logical headroom for Task 4.1's inspector mount), preserving rows/columns and using the existing authenticated query adapter.
  - Expose original envelope and context-bound lifecycle to consumers. Evaluate the shared identity-reconciliation eligibility check synchronously when computing query `enabled` so empty, unresolved or foreign-source saved identities in `widget.storage?.companySelection` disable HTTP requests on first render before `QueryParams.tsx` mounts `CompanySymbolSelector`. Discard previous-context views and ignore late responses.
  - Retain only same-context successful data on failed refresh, visibly separating envelope acquisition time (`retrieved_at`, never confused with TanStack Query's client-side `dataUpdatedAt` cache timestamp), financial observation dates and failed-attempt time; initial failure remains empty with its inline state.
  - Done: focused lifecycle cases prove clear/change race isolation, same-context stale retention and no stale data attributed to a new company. Existing table row rendering remains unchanged.
  - Entire extracted and touched files pass 400/300/50; API adapter, oversized processors and QueryParams remain unchanged.
  - _Boundary: Table query and evidence lifecycle_
  - _Depends: 2_
  - _Requirements: 1.3, 2.2, 3.3, 5.3, 5.4, 6.1_

- [x] 3.3 (P) Preserve unresolved saved company identities
  - Integrate the Task 2 frozen selector reconciliation guard into `useCompanySelection.ts` (keeping the 311-line hook file and 188-line hook body within the 50-logical-unit function cap), using saved source identity and current source without a second persisted flag.
  - Inspect raw `metadata: unknown` before `decodeSelection(metadata)` so malformed or unknown-version imported objects (`metadata !== null && metadata !== undefined && decodeSelection(metadata) === null`) are classified as unresolved saved identities (extracting any safe display `{ name, symbol }`) rather than mistaken for absent initial metadata (`metadata == null`) and overwritten by automatic symbol resolution.
  - Prevent automatic same-symbol replacement across sources; retain the unresolved saved name/symbol and reason until explicit current-source reselection. Ensure legitimate same-source Symbol-group updates from a linked widget clear a prior foreign unresolved state while initial mount/reopen preserves it, and preserve initial defaults without saved metadata.
  - Done: focused selector checks cover foreign-source/ambiguous/malformed saved identity, normal group changes, absent initial metadata and explicit recovery. The later persistence journey verifies unresolved save/reopen.
  - Hook and frozen helper pass 400/300/50; use existing error presentation and leave QueryParams unchanged. This lane does not edit the shared helper; route required changes through the controller. The design retains the same module responsibilities; this plan schedules the pure shared guard before its two consumers.
  - _Boundary: Company identity reconciliation_
  - _Depends: 2_
  - _Requirements: 2.1, 2.2, 5.1, 5.6, 6.1_

- [x] 3.4 (P) Preserve research choices in safe template export
  - Extract pure export serialization from `ExportTemplatePopup.tsx` (currently 384 physical lines with a 182-line `formatDashboardDataForTemplate` function) into cohesive sub-50-unit functions in `exportTemplate.ts` and `researchTemplateState.ts` (reusing `zod`), retaining existing template behavior and group references.
  - Add only validated company selection and research configuration to the allowlist. When exporting validated `companySelection`, explicitly retain `state.params.symbol` (and explicit `period`) even when the value matches the catalog default (`"AAPL"`), preventing default-value omission in `ExportTemplatePopup.tsx` from decoupling `state.params` and `state.storage.companySelection` on import. Exclude provider payloads, credentials and session/request secrets; refuse credential-dependent identities rather than leaking URL components.
  - Reuse the existing import storage merge unchanged and the frozen consumer decoders. Invalid/unknown research versions remain unresolved and retain their original imported configuration.
  - Done: focused serialization roundtrips retain identity, period, price dates, peer order/rationales, layout/groups and unrelated existing allowlisted fields; negative cases demonstrate secret exclusion.
  - Popup and extracted serializers pass 400/300/50 as whole files; existing oversized import/state/schema files remain unchanged.
  - _Boundary: Template serialization_
  - _Depends: 2_
  - _Requirements: 5.1, 5.5, 5.6, 6.1_

- [x] 3.5 (P) Edit an independent candidate peer set
  - Reuse company search, installed `react-hook-form` (`useFieldArray` for add/remove/reorder), `@hookform/resolvers/zod`, `use-debounce` and existing themed UI primitives for peer membership and rationale editing. Display readable names, symbols and available listing/exchange facts.
  - Keep the peer array in its single widget-owned configuration, independent of primary selection. Candidate suggestions are not automatic membership or financial validation.
  - Done: component checks preserve peer identity/order/rationale through edits and reject invalid/oversized configuration without silently discarding input. Search absence or entitlement failure leaves existing choices intact.
  - Editor passes 400/300/50; it consumes frozen contracts and does not modify other lanes' state or selectors.
  - _Boundary: Peer editor_
  - _Depends: 2_
  - _Requirements: 1.2, 1.3, 2.5, 4.1, 4.6_

- [x] 4. Integrate the research experience
- [x] 4.1 (P) Make original financial observations inspectable
  - Present the original-observation selector and financial metadata using existing frame actions/theme controls and installed `@radix-ui` / `fuse.js` primitives, independent of grid transpose/grouping.
  - Show source, definition, unit/scale, row-resolved currency (`currency` or `originalRows[row_index][currency_field]`), value origin, actual acquisition (`retrieved_at`) and observation/valuation/publication dates, fiscal labels, coverage evidence and explicit unknowns. Surface `financial_basis`, `transformations` and `limitations` so analysts can inspect accounting-optimization provenance: disclose SBC treatment in `ebitda`, `operating_cash_flow` or `free_cash_flow` only when supplied definitions or reconciliations establish it; otherwise show treatment unknown. Preserve the supplied measure unchanged and distinguish future house economic-cost adjustments. Keep duplicate rows individually selectable by `source_ordinal`; do not infer period duration or historical availability.
  - Done: inspector checks match original row ordinals and display unknown/provider-calculation limitations, including evidenced SBC add-back, retained expense and unknown treatment; mount through the table evidence seam without per-cell requests. Keyboard navigation and existing controls remain usable.
  - Inspector/helpers and the final table integration pass 400/300/50; controller serializes the table mount after 3.2.
  - _Boundary: Observation inspector integration_
  - _Depends: 2, 3.2_
  - _Requirements: 1.2, 3.1, 3.2, 3.3, 3.4, 3.5, 6.1_

- [x] 4.2 (P) Show provider peer observations with explicit limits
  - Request periodic metrics/ratios separately per selected listing, `ttm=exclude`, using the existing adapter through a bounded 2-request concurrency queue with `refetchInterval: false` (never inheriting `useMultipleQueries` unbounded parallel fan-out or default automatic polling). Count bounded retries in request receipts.
  - Expose dataset/field and original-observation choices with observation/valuation/publication dates, units, row-resolved currency, `financial_basis` and provider origin. Keep duplicate rows available by `source_ordinal` and each failed peer/dataset inline.
  - Use the frozen evidence-only statuses: multiples lacking raw denominator evidence or an applicable EV bridge for an enterprise-value measure in FMP `metrics`/`ratios` responses remain explicitly `unverified` (naming the missing denominator/bridge evidence), explicitly evidenced zero/negative denominators are `not_meaningful`, explicit currency/unit/coverage conflicts are `incompatible` only for a stated comparison requiring matching facts, and apparent matches remain `unverified` for aggregation. Retain generic controls with a persistent valuation limitation notice covering generic table/chart sorting, summary statistics and unadjusted provider conventions (such as SBC treatment and unaligned fiscal calendars).
  - Done: focused orchestration checks demonstrate cancellation/removal/unmount, partial failure, refresh and no cross-context reuse; display has no financial formulas, inferred joins or validated ranking.
  - Query/view files pass 400/300/50; shared evidence/eligibility contracts remain frozen.
  - _Boundary: Peer observations_
  - _Depends: 2, 3.2_
  - _Requirements: 1.3, 3.4, 3.5, 4.2, 4.3, 4.4, 4.5, 4.6, 5.3, 5.4, 6.1_

- [x] 4.3 Join the App, peer widget and saved state
  - Compose the peer editor and observations in the existing widget frame; register the frozen renderer and bind validated configuration to existing widget persistence.
  - Join catalog generation and template serialization, verifying group references after import and independent statement/price/peer parameters. Reconcile only reviewed source changes into exact fork/root revisions.
  - Done: installed catalog opens the complete App, all sections are reachable and no section failure blanks unrelated widgets. Saved configuration carries choices, not provider payloads or a frozen valuation snapshot.
  - Run affected contract/type checks and final shared-module size audit; all maintained join files pass 400/300/50. Generated contracts are regenerated and hashed, not hand-edited.
  - _Boundary: Explicit Workspace/catalog integration_
  - _Depends: 3.1, 3.3, 3.4, 3.5, 4.1, 4.2_
  - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.3, 2.4, 2.5, 4.1, 5.1, 5.5, 5.6, 6.1_

- [ ] 5. Verify and deliver the bounded milestone
- [x] 5.1 Verify the packaged analyst journey with real FMP observations
  - Build the accepted candidate through existing Dagger definitions and run it in owned native Compose with the existing financial browser runner; budget packaged Workspace logins across 5.1 and 5.2 against the 5-logins-per-minute client-IP rate limiter (`testing.md`) to avoid HTTP 429 false failures. Tests/publication remain outside Dagger.
  - Use a primary company and two peers; check displayed values against source evidence (including `stock_based_compensation`, `ebitda`, `operating_cash_flow` and `free_cash_flow` where returned), readable identity changes, annual/quarter changes, independent price dates, peer edits, inspector metadata (row currency, date basis, accounting-optimization limitation disclosures), peer multiple missing-denominator `unverified` states and refresh behavior.
  - Cover missing/incompatible evidence and failure recovery with clearly labelled deterministic cases where live data cannot safely reproduce the condition. Inspect owned browser console/network diagnostics; preserve current theme and controls.
  - Done: focused browser/contract evidence and independent financial review pass against exact source/image identities. Record actual request counts, skipped cases and any unresolved issue; no automatic whole-suite reruns.
  - Test/evidence files are excluded from production caps; any implementation repair returns to its owning task and 400/300/50 checks before acceptance.
  - _Boundary: Packaged browser acceptance_
  - _Depends: 4.3_
  - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4, 3.5, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 5.3, 5.4, 6.1, 6.2_

- [x] 5.2 Verify retained research configuration and template portability
  - Extend the same existing journey (reusing the authenticated session or staying within the 5-logins-per-minute client-IP rate budget from `testing.md`) to fresh authenticated reopen, template export/import and container recreation retaining the owned data directory.
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

## Local runtime acceptance record

2026-11-14: tasks 4.3, 5.1 and 5.2 independently accepted against artifacts/reviewed/company-research/runtime-acceptance.md. The exact source/image/test identities, initial/reopen outcomes, cumulative FMP count 291, zero FRED, fixture classifications and remaining limitations are recorded there. Task 5.3 remains open. Parent tasks 3 and 4 summarize their accepted children; they are not additional executable tasks. This is 12 of 13 executable tasks, not completion of the analyst-workspace umbrella or full IA-B readiness.
