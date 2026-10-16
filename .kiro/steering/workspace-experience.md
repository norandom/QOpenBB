# Preserve the OpenBB experience

Owner direction, 2026-10-16: changes to OpenBB should be subtle at most when replacing charts.

Keep the existing dashboard shell, navigation, widget framing, titles, parameter controls, menus, spacing and light/dark conventions. Put replacement renderers inside the established widget boundary. Reuse existing data, state and action contracts rather than introducing a parallel dashboard interface.

Limit code changes to the replacement adapters, dependency removal and necessary compatibility work. Cohesive extractions required by complexity caps must preserve behavior; they do not authorize unrelated product changes.

Perspective's native exploration controls may differ where the replacement requires it. Keep those differences local, use compatible theme styling, and make unsupported legacy configurations explicit without changing their saved data. Do not add a second toolbar, navigation layer or new visual identity by default.

Integrated renderer review must compare the resulting widget and surrounding dashboard with the owned OpenBB baseline in light and dark modes. Record screenshots and check layout, typography, controls and interaction continuity alongside financial results and lifecycle checks. Standalone runtime fixtures do not establish dashboard visual consistency.
