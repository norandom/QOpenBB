# Heatmap application acceptance review

APPROVED for the bounded HM4 Table/File application milestone on 2026-10-25. The independent reviewer inspected the executed test sources, frozen run identities, financial observations, saved models, strict diagnostics and exported PNGs. No blocking finding remains. Publication and installed deployment are separate gates.

## Evidence and source identity

| Completed run under artifacts/chart-heatmap/hm4/browser | Result | Workspace / image |
| --- | --- | --- |
| candidate2-default | 1 passed, 40.9 s, exit 0 | `c7a7633fd1b864647f55c08dd5ce0d4654fe93a0` / `sha256:e47ef653049844fd77a7bfbd8c27d963400f0f946779f05d7109a9ecd1d36426` |
| candidate3-controls-2 | 1 passed, 71.6 s, exit 0 | `5cae43a52317264067951b111048664292882ec2` / `sha256:6dc3dbfef52cbaa16cdc062d672c63a114a2d6dc8a17daf32a148c915390d42d` |
| candidate3-missing | 1 passed, 28.7 s, exit 0 | same candidate3 source and image |

All runs used one isolated headless worker and the packaged application, with no source overlay and only the disposable data mount. Final runs report no skipped, unexpected or flaky cases. The reviewer did not repeat the browser suite.

The two final test files match their frozen copies in both successful candidate3 runs, SHA-256:

- `heatmap-chart.spec.ts`: `06db99916476aa21f4a9c7a51697e33f90f2c18b2870c14537e76c89666d4591`
- `heatmap-empty.spec.ts`: `0eac8e723614b1b36c002b2d8337ba1ce4eff8bdcfeb39dad17b0520a81dfef0`

These are the regression sources to retain in the Workspace fork. Original-reference probes and raw authenticated evidence remain local. Existing two-file Biome evidence was inspected; no additional heavy verification ran during review.

## Accepted behavior

Candidate2 verifies all eight AAPL FY2025 quarterly cost-of-revenue and gross-profit observations in USD in both light and dark themes, through independently identified cell tooltips. The retained fixture hash is `ca76bb6fedb7a45709b050bc810c57784ac5543b42120b341b9db0690201331b`. Values remain raw comparable USD; labels round to billions. The owner accepted the populated appearance, including the small plot-width and legend-offset differences.

That populated appearance acceptance transfers to candidate3 because its only production delta is the independently reviewed zero-selected-series presentation. Final candidate3 evidence again verifies all eight financial observations after File refresh, fresh populated reopen and fresh empty-selection recovery. No new populated-renderer change warrants another default run.

Controls exercise distinct saved and painted axis widths, labels, tooltip suppression/restoration, paired legend reversal and category recapture. Seven recorded lifecycle stages establish zero-series DOM visibility, retained connected 619 by 593 hidden canvas, category-only persistence, populated fresh-context reopen, saving empty selection from that context, and a second fresh-context reopen followed by eight-cell recovery. Populated appearance options survive reopen. Strict browser/CDP checks pass before each context closes; the main and final empty-context diagnostic arrays are also retained empty. The middle context's clean diagnostics are asserted in executed source rather than separately serialized.

The reviewer visually inspected the actual downloaded populated and empty PNGs: eight labeled cells and gradient remain, and the empty export contains centered no-data text. Executed export checks compare relevant pixel regions with the mounted renderer. This establishes candidate export behavior; it does not claim original empty-export parity.

The actual blank-CSV journey retains the selected Missing domain and category labels without finite paint, gradient, tooltip or no-series DOM message. Selecting Companion restores value 10 and its identified tooltip. The truncated one-field CSV row is removed by the parser; this does not establish arbitrary sparse public-grid admission.

## Retained failures and limits

Candidate2 controls exposed the missing DOM message and led to the reviewed source fix. The first candidate3 controls run reused an earlier session after a fresh login; backend login deliberately deletes previous Pro sessions, so its later save failed. The corrected harness closes each prior page after strict diagnostics before the next login. Failed evidence remains retained, not relabeled as a pass.

First-login onboarding's separately observed 404 remains outside this ordinarily onboarded-user acceptance. Diagnostics were not suppressed and questionnaire state was not seeded. Original empty-export behavior, live provider entitlement/lifecycle, release-image rebuild equivalence and owner-server deployment are not established here.
