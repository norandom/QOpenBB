# Review the controlled Titles subsection

Task 2.50 is ready for independent review within its controlled UI boundary. All four caption sections expose enabled state, text, caller-supplied font/combined-weight/size choices, alpha color and linked spacing controls. Storage mapping, the other Customize groups and full dashboard/renderer acceptance remain pending. The controller owns dock composition and metadata.

## Contract and evidence

The frozen `chart-editor-controls-design.md` Titles API is implemented in `ChartTitlesPanel.tsx`; `CaptionFields.tsx` owns choice preservation and numeric drafts, and `CaptionColorInput.tsx` uses installed react-colorful with ECharts 6 public `color.parse`. Weight keys remain opaque. Supplied unknown choices stay visible. Disabled captions hide fields without changing caller values. No mount, expansion or picker-opening normalization emits edits. Invalid decimal/color drafts remain correctable without emissions. Picker Enter/Escape closes and restores opener focus without rolling back accepted edits.

Requirements checked: 4.8, 4.9, 10.1, 10.4, 10.5 and 10.6 within this UI scope. This evidence does not establish financial rendering or storage semantics. The parent updates breadth/inventory separately. Core product/tech/structure steering files do not exist, as already documented in requirements.md. Other required steering and the kiro-impl implementer template were read; the owner's explicit no-flags instruction overrides its generic flag procedure.

## Verification on 2026-10-17

All commands use existing Debian WSL dependencies and Node 24.22.0, with working directory `vendor/workspace/terminalpro` unless shown otherwise. No installs or new reference harness were added.

- RED: `node node_modules/vitest/vitest.mjs run --config /mnt/d/Source/QOpenBB/artifacts/task-2.50/implementer/unit.config.mjs` failed before implementation because ChartTitlesPanel did not exist. See red.log. An initial implementation run identified and corrected one relative Switch import.
- GREEN: the same command passes 4 tests, exit 0, no skipped tests. Exact edits, unknown choices, all caption routing, disabled retention, alpha colors, invalid drafts and focus are asserted in the real production component.
- Lint: `node node_modules/@biomejs/biome/bin/biome lint src/components/General/Table/Chart/editor/titles src/components/ds/organisms/ChartTitlesPanel.stories.tsx tests/unit/chartTitlesPanel.test.tsx` passes, exit 0.
- Scoped strict types: `node node_modules/typescript/bin/tsc --noEmit --skipLibCheck --strict --target esnext --module esnext --moduleResolution bundler --jsx react-jsx --allowSyntheticDefaultImports src/components/General/Table/Chart/editor/titles/*.tsx src/components/ds/organisms/ChartTitlesPanel.stories.tsx` reports only unchanged DS typography.ts TS2578. The Switch-only baseline reproduces it; see typecheck-baseline.log. Clean typecheck is not claimed.
- Browser: existing Vite with envDir:false serves real modules at owned port 6019. `PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers node /mnt/d/Source/QOpenBB/artifacts/task-2.50/implementer/capture.mjs` passes, exit 0. One isolated headless Chromium context, CDP Runtime/Network enabled, zero console/page/network errors. Tests cover live controls, exact controlled output, alpha picker keyboard input, numeric range keyboard linkage, invalid drafts, retained disabled values and close/focus/no rollback. Owned browser and Vite process were stopped. Screenshot was visually inspected in both themes.
- Size: repository `tools/quality/syntax_units.ts` measures the full TSX files, with all logical/function counts below 300/50. Physical source counts are below 400; source-hashes.json records final LF-normalized bytes. Parent runs the inventory-aware combined gate.

## Reviewable artifacts

Use source-hashes.json for the final six source/test/story hashes, size.json for syntax counts, green.log/lint.log for fresh passing checks, browser-results.json for diagnostics and titles-light-dark.png for the synthetic light/dark view. Vite cache is excluded from publication. Storybook runtime is absent in the existing installation, so the development story is source-reviewed and the same production component was executed through Vite.

The screenshot shows candidate controls and menu examples. It does not establish original pixel parity or complete Customize. The parent will compose both real subsections into the accepted dock for owner visual review.

## Visual correction before freeze

Parent review identified the initial compact label-left layout and gray switches as different from the existing original capture. The final files follow `artifacts/reviewed/parity/line-style-capture/title-enabled.png`: labels above full-width fields, 32px text inputs, borderless dropdowns, blue checked tracks and 18px theme-colored knobs. The existing C02.s03 color capture establishes a floating picker; final implementation uses installed Radix Popover anchored to the full color field with a theme-preserving portal, spectrum, slim hue/alpha bars and editable color footer. `titles-color-popover.png` records the final overlay. No new original captures were taken.

Final browser rerun passed against a restarted Vite process after WSL did not detect Windows-side CSS edits. A browser assertion now checks 32px title height and zero-width font borders. An earlier picker assertion read controlled output before its commit; the final check waits for the displayed rgba output. These were verification timing/cache diagnoses, not ignored product failures. Fresh unit and lint checks pass after the final changes. Typecheck runner `typecheck.mjs` records the actual child-process exit code (2 for both scoped and baseline checks); exits.log avoids shell interpolation of status values. Final source hashes supersede earlier reports.
