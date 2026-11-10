# Native development workflow implementation tasks

Requirements and design were owner-approved on 2026-11-10. This plan migrates the existing workflow; it does not authorize application changes, relaxed assertions, new provider requests, VM reconfiguration or image publication.

## Execution and ownership

Each task is a bounded 1-3 hour work unit, not an elapsed-time promise. If a task exceeds its boundary, stop that lane and split the remaining work before accepting it. Every task uses implement -> independent review -> fresh focused verification -> selective commit. Reuse existing meaningful tests; do not repeat passing suites solely for another report.

Use Sol for implementation/routine review, Astra for private-storage and difficult integration review, Luna only for mechanical audits. At most controller + two implementers + one reviewer. One heavy build/suite at a time. Frozen contracts permit the explicit parallel graph below; this project rule overrides generic numeric sequential ordering.

| Tasks | Exclusive writable scope |
| --- | --- |
| 1 | Tool metadata and native tool evidence; controller owns `pipeline/tools.lock.json` and inventory/checker baseline |
| 2 | `pipeline/dev.ps1`, `pipeline/qopenbb_ci/native_environment.py`, `container_command.py`, focused environment tests |
| 3.1-3.2 | `pipeline/qopenbb_ci/session_files.py`, `windows_private_files.py`, private-file tests; sequential ownership |
| 4 | `pipeline/qopenbb_ci/runtime_descriptor.py`, descriptor/IPC tests; serialized completion of task 3 storage IPC |
| 5-6 | `pipeline/qopenbb_ci/compose_runtime.py`, `tests/delivery/compose.runtime.yaml`, `workspace_runtime.py`, `workspace-runtime.ps1`, `task25_runtime.py`, Compose tests |
| 7-8 | `verification/runner.ts`, `runner.py`, `evidence.ts`, `playwright.config.ts`, `financial-workspace.config.ts`, new `runtime-descriptor.ts`, `tests/e2e/financial-workspace.spec.mts`, isolated Workspace fork `terminalpro/tests/e2e/live-chart/fixtures.ts`, focused browser tests |
| 9 | `pipeline/qopenbb_ci/build_cli.py`, `image_cli.py`, `sources.py`, `images.py`, `catalog_runtime.py`, `publication.py`, existing image/publication tests and `tests/delivery/test_data_runtime_image.py` container selection |
| 10-12 | Controller-owned qualification, existing portable gates, source-pin join, docs/checklists and sanitized acceptance evidence |

Controller alone owns shared source locks, inventory, breadth map and roadmap. Task 2 freezes its helpers before any consumers start. Later entry-point wiring is controller-owned task 11, not simultaneous edits by runtime/browser/build workers. Task 4 freezes descriptor and IPC before runtime/browser consumers. Preserve unrelated dirty catalog-renderer and inventory work and the historical root vendor checkout. Use an isolated accepted-source Workspace checkout for the test-only fork change.

Windows disposable outputs go under `D:/BuildArtifacts/QOpenBB` from repository working directories; Linux dependencies stay within the Linux VM filesystem. All production changes, including runtime helpers located under tests, must pass 400 physical lines/file, 300 logical units/file and 50/function. Tests, generated locks and docs are excluded as specified by steering, not used to hide maintained logic. No implicit size exceptions.

## Tasks

- [ ] 1. Qualify the native protected toolchain and existing size gate
  - Resolve actual Python, Node, pnpm, uv, Safe Chain, Podman and Compose executables and supported cache/output paths without shell-profile aliases. Preserve the locked versions and Node security floor.
  - Verify noninteractive package protection before frozen dependency restoration. Provision the pinned native Dagger executable with verified checksum, retaining CLI/SDK/engine 0.21.8. Do not invoke the global wrapper or relax version checks.
  - Establish the existing combined complexity gate with explicit current fork identities and a clean inventory baseline. Use the implemented `python -m tools.quality.complexity --check` interface from `docs/complexity.md`, explicit scope and external output; record the resolved native interpreter/command.
  - Done: protected native environments and required tools are usable; the existing checker runs natively with accurate scope and no silent partial acceptance. Unsupported prerequisites leave this task open with a specific diagnostic.
  - Verify physical caps for maintained tool metadata changes; dependencies/generated locks are excluded. No new checker framework.
  - _Boundary: Native tooling and inventory foundation_
  - _Requirements: 1.2, 4.1, 5.1, 5.2, 5.3, 6.4_

- [ ] 2. Provide native command and container execution contracts
  - Implement the native entry/environment and shared container command selection from the design. Resolve real executables, explicit Compose provider and selected daemon; preserve required Windows system/temp variables without inheriting provider credentials into builds.
  - Validate working/output/cache roots, spaces in paths and action arguments. Hide helper consoles and propagate errors/exit codes. Freeze the CLI, output-root and subprocess contracts; runtime/build actions cannot report success before their consumers exist.
  - Done: native doctor and focused path/environment tests pass without WSL or profile functions; drive-root, incompatible version and unsafe output cases fail before mutation.
  - Whole-file 400/300/50 checks pass for the native entry and shared helpers; add their actual paths to the maintained inventory through the controller.
  - _Boundary: Native entry and environment_
  - _Depends: 1_
  - _Requirements: 1.1, 1.2, 1.3, 5.1, 5.2, 5.3, 6.4_

- [ ] 3. Protect private session storage
- [ ] 3.1 Establish verified Windows directory and file protection
  - Implement protected directory creation, intended-user ownership/DACL verification, handle-based no-reparse access and confined reads/removals. Write no credentials before verified protection.
  - Done: actual Windows API tests prove user-only protection and checked-handle reads; broad/inherited/null ACL, wrong owner, junction/replaced path and unsupported protection fail closed before credential writes.
  - Independent Astra review and whole-file 400/300/50 checks pass for the Windows security helper. No hand-maintained security logic is excluded as test code.
  - _Boundary: Windows private-file protection_
  - _Depends: 2_
  - _Requirements: 1.3, 5.1, 5.3, 5.4, 5.5, 6.4_

- [ ] 3.2 Provide confined session file lifecycle across platforms
  - Use the accepted Windows protection helper for exclusive creation, checked reads and confined removal. Retain POSIX owner/0600 handling under the same storage contract.
  - Implement atomic replacement within the protected directory, preserving the last valid descriptor on interrupted update. Recheck ownership on reads/deletes and never follow a changed path.
  - Done: focused lifecycle tests prove exclusive creation, successful update, interrupted replacement recovery and repeated removal without touching unrelated state. Actual Windows checks and POSIX tests distinguish platform evidence accurately.
  - Independent review and whole-file 400/300/50 checks pass for the cross-platform storage module and any scoped Windows helper correction.
  - _Boundary: Private session storage lifecycle_
  - _Depends: 3.1_
  - _Requirements: 1.3, 5.1, 5.3, 5.4, 5.5, 6.4_

- [ ] 4. Freeze the versioned runtime descriptor and checked browser reader
  - Define and validate the design's lifecycle, ownership, image, origin and compatibility fields. Reject legacy/unknown schemas rather than silently upgrade private state.
  - Complete the storage module's internal captured-pipe read command; it returns only the checked object to a pipe, while public output remains sanitized. Exercise errors without exposing private payloads in process exceptions.
  - Done: exact descriptor round trips, prepared/ready validation, unknown-version rejection, terminal-output refusal and captured private IPC tests pass. Consumers receive stable schema and reader environment contracts before fan-out.
  - Whole-file 400/300/50 checks pass for descriptor and modified storage modules; independent review covers the private IPC boundary.
  - _Boundary: Runtime descriptor and private IPC_
  - _Depends: 3.2_
  - _Requirements: 1.3, 2.2, 5.3, 5.4, 5.5, 6.4_

- [ ] 5. Start an isolated Compose image pair
  - Implement explicit project/files/environment invocation and effective-config validation. Replace inherited ports and state mounts; reject public bindings, repository deployment state, build directives or unexpected services before startup.
  - Resolve exact image IDs, persist prepared ownership before side effects, and verify the Windows host-to-daemon bind mapping with the nonsecret sentinel. Keep `/data` as an owned bind mount.
  - Reuse existing Full configuration, health, readiness and disposable-login checks without provider requests. Record actual loopback origin, both image identities and resource labels/IDs.
  - Done: a real Podman Compose session reaches ready with a valid private descriptor and verified mount mapping; merge/mapping/readiness failures fail explicitly with sanitized diagnostics.
  - Whole-file 400/300/50 checks pass for the coordinator/helpers; template/configuration receives physical checks. Use approved available images here; final fresh-build acceptance is task 11.
  - _Boundary: Compose startup_
  - _Depends: 4_
  - _Requirements: 1.1, 1.3, 2.1, 2.2, 2.5, 4.3, 5.4, 6.4_

- [ ] 6. Preserve state and recover or clean only owned sessions
  - Implement recreation preserving origin, session name, image pair and bind state while refreshing container identities after readiness. Route maintained lifecycle helpers through the coordinator.
  - Handle interrupted/partial startup using recorded ownership; require matching daemon, resource IDs, labels and mount identity before mutation. Stop preserves state by default; explicit removal rechecks private path ownership.
  - Done: real recreation changes the Workspace container ID while retaining state; wrong-daemon/replacement-resource cases refuse mutation; repeated cleanup handles already removed resources and leaves unrelated containers/state untouched. No unqualified prune or volume deletion.
  - Whole-file 400/300/50 checks pass for all touched lifecycle helpers, including those under tests. Independent review inspects actual recovery and cleanup evidence.
  - _Boundary: Compose lifecycle_
  - _Depends: 5_
  - _Requirements: 1.3, 2.3, 2.4, 2.5, 5.4, 5.5, 6.4_

- [ ] 7. (P) Run the existing browser infrastructure natively
  - Replace Linux Chromium suffixes and POSIX-only entry detection with pinned Playwright platform resolution. Move Python/browser scratch outputs through validated external roots and preserve configured temporary settings.
  - Retain hidden processes, fresh contexts, Chromium diagnostics, bounded workers, login budgets and owned process-tree cleanup.
  - Done: existing infrastructure success/failure checks pass on Windows with the pinned browser, sanitized console/network evidence and correct artifact placement. No user-browser attachment or credential-entry capture occurs.
  - Whole-file 400/300/50 checks pass for maintained verification runners/configuration. This lane does not edit runtime, private storage or shared command helpers.
  - _Boundary: Browser execution and evidence_
  - _Depends: 4_
  - _Requirements: 1.1, 1.3, 3.1, 3.3, 3.4, 5.2, 5.3, 6.4_

- [ ] 8. Connect financial browser consumers to checked private state
  - Implement the typed TypeScript reader bridge and use it in root financial tests and the isolated owned-fork shared login fixture. Both platforms must supply the checked reader; remove direct private-file reads without adding an unchecked fallback.
  - Replace the checkpoint's repository-path guard with the owned external evidence root. Preserve initial exclusive creation, image/name equality, changed-container assertions and all financial UI expectations.
  - Done: focused consumer checks prove checked-object use, malformed/error rejection, secret-safe IPC failures and external checkpoint confinement. Review the test-only fork delta independently; controller records its exact commit for the later pin join.
  - Whole-file 400/300/50 checks cover the new maintained reader and touched runner logic; fixture/test assertions are excluded under the established test policy. Record the exclusion and exact fork change, not an empty change manifest.
  - _Boundary: Financial browser descriptor integration_
  - _Depends: 7_
  - _Requirements: 3.2, 3.3, 3.4, 5.3, 5.4, 5.5, 6.4_

- [ ] 9. (P) Adapt existing image commands to native executable selection
  - Forward explicit Dagger executable, owned engine and SDK interpreter inputs; preserve strict CLI/SDK/engine validation and backend-specific transport without invoking the workstation wrapper.
  - Use the shared container selection in existing load/inspect/catalog/publication/packaged helpers. Preserve argument arrays, source revision/origin/dirty-tree validation and normalize filesystem identities rather than path spelling.
  - Done: existing focused build/publication/source tests plus native path/argv cases pass, including wrong-version, wrong-engine and modified-source failures. Publication semantics remain unchanged; no publication is performed.
  - Whole-file 400/300/50 checks pass for all modified production helpers. This lane reads frozen shared helpers only and does not edit the dirty unrelated catalog CLI.
  - _Boundary: Native build and image adapters_
  - _Depends: 4_
  - _Requirements: 1.1, 1.2, 1.3, 4.1, 4.2, 4.3, 4.4, 5.2, 5.3, 6.4_

- [ ] 10. Qualify the pinned native build path
  - Use the existing foundation image to demonstrate one native export/load through the explicit pinned CLI/SDK/engine and Podman transport. Verify engine identity before and after, archive provenance and actual loaded image identity.
  - Do not claim success from CLI connectivity, mocks or the globally installed 0.21.11 engine. Unsupported pinned transport remains a blocker requiring a reviewed correction, not silent substitution.
  - Done: native foundation export/load and existing archive/image checks pass with exact identities, external outputs and no WSL shell. Record the executable command and failure evidence if qualification fails.
  - This task adds execution evidence rather than production code; production caps do not apply to logs/reports. Any required adapter correction returns to task 9's scoped review and caps.
  - _Boundary: Native build qualification_
  - _Depends: 9_
  - _Requirements: 1.1, 4.1, 4.2, 4.3, 5.2, 6.1_

- [ ] 11. Integrate and verify the native application workflow
- [ ] 11.1 Join native commands and reviewed source identities
  - Integrate accepted runtime/browser/build consumers into the native entry point. Promote only the reviewed test-only Workspace fork commit and corresponding source-lock/inventory changes, preserving unrelated work.
  - Freeze the actual financial test node selection and its provider dependencies, query scope and maximum request budget before live execution. Confirm credential availability privately and whether that budget is authorized; obtain missing authorization before dependent work. No retry expansion or unrelated provider requests.
  - Done: supported native actions route to accepted consumers with checked descriptor, explicit tools and exact reviewed source identities; focused dispatch and contract checks pass. The application acceptance inputs are recorded, not represented as executed.
  - Whole-file 400/300/50 checks pass for the shared entry-point join and reviewed scope; generated locks are excluded. Independent review checks the integration and fork pin promotion.
  - _Boundary: Explicit native command and source integration_
  - _Depends: 6, 8, 10_
  - _Requirements: 1.1, 1.3, 3.2, 4.1, 4.2, 5.3, 6.4_

- [ ] 11.2 Build and verify the actual application image pair
  - Build the actual Workspace/data image pair once through the qualified path; reuse those exact images for existing packaged smoke and browser acceptance. Serialize heavy builds and suites.
  - Done: exact engine, archive, source, loaded image and installed module identities pass existing packaged checks for both images. No publication or provider call is needed for this build/package qualification.
  - Evidence/generated outputs are excluded from production caps; required production corrections return to their owning task's independent review and 400/300/50 gate.
  - _Boundary: Native application image qualification_
  - _Depends: 11.1_
  - _Requirements: 1.1, 4.1, 4.2, 4.3, 5.2, 6.1_

- [ ] 11.3 Accept the existing financial browser and recreated-state journeys
  - Start the exact qualified image pair and run the selected financial journeys for name/symbol selection, displayed values, linked refresh, independent comparison, save/reopen and fresh-login recreation with retained state. Preserve failure cases and financial assertions.
  - Require task 11.1's explicit authorized provider scope/budget and credentials for provider-backed cases. Missing inputs leave this task open; offline cases do not substitute for real financial acceptance.
  - Done: packaged readiness, selected financial journeys and recreated-state assertions pass with sanitized diagnostics, bounded workers/logins and owned cleanup. Existing test failures cannot be hidden by exclusions or replaced with health probes.
  - Independent Astra review accepts cross-component and private-state evidence. Evidence/tests are excluded from production caps; production corrections return to their owning scope's 400/300/50 checks.
  - _Boundary: Explicit runtime and financial browser acceptance_
  - _Depends: 11.2_
  - _Requirements: 1.1, 1.3, 2.2, 2.3, 3.1, 3.2, 3.3, 3.4, 4.3, 5.3, 6.1, 6.4_

- [ ] 12. Verify Linux compatibility and close the migration evidence
  - Run affected portable tests and the existing `pipeline/ci.sh check` entry point in Linux CI with the same reviewed source; include the changed private-reader consumer contract. Windows results cannot substitute for this check. Use the existing prototype workflow's nonpublishing check path (`build_images=false` for manual dispatch); do not dispatch an application release.
  - Verify final cleanup, artifact placement and absence of private configuration in publishable evidence. Update current developer commands, roadmap/README checkboxes and breadth links to actual test paths/results while preserving historical WSL evidence.
  - Done: Linux compatibility and bounded native acceptance are independently reviewed; one concise sanitized acceptance record identifies revisions, image IDs, commands, exit codes and remaining limitations. Sync selected artifacts before the final selective commit/push. No owner-server deployment claim.
  - Run the existing combined shared-module/inventory gate on exact accepted changes; 400/300/50 caps apply to production corrections. Docs/generated evidence are excluded. Do not repeat unchanged suites merely to create another report.
  - _Boundary: Explicit portability and evidence closeout_
  - _Depends: 11.3_
  - _Requirements: 2.4, 4.4, 5.1, 5.2, 5.3, 6.1, 6.2, 6.3, 6.4_

## Dispatch graph and joins

Foundation is `1 -> 2 -> 3.1 -> 3.2 -> 4`. After task 4, runtime `5 -> 6`, browser `7 -> 8`, and build `9 -> 10` have disjoint writable paths. Run at most two implementation lanes at once, reserving one reviewer slot. Shared dependency installation, real Compose sessions, native exports and image builds use the controller's single heavy-operation queue. Tasks `11.1 -> 11.2 -> 11.3` join commands/source pins, qualify the image pair and accept financial browser behavior separately; task 12 closes Linux portability and evidence.

Every implementation handoff includes exact writable paths, prerequisite commits, the frozen design contracts, focused check command and size limits. A contract change pauses dependent lanes for review. No task is complete from planned checks, skipped provider cases or empty reports.
