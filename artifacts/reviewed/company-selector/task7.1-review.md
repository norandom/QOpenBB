# Browser case authoring is approved; live acceptance remains pending

## Review Verdict

- VERDICT: APPROVED
- TASK: company-selector 7.1, browser case authoring; criteria 1.1-1.5.
- MECHANICAL_RESULTS:
  - Tests: discovery PASS, exit 0; three cases in the existing runner. No browser tests executed.
  - TBD/TODO grep: CLEAN.
  - Secrets grep: CLEAN; zero concrete credential-pattern matches and no credentials introduced in the diff.
  - Static checks: PASS; scoped strict TypeScript exit 0, no diagnostics. Diff whitespace exit 0.
  - Boundary: WITHIN; only the existing financial test changed. No production helper, fixture, configuration, dependency or harness change.
  - Boundary audit: CLEAN; runtime recreation remains controller-owned and synthetic responses are separately labelled.
  - RED phase: N/A for this authoring-only task. Discovery/static readiness is its explicit completion gate; task 7.2 owns execution.
- FINDINGS:
  1. FYI: no blocking finding. Discovery establishes test loading, not financial or persistence acceptance.
- REMEDIATION: None for task 7.1.
- SUMMARY: The bounded cases cover the approved journey and are ready for packaged execution under task 7.2.

## Reviewed identity and contracts

Reviewed on 2026-10-30 using the kiro-review protocol. Frozen `tests/e2e/financial-workspace.spec.mts` SHA256 is `21800e9e15e26797dd55c0ed5066423d289e271ee391cb6da3b923bcc0c6450d`, independently rechecked after static verification. Root context is task 6 at `4e686f1`; the inspected native checkout HEAD is Workspace `ab3c357a00cd9ad7395ea2cad0cdbec09a2f3598`, with unchanged accepted data API `28423762e8cc3faae978e770899834b41e7cde99`.

I read the requirement, design and exact task 7.1 boundary, the actual diff and full added cases, and the worker report. Native inspection covered `CompanySymbolSelector`, `QueryParams`, `CompareTermsParam`, `GroupDropdown`/`GroupRow`, `useSyncItems`, and existing browser fixtures, save helper and CDP diagnostics. Their labels, portal roles, comparison trigger labels, group controls and saved-state read contracts align with the authored cases. A direct text comparison independently confirmed that the original Income helpers and regression body remain unchanged; only imports were extended before that original block.

The real case selects actual MSFT and AAPL search listings, checks option attribution and source-qualified persisted sibling metadata, and compares visible Profile/Income/FRED cells to captured responses. Income assertions retain fiscal date, period, currency and unit/scale provenance; number comparisons account for display rounding and the added amount helper requires a fully visible cell. Independent comparison/FRED parameters and comparison group value are checked against a saved baseline, with a request-count sentinel during selection. Financial requests reject extra query keys, keeping selection metadata outside request parameters.

Save/fresh-login checks use the existing sync and validate-and-sync interfaces. The second phase requires the same images/runtime name and a changed container ID before checking restored state and another fresh login. A checkpoint is written only after initial assertions and diagnostics pass. The controller must actually retain the bind and recreate the runtime; this test does not perform or independently prove that operational step.

The synthetic case exercises Tab, arrow/active-descendant, Escape, Enter, entitlement and empty-result feedback, and an obsolete delayed search after a newer selection. Its intercepted names and financial amounts are explicitly synthetic. Diagnostic exclusions are bounded by route/status; separate response records additionally reject any real financial 422 carrying a nonempty Symbol. Aborted search requests are identified separately. Other application failures remain asserted.

## Fresh mechanical evidence

Node `24.22.1` and installed Playwright `1.64.0` were reused under WSL Debian. Commands ran from `/mnt/d/Source/QOpenBB`:

- Discovery: `WORKSPACE_EVIDENCE_ROOT=.../task7.1-review-discovery WORKSPACE_FRONTEND_ORIGIN=http://127.0.0.1:23003 PLAYWRIGHT_BROWSERS_PATH=/home/mc/.cache/ms-playwright QOPENBB_PLAYWRIGHT_PACKAGE=/mnt/d/Source/QOpenBB/verification/node_modules/@playwright/test artifacts/task-1.2/node-v24.22.1-linux-x64/bin/node verification/node_modules/@playwright/test/cli.js test --config verification/financial-workspace.config.ts --list`; exit 0. Cases at lines 137, 461 and 630; retained log `task7.1-review-discovery.log`.
- Strict static check: `artifacts/task-1.2/node-v24.22.1-linux-x64/bin/node verification/node_modules/typescript/bin/tsc -p artifacts/company-selector-implementation/task7.1-types.json`; exit 0. Retained empty diagnostic log `task7.1-review-types.log`. The ignored config maps existing pnpm Playwright types without changing maintained configuration.
- `git diff --check -- tests/e2e/financial-workspace.spec.mts`; exit 0. The existing LF-to-CRLF checkout warning is informational.
- Placeholder/secret scans and exact original-block comparison passed. Tests are excluded from production caps; no maintained helper needs a 400/300/50 measurement in this slice.

My first discovery invocation omitted `QOPENBB_PLAYWRIGHT_PACKAGE` and was rejected by the existing fixture guard before discovery. Adding the required package setting resolved that setup error; the successful invocation above is the readiness evidence. No browser, build, provider call, dependency install or source mutation occurred.

## Limits and preserved work

Actual selectors, provider entitlement, rendered screenshots, runtime recreation and financial persistence have not passed live execution in this review. Those remain task 7.2 checks, alongside the retained Income regression and labelled synthetic case. The report does not approve release publication or deployment.

Foreign inventory/catalog changes remain untouched. Required default steering files `product.md`, `tech.md` and `structure.md` are absent in this checkout; the existing task-specific testing, complexity, delegation, documentation and CI guidance was read. No new requirement or production exception was inferred from their absence.
