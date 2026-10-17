# Task 2.44 source contract is ready for independent review

Grouped-column tooltip edits now use the existing addressed session and integrated reducer. The event accepts only `single`, `shared`, and `compact`, and produces exactly `bar.tooltip.mode`. The stored value for the original Multiple label is `shared`; label strings are rejected at this boundary. A valid stacked-column tooltip event returns a session `unresolved` family diagnostic after stamp validation. The standalone mapper rejects that combination. Malformed events remain `invalid`.

The approved task brief was to preserve the four existing column events for both families, retain the latest supplied storage and saved baseline while editing, reject stale address/generation/data/render stamps before inspecting the event, and contain hostile event descriptors without getter execution or writes. The three modified production files must satisfy the whole-file 400 physical/300 logical/50 per-function caps. The owner explicitly waived the temporary feature-flag protocol for this source-contract task.

## Scope and criteria

Only these production responsibilities changed: `compatibility/optionStateTypes.ts`, `compatibility/editorEvents.ts`, and `application/sessionState.ts`. Tests extend the two assigned existing test files. `application/types.ts`, the option baseline selector, reducer, legacy validator, renderer, UI, guards, save triggers, dependencies and shared metadata were not edited. Concurrent sibling composition and unrelated Perspective work were preserved.

Requirements 4.2 and 4.7 receive source-level preservation evidence through the real reducer; backend/dashboard reopen remains outside this task. Requirements 4.8 and 4.9 receive the exact original tooltip option namespace and retained existing-event behavior. Requirements 10.4, 10.5 and 10.6 receive isolated bounded execution, actual test identities and frozen evidence. The controller owns breadth registration and complete inventory acceptance.

The reviewed design references are `chart-appearance-editor-integration-design.md`, Components and Interfaces / Tooltip event and state contract; File Structure Plan; Dependency Plan and Complexity; and Testing Strategy and Failure Handling. No renderer tooltip, B2, docked editor, application activation or persistence acceptance is claimed.

## Reproduction and observed results

The isolated Debian stage is `/home/mc/qopenbb-work/task244-20261017140641/terminalpro`. It reuses accepted task 2.41 dependencies and pinned Node 24.22.0. `stage.py` copies current source/configuration/test bytes and checks their SHA256 identities. Pending sibling composition/color modules and tests are omitted because they were absent at the frozen prerequisite; the controller's joined stage owns their combined verification. The RED, GREEN and final manifests remain separate.

`run_check.py` invokes pinned Node with explicit subprocess argument arrays, environment and cwd. Its JSON sidecars preserve each command, exit and duration; matching logs preserve complete output. From the stage:

| Check | Command arguments after pinned Node | Observed result |
| --- | --- | --- |
| RED exact patches | `node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/editorEvents.test.ts` | Exit 1: 3 failed, 69 passed; each enum fails with `event.kind is unsupported` before production edits |
| RED session integration | `node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs tests/unit/chart-application/sessionState.test.ts` | Exit 1: 6 failed, 15 passed; grouped edits invalid and stacked tooltip invalid rather than unresolved |
| GREEN exact patches | Same focused compatibility command | Exit 0: 72 passed, no skips |
| GREEN session integration | Same focused application command | Exit 0: 21 passed, no skips |
| Strict application | `node_modules/typescript/bin/tsc --project tests/unit/chart-application/tsconfig.json --noEmit` | Exit 0 |
| Strict compatibility | `node_modules/typescript/bin/tsc --project tests/unit/chart-compatibility/tsconfig.json --noEmit` | Exit 0 |
| Final touched-path lint | `node_modules/@biomejs/biome/bin/biome check` followed by the five assigned source/test paths | Exit 0: checked 5 files, no fixes |

The first two RED launcher attempts failed before testing because the PowerShell/native `sh -c` argument boundary exposed shell PATH quoting; `launcher-failure.txt` records this. They are not behavioral RED evidence. The explicit subprocess runner fixed the launcher. The first lint check found formatting/import organization errors, retained in `lint-initial.log`. Biome fixed three files; its final check passes. These were formatting/import-only changes after GREEN and strict checks. No behavioral correction was needed after GREEN. The independent joined review will rerun complete suites against the final frozen bytes; no unconditional suite rerun was added here.

`measure.py` invokes the existing `tools/quality/syntax_units.ts` parser against the complete owned production files. `size.json` records source hashes and callable measurements:

| Whole file | Physical | Logical | Largest function |
| --- | ---: | ---: | ---: |
| optionStateTypes.ts | 41 | 35 | 0 |
| editorEvents.ts | 98 | 55 | 18 |
| sessionState.ts | 195 | 107 | 19 |

All three pass 400/300/50. Tests and evidence scripts are excluded from maintained production caps. The parent still runs the complete maintained inventory gate with actual fork manifests.

## Behavior evidence

The new mapper cases assert exact nested patches for all three enum values and reject Multiple/other label strings, arbitrary paths, extra string/symbol fields, inherited fields, non-enumerable fields, accessors and throwing proxies. Existing cases still verify title text/enabled, legend position and stroke width for both column families.

The new session cases call the actual baseline selector and reducer. They supply latest storage containing unknown root/partition/model fields and inactive-family ranges, then pass selected `baseline.options` independently from a deliberately conflicting `currentModel.chartOptions` containing a rendering-only title/fill. The expected stored result retains prior title/legend, unknown and inactive-family options and the current model, and contains only the requested tooltip mode change. The supplied inputs remain unchanged. A valid stacked tooltip uses a storage proxy that throws on access and still returns unresolved, proving storage reduction is not reached. Malformed/accessor/revoked/throwing-proxy events return invalid. Every stale stamp dimension returns stale before inspecting a hostile event.

No new TODO, FIXME or TBD markers remain in changed production files. The scoped Git whitespace check passes. `source-manifest.json`, `owned.diff`, and the `source/` snapshots identify final owned bytes; `publication-allowlist.json` lists completed synthetic evidence and scripts with verified SHA256 hashes. It excludes credentials, private state, dependencies and historical unrelated evidence.
