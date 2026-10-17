# Review composed Set Up and Titles controls

The parent-owned development story composes the actual production dock, gallery, Set Up and Titles components in both themes. The isolated browser checks pass for controlled edits across close/reopen and tab changes. This is a component composition preview; application activation, financial rendering, session persistence and complete Customize remain pending.

`dock-setup-light-dark.png` captures initial Set Up. `dock-titles-light-dark.png` captures the enabled Chart Title after retained text edits. Both images were inspected. The 520px dock scrolls the complete Titles contents; lower captions are outside the second screenshot viewport, rather than removed. Scope prose sits outside product controls.

`browser-results.json` records the passing Playwright run, exit 0. In light and dark themes it checks Region category selection, aggregation Average choice, category/series switching, and retained values after closing/reopening and returning from Customize. Chart Title enabled/text edits survive close/reopen and departure/reentry through Set Up. The transient Titles group closes after tab remount while its controlled values remain. CDP Runtime and Network diagnostics recorded zero console/page errors or failed requests.

Scoped Biome checks the story successfully, exit 0 (`lint.log`). Scoped strict TypeScript reports only the previously reproduced unchanged `src/components/ds/plugins/typography.ts:1` TS2578, nonzero WSL tool exit 1 (`typecheck.log`). No new story diagnostic occurred; strict compiler acceptance remains limited by that baseline.

Only combined evidence files were written for this follow-up. No production source, metadata or dependencies changed. The browser used its own headless context; no operator profiles, provider accounts or environment files were accessed. The owned Vite process 93525 was stopped after capture. Text evidence is normalized to LF with one terminal newline. `source-hashes.json` pins the exact production/story inputs observed; `evidence-hashes.json` pins the reviewable outputs. Exclude the generated `.vite` cache from publication.

## Reproduce

From `vendor/workspace/terminalpro`, use the pinned executable `/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node` as `node` below, with existing dependencies:

```sh
node node_modules/@biomejs/biome/bin/biome lint src/components/ds/organisms/ChartEditorControls.stories.tsx
node node_modules/typescript/bin/tsc --noEmit --skipLibCheck --strict --target esnext --module esnext --moduleResolution bundler --jsx react-jsx --allowSyntheticDefaultImports src/components/ds/organisms/ChartEditorControls.stories.tsx
node node_modules/vite/bin/vite.js --config /mnt/d/Source/QOpenBB/artifacts/task-2.49/controller/combined/vite.config.mjs
PLAYWRIGHT_BROWSERS_PATH=/mnt/d/Source/QOpenBB/artifacts/playwright-browsers node /mnt/d/Source/QOpenBB/artifacts/task-2.49/controller/combined/capture.mjs
```

The preview binds loopback port 6017 with `envDir:false`. Run only after acquiring the serialized browser lane, then stop its owned server. Complexity caps do not apply to this evidence-only preview; production inputs retain their owning task audits. Owner visual judgment and independent review remain acceptance gates.
