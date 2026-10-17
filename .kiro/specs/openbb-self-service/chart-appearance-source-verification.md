# Appearance source contracts and the remaining application join

Tasks 2.41-2.45 pass the independent source-contract review: saved-option composition, derived colors and grouped tooltip edits preserve the approved original semantics. These helpers do not activate the Workspace chart journey or establish visual parity.

## Preserved behavior

Composition reads the selected `baseline.options`, replaces its entire common branch with generated common, then applies the original lodash merge order on detached copies. Saved family branches, nulls, own undefined values and arrays retain the existing merge semantics. Rendering output does not replace the model supplied to the persistence reducer.

Color derivation takes separate foreground/background and text/chart-background tokens. It preserves the original normalized-channel arithmetic and literal light/dark ratios. Tests include the `#000000` / `#9b0000` rounding edge yielding `#8b0000`. Malformed inputs return invalid diagnostics; strings outside the captured color domain remain unresolved without guessed colors.

Grouped tooltip edits map single/shared/compact to the original `bar.tooltip.mode` patch. The addressed session rejects stale commands first, preserves latest stored state and distinguishes a valid unresolved stacked tooltip from a malformed event. Existing title, legend and stroke events retain their family behavior.

## Verification and failure evidence

The [fresh combined check](../../../artifacts/reviewed/task-2.45/review/report.md) passes 176 application tests and 274 compatibility tests, both strict TypeScript projects and scoped Biome across 25 files. Seventy-one source/configuration hashes match the isolated stage. The complete maintained complexity audit covers 176 files with no errors or violations.

The reviewed bytes are committed as Workspace `ea02ec15956dee8d2c8a06825387a570757db12d`. The source lock and maintained inventory identify that revision. Full-stage traversal manifests are omitted from publication; labeled chart/config closure derivatives retain their original provenance.

The independent [composition review](../../../artifacts/reviewed/task-2.42/review/review.md) accepts its detached merge behavior. The [tooltip repair review](../../../artifacts/reviewed/task-2.44/review-repair/report.md) accepts the event/session contract and a test-only lifecycle correction.

The full application suite exposed delayed AG Grid animation callbacks after grid destruction. The real-grid fixture now owns its timers, executes queued callbacks while jsdom exists, asserts that no timers remain, and restores globals in a finally block. It does not disable animation or suppress errors. The [root-cause record](../../../artifacts/reviewed/appearance-grid-teardown/report.md) retains the failing run and callback observations alongside passing checks.

Earlier test-harness failures, a mixed lane snapshot and a missing reviewer-stage TypeScript config remain in the reviewed artifacts. Independent runs use explicit source identities and intact logs; an assertion count alone is not a successful command.

## Next consuming boundary

Complete effective appearance and its ECharts field projections must consume these contracts alongside the original docked controls. Transformed snapshots, application activation, export freshness, table return and backend save/reopen/restart still require their own checks. No menu, feature flag, theme layout or deployment topology changes in this batch. Anthropic acceptance remains required before Excel implementation.
