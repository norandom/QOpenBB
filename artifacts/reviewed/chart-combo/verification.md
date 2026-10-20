# Combination chart port verification

C1 and C2a are accepted as inactive assignment and axis-planning components. Combination-chart rendering, editor integration and real-FMP application acceptance remain open. No image release follows these helper tasks.

Workspace source: `99e3f8637960d4981695e73bb8fedd974215c113`.

Independent Sol review inspected both complete files against the retained original ComboChartModel and approved with no blocking findings. The reviewer reran 21 focused Vitest tests and strict scoped TypeScript checking successfully. Coverage includes builtin splits, custom ordering, first duplicate wins, missing/unsupported assignments, primary-only coercion, immutable state and malformed input.

From `vendor/workspace/terminalpro`, using the pinned Node 24.22.0 in WSL:

```sh
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/comboAssignments.test.ts
node node_modules/typescript/bin/tsc --noEmit --strict --skipLibCheck --target ES2022 --module ESNext --moduleResolution Bundler --types node,vitest/globals tests/unit/chart-compatibility/comboAssignments.test.ts src/components/General/Table/Chart/compatibility/comboAssignments.ts
```

The controller independently measured 118 physical lines, 109 logical units and 17 maximum units/function. The portable complexity gate passed with explicit C1 fork changes and no data-api changes. Local scope inputs and raw report remain under ignored `artifacts/chart-combo/`.

The initial RED run failed because the implementation module did not exist; no assertions ran at that stage. Its output remains in tool history, not a persisted log. Broader compatibility TypeScript checking reports existing errors in `typography.ts:1` and `cartesian.geometry.test.ts:42`; the scoped check above does not establish whole-project compilation.

Fresh FMP annual AAPL statements were retrieved for subsequent financial verification. Provider payloads and credentials are excluded from publication. No application runtime, visual parity, save/reopen, export or provider integration is accepted by this report.

## C2a: admission and independent numeric axes

Workspace source: `d5334ae2011ddb8c2875c01143b7d92fbd3f5767`.

Independent Astra review first rejected malformed-row admission and numeric-axis spacing based on raw rather than rounded ticks. Thirteen regression failures reproduced those gaps before repair. A second independent review approved the fixes and reran all 40 focused tests successfully:

```sh
node node_modules/vitest/vitest.mjs run --config tests/unit/chart-compatibility/vitest.config.mjs tests/unit/chart-compatibility/combo.admission.test.ts tests/unit/chart-compatibility/combo.axes.test.ts
```

Coverage includes declared units per axis, separate same-unit secondary axes, all-secondary inputs, stable indexes, duplicate labels/selections, signed stack domains, zero/null values, malformed observations and rounded/rotated tick spacing on either side. Original axis placement controls remain valid inputs.

The portable complexity gate passed with explicit C2a source scope. Production physical/logical/max-function measurements are: types 74/42/no functions, admission 302/131/33 and axes 152/83/24. Scoped strict checking reports only the existing `typography.ts:1` unused directive; this is not a passing whole-project typecheck. Full-project attempts also encounter existing project-reference/compiler configuration errors.

C2a does not assemble mixed series or connect the application. Nonfinite derived geometry throws internally; the C2b public mapper must translate it into diagnostics without partial options. The independently accepted C1 root commit `d60835a` also passed the portable GitHub checks in run 39389836206; image building and alpha publication were skipped as intended.
