# Verification policy

Adapted at the user's request on 2026-10-16 from the sibling because-security-quant-terminal project's AGENTS.md, .kiro/steering/testing.md, perspective/playwright.config.js, and browser checkpoint notes. Its inspected Git HEAD was b10ffd17e5125fcf9ca973994b8be58f3c131b18; working-tree guidance was also read. This imports conventions, not that application's implementation or acceptance evidence.

## Background browser checks

- Use a QOpenBB-owned isolated browser instance/profile. A new tab in the operator's browser is not isolation. Playwright tests use fresh contexts.
- Run headless in the background. Never move the desktop pointer, inject system keyboard events, steal focus, or attach to the user's browser.
- Hide Windows helper consoles as well: Python CREATE_NO_WINDOW, Node windowsHide, or PowerShell Start-Process -WindowStyle Hidden. Capture output and clean up only owned processes.
- Use Chrome DevTools diagnostics against the owned browser endpoint to inspect console/network errors and traces. Verify tool availability and isolation before use; do not claim diagnostics ran merely because configuration exists.
- Keep profiles, screenshots, traces, videos, storage state, and logs in ignored project artifact paths. Do not capture credentials or token-entry cases. Use disposable test accounts.
- Preserve acceptance-critical findings as Playwright regressions against the real application. Assertions verify displayed data and user effects, not just a toast, handler, HTTP 200, or visible button.
- Include success and relevant failure/recovery cases, save/reopen persistence where promised, and console/network failures. Browser checks do not prove financial calculations; those need independent data/reference assertions.

## Bounded parallel checks

- Permit up to three independent verification processes when inputs, outputs, caches, and services do not conflict.
- Run only one heavy suite/build at a time. It may overlap lightweight read-only checks. Serialize dependency installation, shared fixture mutations, and commits.
- For Python tests that use pytest-xdist, cap workers at two (`-n 2 --maxprocesses=2`); avoid unrestricted `-n auto`. Use selected files with `-n0 --no-cov` for focused review or memory diagnosis when those plugins exist.
- Start direct Playwright acceptance runs at one worker. Increase to two only after per-worker isolation of accounts, ports, Compose project names, volumes, and outputs is proven. The sibling project's PostgreSQL isolation does not prove QOpenBB isolation.
- Use disposable state and worker-scoped fixtures; never the owner's live Workspace volume or provider account for ordinary tests. Live FMP checks are explicitly marked and separately configured; missing credentials mean skipped/unverified live evidence, not a pass.
- Capture each command, revision/image digest, exit code, and artifact location. Diagnose failures; do not retry until a pass without explaining the underlying fault or nondeterminism.

## Breadth and evidence

`.kiro/breadth.toml` links capability -> spec criteria -> planned/implemented test -> evidence status. Planned test IDs are not executable tests. Never label a capability verified based on an empty or skipped suite. Parked PostgreSQL work is not a baseline coverage target.

During implementation add actual test paths/IDs and evidence links. Preserve upstream test entry points where usable; do not invent command names or copy Angular/Perspective-specific runners into this React application. Dagger owns the closing gate, including the relevant browser checks; a Python-only gate cannot certify Workspace or Excel.

Current state: policy and initial mapping only. No QOpenBB Playwright runner, DevTools connection, pytest suite, or runtime acceptance run is installed or verified yet.
