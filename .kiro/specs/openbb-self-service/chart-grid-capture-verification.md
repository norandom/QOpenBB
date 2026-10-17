# Ordinary grid-capture verification

Tasks 2.38-2.40 are independently accepted with scoped GO and VERIFIED completion on the committed source. This boundary captures ordinary displayed observations; it does not activate the Workspace chart journey.

## Financial behavior

The adapter reads public unformatted Community GridApi values in displayed row order and preserves the caller-resolved series order. Duplicate category labels retain separate row IDs. Zero, negative, fractional and null values remain unchanged; a displayed percentage does not rescale its underlying observation. The admitted synthetic value getter produces its grid value rather than the raw node-data value.

The existing snapshot validator copies model, original range provenance and descriptor metadata. A1 resolves visibility before capture; the adapter does not repeat selection inference. The caller still owns current-session arbitration and transformation metadata. Empty ready grids are distinct from grids waiting for data. Unsupported models, bounds or observations produce diagnostics rather than silently changing the data.

## Evidence and repair

Workspace `76edf85a46298f7bc5212ff9944e4b66e9baa4af` passes the fresh controller join: 88 application tests and 260 compatibility tests, both strict compiler configurations and scoped Biome. All tests ran without skips. The application suite includes 41 capture contract tests, 11 actual Community-grid tests and 36 existing helper tests. Sixty-six source/configuration identities match the fresh Linux stage exactly.

The initial independent review found that a revoked Proxy thrown by GridApi escaped exception handling. Two new regressions failed before repair. Private WeakMap registration now identifies internal failures without inspecting unknown thrown objects. The original failing probe and rejected review remain published alongside the successful repair and re-review. See [task 2.38 review](../../../artifacts/reviewed/task-2.38/review/verdict.md) and [task 2.39 final review](../../../artifacts/reviewed/task-2.39/review2/verdict.md).

The original missing-module RED preceded production creation. Foundation setup tests exercised existing Community behavior and did not fabricate a product RED. The repaired adapter has 196 physical lines, 92 logical units and a largest function of 22 units, within the 400/300/50 caps. The independent final maintained-scope audit passes 173 files with no errors or violations; all four existing exception targets remain byte-identical. See the [joined verdict](../../../artifacts/reviewed/task-2.40/review/verdict.md).

## Boundary and reproduction

Only five Workspace paths changed from accepted source `945e438a9a65c3eeef7073dbce64a03b02f0ff6f`: the new adapter, its fixture and two test files, and the application test compiler's resolveJsonModule setting. Shared types, existing range/session/snapshot helpers, reducers, mapper, host, UI and flags are unchanged. Other dirty catalog and financial files remain outside acceptance.

Use `wsl -d Debian -u mc -- bash /mnt/d/Source/QOpenBB/artifacts/task-2.40/check.sh` in the recorded pinned local environment. The script creates a fresh stage and uses the accepted dependency tree; it is verification tooling, not a deployment command. Identity checks and explicit fork manifests accompany the full maintained complexity audit. Published scripts preserve their original source-relative paths.

Full appearance and editor behavior, remaining category/transform paths, application invocation, export, save/reopen/restart, renderer-complete images and deployment remain unverified. No browser, build or live-provider acceptance follows these helper tests. The next integration work retains the original 1:1 controls, theme and feature-flag obligations.
