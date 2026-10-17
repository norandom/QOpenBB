# Review the controlled Set Up panel

The production Set Up panel preserves the observed Categories and Series groups, category selection, Aggregate switch and conditional method, ordered series chips with grips and remove icons, and Switch Category / Series. It emits controlled edit intents with exact caller IDs. It performs no calculations or storage writes. This component evidence does not establish dashboard activation, financial rendering, persistence or complete renderer parity.

Design review passed before production edits at design SHA256 `1375e25fff48c78765495979546e57c45e3ac9ea0d4ce54d93a14eae6bd878c7`. Requirements checked: 4.8, 4.9, 10.1, 10.4, 10.5 and 10.6. The frozen Set Up API is exported from `Chart/editor/setup/ChartSetupPanel.tsx`.

Unknown current category/method values display without emitting a fallback. Disabling aggregation hides the method and retains caller state. Duplicate series labels retain independent stable identity. Keyboard Up/Down on a grip requests adjacent reorder and keeps focus; native dragging retains all current IDs exactly once and rejects missing source/target IDs. Removal remains controlled. Both groups collapse through accessible native buttons.

The existing DS Switch is reused with local token styling. Native selects accept the caller's opaque choices including empty and unknown values without the DS Select's Radix nonempty-value constraint and broader application imports. Local collapsible buttons preserve the compact observed presentation without adding animation. No shared DS source changed.

## Focused evidence

- `red.log`: before production existed, Vitest failed to resolve ChartSetupPanel. No flag was added, following the explicit owner override.
- `green.log`: five tests pass, zero skips, final command exit 0. Exact choice/switch callbacks, no mount edits, disabled/unknown retention, duplicate-label removal, keyboard boundary/focus and stale drag identity are asserted.
- `lint.log`: scoped Biome lint passes, exit 0, four files.
- `typecheck.log`: scoped strict TypeScript emits only existing `typography.ts:1` TS2578. `typecheck-baseline.log` reproduces it with existing DS Switch alone. The WSL tool reports nonzero exit 1; this does not constitute strict compiler acceptance.
- `complexity-units.json`: existing pinned syntax checker measures production TSX at 80 logical units, largest function 8. TSX has 82 physical lines; CSS has 22. The parent owns full inventory registration and the joined audit.
- `browser-results.json`: isolated headless Chromium checks actual component light/dark rendering, exact controlled category, aggregation retention, keyboard reorder, native pointer drag reorder, removal, switching and collapse retention. CDP Runtime/Network diagnostics report zero console/page errors and network failures. Capture command exit 0.
- `setup-light-dark.png`: synthetic controlled component preview in both themes. The first visual inspection found a dark fallback chip background in the light theme; the final capture uses the existing surface-divider token. The preview's scope notice is outside production controls. Storybook runtime is unavailable and was not installed.
- `source-hashes.json`: frozen LF-normalized production, story and test bytes. No extra terminal blank lines. Scoped git diff check passes; new files are untracked pending parent review/staging.

One attempted final command batch used a shell variable across PowerShell/WSL argument translation and produced `env: node: Permission denied`; its misleading echoed statuses were discarded. Final commands reran using the absolute Node executable and their actual tool exits above. No production change was made for that harness error.

## Reproduce

From `vendor/workspace/terminalpro`, `node` below is `/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node`. Existing dependencies were reused without installation.

```sh
node node_modules/vitest/vitest.mjs run --config /mnt/d/Source/QOpenBB/artifacts/task-2.49/implementer/unit.config.mjs
node node_modules/@biomejs/biome/bin/biome lint src/components/General/Table/Chart/editor/setup src/components/ds/organisms/ChartSetupPanel.stories.tsx tests/unit/chartSetupPanel.test.tsx
node node_modules/typescript/bin/tsc --noEmit --skipLibCheck --strict --target esnext --module esnext --moduleResolution bundler --jsx react-jsx --allowSyntheticDefaultImports src/components/General/Table/Chart/editor/setup/ChartSetupPanel.tsx src/components/ds/organisms/ChartSetupPanel.stories.tsx
node node_modules/typescript/bin/tsc --noEmit --skipLibCheck --strict --target esnext --module esnext --moduleResolution bundler --jsx react-jsx --allowSyntheticDefaultImports src/components/ds/atoms/Switch.tsx
node node_modules/vite/bin/vite.js --config /mnt/d/Source/QOpenBB/artifacts/task-2.49/implementer/vite.config.mjs
PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers node /mnt/d/Source/QOpenBB/artifacts/task-2.49/implementer/capture.mjs
```

Browser lane was serialized and both owned Vite processes were stopped after capture. No operator profile, credentials, environment file, original application capture or financial provider was accessed. Publication candidates are this report, the screenshot, browser results, hashes, complexity output and reproducible preview/check scripts; omit `.vite` dependency cache and raw runtime logs. Independent review and owner visual judgment remain parent gates.
