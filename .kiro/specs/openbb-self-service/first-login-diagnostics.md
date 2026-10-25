# First-login onboarding diagnostics

First-time onboarding still produces a request error when the account has no saved developer questionnaire. Keep this baseline gap open; chart acceptance for onboarded users does not certify clean first-time onboarding.

Observed on 2026-10-25 with Workspace `432c26b93328b14b7a9d79d37bafe6203a738cfa`, image `sha256:21c08f38e01ddd5ca02b9b5ce0dbc194aa77fa491efb607068a974f319791079`. The same behavior occurred on both preceding hierarchy candidates and was already recorded in the [earlier candidate findings](parity-widget-findings.md).

The existing GET `/pro/pro-developer-onboarding-info` handler returns 404 when no `DeveloperOnboarding` row exists. `/onboarding` fetches that resource on mount and logs the rejected request. The normal name/Continue flow completes; subsequent logins bypass this page and have clean chart diagnostics. This is an absent-record contract mismatch, not a missing route or a chart action.

## Follow-up

- [ ] Review the empty-questionnaire API/UI contract before changing it.
- [ ] Repair first-login handling while preserving saved answers, authentication, skip semantics and the existing onboarding flow.
- [ ] Verify a genuinely new account through onboarding and a later login with strict console/network checks.

Do not suppress 404 diagnostics, seed questionnaire answers or skip onboarding to claim this work complete. The hierarchy run `candidate3-synthetic-1` remains failed; its request and console errors are retained. The comparison across each runtime's first and later cases is in `artifacts/chart-hierarchy/h4/browser/candidate-onboarding-comparison.json`. A later passing chart run applies only to the already-onboarded account.

Implementation is not part of the current hierarchy milestone. This page records the observed gap and its completion criteria, not an approved API redesign.
