## Approved design slice: appearance composition and tooltip source contracts

The owner approved [the appearance/editor amendment](chart-appearance-editor-integration-design.md). Tasks 2.41-2.45 below are proposed for implementation approval, not started. They preserve the original UX obligation and do not activate B2, the mapper, C/D, transformed snapshots or new product restrictions. Existing completed tasks and the parent plan's coverage of all 69 requirements remain unchanged. Candidate baseline is Workspace `76edf85a46298f7bc5212ff9944e4b66e9baa4af`; freeze actual current owned bytes at setup.

- [ ] 2.41 Freeze appearance contracts, reference fixtures and executable verification scope
  - Define the approved composition and color token/result types without runtime stubs. Freeze their exact signatures and fixture hashes for workers; retain the existing option baseline, validation, session and reducer types as dependencies.
  - Derive small data-only expected fixtures from the reviewed saved-input and normalized-color evidence. Record original source/image provenance and distinguish observed winners from proposed invalid-input policy. Keep saved options deliberately different from model.chartOptions so operand mistakes fail tests.
  - Verify existing application/compatibility configs discover new appearance tests and compile-only type fixtures without global mocks; no config change is expected. Snapshot a fresh isolated WSL stage, record Node/dependency/source identities and exercise both existing suites/strict checks before work fans out. Do not import absent implementations or add placeholder production functions.
  - Register the new contracts file in the maintained inventory and confirm existing event/session ownership. Freeze a planned path list for the two implementation files; the checker rejects absent mapped files, so the controller adds each inventory entry only when its worker introduces that file, before its acceptance check. Retain unrelated inventory edits and document test/fixture exclusions. Prepare explicit current workspace/data_api change manifests; preserve exact exception target bytes.
  - Done: independent review accepts the frozen types, finite fixtures, test discovery, passing baseline commands and complete staged identities. New type file and modified maintained configurations pass 400 physical/300 logical units per file and 50/function where applicable; test/fixture files are explicitly excluded. No new exception or dependency upgrade.
  - _Boundary: Controller-owned contract, fixture and scope foundation; exclusive paths in ownership table_
  - _Depends: 1.3, 1.4, 2.40_
  - _Requirements: 1.1, 1.4, 4.8, 4.9, 10.4, 10.5, 10.6_

- [ ] 2.42 (P) Preserve original saved-option composition without mutating state
  - Use the approved saved operand baseline.options and generated operand. Return a detached combined value with generated common replacing saved common, then source-equivalent lodash merge semantics; do not reread baseline.model.chartOptions or storage.
  - Preserve family and unknown branches, own undefined/null/array behavior and input identity/contents. Keep callbacks outside data-only options. Contain accessors, cycles, nonplain values and throwing proxies through the public validation boundary without invoking getters or functions.
  - Write meaningful failing regressions before implementation for saved-common replacement, conflicting bar/line families, mismatched baseline/model options and mutation. Expected fixtures and pinned original-source composition serve as the oracle, not the new helper's output.
  - Done: focused composition tests, strict checking and lint pass after RED evidence; independent review verifies exact source winners and unchanged input state. The complete maintained file passes 400 physical/300 logical/50 per function. No changes to baseline selection, reducers, theme generation, renderer or application hooks.
  - _Boundary: Pure saved-option composition and its owned test file_
  - _Depends: 2.41_
  - _Requirements: 1.1, 1.4, 4.2, 4.7, 4.8, 4.9, 10.5, 10.6_

- [ ] 2.43 (P) Reproduce derived grid and subtitle colors from explicit tokens
  - Accept explicit supported base and foreground/background/text/chart-background tokens. Use the approved normalized-channel operation order, literal ratios and lowercase six-digit output. Do not assume aliases are identical or resolve arbitrary saved theme graphs.
  - Separate descriptor-safe invalid structure from structurally valid unsupported strings; preserve diagnostic paths. Reject missing/non-string/unknown own fields and contain hostile access; unsupported bases/color strings are unresolved without claiming CSS validity.
  - Begin with failing independent expected-color cases, including the #000000/#9b0000 rounding edge yielding #8b0000, dark/light ratios, independent subtitle aliases, upper/lower hex input and black/white bounds. Retain the exhaustive source experiment as historical evidence rather than introducing AG into maintained runtime/tests.
  - Done: focused tests, strict checking, lint and independent review pass; inputs are unchanged and diagnostic cases produce no guessed color. The complete maintained file passes 400 physical/300 logical/50 per function. No general CSS parser, theme selector, stored-state change or renderer dependency is added.
  - _Boundary: Pure derived-color routine and its owned test file_
  - _Depends: 2.41_
  - _Requirements: 1.1, 1.4, 4.8, 4.9, 10.5, 10.6_

- [ ] 2.44 (P) Integrate grouped-column tooltip edits with the existing addressed session
  - Extend the existing event union and mapper with tooltip-mode values single/shared/compact and exactly the bar.tooltip.mode patch. Preserve Multiple -> shared semantics; reject arbitrary paths and malformed values. The mapper retains its current ValidationResult signature.
  - After session stamp validation, distinguish an exact structurally valid stackedColumn tooltip event as unresolved, before mapping or writes. Mapper-level stacked tooltip rejection remains validation failure. Malformed events remain invalid; proxy/accessor handling is exception-contained. The four existing events retain both original column-family behaviors.
  - Exercise the real existing session and reducer with latest storage and baseline.options, never composed rendering options. Preserve unknown and inactive-family state, current model, prior edits and stale-address/generation/data/render revision behavior; no new save trigger.
  - Begin with failing exact-patch and session regressions. Done: actual grouped tooltip edits produce the expected original model fields, invalid/unresolved/stale inputs leave storage untouched, and all existing event/session tests pass under independent review. Both touched responsibility boundaries are an explicit event-to-session integration task.
  - Every modified maintained file is checked whole against 400 physical/300 logical/50 per function. No option reducer, baseline owner, mapper, UI or family visibility changes; no new callback/store.
  - _Boundary: Typed editor event to existing session integration; exclusive files in ownership table_
  - _Depends: 2.41_
  - _Requirements: 4.2, 4.7, 4.8, 4.9, 10.4, 10.5, 10.6_

- [ ] 2.45 Independently verify and join the source contracts without activating the application
  - Freeze all worker writes and snapshot the actual combined source/config/fixture bytes to a fresh stage. Independently rerun both unit suites, both strict compilers and scoped lint with zero hidden skips; preserve failed attempts and exact command exits.
  - Verify the typed composition/color handoffs and event/session integration together against accepted fixtures. Confirm composition/color outputs remain render-only, stored baseline fields survive tooltip edits and no application guard, menu, flag, dependency or UI path changed.
  - Run the complete maintained inventory gate with explicit fork change manifests and exact source identities. All new/modified production files pass 400 physical/300 logical/50 per function; existing exception target bytes remain unchanged. Tests and synthetic fixtures remain declared exclusions.
  - Done: fresh independent review reports scoped GO and verification for 2.41-2.44 only, with actual test paths and source/artifact identities. Record the continuing B2/mapper/editor/transformation/application/persistence gates in breadth; no reference-only or unit result becomes renderer acceptance.
  - Synchronize only frozen reviewed safe artifacts before selective commit/push, preserving unrelated working changes. Reconcile source pins/inventory without absorbing catalog/Perspective work. Corrective production edits return to the owning task and independent review rather than expanding this join's scope.
  - _Boundary: Controller-owned source-contract verification and evidence join; no additional production behavior_
  - _Depends: 2.42, 2.43, 2.44_
  - _Requirements: 1.1, 1.4, 4.2, 4.7, 4.8, 4.9, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_

### Ownership and scheduling for 2.41-2.45

Production paths below are relative to terminalpro/src/components/General/Table/Chart; test paths are relative to terminalpro/tests/unit. Each task is a bounded 1-3 hour work unit, including its focused review, not a delivery-time promise.

| Owner | Exclusive writable paths |
| --- | --- |
| Controller 2.41 | application/appearanceContracts.ts; chart-application/appearanceContracts.types.ts; chart-application/appearanceFixtures.json; root .kiro/complexity-budgets.json and .kiro/breadth.toml; isolated stage/manifest outputs. Existing compiler/Vitest configs are read-only unless a concrete prerequisite is returned for review. |
| Sol 2.42 | application/appearanceComposition.ts; chart-application/appearanceComposition.test.ts |
| Sol 2.43 | application/appearanceColors.ts; chart-application/appearanceColors.test.ts |
| Sol 2.44 | compatibility/optionStateTypes.ts, compatibility/editorEvents.ts, application/sessionState.ts, application/types.ts only if required by approved command typing; chart-compatibility/editorEvents.test.ts, chart-application/sessionState.test.ts |
| Controller 2.45 | Root inventory/breadth/source pins, joined manifests and verification artifacts; no renderer/application edits |

Appearance contracts/fixtures freeze before fan-out; workers may read but not edit them. Schedule two implementation lanes: composition then colors on lane A, tooltip event/session on lane B. 2.43 is logically independent after 2.41; its lane sequencing is a resource limit, not a hidden semantic dependency. Reserve a slot for fresh independent review, using Astra for composition/state/financial boundaries and Sol for bounded routine checks. At most controller + two workers + reviewer. One heavy check at a time; installations/shared mutations/commits remain serialized. The project delegation amendment governs these explicit dependencies rather than generic list-order serialization.

### Verification setup and commands for 2.41-2.45

Use a new isolated WSL stage containing current owned source bytes, not a previous task archive. Reuse pinned Node 24.22.0 and the accepted dependency tree at /home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules. Record actual versions and identities in 2.41. Existing application/compatibility configs already include their own *.ts/*.tsx unit trees and application sources, with jsdom, maxWorkers:1 and no global setup. Compile-only fixtures end in .types.ts. No new install, browser, image or config is assumed. If the accepted runtime is missing, restore through the existing locked protected workflow before proceeding; never silently upgrade.

From the stage's terminalpro directory, with pinned Node on PATH:

```sh
node node_modules/typescript/bin/tsc --project tests/unit/chart-application/tsconfig.json --noEmit
node node_modules/typescript/bin/tsc --project tests/unit/chart-compatibility/tsconfig.json --noEmit
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs
node node_modules/@biomejs/biome/bin/biome check src/components/General/Table/Chart/application src/components/General/Table/Chart/compatibility/editorEvents.ts src/components/General/Table/Chart/compatibility/optionStateTypes.ts tests/unit/chart-application tests/unit/chart-compatibility/editorEvents.test.ts
```

Focused workers append their actual owned test paths to the matching Vitest command. Tests are not considered accepted based on discovery alone. Historical totals of 88 application/260 compatibility tests are baseline evidence, not this wave's results. The joined check runs both complete configurations, not only new files.

Controller-generated manifest paths below are future task outputs. Run the existing full gate from the root with pinned Node on PATH:

```sh
pipeline/.venv/bin/python -m tools.quality.complexity --check --changes workspace=artifacts/appearance-editor-implementation/workspace-changes.json --changes data_api=artifacts/appearance-editor-implementation/data-api-changes.json --output artifacts/appearance-editor-implementation/complexity.json
```

Both manifests contain explicit repository/base/head and complete changed-file scope. Preserve unrelated dirty inventory entries and exact exception targets rather than overwriting or rebinding them without evidence. Source pins change only at the reviewed commit join. No new blanket exception is proposed.

### Continuing gates

The three source contracts feed the already designed B2 and original event/session boundary; they are not disconnected replacement systems. Complete effectiveAppearance, original-to-ECharts field projections, public tooltip rendering, original docked controls, transformed snapshots and D activation remain under the blocked application followups above. This task batch cannot remove guards or accept a reduced product menu. No Excel implementation precedes Anthropic acceptance; Dagger remains image-build-only.
