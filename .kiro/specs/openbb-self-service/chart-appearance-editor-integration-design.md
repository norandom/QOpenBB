# Preserve appearance and editor state through the existing chart session

## Overview

Draft amendment for review, 2026-10-17. This refines B2, the mapper join and C in the [application design](chart-application-integration-design.md). Financial engineers must see the original OpenBB chart settings, colors and financial observations after the renderer swap. The existing session, option reducers, snapshot and ECharts host remain the owners of their respective responsibilities.

Candidate baseline is Workspace `76edf85a46298f7bc5212ff9944e4b66e9baa4af`; reference source is `38dffc33389aca0e4a87e0e88d42f7067aa220df`. [Reviewed runtime findings](chart-runtime-next-plan.md) supply the evidence. This amendment does not reopen accepted tasks 2.34-2.40 or approve implementation. It distinguishes contracts ready for bounded work from later integration gates; it does not claim the complete appearance/editor surface is ready.

## Boundary Commitments

### This amendment owns

- The ordinary saved-option composition contract and derived grid/subtitle color contract consumed by B2.
- Grouped-column tooltip event decoding through the existing column-edit command and reducer.
- The dependency and acceptance contract joining those results into the existing mapper and original docked editor.
- Explicit separation of rendered options, stored options, trusted formatting callbacks and numeric transformations.

### Out of Boundary

No new state store, persisted envelope, chart menu, capability flag, theme system, generic AG interpreter or service. Existing application activation, original editor layout, complete field inventory, transformed snapshots, other chart families and persistence verification remain under the parent application design. They are required later, not removed from the product. This amendment does not authorize changing any original visibility predicate or replacing an unfinished action with a disabled/inert control.

### Allowed Dependencies

Use existing `OptionBaseline`, `RuntimeOptions`, validation, lodash merge semantics, `SessionStamp`, `ChartDisplayPolicy`, snapshot contracts and locked ECharts 6.0.0. No new dependency is proposed. Pure appearance code imports neither React/stores nor GridApi nor AG Charts. Existing owned source and finite original projections are reference evidence; private AG objects and commercial renderer code cannot enter production.

### Revalidation Triggers

Recheck consumers when saved precedence, active-theme selection, supported leaf paths, color evaluation order, stable series identity, tooltip mode, formatting invocation, ECharts version or session revision semantics change. A broader field/family/theme contract requires its own evidence and design amendment, not a permissive fallback.

## Architecture

The dependency order is validated legacy options and immutable theme inputs -> pure appearance composition -> explicit mapper style -> ECharts. Editor events separately flow through the existing addressed session and integrated reducer. The session recomputes appearance from the resulting baseline and advances render revision. Numeric observations never pass through the appearance resolver.

| Component | Input | Output and ownership |
| --- | --- | --- |
| Existing baseline selection | Latest original partition/root state | `OptionBaseline`; remains authoritative for initialize/synchronize semantics |
| Appearance composition | Baseline plus generated data-only options | Detached combined options for later projection; never a replacement stored model |
| Derived colors | Explicit resolved base and color tokens | Grid/subtitle colors; no theme graph traversal |
| Existing column edit path | Stamped typed event | Original model patch through the existing reducer; no direct editor writes |
| B2 and mapper join | Composed options, theme, stable series IDs, display policy | Explicit appearance and public ECharts options; blocked when a required effect is unresolved |
| Existing application session | Current baseline, snapshot, theme and revisions | One coordinated render/export lifecycle and existing save action |

This reuses the existing platform responsibilities. A generic resolver would add unsupported inheritance behavior; a separate editor store would create competing saved state. A small color routine alone is not the integration milestone. B2, mapper projections and original controls must be joined and checked together before application acceptance.

## Components and Interfaces

### Saved composition

Add the pure signature `composeAppearanceOptions(input: AppearanceCompositionInput): ValidationResult<RuntimeOptions>`, with input `{ readonly baseline: OptionBaseline; readonly generated: RuntimeOptions }`. Both values are validated data-only inputs. Catch malformed or uninspectable values at the public boundary, including accessors, nonplain objects, cycles and throwing proxies; do not invoke saved functions or getters.

The result is a detached copy of the existing owned merge: replace the saved options' entire `common` branch with generated `common`, then merge generated options with that adjusted saved copy using the existing lodash semantics. Preserve own undefined, null and array behavior rather than inventing JSON Merge Patch. Do not mutate baseline, generated options or saved unknown branches. Family options survive; saved common does not. The four saved-input fixtures prove captured bar/line conflicts, while owned source establishes composition order. Composition itself does not claim AG's final inheritance or validate a field's visual meaning.

Use the baseline's selected options rather than independently rereading storage. The resolver may return combined data-only options for projection; the session must continue supplying original baseline/model plus event patches to the existing persistence reducer. A derived style must never be serialized as original chart options. Trusted callbacks remain separately supplied through `ChartDisplayPolicy`; no function text or executable value enters `RuntimeOptions`.

Concretely, the saved merge operand is `input.baseline.options`, not `baseline.model.chartOptions`; the generated operand is `input.generated`. At the session call, the existing reducer's `resolvedOptions` receives the latest selected `baseline.options`, never the composed rendering result. Keep the original `currentModel` supplied to the existing reducer unchanged by appearance work.

### Derived colors

Add `deriveAppearanceColors(tokens: AppearanceColorTokens): DerivedAppearanceColors`. Tokens require `base: "ag-default" | "ag-default-dark"` and explicit `foregroundColor`, `backgroundColor`, `textColor`, `chartBackgroundColor` strings. The result is `{status:"resolved", gridLineColor:string, subtleTextColor:string}` or `{status:"invalid"|"unresolved", diagnostics:readonly SnapshotDiagnostic[]}`. Malformed input is invalid; a valid color outside the captured opaque six-digit hex domain is unresolved. This is an internal engineering result and cannot become a shipped restriction or hidden control.

Boundary validation is descriptor-safe and exception-contained: a missing field, non-string token, nonplain object, accessor or throwing proxy is invalid. An otherwise structurally valid string base outside the two supported bases, or a color string not matching `^#[0-9a-fA-F]{6}$`, is unresolved. This does not claim that an unrecognized string is valid CSS and adds no CSS parser. Preserve the diagnostic field path. Upper/lower hex input is accepted; resolved output is lowercase six-digit hex. Unknown own fields are invalid for this small internal token object, without changing saved theme retention elsewhere.

The caller resolves aliases and supplies explicit tokens; the helper never assumes text equals foreground or chart background equals background. Each channel preserves source evaluation order: `Math.round(clamp((fg/255)*(1-t)+(bg/255)*t,0,1)*255)`. Grid uses foreground/background with literal ratios `1-.257` dark and `1-.1` light; subtitle uses text/chart-background with `.57` dark and `.38` light. Interpolate encoded sRGB, not linear-light values. The reviewed counterexample `#000000` and `#9b0000` at `1-.1` yields `#8b0000`. Explicit resolved grid/subtitle overrides take precedence at the consuming B2 field, outside this derivation routine.

### Tooltip event and state contract

Extend the existing `ColumnEditorEvent` union with `{kind:"tooltip-mode"; value:"single"|"shared"|"compact"}`. Keep UI labels Single, Multiple and Compact; Multiple maps to stored `shared`. `mapColumnEditorEvent` emits exactly `{bar:{tooltip:{mode:value}}}`. It must not write `series.tooltip`, invent another persisted mode or accept arbitrary option paths. Actual captured reachability is groupedColumn only: a tooltip event for stackedColumn remains unresolved until its reference behavior is established; the four previously accepted events retain their existing family behavior.

`ColumnEditCommand`, `applyColumnEdit` and the existing integrated reducer remain the sole state path. Validate the session stamp before accepting an event and use latest supplied storage. Preserve inactive-family and unknown options, retain error/stale outcomes, and never reset other controls while applying tooltip mode. This design changes no persistence schema or save trigger.

Keep `MapColumnEditorEvent`'s existing `ValidationResult<RuntimeOptions>` signature. It rejects a stacked tooltip combination and continues accepting the four existing events for both column families. In `applyColumnEdit`, after the stamp check and before mapping, a descriptor-safe, exact-shape check recognizes only a structurally valid tooltip enum paired with stackedColumn and returns `SessionResult.status = "unresolved"` with a family diagnostic. Malformed events remain invalid through the existing mapper path; accessors/proxies are exception-contained. No reducer call or write occurs for either outcome. This explicit session distinction avoids treating every mapper validation error as unresolved.

The later public ECharts tooltip projection must reproduce heading/entry visibility: single includes category and hovered series; shared includes category and the captured series values; compact omits the category heading for the hovered series. Escaped content uses the accepted financial display policy. The present axis-triggered tooltip cannot be treated as equivalent. Missing observations, ties, ordering beyond captured examples, other families, pointer hit testing and keyboard behavior require evidence before that projection is accepted. No arbitrary default order or null-as-zero is permitted.

### Effective appearance and mapper join

Retain the parent signature `resolveApplicationAppearance(input: AppearanceInput): AppearanceResult` and resolved `ResolvedCartesianStyle` output. Its input remains selected stock/custom theme, mode, validated baseline, generated data-only options, family, ordered stable series IDs and precision; callbacks stay outside it. The helper contracts above do not freeze a falsely complete style schema.

At the consuming join, freeze named explicit fields for background visibility/fill, four-sided padding, title/subtitle typography and spacing, separate category/number axes, grid styles, legend geometry, series opacity/dash and retained line marker details. Every admitted field requires its source or finite reference value, precedence rule, ECharts projection and visible assertion. The [leaf audit](chart-appearance-next-audit.md) identifies missing representation; the newer [saved-input results](chart-appearance-saved-composition.md) supersede its narrow missing-composition claim. Do not substitute ECharts defaults for unresolved original leaves.

Keep line stroke/marker fill mapped from palette fills and marker outline mapped from palette strokes. Populate per-stable-ID channels for resolved order; current modulo fallback is not upstream palette-allocation evidence. Disabled markers retain shape/size in the effective/editor contract. Preserve stored baseline details independently. Palette exhaustion/reorder, custom line/stacked behavior, unknown axis line colors and legend-marker width remain named prerequisites for their consuming projections.

### Numeric transformations

Aggregate and Switch Category / Series are not appearance events. The editor may dispatch existing intent only after the separate transformed-snapshot contract is reviewed. Preserve sourceMode; never relabel transformed observations as flat to bypass mapper checks. The captured transpose preserves distinct duplicate Q1 observations and restores original order; the finite Sum fixture yields Q1 220/45. Neither proves missing-value rules, mixed units, overflow, other aggregates or general reordering. No new transform implementation is authorized by this amendment.

## File Structure Plan

Paths below are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/`. New paths are proposed, not present production files.

| Path | Responsibility and change |
| --- | --- |
| `application/appearanceContracts.ts` (new) | Composition and resolved color token/result types; controller freezes them before workers |
| `application/appearanceComposition.ts` (new) | Validated detached source-equivalent composition only |
| `application/appearanceColors.ts` (new) | Opaque-hex derived colors and path diagnostics only |
| `compatibility/optionStateTypes.ts`, `compatibility/editorEvents.ts` | Add one typed tooltip event and exact family patch validation |
| `application/types.ts`, `application/sessionState.ts` | Existing command/session contracts; change only if required for typed tooltip family rejection, no second reducer |
| `application/effectiveAppearance.ts` (later join, new) | Consume composition/colors and resolve admitted original appearance fields |
| `echarts/cartesianTypes.ts` (later join) | Explicit field contracts and retained marker details |
| `echarts/cartesianStyle.ts`, `echarts/cartesian.ts` (later join) | Existing validation/mapper updated at one serialized join |
| `echarts/cartesianAxes.ts`, `echarts/cartesianTooltip.ts` (later join, proposed) | Cohesive axis and tooltip projection if required by the frozen field contract; no generic path interpreter |

Existing `editor/**` and `application/useApplicationChartSession.ts` remain under C/D in the parent design; this amendment does not authorize a parallel editor or context rewrite. Later join paths require their concrete field contracts before task generation. Do not create empty forwarding modules in advance.

Read-only dependencies retain their ownership: `compatibility/optionState.ts` selects the baseline, `compatibility/integratedState.ts` performs existing persistence reduction, and `compatibility/legacyTypes.ts` owns legacy validation/types. Existing `application/financialFormatting.ts` and `echarts/EChartsHost.tsx` retain display-formatting and host lifecycle ownership. No edits to these dependency files are authorized by this amendment.

Maintained tests belong in terminalpro `tests/unit/chart-application/appearanceComposition.test.ts`, `appearanceColors.test.ts` and existing `sessionState.test.ts`; extend `tests/unit/chart-compatibility/editorEvents.test.ts` for the new patch. The controller owns type fixtures, test configuration, root complexity inventory and breadth mapping. Later real-app tests belong to the parent `tests/e2e/chart-application/` boundary.

## Dependency Plan and Complexity

After design approval, generate tasks for controller contract/test-scope freeze, bounded pure composition/color work, typed tooltip event/session work, and an independent joined check. The two implementation lanes have disjoint production files; shared contracts are controller-owned and frozen first. Sol implements, Astra reviews the hard composition/state contracts, and the controller serializes joins. At most four active agents and one heavy check at a time.

This wave may establish the source contracts only. B2's complete field manifest, mapper join, docked controls and D activation need their outstanding contracts before executable tasks. They remain the next consuming milestones; helper completion is not renderer acceptance. Approval here cannot be used to dispatch unfinished C/D tasks or remove guards.

Retain the executable inventory/checker foundation. Every new/modified maintained production file must pass 400 physical lines, 300 logical units and 50/function, including whole existing files. `cartesianStyle.ts` currently has 278 physical lines; plan cohesive validation/axis/tooltip extraction at its later join, not a blanket exception. Tests/docs/reference fixtures are explicit exclusions. Reuse the [complexity commands](../../../docs/complexity.md), explicit fork scope and final shared-module audit. Preserve unrelated dirty catalog/Perspective work.

## Requirements Traceability

This amendment supplements the [main design's full 69-criterion mapping](design.md). The application supplement owns chart integration; unchanged service, provider, AI, Excel, CI and deployment contracts remain in the main design.

| Requirements | Contribution | Acceptance boundary |
| --- | --- | --- |
| 1.1, 1.4 | Pinned owned source and bounded changes | Exact manifests and unchanged dependency versions |
| 4.2, 4.7 | Preserve original state composition | Reducer regressions now; backend reopen remains parent integration gate |
| 4.8, 4.9 | Appearance rules and original tooltip patches | Source/option/color checks now; original/candidate full UI comparison later |
| 10.1, 10.2, 10.3, 10.4 | Isolated bounded verification | Separate numerical, browser, persistence and source evidence |
| 10.5, 10.6 | Traceability and reviewed artifacts | Actual test paths and scoped status in breadth; reviewed publication |

## Testing Strategy and Failure Handling

Composition tests independently specify common replacement, bar/line family survival, null/own-undefined/array semantics, unknown-field retention, no input mutation, and hostile input containment. Compare against the pinned owned source operation for data-only fixtures, not the new helper against itself. Use the four reviewed saved-input fixtures with explicit capture provenance.

Color tests retain the 262,144-pair source comparison as reference evidence and add maintained independent expected colors, alias separation, normalized rounding counterexample, black/white bounds and invalid/unresolved cases. No AG runtime package is added to production or required by the maintained unit suite.

Event/session tests assert the exact bar patch, UI-value distinction, malformed enum rejection, stacked-tooltip unresolved behavior, stale address/generation/revision rejection, latest storage, unknown/inactive-family retention and unchanged previously accepted events. Verify a rendering-derived style is never written as the original saved options.

Run the application and compatibility unit suites, both strict TypeScript checks, scoped lint and complete maintained-size gate. Freeze actual commands and fixture hashes in tasks before execution. Tests and planned browser paths are not passing evidence until run. Public browser joins require original/candidate screenshot and interaction comparisons, financial values, export freshness, table return and backend save/reopen/restart; reference-only captures or a successful POST cannot satisfy them.

Invalid data returns diagnostics without mutation. Unknown valid original effects return unresolved to engineering and block consuming acceptance; never coerce a theme to stock, hide a control or ship a new unsupported screen. Existing session error/recovery, host disposal and stale export rules remain unchanged. Browser checks use owned headless profiles and disposable state; never the operator's desktop or browser.

## Decision and Remaining Gates

The concrete review decision is whether to freeze saved composition, normalized token derivation and the grouped tooltip event path for task generation. Complete effective style, renderer tooltip geometry, remaining original controls and numeric transforms are not yet task-ready under this amendment. Their gates are explicit above and remain obligations of the 1:1 plan. No new service, deployment topology or Anthropic-before-Excel sequencing changes are proposed.
