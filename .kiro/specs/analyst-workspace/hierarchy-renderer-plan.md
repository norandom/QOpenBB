# Hierarchy renderer and controls: next batch

Finish the four interface decisions below, then implement Treemap/Sunburst rendering and controls in parallel. The inactive capture/setup foundation is accepted at Workspace `fb0113c78a9b143edd4df3957e84e13ee3b98647`. Rendering, live integration and packaged financial acceptance remain open. This is the next-work plan dated 2026-10-25, not an approved implementation freeze.

The [hierarchy contract](hierarchy-contract.md) owns behavior, the [setup design](hierarchy-setup-design.md) owns prepared financial data, and the [milestone](hierarchy-milestone.md) owns completion. The [independent renderer design review](../../../artifacts/reviewed/chart-hierarchy/renderer-design-review.md) accepts the architectural direction and identifies the remaining decisions.

## Before parallel implementation

- [ ] Observe only equal finite Color and selected-but-all-missing Color in the pinned original. Record legend labels, bar and control availability for both families using one fixture. Keep the financial legend range separate from the paint fallback; never present an invented 0..1 range as observed data.
- [ ] Freeze exact appearance, editor state and intent interfaces, including their owning files. Reuse existing title/background/padding/tooltip states and transactions. Preserve Size/Color assignment and ordered categories from H1c.
- [ ] Inventory source-valid saved label and paint policies before narrowing the adapter's types. Preserve supported saved configurations; a diagnostic for an unsupported policy is not equivalent rendering or permission to remove a feature.
- [ ] Assign the gradient hover indicator an explicit event and lifecycle owner. Freeze how the renderer and existing host cooperate; do not silently omit the visible effect.

These are focused readiness checks. Do not repeat the completed hierarchy observation matrix or expand into a custom layout framework. If an original edge case requires a financial behavior correction, present that specific choice to the owner.

## Agreed architectural direction

Use native ECharts Treemap and Sunburst with the existing host, lifecycle, export and session ownership. H1c remains the sole aggregation/tree-preparation owner. The renderer consumes prepared subtree weights and raw observations separately; geometric area is not a financial tooltip value.

Keep stable equal-weight Treemap ordering by sorting detached siblings and disabling native sorting. Sunburst retains insertion order. Resolve palette identity and Color extent before removing zero-area geometry, so missing/negative sizes do not silently alter the color scale. Native geometry and label fitting have known differences from the original; acceptance remains the existing side-by-side visual review.

Preserve original control paths and labels. Reuse common editor primitives and add only the required Treemap spacing and continuous gradient groups. No new flags, hidden controls, categorical legend substitutions or independent persistence owner.

Assess the MIT-licensed Culori library for original OKLCH color conversion, with a narrow adapter for the original hue/achromatic rules. A dependency is proposed, not installed. Verify exact runtime/type pins and the protected update command before modifying the existing package/lock pair. Keep the established upstream lock/build workflow; do not introduce a second lockfile. Use native ECharts graphics for a sampled gradient if they preserve the required labels, controls and hover behavior.

## Execution order and ownership

1. Controller completes the readiness checks, publishes the exact shared declarations and dependency decision, and obtains independent design review.
2. Renderer worker owns native hierarchy options, detached data, color, chrome and tooltips. Controls worker owns appearance resolution, editor projection/validation and the two semantic control groups. Their exact writable paths are frozen before dispatch; neither changes shared session owners.
3. One integration owner connects the retained capture, setup, renderer and editor atomically through the existing session. Preserve stale-command checks, recapture behavior and unknown saved settings.
4. Verify a packaged candidate with the retained eight-leaf AAPL FY2025 USD fixture, meaningful control changes, theme, export and fresh-session reopen. Publish representative FMP screenshots and one image release after milestone acceptance.

Each implementation task requires independent review, affected focused tests, baseline-relative static checks and inventory-backed limits of 400 physical lines/file, 300 logical units/file and 50/function. Use at most two disjoint implementers plus a reviewer; serialize heavy verification and builds. Update README/docs checkboxes and breadth mapping with each accepted task. Planned renderer checks are not completed tests.
