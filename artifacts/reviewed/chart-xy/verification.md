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

X1 does not establish rendering acceptance. The next section records the separately reviewed inactive mapper.

## X2 numeric mapper

X2 is accepted at Workspace `7e509d323cfb4b659c5071786d78744a9e8338e0`. The pure mapper retains raw X/Y observations, independent bubble-size domains, missing/negative/equal size semantics and point identities. It does not activate application routing or write saved state.

Independent Astra design review resolved explicit axis bounds, appearance precedence, grid-helper compatibility and triangle anchoring before implementation. Independent implementation review found tooltip rows in X/Y/size order rather than the original descending numeric order. The correction sorts raw tuples before formatting, preserving stable ties and duplicate labels.

Using the same pinned Node and Vitest configuration, `xy.test.ts`, `xy.render.test.ts` and `xyAssignments.test.ts` passed 64/64 tests: 31 X2 and 33 X1. Independent review repeated this command successfully. Actual ECharts SVG rendering checks cover numeric coordinates, scatter and variable-size bubble triangle placement, supported bounds, and datum tooltip identity for overlapping points. RED evidence includes the initial absent implementation, derived-layout overflow and three tooltip-order failures. Raw logs remain ignored in `artifacts/chart-xy/`.

Scoped strict TypeScript reports only inherited `src/components/ds/plugins/typography.ts:1` TS2578 and no XY diagnostics; this is not a clean project compile. The final combined complexity gate exited 0 with no errors or violations. Eight production files measure 37-185 physical lines, 14-88 logical units and at most 14 units per function; all are inventoried.

One-sided explicit bounds excluding all observations currently return an invalid diagnostic because ECharts otherwise reverses the extent. Source characterization establishes that the original renderer instead uses an empty domain with invisible points. The inactive contract permits this temporary safety response, but X4 must implement original-compatible empty geometry before feature acceptance.

Independent review approved the bounded mapper after the tooltip fix. Editor integration, original visual parity, actual FMP application/lifecycle checks and publication remain open. No image build was dispatched for these source-only tasks; the published combination-chart alpha remains the development release.
