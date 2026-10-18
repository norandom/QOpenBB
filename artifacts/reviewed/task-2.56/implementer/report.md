# Combined dock evidence is ready for review

Task 2.56 verifies the real ChartEditorControlsPreview story in both themes. Background follows Padding inside Chart Style; Tooltips sits inside the initially collapsed Series group after Legend. The screenshots show the restored grouping and retained edits. This controlled preview does not establish live chart bindings, storage, full Series/axis coverage or renderer acceptance.

RED used the unchanged story and failed because Customize had no Series button (red.log, red.exit 1). After the controller froze the composed source, Vite was restarted and the same browser script passed (green.log, green.exit 0). The Node run.mjs wrapper records actual process exits; an earlier shell-based recorder was replaced because its variable expansion lost the exit value.

The existing Vite/Playwright harness was reused with envDir:false, one isolated headless Chromium context and one worker. CDP Runtime/Network diagnostics recorded zero page/console/network errors. Checks cover original grouping, Background after Padding, exact single/shared/compact values, independent padding/fill edits, alpha fill retention across toggles, hidden mode retention, close/reopen and tab remount retention, collapsed Series on remount, and availability of Set Up, gallery, Titles and Legend. Both screenshots were visually inspected. Owned Vite PID 11535 was stopped; port 6017 had no remaining listener.

Scoped strict tsc reports only existing DS typography.ts TS2578, exit 2 (typecheck.log/typecheck.exit); the task2.55 Switch-only baseline reproduced the same diagnostic. No clean full application compiler result is claimed.

source-hashes.json pins the exact story and panel bytes used by verification. Publication candidates are capture.mjs, run.mjs, finalize.mjs, preview.tsx, index.html, vite.config.mjs, red.log/red.exit, green.log/green.exit, browser-results.json, typecheck.log/typecheck.exit, source-hashes.json, dock-background-light-dark.png, dock-tooltips-light-dark.png and this report. No credentials, live data or raw browser profiles are included. The parent owns independent review, final publication manifest, metadata, commits and delivery.
