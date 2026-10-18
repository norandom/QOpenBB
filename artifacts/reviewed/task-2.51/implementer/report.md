# Review the controlled Legend panel

Task 2.51 is ready for independent review. The real panel preserves the original field order, labels above fields, paired Size/Color row, blue Enabled switch and thin slider tracks. It emits typed field edits and retains caller values through collapse or disabled visibility. Renderer effects, storage integration and the combined dock are separate obligations.

## Contract and source comparison

The implementation follows the final chart-legend-padding-design.md Legend contract and requirements 4.8, 4.9, 10.1, 10.4, 10.5 and 10.6 within this controlled UI boundary. CaptionColorInput and Titles CSS are imported read-only. Unknown choices remain selectable, caller ordering is retained, combined weight keys remain opaque, and mount/open actions emit nothing. Numeric text permits finite decimals at or above the minimum, including values above presentation bounds. Controlled updates expand the slider maximum. Invalid drafts remain correctable without callbacks.

Original stacked-legend.png, group-Legend.png and legend-after.png were inspected. The last image shows the lower controls, including thin tracks and dark thumbs; local Legend CSS preserves that treatment without changing accepted Titles. Source AgGroupComponent.setEnabled/toggleGroupExpand and LegendPanel in the installed reference AG Grid 34.1.1 explain why Enabled remains visible while its details collapse. The selected-series predicate remains caller-owned. These source clues and the screenshot comparison do not establish full runtime renderer parity or owner visual acceptance.

## Fresh verification on 2026-10-18

Commands use existing Debian WSL dependencies and pinned Node 24.22.0. The working directory is vendor/workspace/terminalpro unless specified. No installs, flags or shared accepted source edits were made.

- RED: `node node_modules/vitest/vitest.mjs run --config /mnt/d/Source/QOpenBB/artifacts/task-2.51/implementer/unit.config.mjs` failed before implementation because ChartLegendPanel did not exist. red.log retains the failure.
- GREEN: the same command passes all four focused tests with no skips. Tests cover every exact numeric callback, typed choices, unknown values, disabled retention, decimal/invalid drafts and alpha picker keyboard focus. green.log records exit 0.
- Lint: `node node_modules/@biomejs/biome/bin/biome lint src/components/General/Table/Chart/editor/legend src/components/ds/organisms/ChartLegendPanel.stories.tsx tests/unit/chartLegendPanel.test.tsx` passes, exit 0. lint.log records the final CSS/source state.
- Scoped types: `node /mnt/d/Source/QOpenBB/artifacts/task-2.51/implementer/typecheck.mjs` invokes strict tsc against the two TSX files and story. Both it and the Switch-only baseline report only unchanged typography.ts TS2578, exit 2. No new errors were waived; a clean application typecheck is not claimed.
- Browser: `PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers node /mnt/d/Source/QOpenBB/artifacts/task-2.51/implementer/capture.mjs` passes, exit 0. One isolated headless Chromium context, one worker, CDP Runtime/Network enabled, zero console/page/network errors. It checks Size/Color geometry, all numeric callbacks, expanded maxima, invalid drafts, range keyboard movement, Enabled Space retention and alpha picker Escape/Enter focus. The final light/dark and picker screenshots were visually inspected. Vite used envDir:false and owned port 6021; owned pid 8691 was stopped and process absence verified.
- Size: repository tools/quality/syntax_units.ts reports ChartLegendPanel 46 logical units and LegendInputs 39, maximum callable 6. Physical source counts are 134 and 96; CSS is 40. All are below 400/300/50. The parent owns inventory-aware combined verification and metadata.

The browser probe first exposed an ambiguous substring label and was corrected to exact matching. A second assertion attempted ArrowRight at Marker Stroke's expanded current maximum, where no increase is expected; the final probe uses ArrowLeft to verify linkage. Vite was restarted after CSS edits because WSL did not detect Windows-side file changes. These verification issues were diagnosed before the final passing run.

## Evidence and limitations

source-hashes.json records the final five source/test/story files, normalized LF bytes and SHA256. size.json records executable syntax measurements. browser-results.json records diagnostics; legend-light-dark.png and legend-color-popover.png show the real component. The story uses example domains and explicitly states its incomplete scope. Storybook runtime is absent from the existing installation, so the production component was exercised with the existing Vite preview pattern. The parent owns task 2.53 composition, breadth/inventory updates, independent review, publication and commits.
