# Legend and padding design review

PASS after one bounded correction pass. The controller join is explicit and the source-supported Enabled visibility rule is frozen. The field inventory, task graph and bounded controlled-panel contracts pass. No new capture or runtime-effect research is required for this UI scope.

Reviewed 2026-10-18 against candidate fork `495a08f`. Accepted design SHA256: `bf9446e4d06d971d7a52b4e67a83c1a6af18cc3ffdd90e06211e573c5b42f6a6`. Accepted draft tasks SHA256: `6b461b96ebcdec4afd1f19d264b0234a4c85e0cebed944033f6cb437327f148d`.

## Resolved corrections

Both findings below were corrected and the resulting files reread. Task 2.53 depends on both independent panels and owns composition/delivery; panel completion is local. The design now explicitly retains Enabled while hiding details without value mutation. The original findings are retained as review rationale.

1. Add an explicit controller integration task depending on both 2.51 and 2.52. Its observable completion owns combined dock composition, shared inventory/breadth updates, and composition verification. Remove combined-preview completion from the two independent panel tasks, whose local completion must be independently achievable. The current draft mentions a controller boundary but has no executable join node; completing either panel currently requires shared work that must wait for its peer. This conflicts with the task-generation integration rule and frozen independent-lane policy.
2. Replace the design's instruction to infer disabled visibility with the precise contract: with Legend expanded, Enabled remains visible; setting it false hides the detail container, retaining all values; setting it true reveals those same details. Hiding must not emit detail edits or reset them. This is supported by the existing installed source, rather than invented behavior. Keep family eligibility and selected-series predicates at the caller boundary.

## Verified boundaries and evidence

- Existing `stacked-legend.json` records Enabled, Font, Weight, Size, Color, Position, Spacing, Marker Size, Marker Stroke, Item Spacing, Horizontal Spacing, Vertical Spacing in that order. Installed `LegendPanel` at `artifacts/task-2.1/frontend/terminalpro/node_modules/ag-grid-enterprise/dist/package/main.cjs.js:48218` agrees; `FontPanel:47233` places Size and Color together. Neither supplies a Shape selector.
- The same installed source's `AgGroupComponent.setEnabled` calls `toggleGroupExpand(enabled)`; its toggle title remains separate from the hidden detail container. `createToggleTitleBar` also initializes expansion from Enabled. This is source evidence, not a claim of newly verified original runtime effects.
- Slider source at line 46394 uses minimum zero and `Math.max(value, defaultMaxValue)`. The design correctly separates slider presentation maxima from retained values and numeric validation. Decimal entry, nonfinite rejection, below-minimum rejection and correctable invalid drafts are explicit controlled-component behavior to verify; the historical capture plan does not establish completed numeric runtime parity.
- Typed field callbacks, caller-owned choices, unknown-value retention and no mount/open edits prevent implicit state migration. Opaque weight keys preserve the existing adapter boundary. Padding edits affect one side and leave geometry outside the component.
- Exclusive Legend/Padding production, unit-test and story ownership is disjoint. Read-only CaptionColorInput reuse is safe. Shared story/metadata belong to the controller. Serialize browser work and shared updates; retain per-task independent review and whole-file 400/300/50 checks using the accepted checker foundation.
- Requirements 4.8, 4.9 and 10.1/10.4/10.5/10.6 are mapped for this bounded delta. Full renderer, persistence, other Chart Style controls and owner visual acceptance remain pending. The draft is an addition to the existing task plan, not a replacement for its broader requirement coverage.

Review used the requested task-generation rules, complexity/delegation/workspace-experience policies, the existing field ledger and Legend plan, and the already installed control source. No production files, runtime, flags, dependencies or research harness were changed.
