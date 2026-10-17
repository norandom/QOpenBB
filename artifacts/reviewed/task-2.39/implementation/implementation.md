# Ordinary displayed capture implementation

Task 2.39 is ready for independent review after the controller's maintained complexity check. The adapter reads public unformatted Community GridApi values and delegates snapshot structure and copying to the accepted validator. It returns the original supplied stamp; current-generation arbitration and transpose metadata remain caller responsibilities.

The task brief requires exact displayed row identity/order, selected column order, finite financial values and explicit null, independent model/range/metadata copies, no grid writes, conservative bounds, and bounded diagnostics. Production scope is one new gridCapture.ts file with the 400 physical / 300 logical / 50 per-function limits; the controller owns inventory and checker evidence.

Requirements checked: 1.1, 4.2, 4.7, 4.8, 4.9, 10.4, 10.5, 10.6. Design checked: design.md approved ordinary-grid supplement and every section of chart-grid-capture-design.md (Overview, Boundary commitments, Contract, Architecture and file structure, Verification and complexity, Sequencing and remaining joins).

RED ran before production creation: red.sh records a missing new adapter import, exit 1, red.log. No feature flag was added. The hostile/unit and real-grid assertions subsequently execute against the implementation.

Final verify.sh ran canonical chart-application tests (86 passed, zero skips), chart-compatibility tests (260 passed, zero skips), both strict TypeScript projects and scoped application/test Biome. Every final command exited 0; individual logs/exits are retained. It used a fresh Linux staging directory, pinned Node v24.22.0 and the accepted existing dependency tree. No installation, browser, build or UI activation occurred. The five accepted real-grid tests remain, with six actual-grid capture cases added. Synthetic getter instrumentation is explicitly identified.

The first shell attempt failed before test execution because bare python3 was unavailable and inline shell PATH quoting expanded Windows paths. The retained red.sh and explicit pipeline virtual-environment Python corrected the invocation; no dependency changes were needed.

The accepted fixture and Vitest configuration remain immutable. owned-identities.json records their hashes alongside the three changed paths. source-stage-manifest.json records the exact staged source/test identities and current dirty Workspace status. Raw source files and dependency trees are not publication artifacts.

Publication allowlist: the three owned code/test paths; implementation.md, stage.py, verify.sh, red.sh, final-identities.py, owned-identities.json, source-stage-manifest.json, red.log, red.exit, format.log, chart-application.log, chart-application.exit, chart-application-tsc.log, chart-application-tsc.exit, chart-compatibility.log, chart-compatibility.exit, chart-compatibility-tsc.log, chart-compatibility-tsc.exit, biome.log, biome.exit. Exclude stage-path.txt because it is a local environment pointer. Controller independently reviews and selects publication paths.

Unverified product obligations include full chart activation, numeric-only categories, general category resolution, transformed/remote captures, full renderer controls and dashboard save/restart. These helper tests do not accept the full product requirements.
