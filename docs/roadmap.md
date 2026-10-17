# Roadmap

Prove the Full Workspace dashboard first, accept Anthropic next, then implement Excel. Each stage below has an evidence gate. This is a dependency overview, not a generated task list or approval to implement.

Current renderer gate: ECharts is selected for charts behind the original OpenBB controls. The prior native Perspective explorer direction is superseded by functional and visual parity requirements. Resolve the [ECharts compatibility findings](../.kiro/specs/openbb-self-service/echarts-findings.md) before resuming financial widget integration; historical acceptance below does not establish renderer parity.

The approved [chart foundation](chart-foundation.md) now has separately reviewed state reducers and a real-browser-tested React/ECharts host. Independent joined review passed for tasks 2.13-2.18. The next approved slice adds [resolved snapshots and three Cartesian mappings](../.kiro/specs/openbb-self-service/chart-snapshot-verification.md), accepted through task 2.23 after independent browser and final joined verification. Original-control integration and the renderer parity gate remain open.

The [phase record](../.kiro/specs/openbb-self-service/spec.json) records approved requirements and [technical design](../.kiro/specs/openbb-self-service/design.md). The owner-approved [implementation plan](../.kiro/specs/openbb-self-service/tasks.md), including the Perspective amendment, has passed independent dependency review. All foundation tasks are accepted, including evidence/runtime contracts, isolated verification and the Dagger export workflow. Full frontend packaging, private account bootstrap and request isolation are accepted. Installed FMP profile/income fixtures and sanitized failure categories are accepted. Single-origin routing and the locked FMP/FRED runtime are accepted on fixture evidence. The provisional Full image has passed independent build/load/runtime verification. The identified data image has also passed independent offline runtime and identity checks. The Community table boundary and supported widget-catalog generation are accepted. Commercial dependency removal is accepted; the standalone Perspective runtime is accepted and financial widget binding is next; dashboard, live-provider and release acceptance remain pending. Read the [feasibility report](../.kiro/specs/openbb-self-service/feasibility.md) before interpreting a source finding or provider probe as integration evidence.

## Dependency gates

Appearance tasks 2.28-2.33 are independently accepted with scoped GO: shared contracts, parallel style/fixture work, mapper integration and browser verification. See [appearance verification](../.kiro/specs/openbb-self-service/chart-appearance-verification.md) for current evidence. Next are original theme resolution and control/application integration; full renderer acceptance remains open.

The owner approved the [original option-state design](../.kiro/specs/openbb-self-service/chart-option-state-design.md) and autonomous implementation. Tasks 2.24-2.27, including both parallel implementation lanes and [joined verification](../.kiro/specs/openbb-self-service/chart-option-state-verification.md), are accepted. [Effective theme resolution](../.kiro/specs/openbb-self-service/chart-effective-style-discovery.md) and application integration remain subsequent work.

| Stage | Work to resolve | Gate before proceeding |
| --- | --- | --- |
| 1. Review requirements and feasibility | Confirm scope, source pins, Full choice, provider/build gaps, and observable journeys | Human requirements approval; unresolved assumptions remain explicit |
| 2. Design the contracts | Define source assembly, API/provider dependencies, widget generation, routing/authentication, state, agent protocol, component rights, and release evidence | Human design approval with testable contracts and failure cases |
| 3. Generate bounded tasks | Define file ownership and dependency joins; plan complexity inventory/checks, verification harness, and breadth foundations before feature acceptance | Human task approval; explicit foundation tasks and evidence criteria |
| 4. Accept the dashboard and data baseline | Implement foundations, adapt Full builds and FMP, select the latest validated API, regenerate widgets, establish FRED and persistence | Executable scope/complexity checks; clean builds; real widget discovery and values; edit/save/restart/reopen/refresh; provider failures; bind-state recovery |
| 5. Accept Anthropic | Implement agent discovery, model access, streaming, selected-data handling, and recovery | Actual Workspace success and failure evidence; dashboards stay usable when the agent is unavailable |
| 6. Implement and accept Excel | Regenerate functions and adapt URLs, authentication, manifest, and API contracts | Stage 5 accepted first; actual Office load/login/function/refresh/reopen through the public access boundary |
| 7. Release and recover on Linux | Finish portable verification/publication commands, Dagger image builds, immutable image manifest, pull-only deployment, and rollback/backup procedure | Required checks pass against recorded revisions/images; Linux journeys and clean restore pass |

Build and CI foundation work may overlap application work after shared contracts are frozen and ownership is disjoint. Publication and release acceptance still wait for their required gates. [Delegation steering](../.kiro/steering/delegation.md) defines permitted lanes, model roles, and independent review. Excel cannot become a spare parallel lane before Anthropic acceptance.

## Known work before a build can prove compatibility

- The selected OpenBB 5 / core 2 API excludes released FMP support. FMP 1.6.1 requires core below 2; a maintained, tested adaptation is required. Static import compatibility does not prove endpoint or financial-data correctness.
- The provisional Full image builds from frozen inputs and passes health/login/private-state checks. The renderer-complete image and integrated dashboard checks remain pending.
- Legacy source-fetch scripts refer to inaccessible split repositories. Assemble the required build context from the owned Workspace monorepo and recorded revisions.
- Prove ECharts compatibility with original OpenBB chart controls, state, themes and actions. Evaluate Perspective for analytics, retain existing Plotly widgets and restore removed table capabilities. Verify saved configuration, financial aggregations, refresh and selected-view AI data; see the [replacement decision](chart-replacement-assessment.md).
- Widget discovery, HTTP path rewriting, agent streaming, and Excel authentication need integration evidence. Selecting Full or declaring Compose services does not implement them.

## Completion evidence

Every code task must carry the applicable caps: 400 physical lines per maintained production file, 300 logical syntax units per maintained Python/JavaScript/TypeScript file, and 50 per function. The [complexity policy](../.kiro/steering/complexity.md) defines inventory, generated/upstream exclusions, measurement, and reviewed exceptions. Policy text alone is not enforcement.

Use isolated background Playwright checks for real user journeys and independent data assertions for financial results. Keep one heavy build or suite active at a time and apply the worker bounds in [testing steering](../.kiro/steering/testing.md). Record command, revision or image digest, exit code, and artifact location. Update the [breadth map](../.kiro/breadth.toml) with actual test paths and evidence; planned or skipped checks remain unverified.

## After the baseline

Consider a separate PostgreSQL connector specification after baseline acceptance. Optional providers and later packaging requests need their own contracts and evidence. Neither is a prerequisite for the current dashboard, Anthropic, or Excel gates.
