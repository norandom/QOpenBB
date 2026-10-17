# Explicit Cartesian appearance verification

Tasks 2.28-2.33 are independently accepted with scoped GO and VERIFIED completion. This boundary makes explicit styling available to the isolated mapper; original Workspace theme resolution and application integration remain open.

## Accepted components

| Task | Result | Independent evidence |
| --- | --- | --- |
| 2.28 | Additive style types and homogeneous financial fixtures; 221 existing units, strict checking and scoped lint passed | `artifacts/task-2.28/review/review.md` |
| 2.29 | Validated style projection, separate fill/stroke and caption typography; 250 units, strict checking and lint passed | `artifacts/task-2.29/review/review.md` |
| 2.30 | Real mapper/host browser scaffold; strict checking, four-entry build and lint passed | `artifacts/task-2.30/review/review.md` |
| 2.31 | Mapper delegates appearance while retaining numerical handling; 260 units, strict checking and lint passed | `artifacts/task-2.31/review/review.md` |
| 2.32 | Four independently reproduced browser cases, exact data and visible/exported pixels, empty CDP diagnostics and cleanup | `artifacts/task-2.32/review/review.md` |

The style module distinguishes malformed input from a well-formed unsupported active marker shape. Optional fields preserve legacy behavior when absent. Title text survives disabled visibility. Caption typography, independent column fill/stroke, line connection and circular markers project through existing ECharts options. Null observations remain null; connection changes only the drawn line. Per-series overrides follow stable descriptor IDs and palette fallback follows selected series order.

## Source and runtime

Starting Workspace revision: `5c2df9864bed000170ffccde146273b468e0552e`. Accepted component commits: `3b24152` (contracts), `82db64f` (scaffold), `93f7170` (projection), `fe7eab3` (mapper join). The [design](chart-appearance-design.md) owns the contract; [original line findings](chart-line-appearance-findings.md) record selected source/UI observations without claiming full visual parity.

Verification uses Node 24.22.0, locked ECharts 6.0.0, Vite 8.2.1, Vitest 4.1.11 and TypeScript 5.9.2. Root verification Playwright 1.64 runs one isolated headless Chromium worker. Application dependencies retain their existing frozen lock. Safe Chain restored 2056 packages without changing that lock. After transient `/mnt/wsl` directories disappeared, stages and dependencies moved to `/home/mc/qopenbb-work/`; the owner reported WSL fixed. Failed infrastructure starts are not test failures or passing evidence.

The test fixture contains Revenue and Costs in USD at scale 1000000, four periods and a shared interior null. Duplicate display labels exercise stable identity. Synthetic style choices are explicitly distinguished from original effective-theme defaults. No live provider/model requests, user state, application control changes or release images are part of this verification.

## Accepted browser evidence

The new regression failed against the old mapper because the expected line bridge contained zero matching pixels. Restoring the integrated mapper produced four passing browser cases, including the existing smoke, lifecycle and Cartesian journeys. The appearance journey decodes real PNG exports, counts marker-color components at non-null positions, samples the gap region, checks retained title and caption colors, switches families, resizes, exports, rejects invalid/unsupported styles without replacing the last good image and recovers with valid input. Exact observations and data/render revisions are checked alongside pixels.

Independent Astra review reproduced all four browser cases, a fresh build, 260 units, strict checks and actual lint. Source/dependency identities matched, CDP diagnostics were empty and owned processes were cleaned up. The temporary Playwright test-module link was restored to application version 1.62.1. Shell-wrapper quoting and CRLF errors were diagnosed before a normalized wrapper recorded exit 0; no product failure was suppressed. Evidence: `artifacts/task-2.32/review/`, with visible/export images under `artifacts/task-2.32/images/`. The controller inspected gap, circular-marker, hidden-title and typography images.

## Joined checks

Workspace revision `b96d36d16ba87db2dd595d5796507d473dd0c0c6` contains exactly eleven changed source/test/configuration files in this slice. Fresh `artifacts/task-2.33/check.sh` passed 260 tests across nine files, strict TypeScript, actual lint on ten supported paths, thirteen registered chart-module caps and 47 source/dependency identity comparisons. The combined repository checker passed 67 files with truthful dirty-fork manifests, no errors and no violations. Unrelated working changes were preserved.

| Maintained module | Physical lines | Logical units | Largest function |
| --- | --- | --- | --- |
| Cartesian types | 108 | 76 | No functions |
| Appearance projection | 278 | 112 | 17 |
| Cartesian mapper | 223 | 72 | 14 |

All satisfy 400/300/50 without new exceptions. Evidence: `artifacts/task-2.33/check.log`, `module-quality.json`, `repository-quality.json` and `source-identities.json`. Independent Astra final review returned scoped GO and VERIFIED completion for tasks 2.28-2.33. Its fresh checks and current-revision repository audit are under `artifacts/task-2.33/review/`; matching-source task 2.32 browser evidence supplies the runtime portion of that gate. No blocking findings remain within this boundary.

## Remaining product work

Original theme/default resolution, full light/dark layout and formatting parity, original editor/control integration, actual grid selection and transformed/mixed-unit paths, and backend save/restart/reopen remain separate obligations. No original feature or flag is removed or hidden by this slice. The overall renderer and release remain unverified.
