# Implementation plan

Design approved by the owner on 2026-10-16 ("go"). The owner approved these implementation tasks on 2026-10-16 ("approve"). Unchecked tasks remain unimplemented or unverified. Each executable leaf targets one 1-3 hour engineering work unit; investigate unexpected scope before splitting a task, rather than silently expanding it. External access, entitlement decisions and build waits are not promised completion times.

The separately approved chart-foundation design has [six foundation tasks](#approved-design-slice-chart-state-and-lifecycle-foundation), approved by the owner on 2026-10-16. Its explicit dependency branch overrides the historical numeric sequence only within that scope. [Independent task review](chart-foundation-task-review.md) passed.

## Execution contract

Renderer amendment, 2026-10-16: the owner selected "Use Perspective baseline". Tasks 2.6-2.12 add the selected viewer and remove commercial dependencies without renumbering prior tasks. Independent controller task-graph sanity review passed after splitting Community isolation from commercial removal; independent amendment review still precedes renderer feature work. No new renderer task is implemented or accepted by this plan.

Superseding owner constraint, 2026-10-16: preserve existing UX, design, themes, functional capabilities and feature-flag behavior. Follow [Workspace experience](../../steering/workspace-experience.md). Instructions below to hide or disable existing actions, or accept unavailable legacy features, are superseded. Completed task checkboxes record historical acceptance only. Renderer and release acceptance now require a capability inventory against the original owned OpenBB source, explicit identification of gaps introduced by tasks 2.6-2.7, and equivalent working replacements with verification evidence. The modified Community baseline cannot redefine the required capabilities. Reconcile affected requirements, design, tasks and breadth coverage before further renderer implementation.

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

- [x] 2.2 Stabilize application startup and private bootstrap state
  - Pin backend build dependencies, retain upstream migration/admin initialization and suppress password printing during bootstrap.
  - Include valid runtime health dependencies and protect persisted credential configuration; extract cohesive helpers before changing oversized maintained scripts if necessary.
  - Done when first startup and repeated startup use the same saved account/state and sanitized logs contain no bootstrap password.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Workspace packaging_
  - _Depends: 2.1_
  - _Requirements: 1.4, 2.2, 2.3, 4.1, 9.6_

- [x] 2.3 Correct application authentication request boundaries
  - Replace substring backend detection with normalized origin and complete-path matching while retaining existing application session handling.
  - Regress application routes, data routes containing the API segment, lookalike prefixes, other origins and connector-supplied headers.
  - Done when application credentials attach only to the intended backend and external connector/agent requests keep their own headers.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Workspace request boundary_
  - _Depends: 2.2_
  - _Requirements: 4.3, 5.3, 5.9, 6.5_

- [x] 2.4 Implement single-origin routing and runtime frontend settings
  - Render absolute public connector bases, configured public scheme and application URLs; add data/agent routing with correct prefix handling and stream behavior.
  - Keep optional Excel upstream absent until enabled and unavailable agent DNS/processes from blocking dashboard startup; disable hosted Copilot/enhancement calls.
  - Done when route contract tests distinguish APIs from SPA fallback, public scheme is correct, and disabled optional upstreams do not prevent origin startup.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Workspace packaging_
  - _Depends: 2.3_
  - _Requirements: 2.3, 2.4, 3.4, 3.5, 3.7, 3.8, 4.4, 12.5_

- [x] 2.5 Build and identify the adapted Full image
  - Add the adapted Full build to the existing Dagger image builder and export its exact source-labeled image.
  - Run packaging health and fresh account smoke checks independently through portable verification; record unavailable upstream capabilities.
  - Done when the clean image loads and starts with expected Full configuration and its source/dependency identities are available for the integration join.
  - This is a provisional local packaging checkpoint, not a publishable image while commercial dependencies remain. Task 2.12 rebuilds the renderer-complete image used by 4.1.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Dagger image builder and Workspace packaging integration_
  - _Depends: 2.4_
  - _Requirements: 1.1, 1.4, 1.5, 3.2, 9.1_

- [x] 2.6 Isolate Community tables and unsupported legacy states
  - Inventory residual grid callers and use Community-supported flat-table options/actions, retaining ordinary sorting, filters and financial formatting.
  - Hide unsupported range charts, legacy grouping/pivots, SSRM/tree/master-detail and Enterprise clipboard/XLSX actions. Preserve imported unsupported state behind an explicit unavailable view; Perspective supplies its own grouping/pivot experience later.
  - Identify oversized modified files before edits and extract cohesive responsibilities or obtain narrowly reviewed measured exceptions; do not hide a broad frontend rewrite in this task.
  - Done when focused tests exercise residual tables and unsupported imports without Enterprise API calls, and the accepted 1.4 checker passes every modified maintained file.
  - Complexity: whole modified maintained files pass 400 physical lines/file, 300 logical units/file and 50/function; record exclusions and reviewed exceptions.
  - _Boundary: Community rendering boundary_
  - _Depends: 1.4, 2.5_
  - _Requirements: 1.3, 1.4, 4.4, 4.6, 5.4, 10.5, 10.6_

- [x] 2.7 Remove commercial renderer and dependency paths
  - Remove AG Enterprise/Highcharts imports, keys, registrations, wrappers, theme-preview paths and package/lock entries, including lazy and type-only paths. Retain inventoried supported standalone Community charts and complementary Plotly widgets.
  - Controller serializes frozen-lock/notices changes. Do not suppress license warnings or rely on tree-shaking as removal evidence.
  - Done when source/dependency/module-graph checks and a clean frontend build contain no removed commercial modules or initialization keys, with unsupported renderer tests passing; image absence is rechecked in 2.12.
  - Complexity: whole modified maintained files pass 400 physical lines/file, 300 logical units/file and 50/function; record exclusions and reviewed exceptions.
  - _Boundary: Community rendering boundary_
  - _Depends: 2.6_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 3.2, 4.4, 9.6, 10.6_

- [x] 2.8 Establish the owned Perspective browser runtime
  - Select an exact compatible current-namespace release/plugins eligible under Safe Chain's package-age policy; verify React/Vite and protected frozen installation through the controller-owned dependency join.
  - Package same-origin WASM/worker assets and an owned React host with bounded worker allocation, explicit viewer/table cleanup, resize and light/dark handling. Add no server, database, Perspective AI or dashboard shell.
  - Done when isolated fixture browser checks mount, resize, hide/show, change theme and repeatedly unmount/remount without leaked owned resources or console/network failures.
  - Complexity: whole modified maintained files pass 400 physical lines/file, 300 logical units/file and 50/function; record exclusions and reviewed exceptions.
  - _Boundary: Perspective runtime_
  - _Depends: 2.7_
  - _Requirements: 1.1, 1.2, 3.2, 4.6, 5.5, 10.1, 10.3_

- [ ] 2.9 Integrate ready financial explorers with the accepted catalog
  - Preserve OpenBB's existing widget framing, controls and styling; keep renderer differences local and verify light/dark visual consistency under [the owner constraint](../../steering/workspace-experience.md). No dashboard redesign or unrelated frontend rewrite.
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

- [x] 3.1 (P) Restore a provenance-preserving FMP extension skeleton
  - Acquire the recorded FMP source and license, restore its provider package in the owned data fork, and restrict initial supported registration to profile and income datasets.
  - Adapt package constraints to the selected core candidate without advertising runtime compatibility; establish the locked provider-test environment with the selected shared equity/economy router packages so subsequent route-level tests have their prerequisites. Isolate unchanged imports from maintained changes.
  - Done when installed provider discovery succeeds against the candidate core and provenance/notice records identify the exact imported artifact.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Maintained FMP_
  - _Depends: 1.8_
  - _Requirements: 1.2, 1.4, 11.1, 11.2_

- [x] 3.2 Adapt and verify the FMP profile fetcher
  - Implement the selected API's profile model/fetcher interface using the stable provider endpoint and server-side credential settings.
  - Use deterministic fixtures to check identity, financial values, available currency metadata and missing-value behavior.
  - Done when the installed shared equity profile route returns the expected typed fixture response with equivalent requested parameters.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Maintained FMP_
  - _Depends: 3.1_
  - _Requirements: 5.1, 5.4, 11.2_

- [x] 3.3 Adapt and verify the FMP income-statement fetcher
  - Implement the annual income statement interface while preserving period, reporting date, currency and financial values supplied by the provider.
  - Verify supported symbol/period/limit behavior, response shape and null handling through the shared income route.
  - Done when route-level fixtures match the source statement without unit conversion, silently filled zeros or altered periods.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Maintained FMP_
  - _Depends: 3.2_
  - _Requirements: 5.1, 5.4, 11.2_

- [x] 3.4 Preserve provider failures without leaking credentials
  - Adapt the shared response helper so authentication, entitlement, throttling, invalid parameters and missing data remain distinguishable.
  - Redact credential-bearing URLs/error text and prohibit fallback to a different provider or fabricated results.
  - Done when each failure fixture produces the expected observable category and sentinel secrets are absent from responses and logs.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Maintained FMP_
  - _Depends: 3.3_
  - _Requirements: 5.2, 5.3, 9.6_

- [x] 3.5 Initialize the data runtime with FRED and shared routers
  - Install the selected owned equity/economy/FRED packages and maintained FMP extension into the locked runtime; initialize provider settings from runtime-only credentials.
  - Implement no-quota health/readiness and the design's owner-managed origin trust choice without mistaking a Workspace session for data API auth.
  - Done when profile/income/GDP routes exist, FRED values/dates/frequency/units and failure fixtures pass, and no custom database or persistent data volume is needed.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Data API runtime_
  - _Depends: 3.4_
  - _Requirements: 5.5, 5.6, 5.8, 5.9, 11.1_

- [x] 3.6 Build and load the identified data runtime image
  - Add the locked owned data runtime to the Dagger builder using recorded local provider packages rather than accidentally resolving replacements from a registry.
  - Export/load the initial image and verify source labels, supported routes and server credential initialization; generation consumes this exact loaded image in the next task.
  - Done when a clean identified image is available to the portable generation command without requiring generated contract snapshots as a build input.
  - Complexity: the task's entire modified maintained production scope passes 400 physical lines/file, 300 logical units/file and 50/function using the implemented checker; record generated exclusions and reviewed exceptions.
  - _Boundary: Dagger image builder and data API integration_
  - _Depends: 2.5, 3.5_
  - _Requirements: 1.1, 1.5, 3.2, 9.1, 11.1_

- [x] 3.7 Freeze installed routes and regenerate the supported catalog
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

- Task 2.4 process note: original RED was an artificial unconditional failure, so test-first compliance is not established. Independent review accepted current behavior after three explicitly retrospective baseline failures and fresh nginx/lint/size checks; artifacts/task-2.4/evidence.json preserves the chronology.
- Task 2.5 packaging note: pinned Dagger requires serial SDK initialization and checksum-preserving HTTP ADD translation. Exact source exceptions retain the frontend build helper and Data component. Independent review reproduced 68 tests and fresh image runtime acceptance; artifacts/task-2.5 holds the identities and evidence. The image remains provisional until renderer replacement.
- Task 2.6 review note: independent review caught pagination settings and saved Set/Multi filter compatibility regressions. Both were repaired with retained failing tests and fresh independent checks. Original implementation RED was captured only in the worker tool transcript; remediation RED logs are retained under artifacts/task-2.6. Whole-project typechecking remains blocked by the unchanged upstream configuration; lint, actual build and focused tests passed.

Task 2.7 accepted after independent Astra review: 70 independently rerun task tests and 10 audit controls passed; the protected clean install, production build, 6,488-module graph and 258 JavaScript chunks contain no removed commercial modules or initialization. Workspace `0341b12524cb822262be631fa820e2ca851a348a`. Exact 55-path snapshot and review evidence: `artifacts/task-2.7/joined-freeze.json`, `review-verification.json`, `committed-complexity.json`. Seven no-growth type-import exceptions are documented in [the narrow review](task-2.7-exception-review.md). Full typechecking remains blocked by upstream configuration; real browser and final-image checks remain later gates.

Task 2.8 accepted after independent Astra review and one repair round. Workspace `48e3f59cc48e0ae7aa6f6ce92069fc5b10ee3e86` adds the owned Perspective 5.6.0 runtime with same-origin worker/WASM assets. Independent 10 unit tests, strict selected TypeScript, Biome and four production browser cases passed; development cases also passed. A reproduced stale-theme rejection race was repaired and retained as a regression. Full-project TypeScript and integrated dashboard visual/financial acceptance remain outside this gate. Evidence: `artifacts/task-2.8/review-round2-verification.json`, `runtime-freeze.json`, `browser-evidence.json` and `committed-complexity.json`. Initial feature RED is retained; the earlier initialization-cleanup regression was GREEN-first, not retrospectively described as TDD.

## Approved design slice: chart state and lifecycle foundation

The owner approved the [first production boundary](echarts-integration-proposal.md#first-production-boundary-for-separate-review) on 2026-10-16. Tasks 2.13-2.18 below were approved by the owner on 2026-10-16 for that boundary only. They neither reactivate superseded tasks 2.9-2.12 nor approve the rest of the renderer design. They support 4.8-4.9 without closing either requirement. Existing task groups retain their own coverage and approval states.

This is an explicit dependency exception to the historical numeric renderer sequence: 2.13 starts from accepted 1.2, 1.4, 1.7 and 2.8, not from pending 2.9-2.12 or later release tasks. Thereafter the dependencies below govern this slice. All leaves target one bounded 1-3 hour engineering work unit; unexpected scope returns to the controller rather than expanding ownership silently.

### Ownership and parallel execution

Workspace paths below are relative to `terminalpro/`; root paths are relative to QOpenBB. New paths are planned, not completed assets. State and host workers are not alone: preserve other work and never revert the untracked financial lane or pending catalog/inventory changes.

| Task/lane | Exclusive writable scope | Prerequisite / model |
| --- | --- | --- |
| 2.13 setup | Workspace package/lock, new `tests/unit/chart-compatibility/vitest.config.mjs`, focused `tsconfig.json`, `tests/e2e/chart-compatibility/` Vite/Playwright fixture setup; root complexity inventory and dependency documentation | Accepted 1.2, 1.4, 1.7, 2.8; controller serializes setup |
| 2.14 contracts | `src/components/General/Table/Chart/compatibility/legacyTypes.ts`; host interface declarations in `Chart/echarts/lifecycle.ts`; contract fixtures/type checks under `tests/unit/chart-compatibility/` | 2.13; controller/Sol, then freeze shared contracts |
| 2.15 state lane | `Chart/compatibility/integratedState.ts`, `detachedState.ts`; corresponding unit fixtures/tests | 2.14; Sol |
| 2.16-2.17 host lane | `Chart/echarts/lifecycle.ts`, `EChartsHost.tsx`; host unit tests and `tests/e2e/chart-compatibility/` fixture/spec files | 2.14, then 2.16; Sol |
| 2.18 join | Controller-owned test scripts/config registration if necessary; inventory, breadth, scoped evidence/docs and source identity records | 2.15 and 2.17; controller with independent Astra review |

Full paths for the new `Chart/` modules resolve under `src/components/General/Table/`. Controller owns package/lock, shared configuration, scope inventory, commits and any root command join throughout. Foundation config ownership transfers to the host lane only after 2.14 freezes interfaces; no concurrent writes to shared files. At most controller + two workers + one reviewer; one heavy install/build/browser at a time. State unit work may overlap host work. Astra reviews state semantics and lifecycle evidence. Each code leaf requires implementation, independent review and fresh verification before its checkbox closes.

Application call sites, `communityBoundary` guards, widget registry/catalog bindings, editor UI, chart-family translation, provider/backend code and release promotion are excluded. The foundation connects through maintained module and browser tests, not a partially enabled product path. Further application integration requires its own approved design/tasks. Anthropic-before-Excel and Dagger-build-only rules remain unchanged.

### Foundation verification contract

Reuse the existing narrow Perspective test patterns without changing their files. Adapted chart commands below are planned until implemented and exercised from the owned Workspace `terminalpro/` directory:

```sh
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs
node node_modules/typescript/bin/tsc --project tests/unit/chart-compatibility/tsconfig.json --noEmit
node node_modules/vite/bin/vite.js build --config tests/e2e/chart-compatibility/vite.config.ts
node <QOPENBB_ROOT>/verification/node_modules/@playwright/test/cli.js test --config tests/e2e/chart-compatibility/playwright.config.ts
```

The Playwright config owns a loopback-only preview server for the freshly built fixture, rejects more than one worker, uses a fresh browser context and never reuses an operator server. Set the documented project-local browser cache explicitly. Vite fixture configuration uses `envDir: false`; tests do not load `.env`, real credentials or provider data. Capture CDP runtime/console/network diagnostics, screenshot/output identities, exits and cleanup. A build or module-presence check is not a rendered-data assertion.

Use the existing [complexity gate](../../../docs/complexity.md) from QOpenBB with explicit current fork base/head or changed-file manifests for both forks. Do not reuse historical scope SHAs or an empty manifest to bypass this lane's changes. Setup must establish and freeze the exact executable scoped command before accepting 2.14 onward. Preserve unrelated unfinished work through isolated snapshots or accurately scoped manifests; do not claim a clean checkout when it is dirty.

Whole-project TypeScript remains separately blocked by upstream TS6305 composite-output and TS5103 configuration issues. These tasks require strict checks of the complete new module/test/fixture dependency closure and cannot relabel that as whole-application typecheck success. Test helpers/fixtures and docs have explicit policy exclusions; maintained build/production logic cannot hide there.

- [x] 2.13 Prepare protected chart dependencies and isolated verification
  - Pin ECharts 6.0.0 in the owned application with the existing validated Bun lock exception; verify Safe Chain interception, the 48-hour age policy and protected frozen restoration. Retain notices and dependency provenance; do not migrate the application lock or inject a global script.
  - Record planned module ownership in the foundation table. Register each maintained module in the executable complexity inventory when introduced, before accepting its leaf; the checker rejects mapped files that do not exist. Preserve unrelated pending entries and the explicit test exclusions. Establish focused Vitest/strict-TypeScript configuration and isolated production-build browser fixture tooling from exercised patterns, without importing broad app configuration or local secrets.
  - Done when protected restore and a real-library fixture smoke render pass, exact commands/tool/source identities are retained, and the scoped complexity command is ready for worker handoffs. This setup proves tooling, not the new host or renderer parity.
  - Complexity: all modified maintained production/build/configuration files pass 400 physical lines/file, 300 logical units/file and 50/function where applicable; package locks, tests and fixture exclusions are recorded rather than measured as production.
  - _Boundary: Controller-owned dependency, verification and inventory setup_
  - _Depends: 1.2, 1.4, 1.7, 2.8_
  - _Requirements: 1.1, 1.2, 4.8, 4.9, 10.1, 10.3, 10.4, 10.5_

- [x] 2.14 Freeze path-specific state inputs and the renderer host contract
  - Define distinct integrated/detached input types, retained JSON values and explicit validation results without `any`. Integrated inputs include resolved state key, current model, resolved option baseline, event options defaulting to an empty object, chart type, resolved total series and pivot. Detached inputs include original storage, event type/options and resolved total series.
  - Freeze the typed complete-option/revision host interface and lifecycle ownership. Callers remain responsible for original state-key/range/count preparation and revision/address checks; reducers neither infer API-derived counts nor silently redirect stale edits.
  - Build source-referenced contract fixtures covering different resolved/persisted options and retained unknown fields. Done when focused strict checking and contract validation pass and both implementation lanes receive immutable interfaces, fixture inputs and commands; do not infer saved paths from the editor's empty write capture.
  - Complexity: new maintained types/validation files pass 400/300/50; source fixture/test data exclusions are explicit. No application-hook extraction or wiring is part of this task.
  - _Boundary: Shared compatibility contracts_
  - _Depends: 2.13_
  - _Requirements: 4.8, 4.9, 10.1, 10.3_

- [x] 2.15 (P) Preserve integrated and detached chart-state updates
  - Implement pure, separate reducers from the frozen inputs. Integrated changes clone the resolved options baseline, retain original deep-merge/array behavior, remove only top-level option theme, overlay the current model and update original root metadata. Detached changes preserve the prior model except chart type and replace root options without integrated theme stripping.
  - Verify input immutability, untouched partition equality, nested unknown values, resolved-versus-persisted baseline differences, array merging, absent event options and both paths' type/count/pivot semantics against source-derived expectations.
  - Done when meaningful failing regression cases pass, focused strict/unit checks and independent state review pass, and no new storage format, model range resolver or UI restriction is introduced.
  - Complexity: each maintained reducer/dependency passes 400 physical lines/file, 300 logical units/file and 50/function with current scope evidence; tests/fixtures are explicitly excluded.
  - _Boundary: State reducer lane_
  - _Depends: 2.14_
  - _Requirements: 4.8, 4.9, 10.1, 10.3_

- [x] 2.16 (P) Implement bounded ECharts instance ownership
  - Implement public-API mount/update/resize/image-export/dispose operations from the frozen complete-option contract. Keep the instance private, defer initialization for an unsized container, and prevent callbacks from mutating a disposed or replaced instance.
  - Test update ordering, cleanup on failure, repeated disposal, replacement/remount, hidden-to-sized recovery and image-export error handling. Do not claim mocked lifecycle tests establish real rendering.
  - Done when lifecycle units and focused strict checking pass with independent review; no provider data, application persistence, chart-family translation or new product controls enter this module.
  - Complexity: all maintained lifecycle code passes 400/300/50 with current scope evidence; no compressed spike code is promoted unchanged.
  - _Boundary: Renderer lifecycle lane_
  - _Depends: 2.14_
  - _Requirements: 4.8, 4.9, 10.1, 10.3_

- [x] 2.17 Bind the typed host and prove its real browser lifecycle
  - Connect React mounting, option/revision updates and resize observation to the accepted lifecycle module. Keep library types within the renderer boundary and export image data without defining original menu/filename semantics.
  - Extend the maintained isolated fixture to exercise populated charts with known options, option/data updates, size changes, zero-size recovery, unmount/remount, failure cleanup and PNG contents. Assert numeric options and visible output, not just constructor calls or canvas existence.
  - Done when the freshly built production fixture passes one-worker Playwright/CDP checks, the actual host is the tested import, resources are cleaned up and an independent reviewer reproduces the bounded result. Keep zoom/selection continuity, original styling and application save/reopen explicitly unverified.
  - Complexity: host and any modified maintained build code pass 400/300/50; test fixture exclusions are recorded. This task can overlap the state lane after 2.16, but owns the sole heavy browser queue while running.
  - _Boundary: Renderer host and browser verification lane_
  - _Depends: 2.16_
  - _Requirements: 4.8, 4.9, 10.1, 10.3, 10.4_

- [x] 2.18 Join and accept only the chart foundation evidence
  - Run the complete focused strict/unit/build/browser gates against joined source and dependency identities, plus relevant existing isolated-runtime regressions affected by dependency/test configuration changes. Register portable invocation paths without moving verification into Dagger.
  - Audit imports and diffs to confirm no application wiring, guard/flag edits, catalog changes or unrelated financial-lane work entered the slice. Selectively commit only reviewed scope. Update breadth with actual test IDs and sanitized evidence; retain overall renderer parity as unverified.
  - Done when independent fresh verification, dependency checks, exact identities and final shared-module scope audit pass; document remaining editor/state-mapping/theme/table/persistence obligations without promoting a release image.
  - Complexity: all joined maintained paths pass the existing 400/300/50 gate with accurate manifests; documentation/evidence-only edits are exempt and needed code fixes return to their owning leaf.
  - _Boundary: Controller integration of foundation tests, inventory and evidence_
  - _Depends: 2.15, 2.17_
  - _Requirements: 1.1, 1.4, 4.8, 4.9, 9.6, 10.1, 10.3, 10.4, 10.5, 10.6_

Task 2.13 accepted after independent Astra review and fresh unit, strict TypeScript, production fixture build/browser and scoped complexity checks. Workspace `e56852deff2679c71e32436554f86ba096b55677` pins ECharts 6.0.0 through protected Bun restoration. Evidence: `artifacts/task-2.13/review/review.md` and `complexity.json`. Existing oversized-file exception targets are byte-identical to the prior source; only their source identity advances. No application wiring or renderer parity is accepted.

Task 2.14 accepted at Workspace `bfba80d7f7875fffa60d6d37645a422a3097ea63` after independent Astra source comparison, 11 unit tests, strict TypeScript, scoped lint and fresh complexity verification. Runtime option values remain separate from serialized unknown JSON, with repeated-edit input/output closure and no new storage envelope. Frozen contracts now permit the state and lifecycle lanes to start. Evidence: `artifacts/task-2.14/review/`.

Task 2.15 accepted at Workspace `5d6674e5629fbceda11047bcefcfac237ccd4e62`. Independent source comparison and 26 tests (16 reducer cases plus 10 contract cases), strict TypeScript, lint and complexity checks passed. Integrated and detached reducers preserve the original distinct writes, including unknown fields and runtime undefined values. Evidence: `artifacts/task-2.15/review/review.md`. These modules are not wired into application controls.

Task 2.16 accepted at Workspace `5937af2c73c3f1943fb9a16c13236b46ee623b9c`. Independent review reproduced 13 lifecycle unit cases, strict TypeScript and lint; the combined complexity gate passed. Evidence: `artifacts/task-2.16/review/review.md`. Mocked library calls establish lifecycle ownership and failure handling; real rendering remains task 2.17.

Task 2.17 accepted at Workspace `042ba87e3208a51857da4ae2d1c3109a680716d9`. Independent Astra verification passed all 46 focused tests, strict TypeScript, production build, two real-browser cases, lint and source identity checks. The reviewer inspected the 640 by 400 PNG with visible USD observations; browser tests also check numeric options, pixels, changed output, recovery and disposal. CDP diagnostics are empty. Evidence: `artifacts/task-2.17/review/verdict.md`. Original styling, interactions and application persistence remain outside this acceptance.

Task 2.18 accepted after independent Astra joined review and scoped integration GO for tasks 2.13-2.18 only. Fresh verification reproduced 46 tests, strict TypeScript, all 24 changed branch-file identities and caps for all five production modules. Matching-source chart browser evidence (two cases) and existing Perspective regression (10 unit/four browser cases) passed. See [foundation verification](chart-foundation-verification.md) and `artifacts/task-2.18/review/verdict.md`. Full renderer and release acceptance remain open.

## Approved design slice: resolved snapshots and Cartesian mappings

The owner approved the [snapshot design](chart-snapshot-design.md). The owner approved tasks 2.19-2.23 for implementation ("yes, that fits the spec"). They extend the accepted foundation without activating application charts. Requirements 4.8-4.9 remain product-level obligations; passing this slice is not full renderer acceptance. Each leaf targets a 1-3 hour engineering unit; unexpected scope returns to the controller before implementation expands.

### Ownership and execution

Paths below are relative to `vendor/workspace/terminalpro/`; `Chart/` abbreviates `src/components/General/Table/Chart/`. Root metadata belongs exclusively to the controller. Every worker receives the approved design, leaf, frozen contracts, current source identities, test commands and 400 physical/300 logical units per file/50 units per function caps. Workers are not alone in the codebase and must preserve other lanes' edits.

| Wave | Task and model | Exclusive writable paths | Join |
| --- | --- | --- | --- |
| Contract | 2.19, controller with independent Astra review | `Chart/compatibility/snapshotTypes.ts`, `Chart/echarts/cartesianTypes.ts`; `tests/unit/chart-compatibility/snapshotContracts.types.ts`, `snapshot.fixtures.ts` | Freeze shared types and fixture expectations before workers start |
| Parallel A | 2.20, Sol implementer | `Chart/compatibility/snapshot.ts`, `tests/unit/chart-compatibility/snapshot.test.ts` | Reviewed validated snapshots |
| Parallel B | 2.21, Sol implementer | `Chart/echarts/cartesian.ts`, `tests/unit/chart-compatibility/cartesian.test.ts` | Reviewed financial mapping against frozen valid inputs |
| Browser join | 2.22, Sol implementer, Astra reviewer | `tests/e2e/chart-compatibility/cartesian.html`, `cartesian.tsx`, `cartesian.spec.ts`, existing `vite.config.ts` and `playwright.config.ts` in that directory | Compose actual validator, mapper and accepted host |
| Acceptance | 2.23, controller, independent Astra review | Root inventory/source identity/breadth records; spec verification report and docs navigation | Fresh joined evidence; no app or release activation |

At most controller + two workers + one reviewer. Each leaf follows implement -> independent review -> fresh verification -> acceptance. Serialize installs, shared configuration, commits and the single heavy build/browser queue. Task 2.21 may consume frozen valid fixtures without importing unfinished task 2.20 code; the actual validator join is mandatory in 2.22. Changes to frozen contracts pause both lanes for review. Controller registers maintained paths before feature acceptance and records test exclusions; no leaf may edit shared inventory independently.

Reuse the accepted Node/dependency environment and existing Vitest, strict TypeScript, Vite and Playwright entry points recorded in [foundation verification](chart-foundation-verification.md). From the frontend root use `node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs`, `node node_modules/typescript/bin/tsc --project tests/unit/chart-compatibility/tsconfig.json --noEmit`, and `node node_modules/vite/bin/vite.js build --config tests/e2e/chart-compatibility/vite.config.ts`. Use the root verification Playwright CLI with the existing chart config, one worker, isolated evidence paths and pinned browser cache. Controller verifies paths/tool identities before dispatch. Use the existing combined checker command from [complexity checks](../../../docs/complexity.md) with truthful fork scope, never an empty manifest masking new files. No dependency additions or package/lock changes are authorized.

- [x] 2.19 Freeze snapshot and render contracts
  - Define deeply readonly snapshot inputs/results, source modes, category ownership, ordered identities, numeric/null/missing cells, JSON provenance, unit/scale metadata and resolved style/translation results from the approved design. Include field-path diagnostics, finite-number rules and explicit unsupported outcomes.
  - Add compile-time contract checks and shared synthetic fixtures with one category descriptor, distinct IDs despite duplicate labels, homogeneous financial units and malformed-input cases. Specify known valid fixtures independently of the future validator. Do not add runtime defaults or decode legacy editor options.
  - Confirm existing strict/unit discovery includes the new paths and register the two newly created type modules in controller-owned scope inventory. Controller adds each runtime module when its owning leaf creates it, before that leaf's acceptance; do not register missing files. Done when strict checks, existing foundation units and independent contract review pass and exact signatures/fixtures are frozen for both lanes.
  - Complexity: both maintained type files pass 400/300/50 with explicit fork scope; test fixtures are excluded. No changes to accepted reducers, host, application flags or guards.
  - _Boundary: Shared snapshot and Cartesian type contracts_
  - _Depends: 2.18_
  - _Requirements: 4.8, 4.9, 10.5, 10.6_

- [x] 2.20 (P) Preserve resolved observations in validated snapshots
  - Implement validation and deep copy without grid, React, ECharts, provider or store imports. Preserve ordering, numeric precision, zeros, missing/null distinctions, original model fields, state address and range provenance.
  - Verify category cardinality/association, unique row/column/selection IDs, numeric-series presence, unknown IDs, invalid provenance, nonfinite values, input mutation isolation, repeated categories and descending dates. Valid nonflat snapshots retain their source mode; renderer support is decided separately.
  - Done when focused snapshot tests, strict checks and independent review pass against frozen contracts, with no financial conversion, sorting, aggregation or persistence added.
  - Complexity: all maintained scope passes 400/300/50 using current measured manifests; tests/fixtures remain recorded exclusions.
  - _Boundary: Snapshot validation lane_
  - _Depends: 2.19_
  - _Requirements: 4.8, 4.9_

- [x] 2.21 (P) Map the three resolved Cartesian families
  - Translate exact groupedColumn, stackedColumn and line inputs through the frozen style contract. Keep series identity and style keyed to column IDs, selection order, repeated category positions and label/tooltip display. Replace complete options so family switches cannot retain bar/stack properties.
  - Validate styles and reject unsupported families/source modes or unknown/incompatible unit/scale semantics with structured results. Test missing/null gaps, negative stacks, display-only precision, numeric fidelity, reordered series styles, title/legend/palette projection and no fallback. No original model options are silently claimed as supported.
  - Done when focused mapping tests, strict checking and independent financial review pass against explicit numerical expectations. No legacy editor decoder, new product controls or production rejection guard is introduced.
  - Complexity: maintained mapper passes 400/300/50; if responsibilities cannot fit, return to controller for reviewed cohesive decomposition, not compressed code or unapproved files.
  - _Boundary: Cartesian mapping lane_
  - _Depends: 2.19_
  - _Requirements: 4.8, 4.9_

- [x] 2.22 Verify snapshot-to-host rendering in an isolated browser
  - Compose actual snapshot validation and mapping with the accepted EChartsHost. The fixture owns monotonic render revisions independently of dataRevision; invalid/unsupported inputs expose diagnostics without submitting partial renders.
  - Exercise homogeneous Revenue/Costs data across all three families, repeated labels, negative stacks, settings-only updates at unchanged dataRevision, stacked-to-line replacement, resize, PNG export, rejection and recovery. Assert exact numeric options and visible labels/output; inspect images as supplementary evidence.
  - Done when the freshly built fixture passes one-worker headless Playwright with sanitized CDP diagnostics and owned cleanup, and independent review reproduces the join. Existing fixture tests remain runnable. No original application UX or persistence acceptance is claimed.
  - Complexity: test/fixture paths are documented exclusions; any maintained configuration receives applicable whole-file checks. Production fixes return to their owning leaf and review.
  - _Boundary: Explicit snapshot/mapper/host integration fixture_
  - _Depends: 2.20, 2.21_
  - _Requirements: 4.8, 4.9, 10.1, 10.2, 10.3, 10.4_

- [x] 2.23 Accept only the joined snapshot and mapping evidence
  - Run fresh focused units, strict TypeScript, fixture build and browser regressions against exact joined source/dependency identities. Audit imports/diffs and all four maintained modules; confirm no app activation, feature/flag edits, editor parsing, SQLite, provider or Excel changes entered the branch.
  - Update actual breadth test paths/results, maintained inventory, source identities and a scoped verification report linked from chart documentation. Preserve unrelated work and overall renderer parity as unverified; select only accepted changes for commits.
  - Done when independent final review passes with reproducible commands, exit codes and sanitized evidence, the shared-module audit passes, and remaining original UI, mixed-unit/multi-axis, grid capture and persistence obligations are explicit. No release image is promoted.
  - Complexity: every joined maintained module passes 400/300/50 with exact source scope; documentation/evidence-only changes are exempt. No new exceptions are authorized.
  - _Boundary: Controller integration of scope, breadth and acceptance evidence_
  - _Depends: 2.22_
  - _Requirements: 1.1, 1.4, 4.8, 4.9, 9.6, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_

Task 2.19 accepted at Workspace 8c12a9127cd913e5f6ebb8a9dfe3fd82ba56138f after independent Astra review. Fresh strict TypeScript, 46 foundation tests, repository-configured lint and the seven-module cap audit passed. Contracts are frozen for tasks 2.20 and 2.21. Evidence: artifacts/task-2.19/review/review.md. Runtime snapshot/mapping behavior remains pending.

Task 2.20 accepted at Workspace 616a0a70241fd15a10e0dc91dcec93cf701847ac after independent Sol review. Fresh 26 snapshot tests, strict TypeScript, actual repository lint and complexity evidence pass (110 physical, 122 logical, largest function 29). Evidence: artifacts/task-2.20/review/review.md. Mapper and browser integration remain separate gates.

Task 2.21 accepted at Workspace 59118937434b9f5a9bebd4e80bcb54f7ca2d552e after independent Astra review. Fresh 52 mapping tests, strict TypeScript and actual repository lint pass. Mapper metrics: 273 physical, 90 logical, largest function 15. Evidence: artifacts/task-2.21/review/verdict.md. Browser composition remains task 2.22; original renderer parity is unverified.

Task 2.22 accepted at Workspace 06fdb859bf426eb44dce13c54b21c494fcc244fd after independent Astra verification: 124 tests, strict TypeScript, build, scoped lint and three browser cases passed; CDP diagnostics are empty. Fresh PNGs show negative stacking, repeated categories and line gaps. Evidence: artifacts/task-2.22/review/review.md. Fixture animation is disabled to make image verification deterministic; original application parity remains unverified.

Task 2.23 accepted after independent Astra joined review and scoped GO for tasks 2.19-2.23 only. Fresh verification passed 124 tests, strict TypeScript, fixture build, all nine production module caps, twenty source/dependency identity checks, metadata and documentation links. Matching-source independent task 2.22 browser evidence supplies three passing cases with empty CDP diagnostics. See [snapshot verification](chart-snapshot-verification.md) and artifacts/task-2.23/review/verdict.md. Full renderer and release acceptance remain open.

## Original option-state slice (tasks 2.24-2.27)

Owner approved the option-state design and autonomous implementation on 2026-10-16. This scope supplements the existing task graph; other requirement coverage remains with existing tasks. Independent task review precedes execution. No renderer activation, theme projection or release acceptance is included.

- [x] 2.24 Freeze option-state contracts and captured editor fixtures
  - Implement the design's shared baseline, initialization/synchronization and column-event types, using existing mutable nested compatibility types and readonly outer fields. Preserve exact kind/value fields and null/undefined distinctions.
  - Freeze minimal independent synthetic expectations from seven original outgoing payloads with source/digest provenance; include supplied model/range and unrelated options needed for reducer composition. No private state is copied.
  - Verify existing unit/strict discovery, register the type module in controller-owned inventory and pass strict checks, existing units and independent contract review before releasing parallel lanes. Any compile-only test belongs to this task's explicitly owned optionStateContracts.types.ts.
  - Done when contracts and fixtures compile, captured values match original evidence and independent review approves the frozen boundary. Production caps 400/300/50 apply to the type module; fixtures/tests are excluded.
  - _Boundary: Shared optionStateTypes.ts, editorPayload.fixtures.ts and optionStateContracts.types.ts; controller inventory_
  - _Depends: 2.23_
  - _Requirements: 4.8, 4.9, 10.5_

- [ ] 2.25 (P) Preserve original baseline selection and partition transitions
  - Implement initialization and synchronization with explicit prior state, validated fallback inputs, independent nested copies and captured address. Preserve empty-partition retention, nonempty partition clearing, original initial type ownership and no synchronization root fallback.
  - Test the design's complete fallback/transition matrix, null/undefined restrictions, malformed unused fallbacks, unknown fields, arrays and special property names, accessors, cycles, throwing inspection and mutation isolation. Errors do not throw or change prior state.
  - Done when focused tests, strict checks, scoped lint and independent review pass without store, React, GridApi or renderer imports. Whole maintained module passes 400/300/50 with registered scope before acceptance.
  - _Boundary: optionState.ts and optionState.test.ts only_
  - _Depends: 2.24_
  - _Requirements: 4.8, 4.9_

- [ ] 2.26 (P) Map column editor events and verify original reducer composition
  - Implement typed title-text/title-enabled, legend-position and stroke-width patches for grouped/stacked columns. Preserve separate text/enabled meaning and exact bar paths; reject invalid input and unsupported families without partial patches.
  - Test all contract value domains, captured title/bottom/width-four cases, independent outputs and malformed events. Record source corroboration for contract value domains without claiming each was browser-captured.
  - Compose with unchanged integrated reducer using complete supplied baseline and patch; compose with detached reducer using a cloned complete event-options object merged with the patch. Verify unrelated options, root-only theme stripping, null/undefined/array behavior, supplied destination range, state-key collisions and bar retention through grouped/stacked/line storage changes.
  - This lane uses frozen fixtures rather than importing the pending baseline implementation; joined baseline-to-editor composition belongs to 2.27.
  - Done when focused tests, strict checks, scoped lint and independent review pass. Whole maintained module passes 400/300/50 before acceptance; no production UI/guard/reducer changes.
  - _Boundary: editorEvents.ts and editorEvents.test.ts only_
  - _Depends: 2.24_
  - _Requirements: 4.8, 4.9_

- [ ] 2.27 Verify and accept the joined option-state boundary
  - Add explicit integration cases to editorEvents.test.ts after both lanes freeze: actual baseline selection -> actual event mapper -> accepted reducers. Verify successive edits, partition transition, supplied family change and detached replacement with independent expected values.
  - Run fresh complete chart units, strict TypeScript, scoped lint, full registered chart-module complexity audit and exact source/dependency identity checks. No new browser acceptance claim: renderer code is unchanged, original runtime parity remains unverified.
  - Update actual test paths/evidence, inventory, source pin and scoped verification report; selectively commit accepted changes while preserving unrelated work. Done when independent final review verifies the joined contract and honest remaining gaps, with reproducible commands and exit codes.
  - Production caps 400/300/50 apply to all three new modules and the shared registered audit; docs/tests excluded. Controller serializes shared inventory, builds/check queue and commits. No release promotion.
  - _Boundary: Explicit integration tests after lane freeze; controller inventory, breadth, source and evidence records_
  - _Depends: 2.25, 2.26_
  - _Requirements: 1.1, 4.8, 4.9, 10.4, 10.5, 10.6_

### Lane ownership and execution prerequisites

Frontend paths are under vendor/workspace/terminalpro/src/components/General/Table/Chart/compatibility or tests/unit/chart-compatibility as specified in the design. Existing WSL pinned Node and restored dependencies are prerequisites already accepted by earlier tasks; no install or lock change is needed. Controller may copy the required source/tests to a fresh isolated stage with the restored node_modules link for reliable Linux checks. One heavy check at a time, one Vitest worker; lightweight independent lane checks must use separate outputs. Shared contracts/fixtures freeze at 2.24. Sol implementers own 2.25 and 2.26 separately, followed by fresh independent reviewers. Astra reviews shared contracts and the final join. A lane cannot change shared interfaces or its peer's files; escalate to controller. Controller owns registration and selective fork/root commits at each acceptance. Task approval follows the owner's explicit autonomous implementation request, without waiving any review gate.

Task 2.24 accepted after independent Astra review: shared contracts and captured projections verified, 124 units, strict TypeScript, scoped lint and registered complexity checks passed. Evidence: artifacts/task-2.24/review/review.md. Contracts and fixtures are frozen for tasks 2.25 and 2.26.
