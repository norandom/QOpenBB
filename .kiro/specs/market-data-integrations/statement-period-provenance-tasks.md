# Statement period provenance implementation tasks

The owner approved requirements and design on 2026-11-10. This seven-task plan implements only the bounded statement-period slice. All checkboxes below are planned work. The accepted native migration, periodic-query repair and sanitizer preservation remain closed.

## Task list

- [x] 1. Prepare the exact source and verification baseline
  - Create an isolated owned API-fork checkout at the accepted pin and an isolated controller snapshot. Confirm native tool metadata, installed package locations and existing Compose/browser entry points; reuse the accepted environment rather than building another harness.
  - Record clean production/inventory inputs, source identities and selected baseline behavior for Income order/overflow and Balance/Cash stable sort/clip. Resolve the named generated contract files and fixture inputs before workers edit them.
  - Done: installed source identity, focused baseline cases, exact checker scope and disjoint worker boundaries are recorded; unrelated catalog, inventory and .openidea changes remain untouched. Register new maintained modules in a clean inventory proposal so later caps are enforceable.
  - This is prerequisite integration, not fresh infrastructure acceptance. Run focused baseline checks once; do not repeat the completed migration suite. Preparation outputs belong under D:/BuildArtifacts/QOpenBB/statement-period-provenance.
  - _Boundary: Controller-owned source/environment/inventory preparation_
  - _Requirements: 3.1, 3.3, 4.3_

- [x] 2. Implement the typed statement provenance contract
  - Add the approved optional statement member and strict row/fact/convention models. Validate indices, counts, presence states, allowlisted keys, conflicts and supported coverage. Reject observation-derived known coverage under v1; live provider conventions remain empty.
  - Keep FinancialSource reference validation at the envelope boundary to avoid circular imports. Reuse safe result validation; preserve FRED metadata and omit the absent statement member for unrelated/older envelopes.
  - Verify old-envelope reading, unchanged FRED serialization, safe malformed input rejection and the explicitly incompatible old strict Python reader. Test synthetic documented conventions without turning them into live FMP assertions.
  - Done: focused core tests and independent Astra review pass; the frozen core types/schema are available to both downstream lanes. All modified/new production files pass 400 physical lines, 300 logical units and 50/function against the prepared inventory. No size exception is preapproved.
  - _Boundary: Core financial metadata and its contract tests_
  - _Depends: 1_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4, 3.2, 3.3_

- [x] 3. (P) Integrate provenance into the three FMP statement routes
  - Capture only allowlisted source facts before alias normalization can overwrite them. Carry source ordinals and facts with validated rows through each route's unchanged ordering/clipping; construct provenance from those final bundles.
  - Preserve current-alias precedence, duplicate rows, values, null/zero states, bounds, transport and acquisition timestamps. Do not fetch another endpoint or infer starts/duration from fiscal labels.
  - Mark unsupported flow coverage unknown consistently in row and common field metadata. Retain stock semantics and closing dates; beginning cash remains undated without supported source evidence. Correct misleading static period descriptions only.
  - Done: all three route tests prove value/order equality, matching row ordinals, alias conflicts, supplied null versus absence, mixed fiscal labels, unknown duration/restatement and correct instant handling. Independent financial review and whole-file 400/300/50 gates pass.
  - _Boundary: FMP statement helper, three adapters/data declarations and provider tests_
  - _Depends: 2_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2_

- [x] 4. (P) Verify the consumer contract against the frozen core schema
  - Add root native-response/schema cases using controlled fixtures for the approved metadata shape. Prove equivalent Python/HTTP metadata, malformed attribution rejection and safe errors. Keep existing FRED and unrelated-provider responses unchanged.
  - Reuse financial OpenAPI projection and native widget generation. Change projection only if required by the added referenced definitions; do not create a schema registry or replace the accepted sanitizer.
  - Prepare strict-client migration documentation tied to the final core/provider revision, explicitly distinguishing generic row consumers from old strict validators.
  - Done: isolated consumer fixtures and schema-reference checks pass against task 2; independent review accepts the bounded consumer changes. Production changes pass 400/300/50; generated snapshots/tests/docs are excluded. Actual provider join and generated-output promotion wait for task 5.
  - _Boundary: Root financial projection and consumer contract tests; no provider edits_
  - _Depends: 2_
  - _Requirements: 2.4, 3.1, 3.2, 3.3_

- [x] 5. Join installed providers, generated consumers and real statement evidence
  - Freeze tasks 3 and 4, refresh the protected native packages through existing uv/Safe Chain commands and verify installed source hashes. Join the actual routes with the consumer assertions, promoting only reviewed source/inventory deltas and preparing source/native generated contract proposals. Canonical image-backed generation waits for task 6; task 5 must not depend on an image not yet built.
  - Reuse retained source receipts for deterministic replay where original hashes are available. Execute the annual/quarterly Income/Balance/Cash matrix for MSFT, ORCL and ADBE through the installed candidate with existing live capture/accounting. The initial matrix contains 18 queries, each limit 2; each single capture supplies both source and response comparisons, with no duplicate validation fetch or automatic rerun.
  - Freeze actual collected cases and transport-attempt bounds before execution. Keep request scope visible and respect existing owner authorization without repeated permission prompts. An entitlement or source failure leaves the affected case open; synthetic rows cannot replace its live result.
  - Done: actual installed Python/native results agree with source values and period facts for the declared matrix, generated schema/catalog comparisons and combined source/inventory gate pass, and Astra accepts the financial join. Unknown coverage remains an honest result, not IA-B readiness. This explicit integration task owns any shared fixes; return substantial production changes to their owning task/reviewer.
  - _Boundary: Controller integration of installed fork, root consumers, catalog and live evidence_
  - _Depends: 3, 4_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 4.1, 4.3_

- [x] 6. Accept the packaged statement widgets in the native workflow
  - Build the candidate image pair once through existing native Dagger, start an owned Compose session and verify the installed source/catalog identity. Reuse the accepted Workspace source and existing financial Playwright journey; add only affected Income/Balance/Cash assertions.
  - Verify visible source-backed values, annual/quarter controls, refresh, widget discovery and saved selections after fresh-login reopen. Keep current UX/theme and focused CDP diagnostics. Do not expand this into a chart matrix or repeat unrelated infrastructure acceptance.
  - Freeze browser request scope/count before execution, reuse already captured response evidence where possible and do not automatically rerun failures. Credentials and raw payloads remain private. Stop only owned containers/networks and preserve evidence/state after the run.
  - Done: exact candidate image identities, affected browser outcomes, request usage and cleanup are independently accepted. A ready health endpoint alone cannot close this task. Any production fix repeats only affected source/package checks and invalidates the corresponding candidate identity.
  - _Boundary: Controller image-backed browser acceptance using existing workflow_
  - _Depends: 5_
  - _Requirements: 3.1, 3.3, 4.2, 4.3_

- [ ] 7. Publish and close the accepted feature milestone
  - Push reviewed per-task commits and use the existing milestone workflow once with image builds enabled. Dagger builds only; verify actual publication and anonymous image identities, canonical installed catalog and portable Linux checks. Do not equate a dispatched workflow with successful release.
  - Bind CI images to accepted source and document local candidate versus published image evidence. Preserve prior release availability; do not claim owner-server deployment. If source/schema drift appears, leave publication acceptance open and diagnose that drift.
  - Done: tagged prerelease, public images and manifest agree with accepted sources, affected packaged/contract checks pass, and independent delivery review accepts the milestone. Sync selected sanitized evidence before selective commit; update README/docs checkboxes, breadth and spec progress, and publish the strict-client migration note. Broader IA-B readiness remains open.
  - This task uses existing delivery machinery. Docs, generated manifests and reviewed evidence are outside production caps; any production fix requires its owning task's checks rather than a delivery-only exemption.
  - _Boundary: Explicit controller delivery integration_
  - _Depends: 6_
  - _Requirements: 3.3, 4.2, 4.3_

## Ownership and fan-out

API paths are relative to `openbb_platform/` in the owned fork. Root paths are relative to QOpenBB. Task titles describe outcomes; this table freezes writable scopes for worker handoffs.

| Task | Writable scope | Role |
| --- | --- | --- |
| 1 | External source/environment baselines and clean inventory proposal only | Controller with bounded Sol preparation |
| 2 | `core/openbb_core/provider/standard_models/{statement_provenance,financial_metadata}.py`; root `tests/providers/test_financial_metadata.py` | Sol implementer, fresh Astra review |
| 3 | `providers/fmp/openbb_fmp/utils/statement_provenance.py`; `models/{income_statement,balance_sheet,cash_flow}.py` and matching `_data.py`; root `tests/providers/test_statement_provenance.py` and existing affected statement tests | Sol implementer, fresh Astra financial review |
| 4 | Root `services/data-api/qopenbb_data/financial_openapi.py`, `tests/providers/test_service_financial.py` and affected financial projection contract tests; migration-note draft | Sol implementer, independent review |
| 5 | Installed environment, shared source lock/inventory proposal, generated contract proposal; root `tests/providers/test_live_financial.py` and existing live support only where needed | Controller joins; bounded disjoint Sol support permitted |
| 6 | Root `tests/e2e/financial-workspace.spec.mts`, existing candidate/session inputs and selected evidence | Controller, independent Astra acceptance |
| 7 | Final generated outputs, release records, README/docs/spec/breadth and sync manifest | Controller, independent delivery review |

Graph: `1 -> 2 -> (3 || 4) -> 5 -> 6 -> 7`. Only tasks 3 and 4 are parallel. They share the accepted core as read-only input and cannot edit each other's files. Contract changes pause both lanes. No worker writes shared source pins, inventory or generated outputs while another lane runs. Use at most controller plus two implementers and one reviewer. Agents are not alone in the codebase and must preserve others' edits. Commits are parent-owned and per accepted task.

Each task is a bounded 1-3 hour work unit, excluding external build/CI waiting time; split an unexpected substantial repair before dispatch rather than absorb another feature. Serialize dependency installation, heavy suites, image builds, shared runtime mutations and commits. Use bounded xdist and one browser worker with zero retries for financial acceptance. New packages, a new runner or a whole-suite expansion are not implicit tasks.

## Verification and delivery inputs

Use native Windows from the repository with `pipeline/dev.ps1`, provisioned tool metadata and D:/BuildArtifacts output paths documented in docs/development.md. Task 1 records the exact existing provider interpreter and protected installation command; it must not silently use the pipeline interpreter as proof that provider packages are installed. Use installed packages, with only root service code on PYTHONPATH where existing checks require it.

Generated proposals cover contracts/{openapi,routes,widgets,apps,catalog-report,compatibility,provenance,hashes}.json. Preserve contracts/datasets.json as the declared inventory unless a reviewed contract change requires it. Use the accepted five-module catalog generator from contracts/provenance.json, excluding dirty renderer work. Task 6 runs the existing catalog_cli against its exact candidate image; task 7 compares the canonical published-image catalog with that accepted proposal.

The existing combined command is `python -m tools.quality.complexity --check --root <clean-root> --repository-root qopenbb=<clean-root> --repository-root workspace=<accepted-fork> --repository-root data_api=<candidate-fork> --changes workspace=<manifest> --changes data_api=<manifest> --output <report>`. The checker reads its inventory beneath the clean root; no inventory override is assumed. Run it with the qualified native interpreter and real accepted manifests, not literal placeholders.

The approved design's paths and requirements are authoritative. Existing initial-provider tests, financial capture helpers, contract generation, complexity checker and native browser fixtures provide the checks. Record exact selected node IDs and exit codes when executing; these planned checks are not evidence. Do not reopen completed periodic-query or sanitizer tasks unless an actual regression appears.

The unrelated catalog/inventory working-tree changes and .openidea directory are outside scope. Never stage, reset or silently use them as accepted inputs. Reconcile only reviewed source/inventory deltas through a clean accepted copy. No Excel, Anthropic, custom database, house calculation or owner-server operation belongs to this task plan.

## Implementation notes

- Task 1 accepted 2026-11-10: protected native install, seven installed source matches, eight baseline checks and the clean 101-file gate passed; independent review accepted. [Evidence](../../../artifacts/reviewed/statement-period-provenance/baseline.md). Current native catalog helper differs from historical canonical provenance; retain the reviewed native helper and regenerate provenance at the join.

- Task 2 accepted 2026-11-10: API b373da3f8d7, 64 installed tests, independent review and whole-file caps passed after compatibility/error-message repairs. [Evidence](../../../artifacts/reviewed/statement-period-provenance/core.md). Preserve annual/quarter scope; no broader Income query change is authorized.

- Task 4 accepted 2026-11-10: existing projection needs no production change; independent consumer review passed 81 tests. [Evidence](../../../artifacts/reviewed/statement-period-provenance/consumer.md). Final provider revision and actual source/live acceptance remain task 5.

- Task 3 accepted 2026-11-10: API e78d87b2000, 102 independently repeated provider checks, nine installed source matches and the clean combined 110-file gate passed. [Evidence](../../../artifacts/reviewed/statement-period-provenance/provider.md). Register the new FMP helper in both ownership include selection and maintained-file inventory; do not claim baseline-valid query labels prove duration.

- Task 5 accepted 2026-11-10: nine installed hashes, native 11-widget proposal, final 110-file gate and corrected 18-case live matrix passed; independent Astra review accepted. Cumulative traffic was 36 FMP and zero FRED, preserving the failed timestamp-comparator run. [Evidence](../../../artifacts/reviewed/statement-period-provenance/join.md). Packaged/browser and publication gates remain open.

- Task 6 integration repair: accept the same immutable image digest with Docker or Podman inspect formatting. Eighteen mocked cases and independent review pass; whole-file caps are 97/69/max19. [Review](../../../artifacts/reviewed/statement-period-provenance/catalog-id-review.md). Packaged/browser acceptance remains open.

- Task 6 catalog text repair: decode container JSON as UTF-8 explicitly on Windows. A real subprocess regression and independent 19-case run pass; [review](../../../artifacts/reviewed/statement-period-provenance/catalog-encoding-review.md). The original native proposal is retained; task 6 uses the canonical sorted-JSON roundtrip for its comparison.

- Task 6 native omission repair accepted: API a965f70c164, 144 installed tests, independent 66-case review and clean combined 110-file gate. [Evidence](../../../artifacts/reviewed/statement-period-provenance/native-defaults.md). Rebuild only the API and repeat the affected browser journey; task 6 remains open.

- Task 6 accepted 2026-11-10: all three statement widgets pass real-data period/refresh/save/fresh-login checks, with 16 FMP sends in the final run, zero FRED, verified catalog/source identities and owned cleanup. [Evidence](../../../artifacts/reviewed/statement-period-provenance/packaged.md). The reused Workspace labels are historical; rebuild both release images from the final lock in task 7.

- Task 7 delivery repair: initial workflow `42876893136` passed application checks but failed before building because executable resolution dereferenced the SDK virtual-environment Python. Preserve its validated launch path for SDK callers; native 170-pass suite and independent offline Linux regression accepted. [Review](../../../artifacts/reviewed/statement-period-provenance/sdk-review.md). Publication remains open until the corrected workflow and published-image checks pass.
