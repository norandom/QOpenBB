# Connect the existing editor to the live chart

Owner amendment, 2026-10-19: [category-axis persistence](chart-axis-persistence-amendment.md) supersedes this document's runtime-only rule only for the selected category type and time format. Position and rotation retain their existing contract; the Widget remains the sole persistence owner.

Implementation amendment, 2026-10-18. The owner has authorized the live ordinary table-to-chart journey and saved settings. This amendment carries that work through the actual Workspace route, rather than accepting another isolated preview. Canonical approval metadata remains controller-owned.

## Outcome and limits

An ordinary table opens groupedColumn, stackedColumn or line in the existing widget. The completed dock controls read the chart's effective settings; edits redraw that chart and update the original saved fields. Set Up changes the selected observations. Theme changes, current-image export, return to table, save/reopen and save-failure recovery complete the journey. The existing Widget owner remains the only persistence owner.

Other families and advanced callers remain visible under their original predicates and remain unreleased parity obligations. This milestone does not claim their acceptance, add a capability flag, silently substitute a supported family, or turn engineering diagnostics into an approved product restriction. A missing required effect within the three-family journey blocks its acceptance and is resolved in this workstream.

Reuse the parent [application design](chart-application-integration-design.md), [appearance amendment](chart-appearance-editor-integration-design.md), accepted components 2.47-2.68 and [worklist](ui-parity-worklist.md). This amendment supersedes the earlier helper-only stopping boundary for this owner-authorized continuation; it does not alter financial requirements or the complete renderer matrix.

## Contract freeze

Preserve `SessionAddress`, `SessionStamp`, `OptionBaseline`, `ResolvedRange`, `ChartDisplayPolicy`, capture/range reducers and legacy model shapes. Do not create another chart store or persistence envelope. New contracts below are typed finite adapters over existing panel props and original leaf paths; they are not a general AG configuration interpreter.

| Boundary | Input and output | Owner |
| --- | --- | --- |
| Effective appearance | Selected stock/custom theme, selected baseline, generated data-only options, family, stable ordered series IDs and display precision -> explicit resolved style | Pure `application/effectiveAppearance.ts` and cohesive appearance helpers |
| Editor selection | Same effective appearance and selected model/range -> existing controlled panel values and eligibility | Pure editor binding selectors; no store reads |
| Editor edit | Discriminated union of existing panel events plus family/axis identity -> validated original option patch | `compatibility/editorBindings/`; no arbitrary string path API |
| Chart edit transaction | Current stamped event, latest widget storage/model, selected original baseline -> existing integrated reducer output | Session, committed by existing Widget updater |
| Setup transaction | Current stamped category/series IDs, order, aggregate/transpose intent -> original range/model transition plus faithfully transformed snapshot | Pure setup adapter and existing range owner |
| Renderer | Snapshot, explicit style and trusted display callbacks -> public ECharts options | Existing mapper with cohesive projections |
| Application join | Existing grid/theme/widget contexts -> one session, original dock and ECharts host | React session and existing callers |

Controller freezes concrete TypeScript contracts before dispatch: `application/appearanceModel.ts`, `compatibility/editorBindings/types.ts` and any required additions to `echarts/cartesianTypes.ts`. Reuse actual panel event/value types. Keep existing fixture callers compatible with optional additions or migrate them explicitly. Do not widen `RuntimeOptions` to permit callbacks. Disabled values remain represented, including marker shape/size, caption text and conditional axis fields.

First-wave signatures are `resolveApplicationAppearance(input: AppearanceInput): AppearanceResult`, `selectApplicationEditorState(input: EditorSelectionInput): EditorSelectionResult` and `mapApplicationEditorEvent(event: ApplicationEditorEvent, family: CartesianFamily): ValidationResult<RuntimeOptions>`. `AppearanceInput` carries the selected baseline, generated options, selected theme/mode and ordered stable IDs; success returns the extended `ResolvedCartesianStyle`. `EditorSelectionInput` carries that style plus original selected model/range; its success returns existing panel prop value types. The finite event union imports existing panel events and tags the panel and, where applicable, category/number axis. Malformed events are invalid; original namespace/eligibility must be checked before reduction. No adapter accepts an arbitrary property path. Controller freezes exact imported type names against source before dispatch.

The field manifest is the union of accepted panel props, not a hand-selected subset: title, subtitle and the two axis captions; caption typography; legend position, spacing and marker/text geometry; four-sided padding; background visibility/fill; tooltip mode; series fill/stroke opacity, width and dash; shadow; labels; line connect-missing-data and markers; both axes' type, time format, position, line, grid, tick, label typography and rotation settings. Each applicable field needs original saved leaf, effective precedence, explicit renderer projection and an observable assertion. Original panel eligibility remains authoritative. Font choices and original unit/range constraints must follow the source contract rather than preview constants.

Use `bar` for grouped/stacked column options and `line` for line options. Horizontal/vertical controls bind the original category/number axis namespaces, not their screen position alone. Existing column event APIs remain backward-compatible; extend the finite event adapter for all panel events and line. A shared appearance view model may feed editor values, but it must never become the persistence payload.

## Appearance and rendering

Compose using accepted `composeAppearanceOptions`, then explicitly resolve the admitted original fields using stock/custom theme inputs and source-backed defaults. Preserve common replacement and family override rules. Use separate palette fills/strokes and stable series identities. Reuse accepted derived colors only within their proven domain; resolve actual application theme aliases before calling them. Valid application colors or settings outside an old helper's narrow domain require implementation of the needed projection or a documented concrete blocker, not conversion to stock defaults.

Extend `ResolvedCartesianStyle` by cohesive named caption, legend, layout, axis, series and tooltip types. Split validation from projections before a modified file exceeds its cap. Public ECharts title/graphic, legend, grid, axes, series, tooltip and dataZoom APIs implement effects; unsupported exact geometry must be investigated specifically and reviewed, never ignored. Retained labels and financial callbacks use raw numeric observations and escaped tooltip content. Stock/custom grouped/stacked/line and light/dark do not inherit ECharts defaults accidentally.

For ambiguous runtime details, consult the existing finite captures and owned source first. A new reference observation is permitted only for a concrete unresolved effect. Resolve it in its consuming task; do not open a generic capture project. Evidence of one palette or tooltip case is not evidence of arbitrary inheritance.

## Session and persistence

`useApplicationChartSession` composes existing grid capture, baseline selection, display policy, appearance, mapping and host. It reads through the current Widget context; each edit uses the existing functional update mechanism against latest storage. It passes `baseline.options` as reducer `resolvedOptions`, never generated/composed appearance or ECharts output. Unknown branches and inactive family partitions survive.

Consecutive synchronous edits from the current control view must both survive. Use the session stamp to reject delayed work from an obsolete address/generation/data view; obtain current accepted render revision when dispatching a synchronous user event. Do not invalidate the second keystroke merely because the first requested another render before React committed. Delayed render/export completions still require exact latest render revision. Test this explicitly against the replay-safe Widget owner from 2.46.

Auto Rotate requires explicit compatibility handling: owned source writes `autoRotate: true` with `rotation: undefined`, but the existing lodash merge retains a saved numeric rotation; original initialization then gives numeric rotation precedence. This is a source-proven reopen limitation, not runtime-observed evidence. Preserve reducer semantics; do not introduce deletion, null or a different merge to repair it silently. Session-local manual-angle retention may support the current control interaction, but reopen must follow original initialization until a separately reviewed behavior change is authorized. Tests distinguish current interaction from reopen; the acceptance record must name this limitation rather than claiming an identical auto-rotation round trip.

The source-backed structural-axis contract also distinguishes current runtime axes from saved theme overrides. Original concrete type, position and time-format choices are not exported by `getChartModel`; reopen reconstructs them from original inputs. Preserve that limitation without inventing persisted fields. The [field and transaction manifest](chart-live-editor-contracts.md) owns these source mappings.

Preserve the exact existing `communityState.getStateKey` algorithm. Address/grid changes and unmount advance generation and dispose the owned host/subscriptions. Data/filter/sort/range changes advance data and render revisions; theme/options changes advance render revision. Baseline synchronize preserves populated-to-empty behavior. No initial render or effective-default calculation writes back normalized style.

Capture uses displayed filtered/sorted rows and raw grid values after flushing table state. Stable IDs distinguish repeated labels. Resolve category and units from actual column/provider semantics; no formatted-string parsing or guessed homogeneous units. Restore original selection, column order/widths and table filters on exit. Preserve missing values, negative values, fiscal labels and precision zero.

The application descriptor adapter at the table-context/session boundary owns unit/scale provenance. The controller freezes its exact metadata source before L3. If ordinary original numeric columns have no declared units, do not invent USD/dimensionless or block them by a new UI restriction. Review an explicit typed raw-observation policy that renders unchanged original magnitudes and makes no unit claim, keeping the existing strict declared-unit snapshot/mapper contract intact for its current callers. This is a separate semantic case, not a feature flag or permission to mix incompatible known units. A synthetic declared-unit fixture alone cannot prove ordinary caller compatibility. This narrow seam blocks descriptor/session acceptance only; appearance and editor lanes proceed independently.

Current source findings establish that `WidgetColumnDef` does not declare unit/scale, its projection drops unknown metadata, and ordinary FRED/FMP columns can lack units. Therefore the application raw-observation policy is required work, not an optional fallback. Freeze this semantic type and its explicit mapper call at L0; implement and independently review it with L2B. Undefined units remain undefined, raw observations remain unchanged, and the existing strict mapper default/tests remain intact. Known contradictory units must not be converted or relabeled under this policy.

Set Up category/series selection and ordering use existing range transitions. Aggregate and Switch Category / Series require explicit transformations and correct original saved flags/model fields; do not relabel transformed sourceMode as flat. Implement only source-established aggregation operators and preserve their missing-value and mixed-unit rules. Tests independently calculate expected sums/order and transpose round trips. An unresolved operator exposed by the ordinary journey blocks that action's acceptance; leaving it inert is not completion.

The chart host owns canvas/lifecycle; the existing shell owns menus, dock-open state and table/chart mode. Export waits for the current successfully drawn revision and uses original filename/menu conditions. Navigator/mini-chart changes displayed extent using public ECharts behavior and original persistence semantics. Save failure retains in-memory edits and the existing error/retry behavior. Reopen reads backend-persisted chart state, not a test-injected object or local shadow store.

## Activation and file ownership

All paths below are relative to `vendor/workspace/terminalpro/src/` unless stated otherwise. Existing exact caller paths are frozen in the controller handoff after the source map; proposed modules are explicitly new.

| Scope | Allowed responsibilities |
| --- | --- |
| `components/General/Table/Chart/application/effectiveAppearance*`, new appearance helpers | Resolve appearance only |
| `components/General/Table/Chart/echarts/cartesian*` | Explicit styles, validation and rendering projections |
| `components/General/Table/Chart/compatibility/editorBindings/` (new) | Typed option edit/select adapters |
| `components/General/Table/Chart/editor/ApplicationChartEditor.tsx` and cohesive section composition (new) | Compose accepted panels with production values/events |
| `components/General/Table/Chart/application/` session/setup modules | Session and transformations; preserve accepted helper ownership |
| Existing `AgChartView`, `useChartOptions`, `useTableContext`, `AgGridTable`, File caller and `communityBoundary.ts` | Restore actual createChartData/toggle/render/settings and persisted model passage |
| Existing Widget owner | Read-only unless a demonstrated consumer defect requires a separately reviewed repair |

Remove forced `chartView=false`, null buttons and unavailable renderer only at the consuming join. Replace recursive saved-chart rejection with explicit original model validation/retention, without letting malformed models crash rendering or deleting unknown saved data. Preserve existing Plotly and other caller routing. Any oversized touched caller is extracted by responsibility before modification acceptance; no implicit size exception.

## Verification and decision

Use focused existing unit/component suites for field patches, numerical transformations, snapshot semantics, mapper effects and session transactions. One joined isolated headless real-route browser suite covers all three families, representative edits from every applicable section, theme, quick actions, export freshness, table return, backend save/reopen/restart and failure/retry. Assert actual plotted values/settings, not only event payloads or successful HTTP responses. Financial calculations also have independent expected-value tests.

The controller updates the existing complexity inventory and breadth map, freezes actual commands/tool paths, and runs the combined 400 physical lines/file, 300 logical units/file and 50/function gate with explicit fork changes. Existing foundation checks are reused. Tests/docs are excluded as documented. Use one worker for the join browser and one heavy check at a time. Publish one concise delivery review record and necessary synthetic light/dark screenshots; raw logs stay local.

Disproof conditions: any completed control has no drawn effect; a later edit loses an earlier one; derived defaults enter storage; values or units change unexpectedly; reopen depends on client memory; the actual table route remains stubbed; other controls are hidden to obtain a pass. Any of these prevents live-journey acceptance. Full renderer/release acceptance remains separately blocked by the remaining capability matrix.

Core steering `product.md`, `tech.md` and `structure.md` were absent when this draft was prepared. Existing complexity, delegation, testing, workspace-experience and documentation policies were read; their absence is not permission to invent architecture policy.
