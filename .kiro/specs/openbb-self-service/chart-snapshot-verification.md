# Resolved chart snapshot verification

All five approved tasks are accepted. The isolated snapshot and Cartesian mapper preserve supplied observations and feed the accepted ECharts host. This record covers tasks 2.19-2.23 only. Original Workspace controls, complete chart families, grid transformations and application persistence remain outside this acceptance boundary.

## Source boundary

The comparison base is Workspace `042ba87e3208a51857da4ae2d1c3109a680716d9`. Contract task 2.19 is `8c12a9127cd913e5f6ebb8a9dfe3fd82ba56138f`; snapshot task 2.20 is `616a0a70241fd15a10e0dc91dcec93cf701847ac`; mapper task 2.21 is `59118937434b9f5a9bebd4e80bcb54f7ca2d552e`. Browser task 2.22 is `06fdb859bf426eb44dce13c54b21c494fcc244fd`. Independent Astra verification passed. Task 2.23 final joined review returned APPROVED and GO for tasks 2.19-2.23 only; the completion claim is VERIFIED in `artifacts/task-2.23/review/verdict.md`.

No package, lockfile, original application caller, feature flag, reducer or host implementation changed. The two Sol implementation lanes used frozen shared contracts and separate test stages. Independent Sol reviewed snapshot validation; Astra reviewed the shared contracts and financial mapping. The controller serialized commits and the browser/build queue.

## Numerical and rendering evidence

| Boundary | Observed result | Evidence |
| --- | --- | --- |
| Shared contracts | Deep readonly types and explicit diagnostic/result contracts; 46 existing foundation tests and strict compilation pass | `artifacts/task-2.19/review/` |
| Snapshot validation | 26 tests pass; preserves order, precision, null/missing/zero, special IDs and opaque JSON; rejects invalid identities, unsafe accessors, cycles and nonfinite data | `artifacts/task-2.20/review/` |
| Cartesian mapping | 52 tests pass; exact grouped columns, stacked columns and lines; stable series identity, repeated-category positions, raw values, explicit styles and unsupported outcomes | `artifacts/task-2.21/review/` |
| Independently verified join | 124 tests, strict compilation, fixture build and three one-worker browser cases pass | `artifacts/task-2.22/review/check.log`, `browser-results.json`, `review.md` |
| Complexity | All nine compatibility/renderer modules pass 400 physical / 300 logical / 50 per function; new mapper is 273/90 with largest function 15, snapshot is 110/122 with largest function 29 | `artifacts/task-2.23/module-quality.json` |
| Tested identities | Twenty module, fixture and dependency files match the tested stages byte-for-byte | `artifacts/task-2.23/tested-source-hashes.json` |

The actual browser fixture calls the validator, mapper and host. Synthetic Revenue/Costs use the same USD unit and scale. Repeated dates retain separate positions; two negative observations stack at one category position. Numeric options preserve the supplied fractions. Settings edits advance render revision while data revision remains 7. Invalid and unsupported submissions leave the accepted render unchanged; valid input recovers. Existing host regression separately exercises renderer failure and cleanup.

The initial image check caught export during animation. The fixture now disables animation explicitly, and image checks count plotted colors inside the plot region. Fresh report images show the completed line and negative stacks. Older extracted PNGs are not acceptance evidence; use the independently reviewed report and its matching images.

## Limits and reproduction

Use the maintained chart commands in [chart foundation](../../../docs/chart-foundation.md); the same configuration now discovers the additional unit and browser tests. Verification remains outside Dagger. Run with the pinned Node/dependency environment, explicit evidence root/browser cache and one background browser worker.

The mapper supports flat, unaggregated inputs with explicit compatible units and scales. This is an isolated development boundary, not a new production restriction. Original mixed-unit/multi-axis behavior, editor field decoding, grid capture, full family coverage, themes, table features and real save/restart/reopen require later integration. Requirements 4.8-4.9 and a deployable release remain unverified. No live provider, Anthropic or Excel acceptance is implied.

Final independent verification reproduced all 124 unit tests, strict compilation and fixture build, rechecked all nine module caps and twenty source/dependency identities, and checked metadata and documentation links. It reused the matching-source independent task 2.22 browser evidence explicitly: three passing cases, no skipped/flaky cases and empty CDP diagnostics. No production code changed after that browser verification.
