# Background controls are ready for independent review

Task 2.54 adds the controlled Background toggle and Color field using the accepted DS Switch, CaptionColorInput and Titles CSS. Exact `visible` and `fill` edits retain caller strings and alpha; hiding the field preserves fill. The shared picker owns invalid drafts and focus behavior. No opacity field, flags, dependencies, renderer or storage behavior was introduced. Design review PASS preceded production edits.

## Verification

Four focused Vitest cases failed before implementation because the component import was missing (`red.log`), then passed (`green.log`). Existing dependencies and the task-local unit config were reused. Biome scoped lint passes. Scoped strict TypeScript reports only unchanged `ds/plugins/typography.ts:1` TS2578; a Switch-only baseline reproduces that failure (`typecheck-baseline.log`). This is not a clean full compiler result.

Run focused checks from `vendor/workspace/terminalpro` using `/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node` through WSL Debian as user mc: `node node_modules/vitest/vitest.mjs run --config /mnt/d/Source/QOpenBB/artifacts/task-2.54/implementer/unit.config.mjs`. `check.mjs` reproduces lint/type checks. `finalize.mjs` records exact source hashes and the existing syntax-unit checker output.

The isolated headless browser run uses the existing Vite/Playwright/CDP pattern, envDir:false, port 6026 and one worker. It passes real light/dark pointer, Space, picker Escape/Enter/focus, raw alpha, invalid-draft recovery and no-mount-edit checks. CDP Runtime/Network diagnostics recorded zero page, console or request failures (`browser-results.json`). The synthetic light/dark PNG was visually inspected. Initial launch without PLAYWRIGHT_BROWSERS_PATH failed before page creation; setting the existing `/mnt/d/Source/QOpenBB/artifacts/playwright-browsers` cache resolved the launch without installing anything. Reproduce with that environment variable and `node capture.mjs` after starting Vite with `vite.config.mjs`. Owned Vite pid 10655 was stopped and the empty port-listener check confirmed cleanup.

Production size is 37 physical lines, 18 logical units, maximum 1 unit per function. `source-hashes.json` records SHA256 values of exact LF source bytes; `size.json` records measured functions. Controller owns maintained inventory, development-story exclusion, breadth mapping and combined dock checks.

## Review scope

Requirements checked: 4.8, 4.9, 10.1, 10.4, 10.5, 10.6. Design checked: chart-background-tooltip-design.md Contracts and ownership; Verification and delivery. The original referenced Chart Style PNG was viewed; it shows Padding with Background below the visible viewport. The design references established JSON/source evidence for Background. This review does not accept full Customize, rendering, persistence or deployment.

Publication candidates: report.md, task-brief.md, unit.config.mjs, check.mjs, finalize.mjs, vite.config.mjs, preview.tsx, index.html, capture.mjs, red.log, green.log, lint.log, typecheck.log, typecheck-baseline.log, check-exits.json, size.json, source-hashes.json, browser-results.json and background-light-dark.png. Exclude .vite, vite.log and capture.log. All fixtures are synthetic; no credentials or private application state were used.
