# Verification policy

Adapted at the user's request on 2026-10-16 from the sibling because-security-quant-terminal project's AGENTS.md, .kiro/steering/testing.md, perspective/playwright.config.js, and browser checkpoint notes. Its inspected Git HEAD was b10ffd17e5125fcf9ca973994b8be58f3c131b18; working-tree guidance was also read. This imports conventions, not that application's implementation or acceptance evidence.

## Background browser checks

Owner authorization, 2026-10-20: run routine local candidate startup and verification autonomously, including WSL Docker. Use the owned disposable runtime and loopback bindings; do not request conversational approval for each run. Tool-enforced rejections still apply and must be reported rather than bypassed.

Owner preference, 2026-10-19: open original/replacement PNG comparisons in qView for visual review. Launch the requested viewer visibly; keep automated browser verification headless and isolated. Opening a comparison does not imply visual acceptance.

- Use a QOpenBB-owned isolated browser instance/profile. A new tab in the operator's browser is not isolation. Playwright tests use fresh contexts.
- Run headless in the background. Never move the desktop pointer, inject system keyboard events, steal focus, or attach to the user's browser.
- Hide Windows helper consoles as well: Python CREATE_NO_WINDOW, Node windowsHide, or PowerShell Start-Process -WindowStyle Hidden. Capture output and clean up only owned processes.
- Use Chrome DevTools diagnostics against the owned browser endpoint to inspect console/network errors and traces. Verify tool availability and isolation before use; do not claim diagnostics ran merely because configuration exists.
- Keep raw profiles, traces, videos, storage state and logs in ignored project artifact paths. Do not capture credentials or token-entry cases. Use disposable test accounts. Reviewed synthetic screenshots and sanitized evidence are published under `artifacts/reviewed/` under the owner instruction below.
- Preserve acceptance-critical findings as Playwright regressions against the real application. Assertions verify displayed data and user effects, not just a toast, handler, HTTP 200, or visible button.
- Include success and relevant failure/recovery cases, save/reopen persistence where promised, and console/network failures. Browser checks do not prove financial calculations; those need independent data/reference assertions.

## Bounded parallel checks

- Permit up to three independent verification processes when inputs, outputs, caches, and services do not conflict.
- Run only one heavy suite/build at a time. It may overlap lightweight read-only checks. Serialize dependency installation, shared fixture mutations, and commits.
- For Python tests that use pytest-xdist, cap workers at two (`-n 2 --maxprocesses=2`); avoid unrestricted `-n auto`. Use selected files with `-n0 --no-cov` for focused review or memory diagnosis when those plugins exist.
- Start direct Playwright acceptance runs at one worker. Increase to two only after per-worker isolation of accounts, ports, Compose project names, volumes, and outputs is proven. The sibling project's PostgreSQL isolation does not prove QOpenBB isolation.
- Budget packaged Workspace logins against the existing five-per-minute client-IP limit. Runtime startup consumes one login; save/reopen journeys usually consume two each. After four browser logins in the startup window, separate the next batch by at least a minute plus a margin. Fresh contexts share the limiter. Do not change request headers or application limits to make checks pass; record any HTTP 429 scheduling failure and rerun only the blocked scope after the window clears.
- Use disposable state and worker-scoped fixtures; never the owner's live Workspace volume or provider account for ordinary tests. Live FMP checks are explicitly marked and separately configured; missing credentials mean skipped/unverified live evidence, not a pass.
- Capture each command, revision/image digest, exit code, and artifact location. Diagnose failures; do not retry until a pass without explaining the underlying fault or nondeterminism.

## Breadth and evidence

Owner amendment, 2026-10-20: chart milestone documents include a small set of representative real-FMP screenshots from verified application runs. Backfill completed milestones and mark unfinished examples pending. This authorizes selected financial chart images in the reviewed mirror after checking for credentials/private account information; retain exact source hashes and captions identifying data, units, period and tested revision. Raw provider captures and authentication artifacts remain excluded. See [chart sample delivery rules](delivery-workflow.md#chart-samples-in-milestone-documents).

Owner amendment, 2026-10-18: keep artifacts and checks to a meaningful set. For routine UI changes, publish one concise verification/review record per delivery and only screenshots needed to assess the changed view. Record source identity, commands/results, reviewer decision and limitations in that record. Raw run logs, RED output, repeated complexity dumps, per-task preview runners and intermediate screenshots stay in ignored local artifacts unless needed to explain an unresolved failure. Independent review still examines the local evidence; review does not require publishing every input. Existing phase approval and per-task commit rules remain.

Maintain regression tests beside the code, grouped by behavior rather than task number. Run the affected component/contract tests and scoped static checks during development; run a shared integration check once at the join. Run broader relevant suites at integration/release boundaries or when a concrete regression risk warrants them. Do not rerun identical checks solely to produce another report. Retain financial semantics, persistence, failure/recovery and distinct UI lifecycle coverage; never delete tests just to lower the count. Reuse browser fixtures and runners instead of copying a harness into each new published task folder.

Historical artifacts may be retired from the working tree when they are not active test inputs or needed reference fixtures. Preserve their original hashes and recovery commit in `sync-manifest.json.archived_entries`; historical publication lists remain historical records, not current-file inventories. See [artifact retention](../../docs/artifact-retention.md). The manifest's `entries` list owns the current mirror. Do not delete installed toolchains, browser caches or active fixtures as part of evidence cleanup.

Owner instruction, 2026-10-17: sync the reviewable artifact folder before committing and pushing, and include the artifacts in the repository. Use `artifacts/reviewed/` as an explicit public evidence mirror of selected local outputs. Preserve original source paths and hashes in its sync manifest, record published hashes and any sanitization or path changes, and identify omitted historical evidence. Synchronize only completed, reviewed outputs; do not copy an actively written run. Check the manifest against actual bytes before staging. Include synthetic screenshots, fixtures, reports and verification scripts needed to assess the recorded result. Exclude credentials, private account/database state, environment files, authentication traces, dependency caches and image archives. Raw evidence stays local; a sanitized derivative must not claim the original file's hash. Independently review the publication set and stage explicit paths before pushing.

`.kiro/breadth.toml` links capability -> spec criteria -> planned/implemented test -> evidence status. Planned test IDs are not executable tests. Never label a capability verified based on an empty or skipped suite. Parked PostgreSQL work is not a baseline coverage target.

During implementation add actual test paths/IDs and evidence links. Preserve upstream test entry points where usable; do not invent command names or copy Angular/Perspective-specific runners into this React application. Portable repository verification commands own the closing gate, including the relevant browser checks; Dagger only builds images, and a Python-only gate cannot certify Workspace or Excel.

Current state: foundation pytest suites validate complexity and evidence contracts. Task 1.7 accepts isolated synthetic browser/CDP diagnostics and bounded Python verification on WSL; use [verification infrastructure](../../docs/verification.md). Application, live-provider and native Windows acceptance remain unverified. The breadth map records accepted checks and remaining gaps.
