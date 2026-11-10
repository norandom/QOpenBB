# Periodic query provenance implementation tasks

The owner approved the [bounded design](periodic-query-provenance-design.md) on 2026-11-06. This four-task amendment exposes the existing periodic-only selection without changing financial results. The owner approved this task plan and implementation on 2026-11-06.

This plan supplements the accepted [main tasks](tasks.md), rather than reopening their 26 completed units. It covers the twelve scoped design criteria and the existing delivery obligations 8.1-8.5. All other criteria retain their main-plan mapping and open follow-on state. No TTM acquisition, financial calculations, UI work or broader IA-B completion is included.

## Tasks

- [x] 1. Establish the existing source and verification baseline
  - Record the controller and data-fork revisions, installed core/FMP module origins and copied-source hashes before editing. Retain the accepted Workspace pin. Confirm the existing provider environment and protected toolchain are usable; do not recreate infrastructure or install unrelated dependencies.
  - Reuse the accepted complexity inventory/checker foundation. Freeze a clean inventory input and exact fork base/head or change manifests for the three production files; preserve the unrelated dirty inventory and catalog-renderer work. Confirm Node 24.22.1 or a later approved patched version for combined checks.
  - Freeze clean accepted catalog generator inputs and the existing package-refresh commands below. Collect the affected offline tests once, without live access. If installation/source prerequisites fail, diagnose that specific failure rather than restart WSL or broaden the task.
  - Done: a concise local baseline identifies the actual source/package identities, runnable selected test nodes, clean generation input and exact check commands. No baseline test result is represented as repaired behavior. This task changes no production code; evidence/configuration copies are excluded from production caps.
  - _Boundary: Existing verification environment and source inventory; controller-owned setup._
  - _Requirements: 6.1, 8.1_

- [x] 2. Preserve the validated periodic selection in result metadata
  - Add the public query key to the existing core allowlist and emit the validated selector from both periodic provider models as one cohesive change. Keep core provider-neutral; retain credential/value validation. Do not echo raw request parameters or create another default table.
  - Extend existing focused tests for default/explicit exclusion in annual/quarter modes, identical upstream requests and financial results, unsafe query rejection, and unsupported include/only/TTM rejection before transport. Capture the meaningful regression failure before the repair, then refresh both copied local packages through the protected toolchain and verify installed bytes before GREEN.
  - Preserve schema version, envelope location, result order, values, units, aliases, defaults, error semantics and explicit missingness. Document in the test assertions that periodic selection does not establish fiscal comparability or introduce derived values.
  - Done: the focused core/Metrics/Ratios tests pass against the changed installed source; every successful case emits `ttm: exclude`. The three modified production files pass whole-file 400 physical lines, 300 logical units and 50/function caps and owning-fork lint. Independent review precedes the task commit.
  - _Boundary: Cohesive core/provider metadata contract; three production files and their focused tests in the ownership table._
  - _Depends: 1_
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 6.1, 7.1, 7.2, 8.4_

- [x] 3. Join native consumers, source identity and bounded provider evidence
  - Extend the existing mounted service assertions so Python and API results retain the same effective selector and financial values. Remove only the obsolete TTM metadata exemption/finding from newly executed research checks; historical IA-A receipts and their hashes remain untouched.
  - Update the exact fork pins and validate a source/native catalog proposal with the clean accepted generator inputs from task 1. Image-backed regeneration belongs to task 4 because the canonical CLI requires an identified candidate image. Check parameter choices/defaults, stable widget identities, financial schemas and native discovery; do not change unrelated catalog behavior or incorporate the unfinished renderer work.
  - Run the affected offline integration selection once after package/source identity is verified. Make at most four fresh FMP requests, one default annual and one explicit quarterly query for each route, using existing bounded capture/sanitization helpers. Compare source values and effective metadata; no retries, FRED calls, repeated 49-call assessment or synthetic substitution for entitlement acceptance.
  - Document the compatibility consequence: older strict Python metadata validators require matching updated core/provider versions. Generic dictionary consumers remain usable; do not advertise old strict validators as compatible. Keep actual duration/YTD, restatement, valuation/share/claim conventions and both false IA-B readiness flags open.
  - Done: reviewed native and four-call evidence identifies exact source revisions, queries, values and outcomes; generated-contract checks and the combined complexity/shared-module gate pass. Source pins and reviewed inventory agree. Missing live access leaves live acceptance open. Generated artifacts/tests/docs are excluded from production caps; any maintained configuration change passes its applicable physical cap. No new generator logic is in scope.
  - _Boundary: Explicit controller integration across source pins, installed API, generated consumers and evidence._
  - _Depends: 2_
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 6.1, 6.2, 6.3, 7.1, 7.2, 8.1, 8.3, 8.4, 8.5_

- [x] 4. Publish one verified image milestone
  - After accepted source/catalog integration, push the reviewed fork and controller commits and dispatch the existing milestone workflow once. Dagger builds images only; existing portable commands own verification, publication and release assets. Preserve the accepted Workspace source and runtime UX.
  - Use the actual built image for canonical catalog generation and compare it with the task-3 source/native proposal before accepting delivery. Promote only reviewed matching generated outputs/provenance. Reuse that same built image; do not dispatch another milestone just to validate its catalog. If contract drift appears, leave release acceptance open and diagnose it. Use the existing packaged API/consumer smoke and public image-pull verification. Tie the API behavior to the exact published image and source; distinguish source tests, packaged checks, registry verification and owner-server deployment. Reuse the four-call evidence; do not expand the live budget for packaging checks. Do not add a chart/browser matrix for this metadata-only repair.
  - Update README and docs checkboxes, provider coverage, breadth, source/image provenance and bounded spec status with actual results. Publish one concise reviewed milestone receipt, synchronize its artifact manifest and include the strict-client migration note before claiming affected consumers supported.
  - Done: the tagged prerelease and both public images resolve to the accepted manifest, relevant package/consumer checks pass, and the pull-only install path is verified. An unavailable build/pull leaves delivery open rather than closing on source tests. This task changes no production/build logic; generated manifests, docs and evidence are excluded from production caps.
  - _Boundary: Explicit controller delivery integration; existing build/publication flow only._
  - _Depends: 3_
  - _Requirements: 6.2, 6.3, 8.1, 8.2, 8.3, 8.4, 8.5_

## Ownership and execution

| Task | Writable scope | Model and join |
| --- | --- | --- |
| 1 | Ignored baseline/scope inputs under `artifacts/periodic-query-provenance/`; no production edits | Sol prepares; controller accepts prerequisites |
| 2 | Data fork `openbb_platform/core/openbb_core/provider/standard_models/financial_metadata.py`, `providers/fmp/openbb_fmp/models/key_metrics.py`, `providers/fmp/openbb_fmp/models/financial_ratios.py`; root `tests/providers/test_financial_metadata.py`, `test_fmp_key_metrics.py`, `test_fmp_financial_ratios.py` | One Sol implementer; independent Astra contract review; controller commits |
| 3 | Root `tests/providers/test_service_financial.py`, `test_live_financial.py`; source lock/mirror, clean inventory input, generated contract proposal listed below; provider coverage migration note and scoped evidence | Controller owns shared joins; Sol may implement disjoint native tests after task 2 freezes; Astra independently reviews integration |
| 4 | Canonical generated-contract promotion and existing release outputs; README, docs roadmap/provider coverage, owning spec status/tasks, `.kiro/breadth.toml`, reviewed milestone/manifest | Controller runs delivery; independent review of acceptance and publication |

Do not concurrently edit the shared metadata contract. There are no independent production `(P)` lanes in this small repair. During task 3, a Sol worker may own only the two named native/live test files while the controller owns source/catalog inputs; generation, environment changes, suites and commits remain serialized. A fresh Astra reviewer reads the frozen join; a Luna auditor may check documentation links/hashes in parallel with that read-only review. At most controller plus three agents; one heavy check/build at a time. Every worker receives caps, exact paths and accepted inputs and must preserve other edits. Each completed task has its own commit; ordinary pushes do not trigger extra milestone builds.

The current unrelated edits in `.kiro/complexity-budgets.json`, `pipeline/qopenbb_ci/catalog_cli.py`, `pipeline/qopenbb_ci/catalog_renderers.py` and `tests/contracts/test_renderers.py` are outside this task plan. Do not reset, stage or silently use them as accepted inputs. Apply only the reviewed source-pin/inventory delta through an isolated accepted copy; reconcile that delta without altering unrelated work.

## Verification commands and inputs

Use the existing WSL environment in `/mnt/d/Source/QOpenBB`. Commands below define planned checks, not completed evidence. Keep provider keys private. If owner execution is required, put the exact current command in ignored LF `run_this.sh`, syntax-check it, and ask only for `bash run_this.sh`.

Focused task-2 selection:

```sh
env PYTHONPATH=services/data-api verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_financial_metadata.py tests/providers/test_fmp_key_metrics.py tests/providers/test_fmp_financial_ratios.py -n0 --maxprocesses=2
```

Task-3 native integration selection:

```sh
env PYTHONPATH=services/data-api verification/provider/.venv/bin/python -m pytest -c verification/provider/pyproject.toml tests/providers/test_service_financial.py tests/providers/test_live_financial.py -m 'not live' -n0 --maxprocesses=2
```

Task 3 adds a narrowly parameterized four-case live selector in the existing live module using its current helpers; collect the exact node IDs before execution. Each case sends one request with `limit=1`, using MSFT, annual/default exclusion or quarter/explicit exclusion. Source comparisons and metadata assertions share that one capture, rather than fetching again. Existing rejection tests remain offline. Freeze the four collected nodes and an attempt ceiling of four before privately enabling live access; no unbounded module-wide live selection is allowed.

The project delivery instructions require the final milestone and documentation update despite the generic task skill's code-only default. This plan adds no infrastructure framework or separate documentation-only task. The accepted foundation and original 44-criterion mapping remain in the main plan; scoped requirement mapping is not an assertion that broader provider or analyst requirements are complete.

Existing toolchain and source/catalog join commands:

- Reuse the protected PATH setup in `artifacts/market-runtime/install.sh`, checking its Node and Safe Chain executables against the current tool lock. Set `UV_PROJECT_ENVIRONMENT` to the existing absolute `verification/provider/.venv`, `UV_LINK_MODE=copy` and `SAFE_CHAIN_MINIMUM_PACKAGE_AGE_HOURS=48`. Verify `uv safe-chain-verify` and `uvx safe-chain-verify`, then run `uv sync --project <exact-source-root>/verification/provider --locked --python "$QOPENBB_TOOLS/python/cpython-3.13.15-linux-x86_64-gnu/bin/python3.13" --reinstall-package openbb-core --reinstall-package openbb-fmp`. Resolve placeholders from task-1 identities. Do not replay the historical `uv lock` step or change dependency versions.
- The accepted generator consists of `pipeline/qopenbb_ci/{catalog,catalog_cli,catalog_financial,catalog_runtime,catalog_upstream}.py`, as hashed in `contracts/provenance.json`. Extract accepted Git blobs into an ignored clean package and verify their hashes, following the existing clean-generator pattern in `artifacts/prototype-batch-20261027/catalog/regenerate-preview.py` with the current five-module list. Do not run that historical script unmodified. Source/native checks in task 3 are not image-backed acceptance.
- Canonical task-4 generation uses `pipeline/.venv/bin/python -m qopenbb_ci.catalog_cli --image <actual-built-data-image-id> --source <candidate-data-api-checkout> --source-lock <candidate-source-lock> --inventory contracts/datasets.json --previous-routes contracts/routes.json --output <proposal-directory> --work <owned-linux-work-directory>` with the clean generator import path. It verifies the image/source-lock identity. The generated set is `contracts/{openapi,routes,widgets,apps,catalog-report,compatibility,provenance,hashes}.json`. Dataset and renderer inputs remain unchanged. A contract-change option permits a review proposal, never automatic acceptance.
- The combined complexity command is `pipeline/.venv/bin/python -m tools.quality.complexity --check --root <clean-intended-root-snapshot> --repository-root qopenbb=<clean-intended-root-snapshot> --repository-root workspace=<accepted-workspace-checkout> --repository-root data_api=<candidate-data-api-checkout> --changes workspace=<workspace-manifest.json> --changes data_api=<data-api-manifest.json> --output <combined-report.json>`. The checker reads the inventory from its root; it has no separate inventory override. Use actual repository URLs/base/head and explicit changed paths per `docs/complexity.md`. The unchanged Workspace manifest explicitly declares no changes. Require combined acceptance, no errors and no violations. Preserve unrelated live-worktree inventory edits.
- Existing milestone dispatch is `gh workflow run prototype.yml --ref main -f build_images=true`. The existing `prototype.yml` and portable `qopenbb_ci.alpha_cli` own both images and publication. Check exact release manifest, three install assets and existing six anonymous pull combinations. Record a source-only or published-only result honestly if a packaged check is blocked; do not silently close task 4.

Do not merge unreviewed clean-snapshot output into the working tree. Controller promotion is restricted to intended source-lock mirrors (`sources.lock.json`, `contracts/sources.json`), the reviewed inventory revision delta, the eight generated contracts above and scoped documentation/evidence. Preserve unrelated changes byte-for-byte apart from an explicitly reviewed, nonconflicting inventory pin hunk; stage only that intended hunk. An actual merge conflict pauses only that promotion until reconciled.

## Implementation Notes

- Task 1 accepted 2026-11-06: source/package/clean-generator identity and protected tooling verified; 102 focused tests collected and 58 native offline tests selected (19 live deselected), no tests executed. Independent Sol review approved. Ignored baseline and review: artifacts/periodic-query-provenance/. Accepted Workspace checkout remains at f832a559; the unrelated root vendor checkout is untouched. Refresh/check scripts are prepared, not behavior acceptance.

- Task 2 accepted 2026-11-06: three-line core/FMP repair, 19 expected RED failures followed by 125 focused passes after protected package refresh and installed-source hash verification. Owning-fork lint and combined 400/300/50 gate pass; independent Astra review approved with four additional identity/schema/empty-result checks. Native/live/catalog/release acceptance remains open. Review: artifacts/periodic-query-provenance/task2-review.md.

- Task 3 accepted 2026-11-06: 73 native/offline checks and four real FMP cases passed (four attempts, all HTTP 200); source/native route comparison unchanged. Independent Astra review approved, including fresh discovery/budget checks and historical receipt hash audit. Two real-data proofs renewed; strict Python-client migration documented. Source pin 2e60c0a7aff039eda5f14a9d494beaec822fb9c4. Public evidence: artifacts/reviewed/periodic-query-provenance/accepted.md. Image acceptance remains task 4.

- Task 4 closeout 2026-11-10: alpha-42231784072-1 publication, six anonymous pulls, three assets, canonical image catalog, three packaged smoke tests and four installed native/Python cases passed. Delivery documentation corrections and final independent recheck complete the acceptance gate. No new build or provider request is required. Owner-server deployment of this release and IA-B readiness remain open.
