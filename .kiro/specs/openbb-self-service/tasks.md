# Implementation plan

Design approved by the owner on 2026-10-16 ("go"). The owner approved these implementation tasks on 2026-10-16 ("approve"). Unchecked tasks remain unimplemented or unverified. Each executable leaf targets one 1-3 hour engineering work unit; investigate unexpected scope before splitting a task, rather than silently expanding it. External access, entitlement decisions and build waits are not promised completion times.

## Execution contract

Renderer amendment, 2026-10-16: the owner selected "Use Perspective baseline". Tasks 2.6-2.12 add the selected viewer and remove commercial dependencies without renumbering prior tasks. Independent controller task-graph sanity review passed after splitting Community isolation from commercial removal; independent amendment review still precedes renderer feature work. No new renderer task is implemented or accepted by this plan.

- Follow the approved [design](design.md), [complexity](../../steering/complexity.md), [testing](../../steering/testing.md), [CI](../../steering/ci.md), [documentation](../../steering/documentation.md) and [delegation](../../steering/delegation.md) policies.
- Every leaf follows implementation -> independent review -> fresh verification -> acceptance. Controller owns shared contract updates, integration joins, commits and the single heavy-check queue. At most two workers plus one reviewer run alongside the controller; up to three independent lightweight checks may overlap. No parallel installation or shared-state mutation.
- Use GPT-6.1 Sol for bounded implementation/routine review, GPT-6 Astra for difficult integration/financial review, and GPT-6 Luna for mechanical inventories. Supply fresh-context workers with the leaf, allowed paths from the design, implemented verification command and complexity scope.
- Numeric order is the default sequence. The explicitly declared lanes below may progress in parallel using their listed dependencies and within-lane order; this is the project's requested fan-out override. A (P) marker identifies a lane entry, not permission to run dependent leaves concurrently. Other groups remain sequential.
- Foundation code is bootstrapped with measured caps and receives executable retrospective verification in 1.4. No feature acceptance precedes that gate. Whole modified upstream files must fit caps or have a measured reviewed exception; generated output is excluded, generator logic is not.
- The current Anthropic-before-Excel gate is the owner's earlier sequencing preference, not a technical dependency: Anthropic powers Workspace chat; Excel uses the application backend and data API directly. No Excel implementation, source changes, generator execution, function snapshots or image builds before 5.5 passes with current identities. Planning and generic eligibility validation are allowed earlier.
- Dagger builds/exports images only. Portable repository commands own generation, checks, image push and promotion. Deployment uses real Compose; Gitea infrastructure/migration is deferred.
- The user's explicit operator documentation and deployment requirements override the generic task rule excluding documentation/deployment. These appear as scoped verification/integration work with exercised procedures, not detached writing tasks.
- Actual Office acceptance, owner-run private-server evidence and required component entitlements are external inputs. The owner deploys locally with Compose; agent SSH access is not required. Missing evidence keeps the affected task unverified; do not fabricate acceptance or silently remove the gate.

## Exclusive lanes and joins

| Wave | Eligible work | Exclusive writable scope | Join and shared ownership |
| --- | --- | --- | --- |
| Foundation | 1.1-1.8; standalone 1.4 parser work may overlap 1.3 after its interface is frozen | 1.3 owns Python/inventory; early 1.4 owns only the TS parser and its unit tests | 1.4 integration and acceptance still require accepted 1.3; remaining foundations stay sequential |
| A: Workspace | 2.1-2.4, provisional 2.5, then 2.6-2.11 in order; 2.9 waits for 3.7 | Owned Workspace packaging, request helpers and renderer scopes/tests | Runs beside Data lane; controller serializes shared locks, catalog bindings and central builder changes |
| A: Data | 3.1-3.5 in order | Owned FMP provider and QOpenBB data-runtime paths/tests | Starts after 1.8; no central source-lock or contract snapshot writes |
| A joins | Provisional 2.5 permits 3.6-3.7; 2.9 binds that catalog; 3.8 verifies final data/catalog identity; 2.12 and 3.8 precede 4.1-4.5 | Controller serializes image builder, locks, renderer/catalog records and runtime integration | The 2.5 image is not publishable; 2.12 supplies the renderer-complete image. Changed contracts pause affected lanes; one heavy build at a time |
| B: Agent | 5.1-5.5 in order | Agent service and agent-specific tests; controller owns builder/origin integration in 5.4 | Runs beside portable delivery; no Excel work until this lane is accepted |
| B: Delivery | 7.1-7.6 in order, after 4.5 | Portable publication/promotion modules, GitHub wrappers, delivery tests and backup/restore scripts | No agent, Excel, central Dagger builder or shared schema edits; frozen schemas from 1.5 are inputs |
| C: Excel | 6.1-6.6 in order, after 5.5 | Owned add-in/generator, Excel-specific tests/assets | May overlap unfinished Delivery lane; controller owns builder/Compose join in 6.5 |
| Final join | 8.1-8.6 | Controller-owned candidate, server/Office/restore acceptance, final docs and promotion | Requires completed Excel and Delivery lanes; release evidence must match the complete candidate |

Scopes refer to the concrete paths in the design's File Structure Plan. Shared source/tool locks, schemas, breadth entries, central image builder and release manifests stay controller-owned. Workers return proposed updates; the controller merges them at joins. Test fixtures belong to their provider/agent/Excel lane; shared verification infrastructure is frozen before fan-out.

## Tasks

- [x] 1. Establish source, quality and execution foundations

- [x] 1.1 Acquire owned sources and record the candidate baseline
  - Acquire exact owned-fork revisions, select the latest API release candidate and record upstream provenance, required package inventory and component license/asset constraints.
  - Distinguish release candidates from validated releases. Record missing/commercial chart assets and remove any assumption that an upstream embedded key establishes entitlement.
  - Done when source hashes and notices are reproducible, adaptation scope is recorded, and essential unresolved asset rights are explicit release blockers.
  - Complexity: acquisition records, notices and inventory-only changes are excluded documentation/data; any maintained executable change returns to a capped production task.
  - _Boundary: Release control_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 11.1_

- [x] 1.2 Establish locked development and verification toolchains
  - Pin stable Python, Node, Bun, Dagger engine/SDK, Docker/Compose, test parsers and base image inputs; create the portable command and test-project scaffolds without application behavior.
  - Apply the owner's implementation steering: prefer pinned pnpm with Safe Chain for maintained JavaScript rewrites and uv/uvx with Safe Chain for Python. Verify protected noninteractive installs; document compatibility exceptions for preserved upstream locks.
  - Verify tools in WSL and define the clean Linux runner prerequisites. Keep runner-specific setup outside core build and verification logic.
  - Done when lock-based setup succeeds and minimal tool smoke checks report exact versions; foundation scope remains provisionally measured until the executable quality gate is complete.
  - Complexity: measure this bootstrap scope against 400 physical/300 logical/50 per-function caps; executable cross-language enforcement in 1.4 must pass before any feature work is accepted.
  - _Boundary: Release control_
  - _Depends: 1.1_
  - _Requirements: 3.1, 9.1, 9.7, 10.4_

- [x] 1.3 Implement physical and Python complexity measurements
  - Create the maintained-scope inventory and physical/Python counters using the documented syntax-unit convention; handle nested callables, docstrings, comments and newline variants.
  - Test exact cap boundaries and reject missing changed-file/base/head inputs; record fork and generated/vendor exclusions.
  - Done when deliberately oversized examples fail and the checker measures its own maintained Python scope reproducibly.
  - Complexity: measure this bootstrap scope against 400 physical/300 logical/50 per-function caps; executable cross-language enforcement in 1.4 must pass before any feature work is accepted.
  - _Boundary: Complexity and breadth_
  - _Depends: 1.2_
  - _Requirements: 10.5, 10.6_

- [x] 1.4 Complete TypeScript measurements and the cross-repository quality gate
  - After 1.2 passes, standalone parser implementation may overlap 1.3 using the controller-reviewed interface: JSON file-path array on stdin (absolute or relative to cwd), JSON measurement array on stdout preserving input paths, with each record containing path, logical and functions (name, line, column, logical; positions are 1-based). Empty input arrays return empty arrays. Parser failures use stderr and exit 2. Early writes are limited to tools/quality/syntax_units.ts and tests/quality/test_syntax_units.mjs; Python integration, inventory and breadth updates wait for 1.3 acceptance.
  - Implement the pinned TypeScript/JavaScript parser counter, expression-bodied callable handling and combined scope reports.
  - Verify whole modified upstream files and documented exceptions; do not infer changed scope from absent container Git metadata.
  - Done when both language counters pass convention fixtures, fail missing scopes, and retroactively certify foundation code from 1.2 and 1.3. Publish the actual verified command for subsequent worker briefs.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Complexity and breadth_
  - _Depends: 1.3_
  - _Requirements: 10.5, 10.6, 9.7_

- [x] 1.5 Implement typed evidence and release identity validation
  - Define source, candidate/release, backup and acceptance record validation and a portable check entry point with stable exit codes.
  - Distinguish passed, failed, skipped and unverified; reject stale revision/image/schema identities and record fixture versus live/manual evidence.
  - Done when malformed and mismatched evidence fails and a missing Anthropic acceptance record cannot make Excel eligible; link implemented checks into the breadth map.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Portable CI commands_
  - _Depends: 1.4_
  - _Requirements: 1.1, 8.1, 9.2, 9.3, 10.5, 10.6, 12.4_

- [x] 1.6 Freeze runtime, source and initial financial contract inputs
  - Build-preflight correction accepted: narrow source-namespace rules retain 32 Workspace and seven data API production paths while excluding adjacent private files. Task 1.8 must also preserve these paths through Docker context handling.
  - Freeze service names, ports, public path rules, bind-only state, credential injection names, source ownership and proposed profile/income/GDP route inventory from the approved design.
  - Retain empty public credential values and exclude local configuration, private state and evidence from build contexts. Preserve the existing private environment file.
  - Done when config validation and source-filter tests pass, worker boundaries are frozen, and initial routes remain labeled provisional until installed-schema validation in 3.7.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Release control_
  - _Depends: 1.5_
  - _Requirements: 2.1, 3.4, 3.6, 3.7, 3.8, 5.3, 5.9, 11.1, 11.6, 11.7_

- [x] 1.7 Establish isolated API and browser verification infrastructure
  - Create fixture-only provider responses, pytest markers, bounded xdist execution and a pinned headless Playwright environment with disposable accounts and output roots.
  - Provide owned-browser CDP diagnostics, sensitive-header redaction, credential-entry trace suppression and hidden Windows helpers where needed.
  - Done when isolation/failure smoke checks run without user-browser attachment, show worker bounds, and preserve sanitized reproducible results; missing live credentials remain unverified.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Verification_
  - _Depends: 1.6_
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.6_

- [x] 1.8 Implement Dagger source filtering and image export foundations
  - Implement locked owned-source acquisition, explicit context filtering, build selection and exported image provenance without adding test, generation, publication or deployment logic to Dagger.
  - Add portable image archive loading separately from Dagger and verify a small build/export/load round trip on WSL and the clean Linux runner.
  - Done when source/layer checks exclude a disposable secret sentinel, exact image identity survives export/load, and no publish credential reaches Dagger.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Dagger image builder_
  - _Depends: 1.7_
  - _Requirements: 1.1, 1.5, 3.2, 9.1, 9.6, 9.7, 11.7_

- [ ] 2. Adapt the Full Workspace baseline

- [x] 2.1 (P) Make the Full frontend build reproducible
  - Use the owned monorepo and pinned Bun frozen-lock install instead of the missing frontend npm lock and unavailable split-repository assembly.
  - Preserve the Full selection and record any narrowly required lock adaptation; keep TradingView disabled unless separately supplied and entitled.
  - Commercial packages still present are unresolved packaging inputs, not accepted dashboard capabilities. No publication before removal and new image evidence in 2.6-2.12.
  - Done when the frontend builds cleanly from recorded inputs without lock rewriting or hidden hosted source fetches.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Workspace packaging_
  - _Depends: 1.8_
  - _Requirements: 1.1, 1.4, 1.5, 3.2_

- [ ] 2.2 Stabilize application startup and private bootstrap state
  - Pin backend build dependencies, retain upstream migration/admin initialization and suppress password printing during bootstrap.
  - Include valid runtime health dependencies and protect persisted credential configuration; extract cohesive helpers before changing oversized maintained scripts if necessary.
  - Done when first startup and repeated startup use the same saved account/state and sanitized logs contain no bootstrap password.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Workspace packaging_
  - _Depends: 2.1_
  - _Requirements: 1.4, 2.2, 2.3, 4.1, 9.6_

- [ ] 2.3 Correct application authentication request boundaries
  - Replace substring backend detection with normalized origin and complete-path matching while retaining existing application session handling.
  - Regress application routes, data routes containing the API segment, lookalike prefixes, other origins and connector-supplied headers.
  - Done when application credentials attach only to the intended backend and external connector/agent requests keep their own headers.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Workspace request boundary_
  - _Depends: 2.2_
  - _Requirements: 4.3, 5.3, 5.9, 6.5_

- [ ] 2.4 Implement single-origin routing and runtime frontend settings
  - Render absolute public connector bases, configured public scheme and application URLs; add data/agent routing with correct prefix handling and stream behavior.
  - Keep optional Excel upstream absent until enabled and unavailable agent DNS/processes from blocking dashboard startup; disable hosted Copilot/enhancement calls.
  - Done when route contract tests distinguish APIs from SPA fallback, public scheme is correct, and disabled optional upstreams do not prevent origin startup.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Workspace packaging_
  - _Depends: 2.3_
  - _Requirements: 2.3, 2.4, 3.4, 3.5, 3.7, 3.8, 4.4, 12.5_

- [ ] 2.5 Build and identify the adapted Full image
  - Add the adapted Full build to the existing Dagger image builder and export its exact source-labeled image.
  - Run packaging health and fresh account smoke checks independently through portable verification; record unavailable upstream capabilities.
  - Done when the clean image loads and starts with expected Full configuration and its source/dependency identities are available for the integration join.
  - This is a provisional local packaging checkpoint, not a publishable image while commercial dependencies remain. Task 2.12 rebuilds the renderer-complete image used by 4.1.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Dagger image builder and Workspace packaging integration_
  - _Depends: 2.4_
  - _Requirements: 1.1, 1.4, 1.5, 3.2, 9.1_

- [ ] 2.6 Isolate Community tables and unsupported legacy states
  - Inventory residual grid callers and use Community-supported flat-table options/actions, retaining ordinary sorting, filters and financial formatting.
  - Hide unsupported range charts, legacy grouping/pivots, SSRM/tree/master-detail and Enterprise clipboard/XLSX actions. Preserve imported unsupported state behind an explicit unavailable view; Perspective supplies its own grouping/pivot experience later.
  - Identify oversized modified files before edits and extract cohesive responsibilities or obtain narrowly reviewed measured exceptions; do not hide a broad frontend rewrite in this task.
  - Done when focused tests exercise residual tables and unsupported imports without Enterprise API calls, and the accepted 1.4 checker passes every modified maintained file.
  - Complexity: whole modified maintained files pass 400 physical lines/file, 300 logical units/file and 50/function; record exclusions and reviewed exceptions.
  - _Boundary: Community rendering boundary_
  - _Depends: 1.4, 2.5_
  - _Requirements: 1.3, 1.4, 4.4, 4.6, 5.4, 10.5, 10.6_

- [ ] 2.7 Remove commercial renderer and dependency paths
  - Remove AG Enterprise/Highcharts imports, keys, registrations, wrappers, theme-preview paths and package/lock entries, including lazy and type-only paths. Retain inventoried supported standalone Community charts and complementary Plotly widgets.
  - Controller serializes frozen-lock/notices changes. Do not suppress license warnings or rely on tree-shaking as removal evidence.
  - Done when source/dependency/module-graph checks and a clean frontend build contain no removed commercial modules or initialization keys, with unsupported renderer tests passing; image absence is rechecked in 2.12.
  - Complexity: whole modified maintained files pass 400 physical lines/file, 300 logical units/file and 50/function; record exclusions and reviewed exceptions.
  - _Boundary: Community rendering boundary_
  - _Depends: 2.6_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 3.2, 4.4, 9.6, 10.6_

- [ ] 2.8 Establish the owned Perspective browser runtime
  - Select an exact compatible current-namespace release/plugins eligible under Safe Chain's package-age policy; verify React/Vite and protected frozen installation through the controller-owned dependency join.
  - Package same-origin WASM/worker assets and an owned React host with bounded worker allocation, explicit viewer/table cleanup, resize and light/dark handling. Add no server, database, Perspective AI or dashboard shell.
  - Done when isolated fixture browser checks mount, resize, hide/show, change theme and repeatedly unmount/remount without leaked owned resources or console/network failures.
  - Complexity: whole modified maintained files pass 400 physical lines/file, 300 logical units/file and 50/function; record exclusions and reviewed exceptions.
  - _Boundary: Perspective runtime_
  - _Depends: 2.7_
  - _Requirements: 1.1, 1.2, 3.2, 4.6, 5.5, 10.1, 10.3_

- [ ] 2.9 Integrate ready financial explorers with the accepted catalog
  - Map profile/income and FRED rows to explicit types, null/date semantics and provenance. Apply field-specific aggregation rules without default sums of ratios, EPS or incompatible currencies/units/frequencies.
  - Bind ready widget IDs, installed operations, parameters, schema versions and useful viewer defaults through the controller-owned renderer/catalog join; keep provider code renderer-independent and add no OHLC endpoint.
  - Done when fixtures prove observations and permitted aggregates, unsupported combinations fail visibly, and generated app/widget references resolve to Perspective without manual widget authoring.
  - Complexity: whole modified maintained files pass 400 physical lines/file, 300 logical units/file and 50/function; generated snapshots are excluded, adapters/generators are not.
  - _Boundary: Perspective data and widget with consumer-contract integration_
  - _Depends: 2.8, 3.7_
  - _Requirements: 4.3, 4.5, 4.6, 5.4, 5.6, 5.7, 11.3_

- [ ] 2.10 Preserve explorer configuration through refresh and reopen
  - Persist validated versioned viewer configuration, source parameters and schema identity in existing widget storage; restore columns, groups/splits, filters, aggregations, plugin settings and theme policy without treating cached rows as authoritative data.
  - Replace complete fetched data while retaining compatible settings; reject stale responses, mark last-success data on refresh failure and recover from incompatible schemas without overwriting saved configuration.
  - Done when fixture tests change parameters/configuration, remount and refresh changed observations, including out-of-order, failure/retry and incompatible-schema cases. Full application restart acceptance remains in 4.5.
  - Complexity: whole modified maintained files pass 400 physical lines/file, 300 logical units/file and 50/function; record exclusions and reviewed exceptions.
  - _Boundary: Perspective state and context_
  - _Depends: 2.9_
  - _Requirements: 2.2, 4.2, 4.7, 5.2, 5.4, 5.7, 5.8_

- [ ] 2.11 Expose configured explorer data through Workspace context
  - Capture the configured view and explicit selection scope with parameters, schema, filters, groups/splits, aggregations, units/periods and data revision; distinguish derived totals from observations.
  - Register the payload at the existing selected-widget seam. Bound exports and handle refresh/reconfiguration/removal races without truncation or full-table substitution; model credentials and inference remain in the later agent service.
  - Done when fixtures match configured/selected exports to displayed financial data and reject stale, unavailable and oversized context. Check configured-view CSV and supported chart-image output; live Anthropic grounding remains in 5.5.
  - Complexity: whole modified maintained files pass 400 physical lines/file, 300 logical units/file and 50/function; record exclusions and reviewed exceptions.
  - _Boundary: Perspective state and context with Workspace integration_
  - _Depends: 2.10_
  - _Requirements: 5.4, 10.3, 12.1, 12.3, 12.5_

- [ ] 2.12 Build and identify the renderer-complete Full image
  - Rebuild through the existing Dagger definition in the single heavy-build queue. Controller joins final Workspace locks, renderer bindings and verified data/catalog hashes into the candidate identity.
  - Run isolated fixture renderer smoke checks and inspect production chunks, installed dependencies and image contents for removed commercial packages/keys; retain notices and explicit unsupported states.
  - Done when independent review accepts fixture evidence and the new image identity, and actual test paths/artifacts reach breadth. This permits the real dashboard join, not complete release promotion or a substitute for 4.3-4.5 acceptance.
  - Complexity: modified maintained builder/helpers pass 400 physical lines/file, 300 logical units/file and 50/function; tests/evidence and generated outputs are recorded exclusions.
  - _Boundary: Dagger image builder and renderer integration_
  - _Depends: 2.11, 3.8_
  - _Requirements: 1.1, 1.2, 1.4, 3.2, 4.4, 9.1, 9.6, 10.5, 10.6_

- [ ] 3. Adapt the data API and generate supported widgets

- [ ] 3.1 (P) Restore a provenance-preserving FMP extension skeleton
  - Acquire the recorded FMP source and license, restore its provider package in the owned data fork, and restrict initial supported registration to profile and income datasets.
  - Adapt package constraints to the selected core candidate without advertising runtime compatibility; establish the locked provider-test environment with the selected shared equity/economy router packages so subsequent route-level tests have their prerequisites. Isolate unchanged imports from maintained changes.
  - Done when installed provider discovery succeeds against the candidate core and provenance/notice records identify the exact imported artifact.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Maintained FMP_
  - _Depends: 1.8_
  - _Requirements: 1.2, 1.4, 11.1, 11.2_

- [ ] 3.2 Adapt and verify the FMP profile fetcher
  - Implement the selected API's profile model/fetcher interface using the stable provider endpoint and server-side credential settings.
  - Use deterministic fixtures to check identity, financial values, available currency metadata and missing-value behavior.
  - Done when the installed shared equity profile route returns the expected typed fixture response with equivalent requested parameters.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Maintained FMP_
  - _Depends: 3.1_
  - _Requirements: 5.1, 5.4, 11.2_

- [ ] 3.3 Adapt and verify the FMP income-statement fetcher
  - Implement the annual income statement interface while preserving period, reporting date, currency and financial values supplied by the provider.
  - Verify supported symbol/period/limit behavior, response shape and null handling through the shared income route.
  - Done when route-level fixtures match the source statement without unit conversion, silently filled zeros or altered periods.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Maintained FMP_
  - _Depends: 3.2_
  - _Requirements: 5.1, 5.4, 11.2_

- [ ] 3.4 Preserve provider failures without leaking credentials
  - Adapt the shared response helper so authentication, entitlement, throttling, invalid parameters and missing data remain distinguishable.
  - Redact credential-bearing URLs/error text and prohibit fallback to a different provider or fabricated results.
  - Done when each failure fixture produces the expected observable category and sentinel secrets are absent from responses and logs.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Maintained FMP_
  - _Depends: 3.3_
  - _Requirements: 5.2, 5.3, 9.6_

- [ ] 3.5 Initialize the data runtime with FRED and shared routers
  - Install the selected owned equity/economy/FRED packages and maintained FMP extension into the locked runtime; initialize provider settings from runtime-only credentials.
  - Implement no-quota health/readiness and the design's owner-managed origin trust choice without mistaking a Workspace session for data API auth.
  - Done when profile/income/GDP routes exist, FRED values/dates/frequency/units and failure fixtures pass, and no custom database or persistent data volume is needed.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Data API runtime_
  - _Depends: 3.4_
  - _Requirements: 5.5, 5.6, 5.8, 5.9, 11.1_

- [ ] 3.6 Build and load the identified data runtime image
  - Add the locked owned data runtime to the Dagger builder using recorded local provider packages rather than accidentally resolving replacements from a registry.
  - Export/load the initial image and verify source labels, supported routes and server credential initialization; generation consumes this exact loaded image in the next task.
  - Done when a clean identified image is available to the portable generation command without requiring generated contract snapshots as a build input.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Dagger image builder and data API integration_
  - _Depends: 2.5, 3.5_
  - _Requirements: 1.1, 1.5, 3.2, 9.1, 11.1_

- [ ] 3.7 Freeze installed routes and regenerate the supported catalog
  - Join the schema served by the loaded image from 3.6 to the provisional dataset inventory; pin operation IDs, parameters and responses only after provider registration succeeds.
  - Implement portable canonical schema/widget/app generation using upstream generators, a mixed-source starter dashboard and the bundled FRED app where compatible.
  - Done when repeated generation has identical hashes, all references resolve, supported mappings are explicit and contract changes stop affected lanes for revalidation.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Consumer contracts and data API integration_
  - _Depends: 3.6_
  - _Requirements: 4.3, 4.5, 5.4, 11.1, 11.3_

- [ ] 3.8 Verify the served image and catalog identity
  - Wait for the controller-owned Perspective bindings from 2.9 before final catalog/image verification; no renderer worker writes shared snapshots independently.
  - Compare the actual image's served schema/catalog with generated snapshots and verify provider credentials are absent from image layers and metadata.
  - If the starter catalog or generated assets must be embedded, rebuild through Dagger after generation and rerun generation/reference checks against that final image; do not reuse prior image evidence.
  - Done when the loaded final image, served metadata and canonical contract hashes agree; retain candidate status until the dashboard live-acceptance join.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Consumer contracts and data API integration_
  - _Depends: 3.7, 2.9_
  - _Requirements: 1.1, 4.3, 4.5, 5.3, 5.9, 9.6, 11.1, 11.3_

- [ ] 4. Join and accept the dashboard baseline

- [ ] 4.1 Implement the controlling Compose definition and preflight
  - Create image-only runtime control with one HTTP publication, project-relative application binds, separate provider/agent credentials and an optional Excel profile.
  - Distinguish identified local candidates from production digests; validate configuration names without values and reject placeholder selected images, wrong mounts and unsafe state roots.
  - For the dashboard checkpoint, explicitly start only Workspace and data-api from the unchanged Compose definition. Preflight validates selected images; an inactive parser-only agent reference must never be pulled, started or published, and Workspace has no startup dependency on agent.
  - Done when tests pass with no agent image available and inactive Excel needs no image. Full baseline startup and release acceptance require the real agent image.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Runtime control_
  - _Depends: 2.12, 3.8_
  - _Requirements: 2.1, 2.3, 2.4, 3.1, 3.4, 3.6, 3.7, 3.8, 11.6_

- [ ] 4.2 Exercise real Compose lifecycle in isolated run directories
  - Implement the direct host Compose harness using unique project names, validated daemon-host roots, archive loading, explicit selected services and owned cleanup; prove the dashboard checkpoint never pulls or starts the inactive agent.
  - Verify actual mounts, fixed port publication, restart behavior, actionable port collisions and rejection of unsupported remote-daemon path assumptions.
  - Done when WSL and clean Linux fixture runs produce equivalent inspected topology and cleanup affects only their own services/data.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Verification and runtime integration_
  - _Depends: 4.1_
  - _Requirements: 2.1, 2.2, 2.3, 3.1, 3.6, 10.4_

- [ ] 4.3 Verify dashboard discovery and editing in the real frontend
  - Implement the real Playwright account/login and connector registration journey against absolute same-origin catalog URLs.
  - Exercise FMP/FRED discovery, add/arrange/resize/remove operations and observable widget content, with console/network diagnostics.
  - Verify ready Perspective explorers, grouping/pivot/filter changes and table/chart switching; assert unsupported legacy controls stay unavailable and residual Community tables still render.
  - Done when assertions verify resulting dashboard layout/data rather than only UI notifications or HTTP success; preserve an executable regression.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Verification and Workspace integration_
  - _Depends: 4.2_
  - _Requirements: 4.1, 4.3, 4.5, 4.6, 10.1, 10.2, 10.3_

- [ ] 4.4 Verify mixed-provider financial fidelity and failure states
  - Compare equivalent Workspace/API parameters and fixture values with units, currency, period and available frequency metadata; include visible failed refresh behavior.
  - Compare configured-view aggregates and exports with independent fixture calculations; prove missing values and incompatible units are not silently coerced, and failed refresh preserves visibly stale last-success data until recovery.
  - Run separately marked entitled live FMP profile/income and FRED GDP checks with narrowly injected local keys.
  - Done when both sources refresh and comparison evidence is recorded; missing entitlement, skipped live checks or substituted data cannot pass baseline acceptance.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Verification and data API integration_
  - _Depends: 4.3_
  - _Requirements: 5.1, 5.2, 5.4, 5.6, 5.7, 5.8, 10.3, 11.2_

- [ ] 4.5 Accept dashboard persistence and the validated API baseline
  - Save widget parameters/layout, stop and restart the environment, sign in again and verify reopen/refresh against the same source/image set.
  - Preserve Perspective columns, groups/splits, filters, aggregation and plugin/theme settings across restart; assert refreshed observations and configured-view context match the new data revision.
  - Join clean-build, contract, financial and UI evidence; update selected release validation status and list unavailable hosted/chart capabilities honestly.
  - Done when independent review accepts a current dashboard baseline record and the breadth map distinguishes accepted, failing and untested capabilities.
  - Complexity: tests and evidence are excluded; any maintained runner or helper changed here passes the 400 physical/300 logical/50 per-function caps.
  - _Boundary: Verification and Workspace integration_
  - _Depends: 4.4_
  - _Requirements: 2.2, 4.2, 4.4, 4.7, 8.1, 10.5, 10.6, 11.1_

- [ ] 5. Implement and accept Anthropic

- [ ] 5.1 Establish the typed agent service and discovery contract
  - Pin compatible SDK/client artifacts, initialize the service's runtime configuration and local health checks, and expose only implemented custom-agent capabilities.
  - Generate the stable agent identity and external query URL from public configuration; do not load provider or application signing keys.
  - Done when request/discovery fixtures validate against the pinned frontend protocol and health checks spend no model quota.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Anthropic agent_
  - _Depends: 4.5_
  - _Requirements: 12.1, 12.3_

- [ ] 5.2 Implement selected-widget continuation without retrieval loops
  - Handle the initial selected-widget descriptors by requesting browser-side data and completing that stream, then process the subsequent tool-result request.
  - Validate message roles, result identities, available metadata and bounded context; reject unavailable/oversized data explicitly without silently truncating observations.
  - Done when continuation/error fixtures prove exactly the required retrieval cycle and no arbitrary server-side widget URL fetching occurs.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Anthropic agent_
  - _Depends: 5.1_
  - _Requirements: 12.1, 12.2_

- [ ] 5.3 Stream Anthropic output with explicit model and failure behavior
  - Translate the validated conversation into Anthropic requests and frontend-compatible text/status events using the exact configured model.
  - Implement cancellation, request limits, auth/model errors and partial-stream handling without automatic model substitution or secret/payload logging.
  - Done when simulated stream/error cases pass and an authorized minimal inference validates the chosen model; model listing alone is insufficient.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Anthropic agent_
  - _Depends: 5.2_
  - _Requirements: 12.1, 12.2, 12.3_

- [ ] 5.4 Build and register the agent without coupling dashboard health
  - Add the real agent image to Dagger's build-only catalog and connect it through the established origin route and existing custom-agent configuration; join the full required service set and reject any parser-only inactive reference.
  - Keep hosted Copilot enhancements disabled; verify stream buffering/timeouts and dashboard operation while the agent is stopped.
  - Done when discovery and a real streamed response work through the configured origin and the data/dashboard journey survives agent unavailability.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Anthropic agent and Workspace integration_
  - _Depends: 5.3_
  - _Requirements: 2.1, 12.1, 12.3, 12.5_

- [ ] 5.5 Accept grounded Workspace AI and unlock Excel work
  - Preserve a Playwright journey selecting a known financial observation and assert that the live answer uses its value, period and unit; include cancellation and visible failures.
  - Tie the independent acceptance record to exact Workspace, data and agent identities plus model and contract hashes.
  - Done when the reviewed current record passes the eligibility validator; otherwise every Excel source, generator, snapshot and image task remains blocked.
  - Complexity: tests and evidence are excluded; any maintained runner or helper changed here passes the 400 physical/300 logical/50 per-function caps.
  - _Boundary: Verification and Anthropic integration_
  - _Depends: 5.4_
  - _Requirements: 8.1, 10.3, 10.5, 10.6, 12.1, 12.2, 12.4, 12.5_

- [ ] 6. Adapt Excel after Anthropic acceptance

- [ ] 6.1 Prepare the add-in and split oversized generator responsibilities
  - Only after agent acceptance, install the locked add-in dependencies and record exact package/asset provenance and unresolved rights.
  - Extract schema-input and compatibility responsibilities from oversized maintained generators without changing the existing supported function behavior.
  - Done when baseline generator fixtures still pass, required source files fit their measured budgets or reviewed exceptions, and unsupported dependencies remain explicit.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Excel adaptation_
  - _Depends: 5.5_
  - _Requirements: 1.2, 1.3, 1.4, 6.5, 11.4_

- [ ] 6.2 Regenerate Excel functions from accepted local contracts
  - Replace private/PAT-based schema fetches with accepted local OpenAPI/widgets and generate supported functions deterministically.
  - Compare namespace, names, argument order/defaults, request paths and spill shapes against prior contracts; retain compatibility wrappers where necessary.
  - Done when contract fixtures pass, repeated output is stable and the machine-readable compatibility report lists workbook impacts.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Excel adaptation_
  - _Depends: 6.1_
  - _Requirements: 6.4, 6.5, 11.3, 11.4_

- [ ] 6.3 Adapt Excel application login and data requests
  - Keep self-hosted application login/session semantics and use the same public data base without assuming its authentication accepts the app bearer.
  - Handle expiry, failed data requests and response envelopes while keeping provider and Cloudflare service secrets out of client assets.
  - Done when controlled login/data/expiry fixtures exercise the expected paths, headers and displayed failures.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Excel adaptation_
  - _Depends: 6.2_
  - _Requirements: 6.2, 6.3, 6.5, 5.3, 5.9_

- [ ] 6.4 Make manifest and add-in URLs deployment-configurable
  - Render runtime public-origin configuration and the trusted HTTPS manifest consistently without rebuilding application images for WSL versus Linux.
  - Preserve the supported function namespace and SharedRuntime contract; distinguish development access from actual Office HTTPS acceptance.
  - Done when two public URL settings produce coherent manifest/assets from the same image inputs and contract checks reject mismatched origins.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Excel adaptation_
  - _Depends: 6.3_
  - _Requirements: 3.3, 3.7, 6.1, 6.5_

- [ ] 6.5 Build Excel assets and integrate the optional runtime profile
  - Add the static add-in image to the Dagger build-only catalog and connect the already defined optional origin route/profile.
  - Verify enabling or disabling the add-in does not change accepted Workspace, data or agent behavior and does not require origin TLS management.
  - Done when the selected image loads correctly through the profile and shared regressions still pass.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Excel adaptation and runtime integration_
  - _Depends: 6.4_
  - _Requirements: 2.4, 6.1, 9.1, 11.5_

- [ ] 6.6 Prepare reproducible Office acceptance inputs
  - Establish a validation workbook/procedure for the supported FMP function with explicit expected values/shape, refresh and reopen checks.
  - Record manifest/function/schema hashes and compatibility expectations; automate all generator/client checks that do not require a real Office host.
  - Done when the input bundle is reproducible and ready for actual Windows Excel testing against a published candidate; browser checks are not labeled Office acceptance.
  - Complexity: tests and evidence are excluded; any maintained runner or helper changed here passes the 400 physical/300 logical/50 per-function caps.
  - _Boundary: Verification and Excel integration_
  - _Depends: 6.5_
  - _Requirements: 6.3, 6.4, 6.5, 11.4, 11.5_

- [ ] 7. Build portable delivery and recovery commands

- [ ] 7.1 (P) Implement portable image publication and candidate identities
  - Load and push exact exported images using configurable registry/source inputs and ephemeral credentials, without rebuilding or giving registry credentials to Dagger.
  - Write unpromoted candidate manifests only for complete selected image sets and verify pushed digest identity.
  - Done when registry integration fixtures prove partial pushes cannot create a complete candidate and publication runs without GitHub-specific inputs.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Portable CI commands_
  - _Depends: 4.5_
  - _Requirements: 1.1, 9.2, 9.6, 9.7_

- [ ] 7.2 Implement release promotion with matching evidence gates
  - Validate full candidate completeness and required live, fixture, Office, Linux and recovery records against exact digests/contracts.
  - Keep internal dashboard/agent checkpoints distinct from complete baseline releases; require prior agent eligibility before accepting Excel work records.
  - Done when absent, stale, skipped and failing records block promotion, while matching complete fixtures produce immutable release settings.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Portable CI commands_
  - _Depends: 7.1_
  - _Requirements: 8.1, 9.2, 9.3, 9.5, 10.6, 12.4_

- [ ] 7.3 Add thin GitHub runners for the portable commands
  - Create pinned verification/release wrappers limited to checkout, setup, permission/secret plumbing, command invocation and artifact retention.
  - Separate untrusted fixture checks from authorized live/publication runs and enforce Excel eligibility before invoking its build/generation tasks.
  - Done when wrapper validation and a clean runner exercise build-only Dagger plus portable verification without duplicated pipeline logic.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Portable CI commands_
  - _Depends: 7.2_
  - _Requirements: 9.1, 9.2, 9.3, 9.6, 9.7_

- [ ] 7.4 Prove the CI command boundary is portable to another runner
  - Invoke the same build/check/publication interfaces in clean Linux with no GitHub-specific environment or API.
  - Vary explicit registry/source/run inputs and verify documented exit/report contracts; retain platform-specific artifact/secret setup only in wrappers.
  - Done when portability checks pass and actual Gitea deployment remains explicitly untested and out of this baseline.
  - Complexity: tests and evidence are excluded; any maintained runner or helper changed here passes the 400 physical/300 logical/50 per-function caps.
  - _Boundary: Verification and portable CI integration_
  - _Depends: 7.3_
  - _Requirements: 9.1, 9.7, 10.6_

- [ ] 7.5 Implement consistent stopped-state backups
  - Capture the stopped Workspace bind tree and a backup manifest tying checksums, ownership, state format and source/image identities together.
  - Handle private runtime configuration separately from public release artifacts and prevent accidental overwrite of the only usable snapshot.
  - Done when backup tests reject running/inconsistent state and secret files never enter public reports.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Runtime control_
  - _Depends: 7.4_
  - _Requirements: 8.2, 8.3, 8.4, 9.5_

- [ ] 7.6 Implement clean restore and incompatible rollback protection
  - Restore verified snapshots into new owned directories using the matching image set; check path boundaries, checksums and file ownership.
  - Reject older images against incompatible migrated state and preserve the original deployment on failure.
  - Done when restore fixtures recover known state, fail corrupted/incompatible inputs safely and record the required previous snapshot for rollback.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Runtime control_
  - _Depends: 7.5_
  - _Requirements: 8.2, 8.3, 8.4, 9.5_

- [ ] 8. Accept the complete candidate and promote the release

- [ ] 8.1 Publish the complete unpromoted baseline candidate
  - Join exact fork revisions, locked builds, supported component rights, contract snapshots and all selected image digests into one complete candidate.
  - Resolve essential component availability/license decisions before acceptance; do not reuse upstream enterprise keys as entitlement evidence.
  - Done when the candidate can be pulled without source builds and its manifest contains no placeholder image, unresolved essential asset or secret.
  - Complexity: execution and evidence-only work has no production-code scope; needed fixes reopen their owning capped task and invalidate affected acceptance.
  - _Boundary: Release control integration_
  - _Depends: 6.6, 7.4, 7.6_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 9.2, 9.6, 11.1_

- [ ] 8.2 Accept pull-only WSL and private Linux operation
  - Use the exact candidate image set in clean WSL and private Linux deployment directories; run the same topology with environment-specific public URL.
  - Verify public HTTPS through the owner's existing Access tunnel, plain HTTP origin publication, bind state, application login and marked provider/agent checks.
  - Done when no application compilation occurs on the target and evidence records actual host, image and route identities. The owner runs Compose locally on the private host and can supply acceptance evidence; missing host evidence remains unverified without requiring agent SSH access.
  - Complexity: execution and evidence-only work has no production-code scope; needed fixes reopen their owning capped task and invalidate affected acceptance.
  - _Boundary: Runtime control integration_
  - _Depends: 8.1_
  - _Requirements: 2.1, 2.3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 9.4_

- [ ] 8.3 Accept the candidate in Windows Excel
  - Load the candidate manifest in the supported Windows Excel host and exercise trusted assets, Access/session behavior and self-hosted application login.
  - Calculate the supported FMP function, compare the equivalent API result, refresh and reopen the validation workbook without signature changes.
  - Done when Office version, manifest/schema/image hashes and observed workbook results are recorded; unsupported host/access behavior blocks acceptance rather than being replaced by browser evidence.
  - Complexity: execution and evidence-only work has no production-code scope; needed fixes reopen their owning capped task and invalidate affected acceptance.
  - _Boundary: Verification and Excel integration_
  - _Depends: 8.2_
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 11.5_

- [ ] 8.4 Accept recovery against the complete candidate
  - Create a stopped snapshot with a known saved dashboard, restore into another clean directory and start the matching pulled image set.
  - Verify account sign-in, widget layout/parameters and live refresh after restore, plus a rejected incompatible rollback.
  - Done when recovery succeeds without altering the only original deployment and prior image/state requirements are recorded.
  - Complexity: execution and evidence-only work has no production-code scope; needed fixes reopen their owning capped task and invalidate affected acceptance.
  - _Boundary: Runtime control integration_
  - _Depends: 8.3_
  - _Requirements: 2.2, 4.2, 4.7, 8.2, 8.3, 8.4, 9.5_

- [ ] 8.5 Close cross-component verification and operator guidance
  - Run the final shared-module complexity audit, relevant secret/layer/log/browser checks and all required regressions against candidate identities.
  - Reconcile every breadth entry with actual checks and sanitized evidence; update financial-engineer development/deployment/recovery/compatibility guidance using the commands just exercised.
  - Done when all required criteria have current passing evidence, capability limitations are explicit, and README/docs navigation leads to accurate procedures.
  - Complexity: all maintained production scopes pass the 400 physical/300 logical/50 per-function audit; tests, generated artifacts and documentation exclusions are explicit.
  - _Boundary: Verification and documentation integration_
  - _Depends: 8.4_
  - _Requirements: 1.3, 1.4, 3.4, 8.1, 9.6, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 11.6, 11.7, 12.3_

- [ ] 8.6 Promote and install the accepted immutable release
  - Run the portable promotion gate on the complete accepted candidate and preserve previous release/backup identifiers.
  - Install by pulling promoted digests and starting without builds; confirm the promoted set matches the accepted candidate and optional Excel leaves the other services usable.
  - Done when the release manifest, installation result and recovery references agree; no check is passed by skipping or relabeling missing evidence.
  - Complexity: execution and evidence-only work has no production-code scope; needed fixes reopen their owning capped task and invalidate affected acceptance.
  - _Boundary: Release control and runtime integration_
  - _Depends: 8.5_
  - _Requirements: 2.4, 8.1, 9.2, 9.3, 9.4, 9.5, 11.5_
