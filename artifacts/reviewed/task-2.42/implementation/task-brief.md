# Task 2.42 verifies detached rendering composition

The helper must reproduce the owned saved-option operation using selected `baseline.options`, even when `model.chartOptions` differs. Generated `common` replaces the entire saved branch before lodash merges generated options with saved overrides. Own undefined, null, arrays, inactive families and unknown data retain source merge semantics. Inputs and stored model stay unchanged; callbacks remain outside rendering data.

The production boundary is `application/appearanceComposition.ts`; maintained regressions are `tests/unit/chart-application/appearanceComposition.test.ts`. Frozen contracts and the four provenance-bearing fixtures remain read-only. `selectOptionBaseline` supplies existing descriptor-safe data validation and detached copies. Invalid accessors, cycles, nonplain values, functions and uninspectable proxies must return validation failures without executing user getters or functions.

Tests precede production code, with the missing implementation captured as RED. Focused Vitest, both existing strict TypeScript configurations and scoped Biome establish this unit boundary. The controller owns inventory registration, complete complexity verification, breadth mapping, independent review and acceptance. Production caps are 400 physical lines, 300 logical units and 50 per function. No feature flag is authorized.

Requirements: 1.1, 1.4, 4.2, 4.7, 4.8, 4.9, 10.5, 10.6. Design: Saved composition; File Structure Plan; Testing Strategy and Failure Handling. Renderer, application activation, persistence/reopen and UI parity remain later acceptance gates.
