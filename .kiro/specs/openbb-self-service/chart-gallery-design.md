# Recreate the original chart-type selector

Implement the Chart-tab gallery as a production React component, using the original observed groups, names, order and selected treatment. This is a visible UI-03 component task authorized by the owner's production-UI direction and latest "go". It does not activate an incomplete chart editor or claim that every chart family is already mapped to ECharts.

## Component boundary

Own `terminalpro/src/components/General/Table/Chart/editor/ChartTypeGallery.tsx`, a cohesive gallery catalog and thumbnail module, and narrowly scoped styles if existing utility classes are insufficient. Reuse existing OpenBB theme tokens and button mechanics where suitable. Do not change global styles, dependencies, product flags, table entry guards or storage.

The gallery is controlled: it receives the ordered available groups/items, selected model type and an `onSelect(modelType)` callback. Each item has a model type and accessible display name. It owns no chart model, persisted state, entitlement policy or family-range conversion. The application caller remains responsible for supplying original visibility predicates and applying a family selection through the existing session. Clicking or using Enter/Space emits the exact model type once. Unknown selected values do not silently select a default.

Use the 34-item observed inventory in the [family navigation plan](../../../artifacts/reviewed/ui-parity-family-navigation-plan/plan.md) as the complete initial preview fixture. The `column` UI token maps to `groupedColumn`; do not persist UI grouping tokens. Support supplied items such as conditional custom-combination choices without silently filtering them. The fixture's 34 items do not replace all production predicates or schema enums.

Match the observed compact right-dock content, three thumbnail columns, group headings, spacing, borders and blue selected outline. Draw small conventional chart silhouettes in owned SVG code; do not copy the commercial editor implementation or its generated assets. Keep graphics decorative and expose the actual button names and selected state accessibly. Each supported supplied item must have an explicit thumbnail treatment; do not silently omit an item because an icon is missing.

Keep the selected value in the caller. Preserve scroll when selection changes without remounting the gallery. Use ordinary keyboard-accessible buttons and visible focus. Do not introduce a separate toolbar or a new product navigation surface.

## Preview and verification

Use the existing Storybook/component development entry to render the real production component with the documented inventory in dark/light themes. Selection must update the preview's selected value through the same callback contract. Clearly label this as a gallery component preview outside the product, not a working full chart editor. Set Up, Customize, chart rendering and persistence are separate integration tasks; do not add fake tabs or inert controls to imply they work.

Focused tests verify all supplied items/order, selected state, exact callback values, keyboard activation, unknown selection, conditional supplied items and scroll retention. Run scoped type/lint and the existing complexity checker. Whole maintained files must meet 400 physical lines, 300 logical units and 50/function; tests/stories are explicit development-only exclusions. Independent review covers the real component and its consumer boundary.

Reuse existing captured original screenshots for comparison. After rendering the component, show matched crops to the owner if spacing, thumbnail treatment or colors remain uncertain. The owner's visual decision applies only to the shown component/revision. No new original-browser collector or general screenshot infrastructure is needed.
