# RC0G independent production review

APPROVED for the inactive pure geometry transfer on 2026-10-24. The typed helper preserves the independently reviewed analytical contract and stays within the exact two-file boundary. Controller-owned inventory and combined maintained-scope verification still gate task completion. This is not complete RC0, Radial rendering, financial semantics or application acceptance.

## Frozen scope and identity

| File, relative to Workspace terminalpro | SHA256 |
| --- | --- |
| `src/components/General/Table/Chart/echarts/radialColumnShape.ts` | `7a69f996c8d47cd4e4aea5783b65e682e3dc1df20deda54ae2cf740a071caeb6` |
| `tests/unit/chart-compatibility/radialColumnShape.test.ts` | `7d62176f1e45e5e7e232a7c5b4c6f8c89329d751edb7802a68082eaabc9bf94d` |

Fresh hashes match the implementer's frozen manifest after review. Both files are new/untracked, so ordinary git diff was empty; I read their complete current contents and verified status rather than treating an empty diff as evidence of no changes. Search finds no production consumer or routing activation of the helper.

Compared the typed implementation with approved analytical geometry SHA256 `671f92739f4314776374db64440bf33f3551e2cbebc832469766ff29060ca563`. Directed radii, explicit caller connectivity, circle shoulders, flat stack seams, upward local coordinates, split baseline arcs, open zero paths and RangeError validation remain unchanged. Added type interfaces and rationale comments do not introduce another data/state owner. There are no AG imports or copied oracle dependencies.

## Fresh checks

The other reviewer and RC2 implementer released the test slot before this run; I released it immediately afterward. Executed the focused Vitest command from check.sh without executing its formatting mutation:

```sh
node node_modules/vitest/vitest.mjs run tests/unit/chart-compatibility/radialColumnShape.test.ts --config tests/unit/chart-compatibility/vitest.config.mjs --maxWorkers=1
```

Pinned Node 24.22.0, WSL Debian, Workspace terminalpro working directory: exit 0, 30/30 tests, one file. This rerun uses the final typed no-fill literal changes that had not been rerun by the implementer. Fresh focused Biome lint exits 0, checks both files and applies no fixes. Fresh strict TypeScript `--noEmit -p artifacts/chart-radial/rc0g/tsconfig.json` exits 0 on production plus test. These are focused checks, not a claim that the entire upstream Workspace typecheck is clean.

Fresh existing syntax measurement: production 99 physical lines, 56 logical units, maximum function 36; all 400/300/50 caps pass. Tests have 186 physical lines and are excluded from production caps. Placeholder/secret-pattern scan found no matches in the two files. No broad suite, browser, build or formatting command was run.

## Boundary and test judgment

The helper accepts only already-resolved plot pixels, each finite and bounded to absolute value at most 1,000,000. It rejects larger values without clamping. Source observation absence, normalization, grouping, scale domains and caller error presentation remain outside this function. The explicit zero flag correctly leaves fill handling with the future caller; zero geometry is not a missing-value policy.

Tests exercise actual ECharts parsed-path containment against independently stated strip/disk inequalities, including inward segments, shoulders, thin segments and explicit connection outside the original caller's usual threshold. The vertical-extremum test checks both sides of the boundary and retains the known split-arc regression, rather than relying solely on command counts. Zero tests assert open output, no fill containment and curved stroke centerline behavior. The five-field overflow tests cover the prior failing finite-large input class; exact-bound geometry remains finite and pickable. Structural invalid inputs reject with RangeError.

The tests would fail for missing geometry, sector substitution, a flat connected baseline, the known containment regression, invalid-input admission or filling zero paths. They are meaningfully scoped. Rotation belongs to the future caller; the unchanged local geometry already has rotated original-oracle research evidence, and this transfer does not introduce transform code. Default ECharts stroke hit tolerance explains the test's 10-pixel outside probe; the centerline assertions remain intact and no stroke-width equivalence claim follows.

Prior independently examined research supplied the relevant failing evidence: unsplit baseline containment mismatches and accepted-input overflow to NaN. This transfer retains their passing regressions. No separate application RED, live financial evidence or activation acceptance is claimed for this pure inactive helper.

## Remaining controller gate

Register the maintained production path in the agreed inventory and run the combined gate using the actual pinned fork scope. Keep the frozen hashes when staging the two files, and preserve other lanes' unfinished edits. A later family mapper must retain caller-selected baseline semantics, missing-data decisions, numeric domains, zero fill/stroke rules and existing lifecycle owners. None is silently accepted here.

Only this ignored review file was written. No production edits, commits or pushes occurred.
