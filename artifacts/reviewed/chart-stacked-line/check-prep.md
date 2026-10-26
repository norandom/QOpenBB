# Stacked line check preparation

Use the two existing Vitest configurations below for focused renderer and React checks. Preserve existing production ownership and inherit the current Cartesian/session/editor implementation. No installation, full suite, build, browser startup, or production mutation was performed for this preparation.

Observed 2026-10-26: Workspace HEAD is `0b2190354d2dc5f4175ffb989cf652ac36237c77`; QOpenBB HEAD is `eac6637cc9f3aaf19e7a6501ed1c3403d0029d06`. The QOpenBB inventory and catalog files already have unrelated working edits. Inventory changes belong to the controller; never replace it with an older copied inventory.

## Small commands

Run in WSL, with existing installed dependencies. These commands are inspected recommendations; only the parser measurement below was executed during preparation.

```sh
cd /mnt/d/Source/QOpenBB
export PATH="$PWD/artifacts/task-1.2/node-v24.22.0-linux-x64/bin:/usr/bin:/bin"
cd vendor/workspace/terminalpro

# Renderer baseline and inherited Cartesian behavior; add the new exact test path.
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/cartesian.test.ts tests/unit/chart-compatibility/cartesian.geometry.test.ts --maxWorkers=1

# Existing React setup/editor/caller inheritance; add the new exact test path.
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-application/vitest.config.mjs tests/unit/chart-application/callerArea.test.ts tests/unit/chart-application/editorArea.test.tsx --maxWorkers=1

# Non-mutating scoped lint example. Append only owned source/test files.
node node_modules/@biomejs/biome/bin/biome check src/components/General/Table/Chart/echarts/cartesian.ts

# Useful strict diagnostic collection, not a known clean baseline.
node /mnt/d/Source/QOpenBB/verification/node_modules/typescript/bin/tsc -p tests/unit/chart-compatibility/tsconfig.json --noEmit
node /mnt/d/Source/QOpenBB/verification/node_modules/typescript/bin/tsc -p tests/unit/chart-application/session.tsconfig.json --noEmit
```

Both focused Vitest configs use jsdom and one worker. Compatibility includes only chart-compatibility tests and its toolchain test; React uses the application config with the `~` alias. A new stacked-line application test must use that second config. Existing area tests are useful inheritance regressions, not stacked-line acceptance. Select financial, null-gap, legend, stamps, storage, recovery and editor behavior tests from the approved contract when choosing the final join.

Do not invoke package `lint`: it formats all `src`, writes fixes, and runs unsafe fixes. Package `typecheck` runs full application `tsc --noEmit`; package `build2` also builds. Neither is the smallest gate.

## TypeScript baseline

`artifacts/chart-funnel/f3b/typecheck.cjs` demonstrates a strict same-root baseline/candidate compiler-host comparison using pinned TypeScript 6.0.3, `strict:true`, `skipLibCheck:true`, `noEmit:true`. Its accepted result retained 2789 inherited diagnostics and added none. This was not a clean compile.

Do not rerun that file as stacked-line evidence: its owned list, baseline source map, diagnostic input and output names are hardcoded to the old Funnel join. Prepare a fresh baseline from `0b2190354d2dc5f4175ffb989cf652ac36237c77`, freeze the same root list for both runs, keep inherited diagnostics, compare exact diagnostic identities, and write new outputs under this milestone. Missing baseline-owned paths must be absent through the compiler host rather than silently reading candidate contents. Do not suppress new diagnostics because the application already has inherited failures.

## Whole-file caps

Current working `echarts/cartesian.ts`, including earlier area edits, was measured with the actual `tools/quality/syntax_units.ts` parser using pinned Node 24.22.0. It has 271 physical lines, 90 logical units, `buildOptions` 21 logical units, `applicationSupport` 16 and `translateCartesian` 21. It has room beneath 400 physical/file, 300 logical/file and 50/function; this is no reason to move state ownership or duplicate projection logic. Re-measure the actual final bytes after the renderer lane lands.

```sh
cd /mnt/d/Source/QOpenBB
printf '["vendor/workspace/terminalpro/src/components/General/Table/Chart/echarts/cartesian.ts"]' | artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node tools/quality/syntax_units.ts
```

The closing combined gate remains:

```sh
pipeline/.venv/bin/python -m tools.quality.complexity --check \
  --changes workspace=artifacts/chart-stacked-line/workspace-changes.json \
  --changes data_api=artifacts/chart-stacked-line/data_api-changes.json \
  --output artifacts/chart-stacked-line/complexity.json
```

Create fresh scope manifests with the inventory-approved fork base, current actual head `0b2190354d2dc5f4175ffb989cf652ac36237c77` until a new commit exists, and complete changed production paths. Do not copy F3b manifests unchanged: those declare pre-F3b head `3cbd6c85f2ac09c943e53120a99e89bb7c636abf`. Preserve the data-api identity and actual unchanged/changed declaration. The combined gate also checks maintained QOpenBB files, so unrelated current edits may affect its result; report that provenance rather than changing another lane. Check errors, violations, applied exceptions and combined acceptance, not just exit status. New maintained files require controller-owned inventory mappings.

## Browser boundary

F3b `ui/run.sh` is a React/jsdom check, not browser or appearance evidence. Its existing harness should be reused through the config, not copied. The real application browser config is `tests/e2e/live-chart/playwright.config.ts`; it forces headless one-worker isolated execution and rejects CLI worker overrides. It requires explicit `WORKSPACE_EVIDENCE_ROOT`, loopback `WORKSPACE_FRONTEND_ORIGIN` and `PLAYWRIGHT_BROWSERS_PATH`. The Vite app runner separately requires disposable loopback `WORKSPACE_BACKEND_ORIGIN`; it must not load owner environment/state. Arrange actual packaged save/reopen/export, console/network diagnostics and source/image identity at the controller's serialized browser join. No such evidence was collected here.
