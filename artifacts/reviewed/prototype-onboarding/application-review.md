# Published prototype installation accepted

Independent Sol review accepted the bounded local prototype on 2026-10-27. [Alpha alpha-40467871625-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-40467871625-1) contains the first-login nullable response, packaged widget/app catalog, local app-preview fallback and explicit empty agent discovery. AI implementation remains separate.

Both CI jobs passed. Three public installation assets and six anonymous image pulls (digest, release tag and latest for each service) match the release manifest. The shipped two-service Compose was pulled and started without building, using fresh relative bind-mounted data. The isolated rehearsal exposed Workspace only at 127.0.0.1:23004; the normal development install remains HTTP on port 23003. Both running image identities matched the exact published digests, with no source overlay.

The maintained browser journey passed in 21.1 seconds with one worker and no retries. A new account completed ordinary onboarding with questionnaire GET 200/null. Connections → Connect Backend → Apps → QOpenBB starter loaded actual FMP annual income. Displayed symbol, date, currency and revenue matched the response, and refresh repeated that comparison. A fresh browser context then logged in without returning to onboarding. Both sessions had zero application errors, HTTP failures, console errors or failed requests.

| Observed value | Live FMP response and displayed widget |
| --- | --- |
| Symbol | AAPL |
| Period ending | 2025-09-27 |
| Currency | USD |
| Annual revenue | 416,161,000,000 |

Published root: `11e84a3f361fb6db8b9eae5a4843242bee042660`; Workspace production: `c767b02019efe1e2bc0070fb180003584648935f`; data API source: `cab81b16bb9ef49272a6f3b0bf04cf9f34bde0ba`. The accepted browser test is committed separately as Workspace `ee7a961f055ac4b867c2b4bd640e2d3af8b2dbcb`; it does not change the published application. Its SHA-256 is `ce91ff9599d64d67c4ef4f9900626911b1656763896dda8faaa181571e45ba18`.

Evidence: [financial observation and diagnostics](application.json), [release manifest](manifest.json), [anonymous pulls](anonymous-pulls.json). Raw failed attempts remain local; no failed run was relabelled passing. Complete diagnostic attachments now precede assertions so related findings can be handled together.

This closes ON2, local P3/P4 and CAT3/4/5 for the stated journey. It does not establish owner-server deployment, broader provider coverage, saved research-context acceptance, backup/restore or AI. Generic widgets inserted with missing required symbols still produce validation errors; use the starter's configured parameters and retain that guard as a separate follow-up. The existing chart milestones retain their own acceptance evidence.
