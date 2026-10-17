# Finish the production Workspace UI

This is the consolidated remaining production worklist, introduced after the owner's 2026-10-17 direction to prioritize UI implementation. It replaces the scattered follow-up tables as the progress index. Existing accepted tasks 2.13-2.45 remain reusable foundations; they do not count as completed application integration. Formal contract/task approvals remain recorded in [spec.json](spec.json) and [tasks.md](tasks.md).

Each row identifies a production outcome. Larger rows must be implemented through bounded leaves with explicit file ownership, rather than dispatched as an unrestricted task. Tests belong to the implementation they verify. Additional reference capture requires a concrete implementation question that existing code/evidence cannot answer.

## Ordinary table and chart journey

| ID | Production change | Owner / dependency | Observable completion | Current status |
| --- | --- | --- | --- | --- |
| UI-01 | Make widget updates replay-safe, then define completion with the chart consumer | Existing `Widget.hooks.tsx`; reuse existing widget storage and persistence | Successive edits use current state; React replay does not duplicate persistence or context updates; chart completion is defined at its real integration boundary | [Bounded existing-owner repair](widget-edit-design.md) accepted as task 2.46; chart-consumer completion remains pending |
| UI-02 | Resolve appearance into the existing ECharts mapper | Existing appearance composition/colors, financial formatting and Cartesian mapper | Stock/custom themes, captions, fonts, axes, legend and shadows follow stored settings in the same chart | Integration pending |
| UI-03 | Implement the original docked settings surface using existing design-system components | Chart editor; controlled tab/open state, existing event/session contracts | Chart / Set Up / Customize navigation, close/reopen, scrolling and focus work with the original layout and theme | [Chart-type gallery](chart-gallery-design.md) implemented and independently reviewed as task 2.47; owner visual judgment pending; dock and remaining tabs pending |
| UI-04 | Connect caption, series, axis, legend and tooltip controls | UI-02, UI-03; existing option reducers and event mapper | Editing each field changes both the displayed chart and the correct original stored field; disabled/conditional values retain original behavior | Remaining typed controls and bindings pending |
| UI-05 | Connect Set Up selections and transformations | Existing grid capture/range owner and editor; UI-03 | Category/series selection, reorder, aggregation and transpose update the intended observations and retain financial meaning | Flat capture exists; remaining transformations pending |
| UI-06 | Compose the chart session with the existing widget owner and host | UI-01, UI-02, UI-04, UI-05 | Data, theme and consecutive edits update the correct chart without stale writes, lost edits or a second storage owner | Integration pending |
| UI-07 | Restore table/chart entry and table-state restoration | UI-06; existing table hooks, `AgChartView`, table/file callers and compatibility boundary | Original toggle opens the selected data as a chart and returns to the same table widths, order and range; original no-series predicate remains | Current entry points remain disconnected |
| UI-08 | Restore quick actions, navigator/mini-chart and current-image export | UI-06, UI-07; existing actions and ECharts host | Original action conditions work; navigator changes the visible extent; exported image reflects the latest visible chart | Integration pending |
| UI-09 | Complete application save/reopen/restart and failure recovery | UI-07, UI-08; existing backend and accepted SQLite repair | Layout, chart model, theme, range and settings state survive reopen/restart; failed saves preserve edits and show failure | Application acceptance pending |

The first reviewable UI preview uses the actual production editor components. It must identify incomplete integration and cannot be presented as the finished product. If appearance is uncertain, show the owner matched screenshots and ask whether it is similar enough. Keep original controls and flags; no hidden reduction is authorized.

UI-04 and UI-05 prepare controls and transformations against frozen contracts. Their live displayed-chart acceptance is joined in UI-06, so the worklist does not require a working session before its own prerequisites can be implemented.

## Remaining full-capability obligations

| ID | Production change | Observable completion | Current status |
| --- | --- | --- | --- |
| UI-10 | Complete Cartesian variants and combination charts | Orientation, stacking, normalization, area/line combinations and per-series axes match original settings and stored types | Three basic mappings exist; broader coverage pending |
| UI-11 | Complete scatter/bubble, distribution and radial charts | XY/size, bins, pie/donut aliases and radial categories preserve values, controls and stored settings | Pending by family |
| UI-12 | Complete range, hierarchy and specialty charts | Range bounds, quartiles, hierarchy, heatmaps, waterfall and funnel-family settings retain their original meanings | Pending by family |
| UI-13 | Connect standalone, table-derived, AI chart and theme-preview entry points | Existing entry points render and edit their saved configurations through the replacement, preserving original access conditions | Pending by entry point |
| UI-14 | Restore advanced table settings, formulas, grouping, pivot and statistics | Original controls compute and save the expected results; existing financial observations and flags are preserved | Pending; unrelated financial-lane work is not accepted by this list |
| UI-15 | Restore specialized/remote tables, sparklines, selection/copy and exports | Original caller-specific data, paging, selection and CSV/XLSX behavior work without dropping saved configuration | Pending by caller |
| UI-16 | Accept the complete application UI and renderer image | Integrated light/dark comparison, working controls, financial values, export and persistence pass against the original capability inventory | Blocked on production outcomes above |

The [renderer capability matrix](../../../docs/renderer-capability-matrix.md) owns exact chart names, caller paths and conditions for UI-10 through UI-16. These rows do not claim that every schema-defined option is a reachable original feature. Preserve documented original blockers; do not invent functionality or silently drop an existing reachable action.

## Execution rules

- Begin with UI-01 and the concrete UI-03 component boundary. Freeze shared props/state contracts before dispatching independent implementation lanes. Integrate through the existing mapper, reducers, widget storage and ECharts host.
- Use Sol for bounded production implementation and Astra for state/financial/integration review. Keep one heavy build/browser lane. Commit each accepted implementation task with its focused evidence; do not turn routine checks into separate planning projects.
- Every modified maintained file must pass the existing complexity checker: 400 physical lines/file, 300 logical units/file and 50/function. Split oversized files by responsibility or obtain a concrete reviewed exception. Preserve unrelated edits.
- Reuse existing screenshots, fixtures and checks. Review owner-approved visual differences against the shown revision/view. Functional behavior and financial values still require meaningful assertions.
- Update this worklist from implemented outcomes. A collector, proposed test, successful health probe or source-only helper does not complete a UI row. Image publication and deployment remain later tasks in the main plan; Dagger builds images only.
