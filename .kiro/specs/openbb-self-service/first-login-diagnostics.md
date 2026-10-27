# First-login onboarding diagnostics

First-time onboarding still produces a request error when the account has no saved developer questionnaire. Keep this baseline gap open; chart acceptance for onboarded users does not certify clean first-time onboarding.

Observed on 2026-10-25 with Workspace `432c26b93328b14b7a9d79d37bafe6203a738cfa`, image `sha256:21c08f38e01ddd5ca02b9b5ce0dbc194aa77fa491efb607068a974f319791079`. The same behavior occurred on both preceding hierarchy candidates and was already recorded in the [earlier candidate findings](parity-widget-findings.md).

The existing GET `/pro/pro-developer-onboarding-info` handler returns 404 when no `DeveloperOnboarding` row exists. `/onboarding` fetches that resource on mount and logs the rejected request. The normal name/Continue flow completes; subsequent logins bypass this page and have clean chart diagnostics. This is an absent-record contract mismatch, not a missing route or a chart action.

## Follow-up

- [x] Review the empty-questionnaire API/UI contract before changing it.
- [ ] Repair first-login handling while preserving saved answers, authentication, skip semantics and the existing onboarding flow.
- [ ] Verify a genuinely new account through onboarding and a later login with strict console/network checks.

Do not suppress 404 diagnostics, seed questionnaire answers or skip onboarding to claim this work complete. The hierarchy run `candidate3-synthetic-1` remains failed; its request and console errors are retained. The comparison across each runtime's first and later cases is in `artifacts/chart-hierarchy/h4/browser/candidate-onboarding-comparison.json`. A later passing chart run applies only to the already-onboarded account.

This follow-up is separate from the completed hierarchy milestone.

## Authorized prototype batch, 2026-10-27

The owner requested autonomous roadmap batches with role-based subagents and focused verification. Under the prototype-first agile amendment, this slice repairs the existing empty-state mismatch without changing onboarding UX. Independent Sol contract review accepted the following boundary before implementation.

The authenticated GET returns HTTP 200 with JSON `null` when no questionnaire exists. The helper already returns an optional result and the frontend already guards absent answers. Populated responses, authentication, POST, stored answers and skip semantics remain unchanged. A read must not create a questionnaire. Unexpected backend errors must remain visible.

The existing `backend-api/backend/routers/pro/index.py` exceeds the normal production caps. The reviewed exception permits no growth beyond its measured baseline of 2007 physical lines and 608 logical units, and permits only the existing unchanged `login` function's 69 logical units. It expires on 2026-11-27 and covers only the GET empty-result repair. Other functions retain the 50-unit cap. Register and enforce this exception in the existing inventory; do not extract unrelated routes merely to make this small fix fit a counter.

- [x] ON1. Repair the nullable GET contract and pass focused empty/populated/authentication/error regressions against the real route and isolated database; independent source review and scoped complexity checks required.
- [ ] ON2. Verify a genuinely new account completing ordinary onboarding and a later login, with strict browser diagnostics and no seeded questionnaire or suppressed errors.
- [ ] P3/P4. Rehearse the published two-service Compose install with disposable relative bind-mounted data and one real FMP income-statement widget through the advertised data route. Verify displayed identity, date, currency and revenue against the browser response, then refresh. Provider entitlement failure is a recorded limitation, not a pass.

Sol owns the route and its focused contract test. A separate Sol worker prepares the existing Playwright journey and small ignored Compose runner; it does not modify production routes or start services concurrently. A fresh reviewer checks each implementation. The controller owns shared inventory, pins, evidence and commits. One heavy check/build runs at a time. Reuse the existing browser fixtures and Docker/request helpers; no new verification platform or broad chart matrix is part of this batch. Owner-server deployment and backup/restore remain separate.

ON1 source acceptance: Workspace `c767b02019efe1e2bc0070fb180003584648935f`; [focused verification and independent review](../../../artifacts/reviewed/prototype-onboarding/source-review.md). ON2 and the assembled prototype remain unverified.

## Catalog integration found by the Compose journey

The published `alpha-40457587542-1` run completed new-account onboarding with GET 200/null, then failed when Add Data requested `/data/widgets.json`. Health, readiness and OpenAPI were available, but the data image neither packaged nor served its generated catalog. This is the remaining task 3.8 prototype integration, not a test URL error or a provider entitlement failure. Retain the failed journey; do not substitute File/CSV rendering for this criterion.

Independent review approved two disjoint implementation lanes. Package exactly the clean committed `contracts/widgets.json` and `contracts/apps.json` through the existing runtime-input allowlist and provenance hashes, then copy them to `/app/qopenbb_data/catalog`. Serve two fixed JSON GET routes before the upstream mount, using that sibling directory. Preserve metadata, `/api/v1` endpoints, authentication policy and existing readiness semantics. Staging rejects absent/tampered assets; runtime missing-file failures remain visible. The existing three widgets and two apps are unchanged. The existing route/component compatibility check against the running API reports no changes or revalidation requirement.

- [x] CAT1. Package the two existing catalog assets with the existing provenance/tamper checks. Owner: packaging worker; files `runtime_inputs.py`, Dagger `data_api.py` and their existing delivery tests.
- [x] CAT2. Serve exact catalog bytes through the two fixed read-only routes. Owner: runtime worker; files `qopenbb_data/app.py` and existing runtime tests. No new verification framework or readiness redesign.
- [ ] CAT3. Independently review the joined source, enforce production size caps, publish once, and rerun the same assembled Compose journey. Do not mark task 3.8's broader renderer bindings or successor features complete from this bounded prototype result.

CAT1/CAT2 source acceptance: [joined verification and independent review](../../../artifacts/reviewed/prototype-onboarding/catalog-source-review.md). CAT3 and the actual live-data journey remain open.
