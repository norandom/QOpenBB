# Original grouped-bar miniature fails

The original grouped-bar navigator changes numeric X correctly, but enabling its miniature leaves the overview empty and emits `AG Charts - internal config error: keys must come before values`. The bounded final observation recorded no chart error before the action and the error immediately afterward; Hide mini chart was visible afterward. [Original result](original-empty-miniature.png).

Independent Astra review confirmed the numeric-X drag effect, retained category order, empty grouped-bar overview and original error. This finding needs an owner repair decision; task 2.78 is not complete. The earlier source/numerical review found no defect in the prepared family union/predicate or expected-value fixture. Renderer/control implementation has not started.

Reference identity: original Workspace `38dffc33389aca0e4a87e0e88d42f7067aa220df`, image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`. Original frontend is served by the existing owned disposable container; its backend is source-overlaid with the accepted SQLite repair. This is not a release-image acceptance.

Original File retrieval returned 401 because its fetch omitted the API bearer. The collector forwards the same disposable session's bearer only to the exact synthetic CSV URL returned by this run's upload. It stays in memory, outside artifacts. The actual request/response data is otherwise unchanged. A previous dashboard file still produced a separate 401 before this fixture; this is disclosed rather than allowlisted as an application pass. The result establishes chart behavior only, not the original File authentication journey.

The retained original source strips miniature bar direction, which falls back to vertical; that is not proven working behavior. A working horizontal overview would align its numeric X with the main navigator. Such a repair preserves the original controls but is an intentional difference requiring owner approval.

Collection: pinned Node 24.22.0 / Playwright 1.64.0, existing live-chart configuration and fixtures, one headless worker, no retries. `test reference.spec.ts --config artifacts/live-editor/horizontal-bars/reference.config.ts` completed 1/1 in 16.5 seconds. Raw evidence is under `artifacts/live-editor/horizontal-bars/reference-mini-error/`. Procedural success means collection completed, not miniature acceptance. Source checks identify AG Charts 12.1.1; package hashes and numerical contracts are recorded beside the design.

No runtime repair was made. Switching to stackedBar renders main stacks and removes the strip; that does not independently prove its miniature fails. Broad renderer and release acceptance remain pending.
