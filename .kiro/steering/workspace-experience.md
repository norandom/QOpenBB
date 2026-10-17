# Preserve the OpenBB experience

Owner direction, 2026-10-16: replace the rendering library while preserving OpenBB's UX, flow, design and themes. This is an internal library substitution, with no intended visible redesign or new visual effects.

Owner selected Apache ECharts as the replacement chart engine. Use its public APIs behind the existing OpenBB controls. Perspective remains the candidate analytical engine; this choice does not authorize replacing the table UI or adding another chart editor. Existing Plotly widgets remain in scope. Library selection is approved, while compatibility design, implementation tasks and parity acceptance remain separate gates.

Keep the existing dashboard shell, navigation, widget framing, titles, parameter controls, menus, spacing and light/dark conventions. Put replacement renderers inside the established widget boundary. Reuse existing data, state and action contracts rather than introducing a parallel dashboard interface.

Functional parity is required. Do not remove, hide or disable existing features, buttons, menus or actions to accommodate the replacement library. Preserve feature flags, their defaults and their effect; do not introduce hidden capability reductions. Keeping a visible button with a no-op, degraded result or unavailable message does not establish parity.

Use the original owned OpenBB source before renderer removal as the capability baseline. Inventory its controls, actions, chart types, settings, export paths and flag conditions, then map each to replacement behavior and verification evidence. Include conditional and less visible paths. Compare both rendered controls and their working outcomes; screenshots alone cannot prove functional parity.

This direction supersedes earlier permission to hide Enterprise actions or replace working legacy features with unavailable states. Earlier task acceptance remains historical evidence, not proof of compliance with the new requirement. Identify and repair those gaps before renderer or release acceptance. Report any unresolved gap explicitly; do not silently narrow the baseline to the already modified code.

Limit code changes to the replacement adapters, dependency removal and necessary compatibility work. Cohesive extractions required by complexity caps must preserve behavior; they do not authorize unrelated product changes.

Adapt the replacement library to OpenBB's existing controls and interactions. Perspective's native interface is not automatically an acceptable replacement for the established workflow. Preserve chart styling, typography, colors, spacing, tooltips, legends and interaction behavior wherever supported. Do not add a second toolbar, navigation layer, animation or new visual identity. Make unsupported legacy configurations explicit without changing their saved data.

If a library limitation prevents equivalent behavior or appearance, document the concrete difference and obtain the owner's decision before accepting that deviation. The earlier choice of Perspective does not authorize visible UX changes. Standalone native-plugin feasibility tests establish rendering capability only; they do not establish suitability for the integrated OpenBB experience.

Integrated renderer review must compare the resulting widget and surrounding dashboard with the owned OpenBB baseline in light and dark modes. Record screenshots and check layout, typography, controls and interaction continuity alongside financial results and lifecycle checks. Standalone runtime fixtures do not establish dashboard visual consistency.

## Production UI focus and owner visual review

Owner direction, 2026-10-17: prioritize production UI changes over further standalone reference research or verification infrastructure. Reuse the accepted helpers and existing evidence. Organize work around concrete UI deliverables, with focused checks attached to each implementation task. Do not open another harness or capture workstream unless a specific implementation blocker requires it.

When visual similarity is uncertain, show the owner matched original/replacement screenshots in the same theme, viewport and data state, identify the concrete differences, and ask whether the result is similar enough. Record the decision against the shown revision and view. The owner can accept a visual difference without an extended attempt to prove pixel equivalence. Do not infer that decision from silence or extend it to other views.

Keep functional, financial-data and persistence checks focused on the changed behavior. Visual acceptance does not silently remove controls, change feature flags or accept broken actions. A preview used for comparison must state its incomplete scope and must not be presented as full renderer or release acceptance.
