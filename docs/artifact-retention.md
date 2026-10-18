# Keep useful tests and compact evidence

Tests protect behavior; artifacts record what a particular run established. Removing a historical screenshot or log does not reduce the executable test suite or make it faster. QOpenBB keeps maintained regression tests and reduces repeated delivery evidence.

For routine UI work, keep the affected unit/contract tests, scoped lint/types and one joined browser check for the changed flow. Keep financial transformations, persistence and failure recovery tests when those behaviors change. A broader suite belongs at an integration or release boundary, or where a concrete dependency risk requires it. Independent review remains required; it can inspect local logs without copying them all into Git.

Publish a concise verification record with the source revision, check commands/results, review decision and remaining limitations. Include the light/dark screenshots that let the owner judge the changed view. Raw logs, intermediate screenshots, duplicate size reports and one-off preview scaffolding stay local. Reuse maintained test fixtures and browser runners.

The editor components share `vendor/workspace/terminalpro/tests/unit/chart-editor/vitest.config.mjs`. From `vendor/workspace/terminalpro`, use the installed pinned toolchain to run:

```sh
pnpm exec vitest run --config tests/unit/chart-editor/vitest.config.mjs
```

For a local panel change, append its test filename, such as `tests/unit/chartShadowPanel.test.tsx`. The shared configuration selects editor panels, dock navigation and the gallery, runs one worker, and does not load the application Vite configuration. It replaces per-task unit-runner copies without removing behavioral assertions. This command is a component check, not dashboard, financial or deployment acceptance.

## Historical cleanup

The first cleanup retires 118 historical run-log and preview-scaffolding files from UI tasks 2.47 through 2.56, totaling about 102 KB. It reduces navigation clutter, not repository storage substantially. Reports, screenshots, structured results, source hashes, original reference captures and active regression inputs remain. The three browser captures currently named in the breadth map and their runner dependencies are retained, as is the missing-source regression fixture.

Retired files remain recoverable from commit `e62f6c029c50b1f38c5e7378fd21c2d4406136c1`. The public mirror's sync manifest records each original path, hash and recovery commit in `archived_entries`. Its `entries` list describes current files. Historical publication lists and reports describe their original run and may mention retired local evidence; they are not a promise that every raw file stays in the current checkout.

To inspect an archived file without restoring it, use:

```sh
git show e62f6c029c50b1f38c5e7378fd21c2d4406136c1:artifacts/reviewed/task-2.54/implementer/green.log
```

The initial inventory contained 3,904 tracked artifacts (166.4 MB), including 1,152 duplicate files by content. Most bytes belong to original reference JSON captures. Deduplicating those requires resolving their reference consumers first; this cleanup does not remove that evidence or claim storage savings it has not achieved.
