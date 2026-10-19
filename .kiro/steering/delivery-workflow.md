# Prototype-first agile delivery

Owner direction, 2026-10-19: deploy the current prototype next, prioritize portable CI/CD and breadth mapping, and retain the existing end-to-end verification flow.

This amendment supersedes whole-spec phase gates where they would require complete future requirements/design/tasks before a bounded delivery. Kiro remains the durable scope, decision, task and evidence record. Use a short acceptance contract, implementation, independent review, affected checks and candidate-image E2E acceptance per slice. Historical approvals remain historical.

The current prototype includes existing Full Workspace and the installed data API baseline. Provider expansion, analyst workspace/theme, AI/Anthropic, Excel and custom data sources have separate spec ownership and do not block this release. Preserve the Anthropic-before-Excel dependency between successor specs. Quant plugins remain later work.

Release gates cover the declared prototype: authentication, usable supported widgets, actual service routing, visible failures and image identity. Owner clarification: dashboard persistence acceptance belongs to analyst-workspace; backup/restore and rollback verification remain deferred delivery work. Neither blocks the prototype. Keep the configured bind mount, existing implementation and E2E regressions; deferred acceptance is not a pass. Keep financial semantics and browser/CDP checks. Do not suppress application errors to make a prototype pass.

Dagger builds images only. Portable commands own checks, publication and release manifests; GitHub Actions stays a thin runner portable to Gitea. Deploy immutable image pulls through Compose, HTTP on 0.0.0.0:23003, owner-managed cloudflared and relative bind mounts. Never start parser-only placeholder images.

Keep one delivery slice active; fan out only disjoint bounded work. Retain per-task commits, independent review, background browser/xdist worker limits and caps of 400 physical lines/file, 300 logical units/file and 50/function. Publish concise reviewed evidence.

The roadmap owns sequencing; the spec ownership map owns handover; the breadth map retains actual criterion/test/evidence links. Transferred work stays open. The original full scope must not be called complete merely because the prototype ships.
