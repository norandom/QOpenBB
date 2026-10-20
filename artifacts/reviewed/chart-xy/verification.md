# Scatter and bubble verification

X1 is accepted at Workspace `e343e16499ba2a087a90ee6e4dd1091a3b4e2bc9`. The inactive resolver preserves selected column order, paired/unpaired scatter and bubble grouping, default pairing and incomplete-group behavior. It rejects malformed identities atomically and does not mutate supplied state. No chart routing, editor or geometry has been activated.

Independent Astra review approved the assignment contract against retained AG Grid Enterprise 34.1.1 `getSeriesDefinitions` and `isPaired`. Independent Sol implementation review then inspected the actual module/tests and repeated the focused checks.

From `vendor/workspace/terminalpro`, using pinned Node 24.22.0 in WSL:

```sh
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/xyAssignments.test.ts
node node_modules/typescript/bin/tsc --noEmit --strict --skipLibCheck --target ES2022 --module ESNext --moduleResolution Bundler --types node,vitest/globals src/components/General/Table/Chart/compatibility/xyAssignments.ts tests/unit/chart-compatibility/xyAssignments.test.ts
```

Both commands exited 0; 33 tests passed. The preceding RED run recorded 31 failures and two passes against an empty resolver, including intended grouping failures. Raw logs remain ignored under `artifacts/chart-xy/x1-{red,green,tsc}.log`.

The portable combined complexity gate passed with explicit Workspace/data-API scope manifests: 89 physical lines, 72 logical units and largest function 17. No errors or violations. The maintained inventory includes the module. Independent review approved X1 with no findings. Final Git whitespace checks required normalizing mixed line endings in the two new files; their code was unchanged.

The milestone's mapper, editor, actual FMP drawing/lifecycle acceptance and publication remain open. No image build was dispatched for this source-only task. The previously published combination-chart alpha remains the development release.
