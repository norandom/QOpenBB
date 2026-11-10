# Native browser infrastructure

Task 7 passed independent Sol review on 2026-11-10. The existing headless infrastructure now resolves pinned Chromium through Playwright on Windows, uses external evidence/profile directories, preserves valid configured caches and bounds owned-process cleanup. The browser remains isolated from the user's browser.

The existing browser suite passed nine checks with one worker; an additional output/cache-path refusal check passed. Focused Python runner checks passed ten cases with one live-provider case deselected. Scoped strict TypeScript compilation passed using the restored native Node typings. No provider requests were made.

Development checks caught Linux-only executable/entry assumptions and a Windows timeout cleanup delay. The final cleanup uses the explicit system executable and required environment; the regression completes within its bound. Review also caught an overrestrictive POSIX cache check, which now permits legitimate Linux cache directories. That branch has focused mocked coverage; actual Linux execution remains task 12.

The infrastructure test keeps its assertions and now uses the `.mts` extension so Playwright and its ESM configuration load the same evidence module. The combined size gate passed for 88 controller files with zero errors or violations, using clean `ada7d5d` plus the five changed production files. Dependency locks and the existing Linux dependency tree were preserved.

Raw commands, source hashes and results remain under `D:/BuildArtifacts/QOpenBB/native-browser`: `handoff.txt`, `source-hashes.json`, `green.log`, `path-green.log`, `python-green-final.log`, `typecheck.log`, `combined.json` and `review-verdict.md`. Chromium revision 1248 came from the configured external cache through Playwright 1.64.0; no browser installation was needed.

This accepts synthetic browser infrastructure only. The checked descriptor bridge, financial journeys and actual Linux compatibility remain later tasks in the [migration plan](../../../.kiro/specs/native-development-workflow/tasks.md).
