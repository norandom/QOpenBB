# Review the controlled chart editor dock

The production dock composes the accepted gallery and caller-supplied Set Up and Customize React elements. Its parent controls openness and selected tab. Closing hides the mounted subtree, preserves fields and scroll, and restores the opener only when focus was inside. Reopening focuses the selected tab. Leaving Customize unmounts its descendants; changing the live theme key rebuilds them without changing the outer tab.

The dock is 260 px including its border. Its 28 px header places the collapse chevron before Chart, Set Up and Customize. Existing design-system Radix tabs supply tab relationships and keyboard navigation. No application chart guard, flag, storage, session, dependency or accepted gallery source changed. Fixture panels in tests, story and preview are development-only; this does not establish full application integration or complete panel controls.

Frozen production, test and story hashes are recorded in `artifacts/task-2.48/implementer/source-hashes.json`. The parent owns inventory, breadth registration, whole-file complexity verification and acceptance. The independent design review passed before production edits.

## Focused evidence

- `red.log`: the focused test failed before implementation because ChartEditorDock did not exist. No feature flag was introduced, following the explicit owner instruction.
- `green.log`: four component tests passed with zero skips, exit 0, using the existing Vitest 4.1.11 runner and one worker. They exercise actual dock/gallery composition, controlled callbacks, all three destinations, retained state and scroll, focus, keyboard tabs, tab departure and theme resets.
- `lint.log`: Biome checked the two production files, test and story, exit 0. An initial unused React import in the test was removed.
- `typecheck.log`: scoped strict TypeScript returned exit 2 solely for unchanged `src/components/ds/plugins/typography.ts:1`, TS2578 unused `@ts-expect-error`. `typecheck-baseline.log` reproduces that exact diagnostic by checking the existing DS Tabs alone. No new module diagnostic was emitted; strict type-check acceptance remains limited by this baseline.
- `browser-results.json`: isolated headless Chromium, one context, CDP Runtime/Network enabled, zero console/page errors and network failures. It checks exact gallery selection, gallery scroll 300, Customize scroll 547, retained fixture value, opener focus when closing a focused input, selected-tab focus on reopen, all destinations and reset behavior. Measured width is 260 px.
- `dock-light-dark.png`: actual production dock/gallery in both token themes, 343 px total height. Fixture status is visible outside the component. Storybook runtime remains unavailable in the existing dependency tree; it was not installed or claimed verified.

The first browser attempt used a 900 px fixture whose maximum scroll was below 547; the assertion correctly failed. The fixture was enlarged to 1200 px and the preview explicitly restarted before the final run. An attempted restart initially left the owned server running; its exact process was stopped before restarting. These are evidence setup corrections, not product failures. Raw server logs are excluded from publication.

## Reproduce

From `vendor/workspace/terminalpro`, use `/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node` as `node` below. Existing dependencies are linked to the already installed appearance dependency tree. No installation occurred.

```sh
node node_modules/vitest/vitest.mjs run --config /mnt/d/Source/QOpenBB/artifacts/task-2.48/implementer/unit.config.mjs
node node_modules/@biomejs/biome/bin/biome lint src/components/General/Table/Chart/editor/ChartEditorDock.tsx src/components/General/Table/Chart/editor/chartEditorDock.css src/components/ds/organisms/ChartEditorDock.stories.tsx tests/unit/chartEditorDock.test.tsx
node node_modules/typescript/bin/tsc --noEmit --skipLibCheck --strict --target esnext --module esnext --moduleResolution bundler --jsx react-jsx --allowSyntheticDefaultImports src/components/General/Table/Chart/editor/ChartEditorDock.tsx src/components/ds/organisms/ChartEditorDock.stories.tsx
node node_modules/typescript/bin/tsc --noEmit --skipLibCheck --strict --target esnext --module esnext --moduleResolution bundler --jsx react-jsx --allowSyntheticDefaultImports src/components/ds/molecules/Tabs.tsx
node node_modules/vite/bin/vite.js --config /mnt/d/Source/QOpenBB/artifacts/task-2.48/implementer/vite.config.mjs
PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers node /mnt/d/Source/QOpenBB/artifacts/task-2.48/implementer/capture.mjs
```

Vite uses owned loopback port 6017, `envDir:false`, existing React aliases and the evidence-only preview. Stop the owned server after capture. The browser closes in `finally`. Original reference captures, operator browsers, accounts and persistent application state were not used.

Delivery normalization removed trailing whitespace and extra terminal blank lines and normalized the four new files to LF. No tokens or behavior changed; source-hashes.json records the normalized delivery bytes.
