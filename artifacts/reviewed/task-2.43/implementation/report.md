# Task 2.43 is ready for independent source-contract review

The pure helper derives grid/subtitle colors from the frozen five-token contract. Its maintained suite passes 42 tests; both strict TypeScript configurations and scoped Biome pass. The complete production file measures 118 physical lines, 53 logical units and at most 16 units per function. These results establish this helper boundary. Full application, renderer, original editor, visual and persistence acceptance remain open.

`appearanceColors.ts` imports only types from `appearanceContracts.ts`. Descriptor inspection admits plain records, including null-prototype records, and reads no ordinary input properties. Unknown own fields, missing/non-string properties, accessors and inspection failures return invalid diagnostics. Supported structure with unsupported base/color strings returns unresolved diagnostics at the affected field. Every failure contains no guessed output color. Inputs remain unchanged.

The resolver preserves encoded-sRGB normalization, interpolation, clamping, multiplication and rounding order. Grid and subtitle use separate alias pairs and the approved literal dark/light ratios. Static finite expectations cover both directions of black/white bounds, primary-color alias separation, mixed-case input, the reviewed finite fixture and the `#000000`/`#9b0000` light-grid result `#8b0000`. Unsupported strings include malformed hex, names, RGB text and trailing whitespace; no CSS-validity claim or general parser is added.

The RED run was executed before the production file existed and exited 1 on its missing module import. The first GREEN attempt preserved one incorrect independent expectation: white foreground against black background under the light grid ratio was initially hand-calculated as `#1a1a1a`. Literal `1-(1-.1)` evaluates to `0.09999999999999998`, yielding `25.499999999999993` before rounding, so the correct result is `#191919`. `rounding-oracle.py/json` establishes that result independently using the specified IEEE-754 expression and its exact binary fraction. Only the test expectation changed; the production algorithm remained unchanged. `green-vitest.log` preserves the 41/42 failure and `green-vitest-retry1.log` records 42/42 passing after correction.

| Check | Evidence | Result |
| --- | --- | --- |
| Preimplementation focused RED | `red-vitest.json`, `red-vitest.log` | Expected exit 1, production import absent |
| Focused color suite | `green-vitest-retry1.json`, `green-vitest-retry1.log` | Exit 0, 42 passed |
| Strict application compiler | `strict-application.json`, `strict-application.log` | Exit 0 |
| Strict compatibility compiler | `strict-compatibility.json`, `strict-compatibility.log` | Exit 0 |
| Own-file Biome | `biome.json`, `biome.log` | Exit 0, two files checked |
| Whole-file complexity | `size.py`, `size.json` | No violations; task-local metric only |

The isolated stage is `/home/mc/qopenbb-work/task243-colors-20261017/terminalpro`. It clones frozen task 2.41, adds accepted task 2.42 composition bytes from `0a4b2ea256816111702b2de1d2a284bade9a30ec`, and adds only this lane's two files. `red-stage-manifest.json` records the preimplementation snapshot; `source-manifest.json` records the final snapshot and verifies the immutable contracts/fixtures against `bc42d60`. Pending tooltip and grid-fixture repairs are excluded. Existing accepted dependencies are reused through the stage's node_modules symlink; no install, browser or renderer check ran. Exact commands, working directories and exits are in each check's JSON. Node 24.22.0 and TypeScript 6.0.3 are recorded by the size checker; Vitest reports 4.1.11.

Self-review checked requirements 1.1, 1.4, 4.8, 4.9, 10.5 and 10.6 against Derived colors and Testing Strategy and Failure Handling in `chart-appearance-editor-integration-design.md`. Frozen contracts and fixtures are unchanged. The implementation adds no runtime dependency, state write, stored option, theme traversal, feature flag, UI control or renderer path. Production imports are type-only, and no TODO, FIXME or TBD remains. Independent review, breadth/inventory publication, full-suite verification and the combined maintained gate belong to the controller.

`publication-allowlist.json` freezes the two owned source/test files and selected safe evidence by path and SHA-256. It excludes dependency bytes and any private state. Logs contain synthetic tests and local stage paths; the initial shell-launch diagnostic is a sanitized derivative with its omission explained in `launcher-failure.txt`. No publication or commit was performed by this lane.
