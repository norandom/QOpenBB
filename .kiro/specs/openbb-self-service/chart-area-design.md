# Restore ordinary area charts

## Overview

Restore `area`, `stackedArea` and `normalizedArea` in the existing Table/File chart journey. Financial engineers retain the original gallery, settings, themes, raw observations and saved model types. This scoped UI-10 amendment extends the accepted Cartesian application; it does not accept combination charts or a deployment image.

### Goals and non-goals

Make the three area choices render, respond to original controls, refresh, export and survive save/reopen. Preserve the seven accepted Cartesian families. Combination charts, per-series secondary axes, advanced callers, table analytics, providers, AI, Excel and release packaging are outside this slice.

## Boundary Commitments

### This Spec Owns

Area geometry and presentation in the existing ECharts mapper, area-specific appearance/editor bindings, and the ordinary application join. Widget state remains authoritative for saved configuration; ECharts remains authoritative for transient legend selection.

### Out of Boundary

No new chart shell, toolbar, flags, persistence schema, state store, dependency or generic renderer registry. Do not reuse bar arithmetic merely because both chart types can be normalized. Do not hide controls to accommodate the replacement.

### Allowed Dependencies

Reuse accepted snapshots, ranges, financial formatters, appearance resolution, editor components, native legend projection callback, navigator, host lifecycle, and isolated browser helpers. Source identities: current Workspace `375fe8990c698ef5e9d4c972f92e6b77c242dae3`; original Workspace `38dffc33389aca0e4a87e0e88d42f7067aa220df`; retained AG Grid Enterprise 34.1.1 and AG Charts 12.1.1. No dependency upgrade is required.

### Revalidation Triggers

Changes to area accumulation, missing-value treatment, option namespace, family predicates or overview construction require affected renderer/editor checks and the final joined journey. Changes to shared legend lifecycle require its existing regression suite. Visible deviations beyond the approved views require an owner decision.

## Architecture and contracts

The existing flow remains raw snapshot -> resolved appearance -> Cartesian projection -> ECharts host. Editor events update the existing saved model and produce a new projection; derived percentages never enter saved financial data.

### Numerical contract

Independent areas use their own zero baseline. Stacked areas require original ordered algebraic accumulation, not the separate positive/negative stacks used by bars. Normalized areas require their own source-backed extent calculation. Preliminary pinned-source inference for ordered values `[7,-6,5]` gives cumulative endpoints `[7,1,6]` and normalization extent 7; the bar denominator would be 12. This distinction must be frozen by the prerequisite below before implementation, including sign changes between categories.

A pure typed area projection receives immutable raw snapshot, ordered selected columns, family and enabled-series membership. It returns drawn segments/boundaries and gap metadata without modifying raw observations. Renderer-internal missing-value coercion must not become a financial zero in labels, tooltips, exports or persistence. Handle zero-only, all-hidden, all-missing, repeated category labels and large finite values explicitly. Preserve raw labels/tooltips and original percent-axis/crosshair precedence.

Use native ECharts line/area rendering where it reproduces the frozen geometry. Do not assume its default stacking or gap fill matches AG Charts. A bounded native geometry check is required before committing to a stack strategy; if native options cannot preserve the original fill boundaries, return a concrete adapter design for review rather than silently changing the shape.

### Appearance and editor contract

All three saved model types read/write the original `area` option branch. Extend existing family predicates; distinguish line-like geometry from area-specific control eligibility. Original defaults retain area marker configuration but remove `connectMissingData`; do not infer control availability solely from that default removal. Freeze original marker, label, shadow, fill/stroke, dash, opacity and connect-missing predicates from the original settings implementation and a targeted runtime witness where source is insufficient.

Preserve the original single-date conversion of exact `area` or `line` to `groupedColumn` where the existing caller applies it; gallery presence is not evidence of bypassing that condition. Keep original gallery drawings and existing editor components. Preserve inactive option branches and family-specific ranges. Area category spacing and numeric domain must follow the original area axis contract, rather than inheriting bar band padding.

### Legend, navigator and persistence

Reuse the accepted native legend scope and latest-request callback for normalizedArea. Hiding a series must recompute the original normalization and stack membership. Theme/data/resize updates retain current transient selection; family/session replacement resets it under the accepted lifecycle contract. No saved legend-selection field is introduced.

Keep physical-X category navigation. Construct the miniature from full selected-series inputs independently of main legend membership where confirmed by the original area contract. Miniature fill boundaries and gap semantics use the same area projection. Export reflects current rendered geometry. Save/reopen restores exact family, range, options and unknown branches; transient selection follows the observed original lifetime.

## File Structure Plan

Production paths are relative to `vendor/workspace/terminalpro/src/components/General/Table/Chart/`. Test paths are relative to `vendor/workspace/terminalpro/`; delivery paths are relative to the QOpenBB root.

| Ownership | Paths | Responsibility |
| --- | --- | --- |
| Controller contract prerequisite | `echarts/cartesianTypes.ts`; new `echarts/cartesianAreaTypes.ts`; test fixture `tests/unit/chart-compatibility/fixtures/area-charts.json` | Family types and typed numerical seam; frozen original semantics before fan-out; keep isCartesianFamily admission unchanged until join |
| Sol renderer lane | New `echarts/cartesianArea.ts`; `echarts/cartesian.ts`, `echarts/cartesianSeries.ts`, `echarts/cartesianAxes.ts`, `echarts/cartesianDisplay.ts`, `echarts/cartesianStyle.ts`, `echarts/cartesianNavigator.ts`, `echarts/cartesianLayout.ts`, `echarts/cartesianBarColors.ts` | Area projection, native fill/line/marker geometry, domain/spacing, formatting and overview |
| Sol appearance/editor lane | `application/effectiveAppearance.ts`, `application/effectiveAppearanceDefaults.ts`, `application/effectiveAppearanceSeries.ts`; `compatibility/editorBindings/eligibility.ts`, `compatibility/editorBindings/mapApplicationEditorEvent.ts`, `compatibility/editorBindings/selectApplicationEditorState.ts`, `compatibility/editorBindings/rehydrateApplicationEditorEvent.ts` | Area namespace, source-backed defaults and original visible control effects |
| Controller join | `echarts/cartesianTypes.ts` admission predicate after lane freeze; `application/applicationSessionProjection.ts`, `application/axisStructure.ts`; `AgChartView.tsx`, `caller/chartInputs.ts` only where shared predicates do not suffice | Atomic family activation, normalized callback/overview composition and retained family ranges |
| Controller delivery | `.kiro/complexity-budgets.json`, `.kiro/breadth.toml`, `.kiro/specs/openbb-self-service/`, `sources.lock.json`; tests under `tests/unit/chart-compatibility/`, `tests/unit/chart-application/`, `tests/e2e/live-chart/` | Combined scope audit, actual application acceptance, selective artifact sync and commits |

Predicate expansion can transitively activate callers. The prerequisite may extend the family type and add area-specific numerical predicates, but must keep runtime admission unchanged, including transitive dependencies such as isNormalizedFamily called by isCartesianFamily. Existing normalization predicates expand only at the join; separate pure area predicates may be used by the renderer before activation. The controller expands admission only after both production lanes are ready; no feature flag is added. If a shared file needs edits from both lanes, assign it to the controller and serialize the join.

Production limits remain 400 physical lines/file, 300 logical units/file and 50/function, checked on whole modified files with the existing inventory/checker and explicit fork change manifests. Register new helpers. Split cohesive responsibilities before a cap is exceeded; no exception is proposed. Each later executable task must be bounded to a 1-3 hour unit. Tests and documentation are outside production caps.

## Prerequisite and execution order

1. Freeze area arithmetic, gap/fill boundaries, axis/default/control predicates, native legend membership and miniature semantics against retained original sources. Reuse one bounded synthetic original journey for unresolved visible effects and one native geometry discriminator. These answer concrete implementation questions; no new harness or general reference campaign.
2. Freeze the typed area projection seam and exact lane files. Parallelize numerical rendering and area editor bindings using Sol; keep one heavy verification process.
3. Controller joins the existing application and runs one focused ordinary area journey. Astra independently reviews financial/state integration. Sync concise evidence and commit each accepted task.

Contract disagreement or native geometry mismatch blocks dependent work. It does not authorize a bar-style approximation. Task generation follows design approval; this document does not create implementation approval.

## Verification and requirements traceability

| Criteria | Evidence required |
| --- | --- |
| 4.8, 4.9 | Unequal signed/ordered area fixtures, native boundaries, missing/gap and zero cases; raw labels/tooltips, original percent formatting and control effects; all seven accepted families retain behavior |
| 4.7, 4.8 | Distinct family ranges, unknown/inactive branches, exact saved types and fresh-session reopen; no raw financial value mutation |
| 10.1, 10.2, 10.3 | One isolated Workspace journey across three area types, legend, markers/fill/stroke, navigation/overview, themes, current PNG and save/reopen with CDP diagnostics |
| 10.4, 10.5, 10.6 | Frozen parallel ownership, independent review, combined caps, actual test paths and scoped acceptance status |

Add behavior-named area mapper/caller tests and a single `tests/e2e/live-chart/area-charts.spec.ts` using existing helpers. Reuse accepted persistence failure/restart and host cleanup evidence unless changed ownership creates a concrete regression risk. Publish one concise review and only necessary synthetic screenshots. This amendment covers the stated criteria within the main approved design; other requirements remain owned by that design.

Wrong ordered accumulation, raw-to-percentage tooltip substitution, coerced missing financial observations, disconnected area controls, hidden actions, stale export or lost saved branches prevent acceptance. Broader UI-10 and release-image status remain pending.

## Research basis

Two read-only Sol investigations found that current area gallery entries exist but the active Cartesian family contract admits only seven families. Appearance and editor reducers currently select line or bar namespaces; markers are guarded as line-only. Original `hooks/useChartOptions.tsx` removes area connect-missing defaults but retains markers.

Retained AG Charts Community `AreaSeries.processData` at lines 39922-39961 uses algebraic accumulation and normalizes raw/cumulative/window groups. `accumulateGroup` defaults separateNegative to false at line 29258. This differs from the accepted bar projection. Exact package identity and inferred versus observed fixture fields must be recorded at the prerequisite.

Synthesis: reuse the existing lifecycle, editor and state owners; introduce only the cohesive area numerical projection. Existing ECharts supplies rendering; native compatibility must be demonstrated for the concrete signed/gap discriminator. Core product/tech/structure steering remains absent; approved requirements and the maintained project policies supply context. Kiro extension discovery and COBESY conclusion-first documentation were applied.
