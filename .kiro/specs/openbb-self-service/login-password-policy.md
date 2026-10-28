# Authenticate existing credentials without creation-time password rules

Owner-approved correction, 2026-10-28. A deployment configured with an existing password outside the UI's current strength policy cannot authenticate: both the login form and `/api/pro/login` reject the password before checking its hash. Treat deployment password updates and login validation as separate acceptance cases.

## Contract

- LP1: login accepts a supplied nonempty password unchanged and delegates authentication to the existing backend. Do not trim, normalize, apply strength rules or reveal whether an account exists. Hash verification, throttling, sessions, MFA and authorization remain unchanged.
- LP2: an existing/current password used to authorize a password change follows the same rule. Registration, reset and the new-password field retain the existing strength policy and warnings.
- LP3: changing the bootstrap administrator password in the deployment's private `.env` and recreating Workspace updates that same account. Verify with retained state: the new credential succeeds and the old one fails. A plain container restart does not reload Compose environment values. Never require deletion of the Workspace bind directory.
- LP4: verify browser login against an identified packaged image, including a noncompliant existing password, wrong-password rejection and unchanged new-password warnings. Verify backend HTTP behavior and clean diagnostics; focused schema tests alone are insufficient.
- LP5: publish one corrected image milestone after independent acceptance. Update installation guidance and evidence with the tested semantics. Keep the owner's actual domain in private deployment configuration; public examples remain generic.

## Bounded implementation and delegation

Frontend owns the login form and focused UI regressions. Backend owns the login/current-password schema annotations and focused schema regressions. The controller owns bootstrap/Compose acceptance, source joins, build/publication and documentation. An independent reviewer checks both changes and the retained tests before integration. No signup, password-reset UI, OAuth flow, authentication handler or database redesign is authorized by this slice.

The production changes are annotation-only substitutions in existing oversized upstream files. Independent review approved narrowly scoped no-growth exceptions: backend `api/schemas.py` has 2032 physical lines and 1291 logical units; frontend `routes/login.tsx` has 893 physical lines and 303 logical units. All functions remain within 50 units. Exceptions expire 2026-11-28 and permit only these credential-validation changes. The executable inventory must enforce these exact bounds.

## Progress

- [x] Reproduce the login policy rejection and freeze the correction boundary.
- [x] Independently accept frontend and backend source, focused regressions and complexity checks. Workspace `22180d8`: 31 backend and 84 frontend checks; 75 maintained files pass the joined complexity gate. [Source review](../../../artifacts/reviewed/login-password/source-review.md).
- [x] Verify existing-account `.env` password update with retained state. Disposable Compose recreation preserves the same administrator UUID and synthetic dashboard database content; the new credential returns 200 and the old credential returns 401. This is a database retention proof, not a dashboard UI save/reopen claim.
- [x] Verify packaged browser and HTTP login and password-setting policy boundaries for the enabled configuration. Dagger candidate `sha256:9a0854a4720c099f333c4f597b594c5b327dacabdb7229590eade6015c18d358`, root `eb0b18b`, Workspace `22180d8`: weak existing password reaches an authenticated browser session unchanged; wrong credentials fail; the backend rejects weak new passwords and wrong current passwords, and accepts a strong replacement authorized by the weak current password. Browser/CDP diagnostics are clean. Reset is disabled in this configuration, so reset-form warnings were not browser-tested; preserved validators and 76 frontend policy checks establish source coverage. [Application review](../../../artifacts/reviewed/login-password/application-review.md).
- [x] Independently accept publication and close delivery. `alpha-40676586728-1` is published from root `eb0b18bf83f2597f126b89e8483e38ccac296ab9`; both CI jobs, three public assets and six anonymous image pulls pass. [Installation guidance](../../../docs/install.md) now references this release. [Publication review](../../../artifacts/reviewed/login-password/publication-review.md) is independently accepted; published CI image bytes have not repeated candidate browser acceptance.
