# PASS: appearance/editor task graph

Tasks 2.41-2.45 are ready for the owner's task approval. This independent review accepts the proposed source-contract task graph only. It does not authorize implementation, activate the application or accept renderer parity. No repair was needed.

Reviewed draft: `artifacts/appearance-editor-task-plan/draft.md`, SHA-256 `400277f810a28ededb8ecfc71490744f29fcd3ba6e91e4c7b71caf6a6565d2d3`.

Approved amendment: `chart-appearance-editor-integration-design.md`, SHA-256 `05d12b46374cfaf1bf9986da24efc8e8fed7ded9b0b13eee333518285926d76b`. The approval and bounded implementation gate match spec.json. The existing tasks.md baseline is pinned to root revision `cff08b347cedbaef95aea064d7fc1d5253d5f300`, with its Git blob hash recorded in mechanical-check.json. The checker reads that pinned baseline before adding the draft, so replay after canonical publication does not count the suffix twice. Publication must preserve prior task bodies and statuses.

## Coverage and dependencies

The mechanical check derives all 69 criterion IDs from requirements.md and finds all 69 in the combined existing plan plus proposed suffix. It finds no unknown mappings, duplicate new task IDs, overlap with existing IDs, missing dependency targets or cycles. Every new task is unchecked and has a boundary and observable completion condition. This is mapping coverage, not completed acceptance: full UI, persistence, provider, AI, Office and delivery gates retain their existing statuses.

The dependency graph is accepted foundations 1.3/1.4 and accepted ordinary capture 2.40 -> controller freeze 2.41 -> independent source work 2.42/2.43/2.44 -> joined verification 2.45. Historical accepted session/reducer work is retained through the existing plan and read-only dependency contract. The explicit project fan-out override governs this branch. Lane A runs composition then colors; lane B runs tooltip/session work. Their production and test ownership sets do not overlap. The controller owns types, fixtures, inventory and shared metadata, and freezes these before workers begin. The limit of two implementers plus a reserved reviewer slot is retained; three `(P)` tasks do not authorize three simultaneous implementers.

Each task has one bounded deliverable appropriate to a 1-3 hour engineering unit: frozen source/test contracts, detached saved composition, explicit token colors, one event-to-session integration, and independent joined verification. The event/session task deliberately crosses two existing responsibilities and identifies itself as integration. No task creates a second persistence owner, changes the reducer, activates the renderer, or begins a new editor. The prohibition on mapper changes in 2.44 means the later renderer mapper; its first bullet and ownership table explicitly authorize the existing event mapper change.

## Contract and prerequisite checks

| Approved contract | Planned owner and observable check |
| --- | --- |
| Composition uses baseline.options with generated common replacement and lodash merge behavior | 2.41 types/oracles, 2.42 independent winners, own undefined/null/array and mutation checks |
| Strict data-only boundary, unknown-family preservation and hostile input containment | 2.42 public boundary and state identity assertions |
| Normalized-channel color order, literal ratios, explicit aliases and rounding counterexample | 2.43 independent expected colors and invalid/unresolved diagnostics |
| Exact bar.tooltip.mode patch with shared stored value for Multiple | 2.44 event mapper and regression suite |
| Stacked tooltip unresolved only after stamp validation; malformed events invalid | 2.44 actual session and reducer assertions, no writes on rejection |
| Latest selected baseline remains original persistence operand | 2.44 latest-storage tests, 2.45 independent joined audit |
| Existing financial formatting, baseline/reducer and host remain owned dependencies | Read-only paths retained; no dependency upgrade or competing store |
| B2, full field manifest, tooltip projection, original docked editor, transformed snapshots and activation | Explicit continuing gates; no implementation task invents their missing contracts |

Inspected actual compiler, Vitest and Biome configurations. Application TypeScript includes application `.ts` source and its unit `.ts/.tsx` tree, so the new types, helpers, `.types.ts` fixture and tests are discovered. It inherits strict mode and enables JSON imports. Compatibility TypeScript includes compatibility/ECharts source, compatibility unit tests and its existing e2e fixture tree. The two Vitest configurations discover the proposed unit files; compatibility also retains its toolchain fixture test. Both use jsdom and one worker with no global setup. The draft's scoped Biome command covers all proposed production changes and owned test/type/JSON fixture paths. Existing configuration permits those paths; no hidden config edit is necessary. These are static scope checks, not passing compiler/lint evidence.

The inventory existence audit finds no currently mapped missing files. All existing event/session production paths are mapped. The three new appearance files are correctly treated as future files: 2.41 adds its created contract file, while controller-owned helper inventory entries wait until each worker creates its helper. This matches tools/quality/scope.py, which rejects absent mapped files. Full changed-file manifests and unchanged exception target bytes remain required; unrelated catalog/Perspective modifications cannot be erased or silently adopted. Whole-file 400 physical/300 logical/50 function limits and final shared-module audit are explicit. Tests and fixtures remain excluded with provenance.

## Evidence and publication limits

Executed `py -3 artifacts/appearance-editor-task-plan/review/check_plan.py`, exit 0. The output is mechanical-check.json. Two environment discovery attempts preceded it: `python` reached the Windows Store alias without executing the script, and default-WSL `python3` was absent. Neither was a verification pass; the installed Windows Python launcher executed the static check successfully. No application tests, compiler, lint, production complexity measurement, install, browser or image command was run during this review.

The task draft requires fresh baseline and joined verification in a new stage with exact current bytes, pinned runtime identities, command exits and failed-attempt preservation. Runtime restoration remains a prerequisite if the accepted dependency tree is absent. No historical test total is reused as fresh evidence. Browser-only criteria in 2.45 are continuing-gate traceability, not claims that this unit-only source slice satisfies them.

The reviewed publication allowlist contains only the task draft, this report, the static checker and its JSON output, with source hashes. They contain project-relative paths, public source identities and synthetic task metadata, not operator state or credentials. Copy only the exact allowlisted bytes to the reviewed mirror and record destination hashes in the controller's synchronization manifest. The allowlist file is the manifest container and intentionally does not self-hash. Any substantive draft change or changed input dependency requires a fresh review; a mechanical rerun alone does not approve new task scope.
