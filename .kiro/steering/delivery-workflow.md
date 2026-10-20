# Prototype-first agile delivery

Owner direction, 2026-10-19: deploy the current prototype next, prioritize portable CI/CD and breadth mapping, and retain the existing end-to-end verification flow.

This amendment supersedes whole-spec phase gates where they would require complete future requirements/design/tasks before a bounded delivery. Kiro remains the durable scope, decision, task and evidence record. Use a short acceptance contract, implementation, independent review, affected checks and candidate-image E2E acceptance per slice. Historical approvals remain historical.

The current prototype includes existing Full Workspace and the installed data API baseline. Provider expansion, analyst workspace/theme, AI/Anthropic, Excel and custom data sources have separate spec ownership and do not block this release. Preserve the Anthropic-before-Excel dependency between successor specs. Quant plugins remain later work.

Release gates cover the declared prototype: authentication, usable supported widgets, actual service routing, visible failures and image identity. Owner clarification: dashboard persistence acceptance belongs to analyst-workspace; backup/restore and rollback verification remain deferred delivery work. Neither blocks the prototype. Keep the configured bind mount, existing implementation and E2E regressions; deferred acceptance is not a pass. Keep financial semantics and browser/CDP checks. Do not suppress application errors to make a prototype pass.

Dagger builds images only. Portable commands own checks, publication and release manifests; GitHub Actions stays a thin runner portable to Gitea. Deploy immutable image pulls through Compose, HTTP on 0.0.0.0:23003, owner-managed cloudflared and relative bind mounts. Never start parser-only placeholder images.

Keep one delivery slice active; fan out only disjoint bounded work. Retain per-task commits, independent review, background browser/xdist worker limits and caps of 400 physical lines/file, 300 logical units/file and 50/function. Publish concise reviewed evidence.

The roadmap owns sequencing; the spec ownership map owns handover; the breadth map retains actual criterion/test/evidence links. Transferred work stays open. The original full scope must not be called complete merely because the prototype ships.

## Development alpha publication amendment

Owner direction on 2026-10-19: ship the current development alpha as prebuilt `latest` images and create a tagged GitHub prerelease. Stable releases later use pinned versions. For this alpha, successful source checks, identified builds and verified registry identities permit publication; remaining browser, financial, renderer and persistence acceptance stays open rather than being relabeled complete. The release manifest retains exact image digests even though development Compose defaults to `latest`. PRs never publish. This amendment supersedes the earlier immutable-only development-install and whole-prototype publication sequencing above.

## Completed-feature cadence and real-data acceptance

Owner direction, 2026-10-20: normal pushes run checks only. Build and publish images once a meaningful feature milestone, possibly spanning several commits, is complete. The controller dispatches `prototype.yml` on main with `build_images=true` after independent review and the milestone's acceptance checks. Do not dispatch for each implementation commit or documentation update.

Chart porting completion means usable replacement functionality, not merely removal of a Highcharts dependency. Preserve reachable controls, saved configurations and caller behavior; no hidden flags, disabled buttons or unavailable placeholders count as completed replacements. Track each applicable chart family and entry point explicitly.

Every chart milestone must exercise real FMP data through the application and verify displayed values, units, dates and transformations against the provider response. Record endpoint, parameters, retrieval time and source/image revision without credentials. Cover the milestone's relevant editor controls, theme, refresh, save/reopen and export behavior. Keep synthetic regressions for edge cases, but they cannot alone establish feature completion. Provider entitlement failures remain visible blockers for the affected live-data check; do not silently replace those checks with synthetic data. If an FMP dataset cannot represent a chart's financial meaning, record the gap and choose an appropriate real dataset before accepting it.

The previously published alpha remains available. Its publication does not retroactively establish complete chart-port or live-FMP acceptance.
