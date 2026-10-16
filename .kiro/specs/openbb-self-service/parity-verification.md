# Renderer parity verification contract

Requirements 4.8-4.9 require equivalent user behavior and appearance. This is a proposed verification contract for the revised renderer design, not evidence that parity tests exist or pass.

## Reference and comparison

Use owned Workspace `38dffc33389aca0e4a87e0e88d42f7067aa220df` as the pre-removal reference. Record the candidate commit and any working-tree manifest separately. Preserve the initial acquired source reference in `sources.lock.json`; the pre-removal reference includes accepted hosting fixes and does not redefine upstream provenance.

Run paired cases with identical synthetic data, viewport, font assets, theme, account tier, flag values and saved configuration. Keep each instance's accounts and storage isolated. Do not use the owner's browser, provider accounts or live dashboard state. Record unavailable reference prerequisites as unverified cases; a failing reference environment cannot establish that a feature is absent.

Preserve conditional behavior in both directions: a feature visible under an existing condition must work there, and a feature hidden by the original condition must remain hidden under that same condition. Do not enable every flag as a shortcut, remove original restrictions or silently change defaults. Source inspection establishes conditions; interaction checks establish their effects.

The original aggregate list and default sum require explicit compatibility review against the uncommitted financial adapter's EPS/unit/currency restrictions. Those restrictions are not accepted permission to disable existing actions or change their results. Resolve this mismatch in design before integrating the adapter into existing widgets.

## Per-capability evidence

Each capability record must contain:

- Original source path, symbol, revision and caller/visibility condition.
- Input fixture, initial configuration and exact user interaction sequence.
- Expected displayed result, emitted action, saved-state change and export effect where applicable.
- Candidate implementation path and actual test path/test ID once implemented.
- Reference and candidate evidence identities, command, exit code and unresolved differences.

Use explicit states: source-mapped, reference-unverified, candidate-unimplemented, candidate-failed or verified. A test which asserts that an existing feature is unavailable cannot satisfy a parity record. Do not count a handler invocation, visible button, HTTP success or screenshot without its required outcome.

## Required comparisons

| Surface | Observable checks |
| --- | --- |
| Menus and flags | Labels, ordering, icons, enabled/visible conditions, keyboard access, defaults and action outcomes match the reference. |
| Table selection | Cell ranges, headers and row gestures select the same data; clipboard, chart creation and AI context consume the same selection. |
| Chart interactions | Existing chart types, settings, tooltips, legends, axes, zoom and navigation produce equivalent results using the same controls. |
| Advanced tables | Grouping, pivots, filters, formulas, statistics, hierarchy and remote requests retain their financial and state semantics. |
| Appearance | Compare the integrated widget and surrounding dashboard in light and dark themes, including saved/custom theme properties. No broad screenshot masks over changed controls or plots. |
| Persistence | Open original saved state, change settings, save, restart and reopen; compare behavior and preserve the original payload for diagnosis. No silent conversion to a simpler view. |
| Exports | Check clipboard content, CSV, XLSX and chart-image contents against the configured view, including headers, financial values and applicable formatting. |
| Authoring | Existing widget types remain selectable/importable; valid original configurations render and retain their settings. |
| Failures | Recovery, asynchronous refresh, removal and stale selection retain correct state and never display a fabricated result. |

Small rendering differences from browser rasterization require narrowly explained comparisons; they do not justify new typography, changed spacing, missing chart elements or different interactions. Financial values and action/state outcomes require semantic assertions independent of image comparison.

## Execution and acceptance

Keep Playwright at one worker initially and run one heavy suite/build at a time. Use the project-owned background browser and CDP diagnostics. Record the proven software-WebGL environment when exercising canvas charts; a blank chart with no console error is still a failure. Do not substitute standalone Perspective tests for integrated OpenBB checks.

Independent review checks both the source inventory and runtime evidence. Complete the inventory before treating a green subset as renderer acceptance. `.kiro/breadth.toml` must name actual tests only when they exist and retain unverified entries for all remaining capabilities. Production adapters must pass the existing 400/300/50 complexity gate; verification does not waive source ownership or task review.
