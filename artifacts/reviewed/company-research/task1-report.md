# Company Research task 1 baseline

2026-11-14. The isolated implementation foundation is ready for independent review. The existing combined checker accepts explicit fork manifests and measures 706 complete maintained files with zero errors and zero unsuppressed violations. This is source-size evidence, not Company Research, live-provider, runtime or financial acceptance.

## Task brief and ownership

Requirements 6.1 and 6.4 require identifiable participating contracts and qualified delivery evidence. The approved design's File responsibility plan, Complexity and dependency order, and Verification and rollout sections require the existing checker, complete integration baselines and existing runner reuse. Task 1 establishes those inputs without feature code, builds, installation, runtime startup or provider requests.

Canonical approved specs remain D:/Source/QOpenBB/.kiro/specs/analyst-workspace. The detached root at root/ is based on QOpenBB 1b31e77fa0293649ce82eefb4f6f023bcbb530a1. Workspace at workspace/ is e1a12c3a031a23598f41166a0f91b8fb24ac2387; Data API at data-api/ is a965f70c164fe477ce9c99654b9be48e2f1bc9fd. Both forks are clean. Exact roots, origins and status are in source-identities.json. Root has only the two task-owned inventory changes. No unaccepted catalog, renderer or inventory bytes were imported from D:/Source/QOpenBB; no commits were created.

The controller owns these inventory copies and later shared source-lock/catalog changes. Workspace future workers own only task-assigned paths. The root worktree's old spec approval metadata is historical; canonical approval is the source repository's updated spec and owner conversation.

## Measured integration baselines

| File | Physical | Logical | Largest callable logical units |
| --- | ---: | ---: | ---: |
| AgGridTable.tsx | 347 | 105 | 19 |
| useCompanySelection.ts | 311 | 137 | 23 |
| ExportTemplatePopup.tsx | 384 | 162 | 29 |
| components/Widgets/index.ts | 340 | 189 | 3 |
| pipeline/qopenbb_ci/catalog.py | 234 | 169 | 32 |
| pipeline/qopenbb_ci/catalog_cli.py | 81 | 56 | 21 |

integration-baselines.json retains every callable name, line, column and logical count, not only maxima. baseline.json retains the complete 706-file physical/logical/callable scope. No integration target above uses an exception. Nineteen existing exceptions apply only to nine other unchanged Workspace files: backend API crud.py and schemas.py, pro router index.py, QueryParams.tsx, Table/utils.tsx, components/types.d.ts, state/copilot.ts, types/app.ts and routes/login.tsx. applied-exceptions.json gives exact metric, bound, revision, rationale, expiry and approval for each. Those exceptions do not authorize Company Research edits to those files.

The isolated inventories remain executable measured configuration: complexity-budgets.json has 365 physical lines and complexity/workspace.json has 92, below 400. Existing integration ownership transfers to the Company Research owner. The .git worktree pointer receives the same metadata exclusion as .git directory contents. No production size limits or checker code changed. planned-production-paths.json records all new design/task paths; activate each exact path in its owner.files at creation. Listing nonexistent future files in the active inventory is invalid because the checker fails closed on mapped missing files. No placeholders were introduced.

## Reproduce and continue

From a repository working directory, run:

```powershell
& D:/BuildArtifacts/QOpenBB/company-research/check-baseline.ps1
```

The script freezes the real interpreter, root, both --repository-root inputs, both --changes manifests and external output. It returned 0. Manifests deliberately declare the complete mapped maintained fork scope at the accepted snapshot, rather than pretending no fork code needs measurement. Their base identities match clean inventories/source lock. Provenance is manifest-declared; clean HEAD/origin identities are separately observed in source-identities.json. For each later task, update the manifest head and include every actual changed path, including additions/renames/deletions; keep whole touched integration files and activate new owner mappings. Do not replace changed scope with empty manifests.

Actual tools: CPython3.13.15, Node24.22.1, TypeScript6.0.3, Playwright1.64.0, pytest9.1.1, pytest-xdist3.8.0, pydantic2.12.5, jsonschema4.26.0. tool-identities.json records executable/package versions. The native tool receipt remains D:/BuildArtifacts/QOpenBB/native-foundation/resolved-tools.json. Bare python is not used. Existing locked verification dependencies are reused through root/verification/node_modules junction to native-foundation/snapshot/verification/node_modules; no dependency bytes were installed or changed.

Focused checker regressions, from root/:

```powershell
& D:/BuildArtifacts/QOpenBB/native-foundation/pipeline-venv/Scripts/python.exe -B -m pytest -c pipeline/pyproject.toml tests/quality -n0 --maxprocesses=2 -q --basetemp D:/BuildArtifacts/QOpenBB/company-research/pytest-temp
node --test tests/quality/test_syntax_units.mjs
node verification/node_modules/typescript/bin/tsc --project tools/quality/tsconfig.json
```

Node suite:15 passed; strict tsc:exit0. Python:94 passed,2 skipped,1 failed. quality-tests-final.log preserves the failure in test_real_git_scope_verifies_origin_head_cleanliness_and_diff: tools/quality/changes.py compares Git's Windows forward-slash root string with str(Path.resolve()) using backslashes. This is a production Git-mode path normalization defect, not a reason to weaken the fixture. It predates these inventory changes; the prescribed manifest route bypasses Git-mode discovery and passes. Fixing Git-mode portability is a separate scoped production change. Initial quality-tests.log records an invocation rejected for unsupported --no-cov (pytest-cov is not installed); the corrected command above ran the actual suite. No artificial tests or RED claim were created for inventory-only work.

Workspace package scripts already supply test:unit (vitest run tests/unit), test:integration and typecheck. The isolated accepted fork has no frontend node_modules. Before task2 executable contract tests, locate an accepted matching frozen-lock dependency tree or perform a protected frozen Bun install under existing cache policy, only when installation is authorized. Reuse the maintained verification Playwright1.64.0 rather than the fork's older browser package. Installed library declarations include zod^4.4.3, dayjs^1.11.10, react-hook-form^7.75.0, use-debounce^10.0.0 and @hookform/resolvers^5.2.2; application installation was not claimed.

## Existing runner assessment and concrete prerequisites

pipeline/dev.ps1 start accepts -SessionPath, -WorkspaceImage and -DataImage. compose_runtime.prepare creates a unique qopenbb-browser UUID project, loopback origin and session-owned retained state directory under the requested new private session parent; recreate consumes that existing descriptor. This supports the planned owned local project and retained-directory journey without a new harness. A future proposed session is D:/BuildArtifacts/QOpenBB/company-research/runtime/session/runtime.json; its parent must not already exist at start. Do not precreate or use the operator's live data.

verification/financial-workspace.config.ts uses the accepted Workspace live-chart config: one worker, no retries, isolated/headless browser, explicit loopback origin and output/cache roots. The root browser spec reads a checked runtime descriptor through QOPENBB_RUNTIME_READER, QOPENBB_RUNTIME_PYTHON and WORKSPACE_RUNTIME_PRIVATE. Config additionally requires WORKSPACE_EVIDENCE_ROOT, WORKSPACE_FRONTEND_ORIGIN, PLAYWRIGHT_BROWSERS_PATH and QOPENBB_PLAYWRIGHT_PACKAGE. Python child imports need root/pipeline on PYTHONPATH. Keep all browser outputs/caches under D:/BuildArtifacts and private descriptor credentials out of published receipts.

Concrete later prerequisites: wire the isolated root vendor/workspace fixture import to the accepted checkout (the new root has an unpopulated historical submodule); supply the already installed verification package through QOPENBB_PLAYWRIGHT_PACKAGE; select the owned browser cache; supply checked immutable candidate image identities after future builds; establish the explicit Podman daemon endpoint; then start a fresh private session and retain its state directory for recreate. The runner's current verify action checks synthetic infrastructure; Company Research acceptance extends the existing financial browser journey. No runtime, daemon, image-presence or browser-liveness check ran in this task, so this assessment establishes supported interfaces, not current service readiness.

Core default product.md, tech.md and structure.md do not exist in current .kiro/steering. Applicable complexity/testing/ci/delegation/documentation policy and canonical approved task/design/requirements were read. Root dirty source files and canonical plan were preserved. Receipt hashes bind the measured inventories/manifests/reports; refresh hashes when a later accepted task updates them.
