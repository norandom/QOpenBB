# Login credential policy independent source review

- VERDICT: APPROVED for source integration and the four measured no-growth exceptions; deployment and packaged-browser acceptance remain open.
- TASK: LP1/LP2 source boundary in `.kiro/specs/openbb-self-service/login-password-policy.md`.
- Reviewer independently read the exact fork diff, production call chain, retained tests, RED/GREEN logs and metric outputs. No application runtime, owner credentials or network was accessed.

## Mechanical results

- `git -C vendor/workspace diff --check`: exit 0.
- Backend retained evidence: `artifacts/deployment-login/backend-red.txt` shows 11 failures/20 passes before correction; `backend-green.txt` shows 31 passes. Tests execute selected real AST definitions with service dependencies stubbed. These establish schema behavior, not live HTTP authentication.
- Frontend retained evidence: `artifacts/login-policy-red.log` shows 4 failures/4 passes before correction; `artifacts/login-policy-green.log` shows 84 passes across real LoginPage and existing zodForms suites. Auth API is mocked; these establish form submission/error behavior, not real sessions.
- New placeholder markers and secrets in bounded diffs: none. Synthetic weak-password strings are deliberate regression fixtures.
- Static review: replacement annotations/imports resolve existing imports; no module-load dependencies added. Implementer reports final frontend Biome pass.
- Boundary: two schema annotations, login validator/import and focused regressions only. New-password validators, handlers, MFA, rate limit and session code unchanged.

## Findings and contract reasoning

No blocking source findings. ProUserLogin inherits UserLogin's nonempty string; password text is preserved. OAuthLogin's override and private bypass flag are unchanged. The regular login route still calls check_login, which verifies the supplied password against the stored bcrypt hash. Removing creation-time validation does not bypass authentication.

UserUpdate keeps current-password verification in validated_dict before returning an updated password. Wrong current credentials still raise Invalid password. A missing old/new pair does not install a new password. UserCreate, UserReset and UserUpdate.new_password retain check_password. The frontend new-password reset schema retains zodPassword; login's existing password is passed unchanged to updatePassword.

## Reviewed complexity exceptions

Approve only physical/logical no-growth bounds through 2026-11-28, for this credential-validation substitution:

| Fork path | Physical baseline/head | Logical baseline/head | Function cap |
| --- | --- | --- | --- |
| backend-api/backend/api/schemas.py | 2032/2032 | 1291/1291 | All <=50 |
| terminalpro/src/routes/login.tsx | 893/893 | 303/303 | Maximum 30 |

Backend evidence: `artifacts/deployment-login/backend-metrics.json`. Frontend evidence: `artifacts/login-policy-baseline-metrics.json` and `artifacts/login-policy-metrics.json`; reviewed exact changes preserve physical counts. Extraction would materially widen this urgent authentication correction. No function exception approved. Controller must bind exceptions to actual fork revision and run executable inventory gate; no broad grandfathering is approved.

## Bootstrap contract and remaining acceptance

Source inspection confirms bootstrap.resolve_secrets prioritizes nonempty process environment over persisted secrets. entrypoint invokes bootstrap, rewrites config.toml, then invokes scripts.init_users on every startup. SetupConfig.create_admin matches exact email; if the configured password fails stored-hash verification it updates that same user's password. SQLAlchemy PasswordType hashes inserted/updated plaintext. The initialised marker does not skip this sequence.

Relevant counterexamples: restarting an existing container does not reload .env; shell-exported Compose variables may override .env; blank values preserve stored secrets; changing email can create a separate administrator; extra config TOML files for the same admin may override in their processing order; migration/configuration errors stop startup. These do not contradict the bounded same-email/nonempty-password/recreated-container contract.

Before LP3/LP4 closure, run a disposable published-image Compose proof with isolated bind state and fixed email: authenticate a weak existing password, retain a saved dashboard and account UUID, edit private environment password and recreate Workspace, prove new password succeeds and old password fails while UUID/dashboard remain. Verify real browser submission and backend HTTP status, new-password warnings, and diagnostics with login-rate scheduling. Record image digest and sanitized assertions only; do not retain credentials, tokens or auth traces. Current schema/form evidence is insufficient for that runtime acceptance.

## Reviewed source identity

SHA256:
- backend-api/backend/api/schemas.py: 7DEB1C432E3855AA90BBDC4EBB9ABDAE4B4F999DF77600FB49270C6CEEC82645
- terminalpro/src/routes/login.tsx: 553F93E147B251D88471938241A3067EFA30473848F02F621413DE9E3C220951
- tests/delivery/test_workspace_password_policy.py: 12D651ACAC533AE8F044D19498BCAE9DF6E570FA8285FD70E1AB0DD79622E9BA
- terminalpro/tests/unit/routes/login.test.tsx: 4EC23F75FB0C8A14F5C89C0B71277C5B25C381EBD6FA0C76727A5637F76031F4
