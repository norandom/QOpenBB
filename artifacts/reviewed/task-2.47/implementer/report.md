# Controlled gallery implementation

The production gallery renders caller-supplied groups and choices without filtering, emits the exact model token, and keeps selection in the caller. The 34-choice preview catalog preserves the observed 12-group order and maps grouped column/bar to their model tokens. Conditional custom combinations remain supplied by the consumer. No product guard, flag, session, storage or renderer integration changed.

Frozen source identities are in `source-hashes.json`. The Storybook story uses the existing `ds/**` discovery and labels its limited scope. The existing dependency tree has no Storybook runtime package, so its CLI failed before startup; no package was installed. With controller authorization, the same production component was displayed using existing Vite and theme CSS through the local evidence-only entry.

## Verification

- `red.log`: focused test failed because the production gallery module did not yet exist. An earlier command used the absent local dependency link; this was diagnosed and corrected using a symlink to the existing appearance dependency tree.
- `green.log`: three focused tests passed, covering full order/callback inventory, exact once native Enter/Space activation, supplied custom combination, unknown selection and controlled scroll retention.
- `typecheck.log`: strict scoped TypeScript no-emit check passed for production modules and Storybook story.
- `lint.log`: scoped Biome lint passed for five files. An unnecessary region tab stop was removed after the first lint finding.
- `browser-results.json`: isolated headless Chromium with CDP Runtime/Network enabled reported zero console/page errors, 34 buttons, Enter/Space selection and scroll position 300 retained. Browser closed in `finally`.
- `gallery-light-dark.png` and `gallery-keyboard-selection.png`: actual production component preview using established light/dark tokens. The final radial silhouette change is below these captured viewports; visible captured code is unchanged.
- Whole-file complexity verification is controller-owned. Independent review and owner visual acceptance are separate gates.

## Reproduction

Use WSL Node `/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node` and the existing linked dependencies at `vendor/workspace/terminalpro/node_modules`. From that package run `node node_modules/vitest/vitest.mjs run --config /mnt/d/Source/QOpenBB/artifacts/task-2.47/implementer/unit.config.mjs`. Scoped type checking uses `typescript/bin/tsc --noEmit --skipLibCheck --strict --target esnext --module esnext --moduleResolution bundler --jsx react-jsx --allowSyntheticDefaultImports` with the three production TS/TSX files and story. Lint uses `@biomejs/biome/bin/biome lint` with the editor directory and story.

The evidence-only Vite entry uses `vite.config.mjs` on owned loopback port 6017; capture uses `PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers node capture.mjs`. Initial blank-preview failures were diagnosed as raw CommonJS React imports and stale WSL file watching; bare imports with aliases and explicit Vite restart resolved them. The final owned Vite process was stopped after capture. No installation, account, environment file, original browser or persistent application state was used.
