# First-login onboarding diagnostics

This record tracks the baseline first-login error and its prototype repair. The nullable response fix is implemented and published; the assembled acceptance gates below distinguish source completion from verified installation behavior.

Observed on 2026-10-25 with Workspace `432c26b93328b14b7a9d79d37bafe6203a738cfa`, image `sha256:21c08f38e01ddd5ca02b9b5ce0dbc194aa77fa491efb607068a974f319791079`. The same behavior occurred on both preceding hierarchy candidates and was already recorded in the [earlier candidate findings](parity-widget-findings.md).

The original GET `/pro/pro-developer-onboarding-info` handler returned 404 when no `DeveloperOnboarding` row existed. `/onboarding` fetched that resource on mount and logged the rejected request. The normal name/Continue flow completed; subsequent logins bypassed this page and had clean chart diagnostics. This was an absent-record contract mismatch, not a missing route or a chart action.

## Follow-up

- [x] Review the empty-questionnaire API/UI contract before changing it.
- [x] Repair first-login handling while preserving saved answers, authentication, skip semantics and the existing onboarding flow.
- [x] Verify a genuinely new account through onboarding and a later login with strict console/network checks.

Do not suppress 404 diagnostics, seed questionnaire answers or skip onboarding to claim this work complete. The hierarchy run `candidate3-synthetic-1` remains failed; its request and console errors are retained. The comparison across each runtime's first and later cases is in `artifacts/chart-hierarchy/h4/browser/candidate-onboarding-comparison.json`. A later passing chart run applies only to the already-onboarded account.

This follow-up is separate from the completed hierarchy milestone.

## Authorized prototype batch, 2026-10-27

The owner requested autonomous roadmap batches with role-based subagents and focused verification. Under the prototype-first agile amendment, this slice repairs the existing empty-state mismatch without changing onboarding UX. Independent Sol contract review accepted the following boundary before implementation.

The authenticated GET returns HTTP 200 with JSON `null` when no questionnaire exists. The helper already returns an optional result and the frontend already guards absent answers. Populated responses, authentication, POST, stored answers and skip semantics remain unchanged. A read must not create a questionnaire. Unexpected backend errors must remain visible.

The existing `backend-api/backend/routers/pro/index.py` exceeds the normal production caps. The reviewed exception permits no growth beyond its measured baseline of 2007 physical lines and 608 logical units, and permits only the existing unchanged `login` function's 69 logical units. It expires on 2026-11-27 and covers only the GET empty-result repair. Other functions retain the 50-unit cap. Register and enforce this exception in the existing inventory; do not extract unrelated routes merely to make this small fix fit a counter.

- [x] ON1. Repair the nullable GET contract and pass focused empty/populated/authentication/error regressions against the real route and isolated database; independent source review and scoped complexity checks required.
- [x] ON2. Verify a genuinely new account completing ordinary onboarding and a later login, with strict browser diagnostics and no seeded questionnaire or suppressed errors.
- [x] P3/P4. Rehearse the published two-service Compose install with disposable relative bind-mounted data and one real FMP income-statement widget through the advertised data route. Verify displayed identity, date, currency and revenue against the browser response, then refresh. Provider entitlement failure is a recorded limitation, not a pass.

Sol owns the route and its focused contract test. A separate Sol worker prepares the existing Playwright journey and small ignored Compose runner; it does not modify production routes or start services concurrently. A fresh reviewer checks each implementation. The controller owns shared inventory, pins, evidence and commits. One heavy check/build runs at a time. Reuse the existing browser fixtures and Docker/request helpers; no new verification platform or broad chart matrix is part of this batch. Owner-server deployment and backup/restore remain separate.

ON1 source acceptance: Workspace `c767b02019efe1e2bc0070fb180003584648935f`; [focused verification and independent review](../../../artifacts/reviewed/prototype-onboarding/source-review.md). The accepted assembled journey is recorded below.

## Catalog integration found by the Compose journey

The published `alpha-40457587542-1` run completed new-account onboarding with GET 200/null, then failed when Add Data requested `/data/widgets.json`. Health, readiness and OpenAPI were available, but the data image neither packaged nor served its generated catalog. This is the remaining task 3.8 prototype integration, not a test URL error or a provider entitlement failure. Retain the failed journey; do not substitute File/CSV rendering for this criterion.

Independent review approved two disjoint implementation lanes. Package exactly the clean committed `contracts/widgets.json` and `contracts/apps.json` through the existing runtime-input allowlist and provenance hashes, then copy them to `/app/qopenbb_data/catalog`. Serve two fixed JSON GET routes before the upstream mount, using that sibling directory. Preserve metadata, `/api/v1` endpoints, authentication policy and existing readiness semantics. Staging rejects absent/tampered assets; runtime missing-file failures remain visible. The existing three widgets and two apps are unchanged. The existing route/component compatibility check against the running API reports no changes or revalidation requirement.

- [x] CAT1. Package the two existing catalog assets with the existing provenance/tamper checks. Owner: packaging worker; files `runtime_inputs.py`, Dagger `data_api.py` and their existing delivery tests.
- [x] CAT2. Serve exact catalog bytes through the two fixed read-only routes. Owner: runtime worker; files `qopenbb_data/app.py` and existing runtime tests. No new verification framework or readiness redesign.
- [x] CAT3. Independently review the joined source, enforce production size caps, publish once, and rerun the same assembled Compose journey. Do not mark task 3.8's broader renderer bindings or successor features complete from this bounded prototype result.

CAT1/CAT2 source acceptance: [joined verification and independent review](../../../artifacts/reviewed/prototype-onboarding/catalog-source-review.md). The accepted published-image journey is recorded below.

## Starter application and preview repair

The published catalog is reachable in `alpha-40460846959-1`. The supported installation path is Connections â†’ Connect Backend â†’ Apps â†’ QOpenBB starter. Its saved AAPL/annual and GDP parameters load actual provider data. Adding generic widgets directly to an empty dashboard instead mounts missing required symbols and produces validation errors; that separate missing-input guard remains open.

The existing-account probe verified displayed AAPL identity, reporting date, USD revenue and refresh against the live FMP response. Strict diagnostics then found an unavailable external FRED app thumbnail. This probe is not full fresh-install acceptance. Earlier failed runs remain retained.

Independent review accepted removing only external optional `img`, `img_light` and `img_dark` previews during catalog adaptation, with an explicit omission record and the existing AppCard fallback. Preserve local previews, application identity, layout, groups, parameters and data. Regenerate through the clean maintained generator against the retained schema/image/inventory; unrelated renderer work stays excluded. No image proxy or frontend redesign is required.

- [x] CAT4 source. Apply the preview adaptation; pass external/local/immutability cases and production caps with independent review.
- [x] CAT4 delivery. Review regenerated assets, publish the corrected image pair and complete the same fresh-account starter journey with strict diagnostics.
- [ ] Separate follow-up: prevent generic widgets from requesting data until required parameters are present, preserving their existing controls and visible validation.

The fresh `alpha-40465574999-1` journey confirms the preview repair, onboarding, live income values and refresh. Strict diagnostics expose the remaining optional `/data/agents.json` discovery 404. The reviewed data-only contract returns HTTP 200 with `[]`, accepted by both Workspace consumers, without claiming AI implementation. A focused no-provider-call regression passes with the existing runtime tests.

- [x] CAT5 source. Serve the fixed empty agent catalog before the upstream mount; independent review and all nine runtime cases pass. See [source evidence](../../../artifacts/reviewed/prototype-onboarding/agents-source-review.md).
- [x] CAT5 delivery. Publish and verify the corrected pair, then complete the fresh starter journey and later login with all diagnostics retained.

## Local prototype acceptance, 2026-10-27

Independent review accepted ON2, local P3/P4 and CAT3/4/5 on published `alpha-40467871625-1`. The fresh-account journey passed in 21.1 seconds against the exact two-image digest pair, with no source overlay: ordinary onboarding (200/null), installed starter AAPL annual-income values and refresh, then later login without onboarding. Both sessions have clean console/network/application diagnostics. Displayed USD revenue 416,161,000,000 for 2025-09-27 matches the live FMP response.

See the [review and scope](../../../artifacts/reviewed/prototype-onboarding/application-review.md) and [financial observation](../../../artifacts/reviewed/prototype-onboarding/application.json). The maintained test is Workspace `ee7a961f055ac4b867c2b4bd640e2d3af8b2dbcb`; published application sources remain those in the release manifest. Owner-server deployment, broader provider coverage, analyst persistence, backup/restore and the separate generic required-parameter guard remain open.
