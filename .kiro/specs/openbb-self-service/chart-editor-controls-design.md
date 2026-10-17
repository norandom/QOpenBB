# Replace preview fixtures with real chart controls

Implement the observed Set Up panel and the complete Titles subsection as controlled production components in parallel. The owner authorized continuing with these controls after the dock preview. They compose into the accepted dock; chart-session storage adapters, the other Customize groups and dashboard activation remain separate work. Do not label this complete Customize or full application integration.

## Frozen ownership and callbacks

Task 2.49 owns `Chart/editor/setup/` production modules, `tests/unit/chartSetupPanel.test.tsx` and its development story. Task 2.50 owns `Chart/editor/titles/` production modules, `tests/unit/chartTitlesPanel.test.tsx` and its development story. Neither changes the accepted dock/gallery, shared design system, dependencies, storage, flags or renderer guards. The controller owns the combined development preview and metadata. Both depend on accepted 2.48; neither depends on the other.

These are UI values and edit intents, not a replacement persisted schema. Callers supply current values and all menu choices, including family-specific visibility and original entitlement predicates. Preserve supplied ordering and unknown current values; never silently choose a default or drop an item. No changes are emitted on mounting or opening a group.

### Set Up, task 2.49

Use the original collapsible `Categories` and `Series` headings, category selector, `Aggregate` switch and conditional method selector, ordered series chips with grip and remove icon, and `Switch Category / Series` switch. Existing reference: `artifacts/reviewed/parity/editor-runtime-next/focused/setup-default.png` and the editor field ledger. Series are chips, not checkboxes.

Export `ChartSetupPanel`, `ChartSetupState`, `ChartSetupEdit` and `ChartSetupChoice`. State contains `categoryId: string`, `aggregate: boolean`, `aggregationMethod: string`, `series: readonly {id: string; label: string}[]`, and `switchCategorySeries: boolean`. Props are `value`, `categories: readonly {value: string; label: string}[]`, `aggregationMethods` in the same choice shape, and `onEdit(edit)`.

The edit union is `{kind: "category" | "aggregation-method", value: string}`, `{kind: "aggregate" | "switch-category-series", value: boolean}`, `{kind: "series-remove", id: string}`, or `{kind: "series-order", ids: readonly string[]}`. Emit exact stable IDs. Removal and order remain caller-controlled. Dragging must retain every other ID exactly once; ignore stale/missing drag IDs. Provide keyboard reordering from the grip without adding a second visible toolbar. No calculations or data transformations occur in this component.

Disabling aggregation hides its method selector and retains the caller's method. Unknown menu values remain displayed without changing the model. The initial preview uses the captured `Period`, `Sum` and synthetic series names. Other caller-supplied choices are tested without claiming their original menu domain was captured. Drag gestures and candidate callbacks need verification; the screenshot alone does not prove legacy storage semantics.

### Titles, task 2.50

Export `ChartTitlesPanel`, `ChartCaptionId`, `ChartCaptionState` and `ChartCaptionEdit`. Caption IDs are `title`, `subtitle`, `horizontalAxisTitle`, `verticalAxisTitle`, labeled `Chart Title`, `Subtitle`, `Horizontal Axis Title`, `Vertical Axis Title`. Each state contains `enabled: boolean`, `text`, `font`, `weight`, `color` as strings and `size`, `spacing` as numbers. Props contain `value: Record<ChartCaptionId, ChartCaptionState>`, caller-supplied `fonts`, `weights` and `sizes` choices, `spacingBounds: {min: number; max: number; step: number}`, and `onEdit(edit)`.

String choices use `{value: string; label: string}`; sizes use `{value: number; label: string}`. `ChartCaptionEdit` is a discriminated union pairing `caption`, `field` and the corresponding field value type. Weight is an opaque caller choice key; translating it into ordered fontWeight/fontStyle writes belongs to the later storage adapter. Do not collapse numeric/string or absent/explicit style distinctions in this UI.

The `Titles` group contains all four toggles. Each enabled caption reveals `Title`, `Font`, `Weight`, `Size`, `Color` and `Spacing` (linked slider and numeric field). Turning a caption off hides its fields but keeps their values. Expansion is transient and resets naturally when the dock remounts the subtree. Preserve other caption values on edits. Numeric draft text must not emit NaN, an empty string coerced to zero, or out-of-bound values.

Use existing design-system controls where compatible. Do not use the fixed FontFamilyInput menu, which omits observed Verdana. Color must retain alpha; the existing hex-only ColorPicker cannot silently remove it. Use existing react-colorful with the pinned ECharts public color parsing utility if suitable, behind a cohesive local color input. Invalid color text produces no edit; retain a correctable draft and indicate invalid input. Enter/Escape close the picker and return focus, without inventing rollback on Escape. Do not emit normalization merely on opening; caption opening effects are not established by axis captures.

Reference inputs are the existing caption/padding and color/shadow findings and captured Titles images. Initial values use captured Verdana and sizes/spacing. Menu domains and numeric bounds are supplied explicitly by the caller; preview choices beyond captured values are candidate examples, not new claims about original menus. Keep the existing combined Weight menu presentation.

## Composition, verification and delivery

Use the production components as the dock's Set Up/Customize children in a clearly labeled development preview. Customize currently contains Titles only; do not add fake placeholders or claim the missing groups are implemented. Callbacks update controlled preview values and demonstrate retained edits; this is not backend persistence or live financial chart acceptance.

Reuse existing dark/light screenshot references, installed dependencies and isolated Vite/Playwright setup. One browser lane at a time; focused unit checks may run independently. Cover exact callbacks, unknown values, disabled retention, real keyboard interactions, series identity/order, independent caption edits, valid alpha and invalid color, numeric drafts, and dock composition. Test changes with meaningful assertions; no new reference capture framework or provider calls.

Each whole production file must satisfy 400 physical lines, 300 logical units and 50/function. Extract cohesive row/color responsibilities if needed. Register files in the existing inventory. Run focused unit tests, scoped types/lint, browser checks and independent review. Retain the existing upstream DS TypeScript diagnostic as a documented limitation if unchanged; do not expand into an unrelated design-system repair. Commit each accepted task and its reviewed evidence separately.

Both tasks implement requirements 4.8, 4.9, 10.1, 10.4, 10.5 and 10.6 within their UI boundaries. User visual judgment resolves uncertain similarity. No hidden feature, flag or capability reduction is authorized.
