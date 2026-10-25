# Roadmap

Deploy the current QOpenBB prototype next, then evolve it through small verified deliveries. This owner-approved sequence replaces the former all-features-before-release plan. Existing evidence and unfinished obligations remain intact.

## Now: deploy the prototype

Scope: existing Full Workspace and installed data API. Further provider coverage, renderer families, theme changes, commands, AI, Excel and custom sources are not prerequisites. Preserve working functionality and disclose supported capabilities and gaps.

| Slice | Deliverable | Acceptance |
| --- | --- | --- |
| P1: freeze candidate | Reconcile pending fixes, fork pins and supported-capability manifest | No unrelated edits included; source identities and known gaps recorded |
| P2: CI/CD | Portable checks/publication, thin GitHub runner and Dagger image builds | Checks fail closed; PR jobs exclude publication/provider secrets; immutable image identities |
| P3: assembled prototype | Real service images in executable Compose | Existing isolated E2E proves login, supported data/widget use and diagnostics against candidate images |
| P4: install | Pull-only instructions and release manifest | Installation rehearsal; owner-run server outcome recorded separately |

Owner clarification: saved research-context persistence acceptance moves to `analyst-workspace`. Infrastructure backup/restore and rollback verification remain deferred delivery work. Neither blocks the prototype; the bind mount and existing tests remain intact.

Target: HTTP on `0.0.0.0:23003`, `qopenbb.example.com` through owner-managed cloudflared, relative bind-mounted data. The owner deploys locally with Compose; no SSH, tunnel service or Jupyter dependency.

Current state: [alpha-40125164959-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-40125164959-1) is published with prebuilt images. Combination, scatter/bubble, histogram, pie/donut, Box Plot, Range Bar/Area, Waterfall Radar Line/Area and Nightingale acceptance cover identified local packaged images and captured FMP data in the ordinary Table/File journey. Nightingale passes its financial/control/lifecycle journey and has owner-approved appearance. Both publication jobs, release assets and six anonymous image pulls are verified separately from local browser acceptance. The pictured visual differences are accepted; pixel identity is not claimed. Assembled Compose and owner-run server acceptance remain open. See the [current chart checklist](echarts-status.md) and [Radial evidence](../artifacts/reviewed/chart-radial/verification.md#published-radial-alpha).

## Subsequent workstreams

| Spec | Responsibility | Sequence |
| --- | --- | --- |
| [openbb-self-service](../.kiro/specs/openbb-self-service/spec.json) | Foundation and prototype delivery | Active now; close with explicit scope/evidence handover |
| [market-data-integrations](../.kiro/specs/market-data-integrations/requirements.md) | Broad primary FMP coverage, yfinance price gaps, FRED economic series and future providers; consistent UX with labeled provenance | After prototype; installed adapters stay in baseline |
| [analyst-workspace](../.kiro/specs/analyst-workspace/requirements.md) | Saved research context, widgets, commands, linked instrument/time views, Bloomberg-inspired theme and remaining renderer/table functionality | After prototype; build on existing work |
| [workspace-ai](../.kiro/specs/workspace-ai/requirements.md) | Anthropic, grounding, streaming and recovery | Independent of prototype |
| [openbb-excel](../.kiro/specs/openbb-excel/requirements.md) | Add-in, generated functions, authentication and Office acceptance | Retained dependency: Anthropic accepted first |
| [custom-data-source](../.kiro/specs/custom-data-source/requirements.md) | Own datasets and later PostgreSQL | Deferred |

Build the analyst experience on existing widget, theme and ECharts work. FMP, yfinance and FRED should use interchangeable interaction patterns where their data contracts permit, with provider provenance visible. Shared controls must preserve instrument identity, time ranges, currency, units and frequency rather than imply that different datasets are equivalent.

Renderer responsibilities belong to analyst-workspace:

| Renderer | Existing scope and remaining work |
| --- | --- |
| ECharts | Integrated table charts for selected families; remaining controls, families and saved-state behavior need their own acceptance |
| Perspective 5.6 | Packages, runtime host and isolated tests exist; production dashboard binding and analytical workflow acceptance remain open |
| Plotly | Retain useful supported widgets and their financial semantics |
| Highcharts | Removed; removal does not mean ECharts replaces every former renderer capability |

These renderer obligations do not block the prototype. Full original visual parity is not a prototype release gate. The Bloomberg-inspired theme should extend the existing work and keep widget controls, commands and linked views consistent.

Quant plugins remain later work. Successor specs are initialized scope descriptions, not approved detailed requirements or tasks. Do not generate all their implementation plans before shipping the prototype.

## Breadth and end-to-end checks

[Spec ownership](../.kiro/spec-ownership.toml) records transferred obligations. The existing [breadth map](../.kiro/breadth.toml) retains historical criteria, actual tests and evidence. New capability records need one owning spec/criterion, implementation state, actual test paths, evidence identity and release relevance. Planned checks never count as passing tests.

The [provider map](provider-coverage.md) describes horizontal scope. Track provider availability separately from adapter, widget, consistency and E2E acceptance. Shared semantics cover readable identities, units, time, provenance and linking; provider origin should not change the analyst's interaction pattern.

Keep isolated Playwright/CDP, bounded xdist, financial semantics and existing persistence and failure/recovery regressions. Run affected checks per change and the integrated prototype journey at the release gate. Saved research-context acceptance belongs to analyst-workspace; infrastructure backup/restore and rollback verification remain deferred. Publish concise reviewed evidence; do not turn each check into another planning project.

The [agile delivery amendment](../.kiro/steering/delivery-workflow.md) supersedes older sequencing and whole-spec gates. Retain independent review, complexity caps and per-task commits. Transfer unfinished work without marking it complete.

## Active chart delivery queue

The owner authorized starting the next family while the accepted predecessor finishes publication on 2026-10-24. Each release remains pinned to its accepted source; the installed Compose environment is unchanged by development.

| Order | Work | State | Dependency |
| --- | --- | --- | --- |
| 1 | Nightingale | Accepted and published | Tagged assets and public image pulls verified |
| 2 | [Radial Column and Radial Bar](../.kiro/specs/analyst-workspace/radial-milestone.md) | Accepted and published; owner approved both appearances | RC5 assets and anonymous pulls verified |
| 3 | [Treemap and Sunburst](../.kiro/specs/analyst-workspace/hierarchy-milestone.md) | Locally accepted for onboarded users; both appearances approved | H5 prebuilt milestone publication |
| Later | Heatmap, funnel family and remaining caller/table obligations | Open | Follow the capability matrix and actual original reachability |

Renderer and control lanes may run concurrently after their shared contract is accepted. Shared application integration, local heavy checks and publication gates remain serialized. This queue does not mark planned tests or unsupported original paths complete.

- [ ] Resolve the existing [first-login onboarding diagnostics](../.kiro/specs/openbb-self-service/first-login-diagnostics.md). This baseline follow-up is separate from chart acceptance for onboarded users.
