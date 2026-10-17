# Task 2.46 implementer receipt

The existing production widget owner now reduces updates without mutating submitted functions or delivering effects during calculation. One reducer owns widget, dirty state and committed effect records. Layout delivery publishes the committed state before save and cleanup, then delivers and acknowledges exact operation identities.

The delivery watermark retains sparse identities only while earlier operations remain outstanding. Deferred work rebased behind a delivered urgent operation publishes the final committed snapshot to store/override callbacks; ordinary same-priority snapshots retain operation order. Save acknowledgment requires the exact saved widget identity as well as its revision, so a deferred edit remains dirty after an urgent commit was saved.

Production and test paths and exact frozen hashes are in `frozen-hashes.json`. No context/schema, dependency, chart guard, feature flag, catalog or financial files were changed. The persistence predicate was moved unchanged and re-exported from its original hook.

## Focused verification

Run in Debian WSL at `/home/mc/qopenbb-work/widget-246-stage/terminalpro`. The stage was populated with the Workspace fork's `git archive HEAD terminalpro` plus only owned changed source/test files; dependencies are linked from `/home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules`. No installation or browser was used.

Pinned Node: `/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node`.

- `node node_modules/vitest/vitest.mjs run --config tests/unit/widget-sync/vitest.config.mjs`: exit 0, 12 actual production-hook/pure-reducer tests. See `tests-green.txt`.
- `node node_modules/@biomejs/biome/bin/biome check src/components/Widget.hooks.tsx src/components/widgetSync`: exit 0, four files; no changes. See `biome-green.txt`.
- `node /mnt/d/Source/QOpenBB/artifacts/task-2.46/implementer/scoped-typecheck.mjs`: exit 0, four actual production modules, zero owned diagnostics. Uses the actual WidgetT declaration and React declarations; external application dependencies use explicit declaration-only boundaries. Event names were checked against the source generic event contract; this caught and corrected the initial overly broad notification-name type. The existing incompatible store subscription overload suppression remains opaque at this boundary. This is scoped evidence, not full application type certification.

Meaningful failures preserved:

- `baseline-red.txt`: actual submitted hook calculation against fork HEAD loses an intervening name. Targeted test exit 1; repaired production source passes.
- `priority-red.txt`: initial max-ID acknowledgment skips deferred persistence after urgent commit. Targeted test exit 1; exact-ID acknowledgment and committed rebase delivery pass.
- `save-rebase-red.txt`: revision-only save acknowledgment incorrectly clears deferred dirtiness. Targeted test exit 1; exact saved-widget identity guard passes.
- `typecheck.txt`: original full-app type command exits 1 on baseline project-reference/ignoreDeprecations incompatibilities with the reused dependency toolchain.
- `typecheck-isolated.txt`: no-reference compatibility override exhausted Node's default heap. No full-app type pass is claimed and no larger retry was made.

The controller owns current inventory registration and the combined complexity gate. Initial parser measurements are in `size.json`; the final controller gate must measure the frozen files after the small rebase corrections. No Git commit was made by this worker.

Final review correction: `rebase-tail-red.txt` captures deferred ID1, committed urgent ID2, and a fresh deferred nonpersisting ID3. Checking only the final revision missed ID2 and rolled its persisted name back. A scalar maximum delivered ID now detects any already-delivered higher operation; exact acknowledgment and compact deduplication are unchanged. The final 12-test suite, Biome check and scoped type check pass.
