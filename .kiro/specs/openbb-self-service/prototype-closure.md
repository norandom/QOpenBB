# First-spec delivery: prototype deployed

The first deployable QOpenBB prototype is delivered. The owner confirmed the current alpha is up on 2026-10-28 after publication of `alpha-40689838352-1`. This closes the prototype deployment milestone. It does not assert an independent audit of the owner's server or completion of every requirement in the original all-features plan.

## Completed delivery checklist

These are the current prototype-scoped tasks under the [delivery amendment](../../steering/delivery-workflow.md). They replace the original all-features sequencing for this release; historical task bodies below the summary in `tasks.md` retain their original evidence boundaries.

- [x] P1: Package Full Workspace and the self-hosted data API with identified source revisions and a pull-only two-service Compose deployment. [Current release evidence](../../../artifacts/reviewed/python-source-packaging/publication-review.md).
- [x] P2: Build through Dagger in GitHub, publish both public images, verify release/digest/latest pulls and attach installation assets to a tagged alpha. [Publication review](../../../artifacts/reviewed/python-source-packaging/publication-review.md).
- [x] P3: Repair onboarding, installed widget discovery, optional preview fallback and empty agent discovery; accept the supported live FMP income/login/refresh journey. [Application review](../../../artifacts/reviewed/prototype-onboarding/application-review.md).
- [x] P4: Complete the local installation rehearsal and receive owner confirmation that the server deployment is up. Owner confirmed the deployment is up on 2026-10-28. This is reported deployment, not agent-observed host inspection.
- [x] P5: Deliver the accepted ECharts chart milestones and persistent 36-chart historical FMP showcase. [Chart checklist](../../../docs/echarts-status.md) and [gallery verification](../../../artifacts/reviewed/chart-gallery/verification.md) define the exact family/control coverage.
- [x] P6: Remove Highcharts from the inspected runtime dependency set. [Artifact audit](../../../artifacts/reviewed/renderer-dependencies/verification.md). Legacy caller functionality and broad license clearance are not implied.
- [x] P7: Correct existing-password login validation and verify `.env` password replacement after recreation; retain new-password strength enforcement. [Login acceptance](../../../artifacts/reviewed/login-password/application-review.md).
- [x] P8: Replace source-hiding Cython/Poetry packaging with native locked uv and readable Python source under CPython. [Source and runtime contract](python-source-packaging.md).
- [x] P9: Replace embedded Redis with Valkey 9.0.7; verify the bounded synthetic snapshot, queue access and recreation checks and publish the result. [Valkey contract](valkey-packaging.md).

## What remains, and who owns it

| Work | Status and owner |
| --- | --- |
| Investment-analysis dashboards, peer valuation, DCF/WACC and saved research context | Next: [analyst-workspace contract](../analyst-workspace/investment-analysis-contract.md), with provider expansion in market-data-integrations |
| Remaining former-renderer callers, Perspective dashboard integration, advanced themes and table functionality | Open in analyst-workspace; accepted chart families are not blanket parity |
| Generic widget required-symbol guard | Open prototype follow-up; current deployment is not blocked |
| First manually published prerelease path and clean alternative-runner portability exercise | Remaining delivery verification; ordinary milestone publication is accepted |
| Infrastructure backup/restore and compatible rollback | Explicitly deferred delivery work |
| Anthropic, Excel, custom data and Quant plugins | Separate successor scope; Anthropic remains a prerequisite for Excel implementation |

## Historical task reconciliation

Original 3.8 and 4.1-4.4 contain broader catalog, renderer, mixed-provider or lifecycle criteria; P1/P3 close their supported prototype outcome, not all original clauses. Original 4.5 and remaining UI obligations transfer to analyst-workspace. Original 7.1-7.3 and 8.1/8.5/8.6 have implemented alpha publication counterparts in P2; their complete-baseline/Office/recovery gates were superseded for this prototype, not proven. P4 closes reported prototype installation; original 8.2's full host/image/route inspection matrix remains unverified.

Do not interpret unchecked historical tasks as a requirement to rebuild the delivered foundation. Consult this checklist and the [ownership map](../../spec-ownership.toml) for current work. The repository has no GitHub Issues at reconciliation time; task tracking is in the Markdown/spec checklists published to GitHub.
