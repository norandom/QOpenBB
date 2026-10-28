# Roadmap

The prototype is deployed; the next delivery track is investment analysis and valuation through small verified slices. This owner-approved sequence replaces the former all-features-before-release plan. Existing evidence and unfinished obligations remain intact.

## Delivered: prototype foundation

Scope: existing Full Workspace and installed data API. Further provider coverage, renderer families, theme changes, commands, AI, Excel and custom sources are not prerequisites. Preserve working functionality and disclose supported capabilities and gaps.

| Slice | Deliverable | Acceptance |
| --- | --- | --- |
| P1: freeze candidate | Reconcile pending fixes, fork pins and supported-capability manifest | No unrelated edits included; source identities and known gaps recorded |
| P2: CI/CD | Portable checks/publication, thin GitHub runner and Dagger image builds | Checks fail closed; PR jobs exclude publication/provider secrets; immutable image identities |
| P3: assembled prototype | Real service images in executable Compose | Existing isolated E2E proves login, supported data/widget use and diagnostics against candidate images |
| P4: install | Pull-only instructions and release manifest | Installation rehearsal; owner-run server outcome recorded separately |

Owner clarification: saved research-context persistence acceptance moves to `analyst-workspace`. Infrastructure backup/restore and rollback verification remain deferred delivery work. Neither blocks the prototype; the bind mount and existing tests remain intact.

Target: HTTP on `0.0.0.0:23003`, `qopenbb.example.com` through owner-managed cloudflared, relative bind-mounted data. The owner deploys locally with Compose; no SSH, tunnel service or Jupyter dependency.

Latest accepted chart milestone: [alpha-40652638534-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-40652638534-1) includes the 36-chart historical FMP gallery in Apps. Local acceptance covers the changed combination assignment, native save, fresh authenticated reopening and retained-bind Compose recreation. [Publication evidence](../artifacts/reviewed/chart-gallery/publication-review.md) verifies the public image pair separately; browser acceptance has not been repeated on the CI image bytes. This historical chart record is separate from the current owner-confirmed prototype deployment. See the [current chart checklist](echarts-status.md) for individual chart milestones.

The completed prototype batch repairs four observed integration gaps: an absent first-login questionnaire returns HTTP 200/null, the data image packages and serves its existing widget/app catalog, optional external app previews use Workspace's existing fallback, and the data-only backend advertises an empty agent list. [alpha-40467871625-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-40467871625-1) passes CI, release-asset checks, six anonymous pulls and the fresh-account assembled Compose journey. P3 and the local P4 installation rehearsal are accepted for onboarding, later login, live annual AAPL income values, refresh and clean diagnostics. The generic-widget required-symbol guard, broader provider acceptance, analyst persistence and backup/restore remain open. Current owner-reported startup is recorded below. AI remains a separate spec. See the [application review](../artifacts/reviewed/prototype-onboarding/application-review.md), [application result](../artifacts/reviewed/prototype-onboarding/application.json) and [delivery status](prototype-delivery.md#current-prototype-repair).

Latest delivery: [alpha-40689838352-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-40689838352-1) packages native uv, readable Python source and Valkey. The owner reported that it is up on 2026-10-28. This records startup confirmation, not an independent server-side financial or persistence audit. [Runtime and publication evidence](prototype-delivery.md) remain separately scoped.

## Next: investment analysis and valuation

The [market-data requirements](../.kiro/specs/market-data-integrations/requirements.md) are owner-approved. The [design](../.kiro/specs/market-data-integrations/design.md) is also owner-approved. The independently reviewed [first task batch](../.kiro/specs/market-data-integrations/tasks.md) is owner-approved and implementation has started: 26 bounded tasks covering shared contracts, FMP financial inputs, FRED provenance, consumer integration and milestone delivery. Later DCF, narrative and wider provider families remain explicit follow-on work. [Research](../.kiro/specs/market-data-integrations/research.md) confirms reuse of the owned OpenBB framework and retained legacy provider code. Broad exploratory provider coverage supplies the analyst dashboards; it is not limited to one example company.

The [investment-analysis contract](../.kiro/specs/analyst-workspace/investment-analysis-contract.md) defines the next analyst workflow: quarterly performance and cash conversion, defensible peer valuation, FMP DCF with a cost-of-capital/macro bridge, then linked expectations, news, transcripts and thesis context. Reuse OpenBB widgets and linking; no embedded browser is required. CFA-level analytical discipline is a quality target, not a certification claim.

- [ ] Verify actual FMP/FRED data coverage and existing implementation reuse for the first financial workflow.
- [ ] Deliver quarterly financial analysis and peer valuation, with consistent periods, metric definitions and saved research context.
- [ ] Connect FMP DCF assumptions to rates, credit conditions, WACC and defensible sensitivities.
- [ ] Complete linked expectations, inline news/transcripts and thesis tracking.

These are planned financial capabilities, not completed chart-rendering features. Detailed scope and acceptance are IA1-IA10 in the contract.

[First-spec closure](../.kiro/specs/openbb-self-service/prototype-closure.md) records nine completed delivery milestones and transferred/deferred obligations.

## Subsequent workstreams

| Spec | Responsibility | Sequence |
| --- | --- | --- |
| [openbb-self-service](../.kiro/specs/openbb-self-service/spec.json) | Foundation and prototype delivery | Prototype delivered; [closure and remaining work](../.kiro/specs/openbb-self-service/prototype-closure.md) |
| [market-data-integrations](../.kiro/specs/market-data-integrations/requirements.md) | Broad primary FMP coverage, yfinance price gaps, FRED economic series and future providers; consistent UX with labeled provenance | After prototype; installed adapters stay in baseline |
| [analyst-workspace](../.kiro/specs/analyst-workspace/requirements.md) | Saved research context, widgets, commands, linked instrument/time views, Bloomberg-inspired theme and remaining renderer/table functionality | After prototype; build on existing work |
| [workspace-ai](../.kiro/specs/workspace-ai/requirements.md) | Anthropic, grounding, streaming and recovery | Independent of prototype |
| [openbb-excel](../.kiro/specs/openbb-excel/requirements.md) | Add-in, generated functions, authentication and Office acceptance | Retained dependency: Anthropic accepted first |
| [custom-data-source](../.kiro/specs/custom-data-source/requirements.md) | Own datasets and later PostgreSQL | Deferred |

Build the analyst experience on existing widget, theme and ECharts work. FMP, yfinance and FRED should use interchangeable interaction patterns where their data contracts permit, with provider provenance visible. Shared controls must preserve instrument identity, time ranges, currency, units and frequency rather than imply that different datasets are equivalent.

The [capability reuse inventory](capability-reuse.md) anchors the next analyst slice in existing OpenBB source and installed catalog evidence. After the current delivery, uv/Python packaging and Valkey work, specify a Company Research App with one shared name/symbol selection across price, profile, statements, news, earnings calls and analyst views. Reuse the existing App JSON, widget controls, linked groups, tables and chart renderers; extend missing installed catalog/provider paths in small increments. Each increment needs source, installed configuration, real-provider and save/reopen acceptance before broader provider expansion. Existing mechanisms are not proof that the proposed App already works; the successor requirements remain scope stubs until their bounded contract is approved.

Renderer responsibilities belong to analyst-workspace:

| Renderer | Existing scope and remaining work |
| --- | --- |
| ECharts | Integrated table charts for selected families; remaining controls, families and saved-state behavior need their own acceptance |
| Perspective 5.6 | Packages, runtime host and isolated tests exist; production dashboard binding and analytical workflow acceptance remain open |
| Plotly | Retain useful supported widgets and their financial semantics |
| Highcharts | Dependencies/imports removed; legacy `ChartHighcharts` still maps to `UnsupportedRenderer`. Full former-caller parity remains open |

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
| 3 | [Treemap and Sunburst](../.kiro/specs/analyst-workspace/hierarchy-milestone.md) | Accepted and published for onboarded users; both appearances approved | H5 assets and anonymous pulls verified |
| 4 | [Heatmap](../.kiro/specs/analyst-workspace/heatmap-milestone.md) | Accepted and published for onboarded users | HM5 assets and anonymous pulls verified |
| 5 | [Funnel, Cone Funnel and Pyramid](../.kiro/specs/analyst-workspace/funnel-milestone.md) | Accepted and published for onboarded users | F5 tagged assets and public image pulls verified |
| 6 | [Stacked Line and 100% Stacked Line](../.kiro/specs/analyst-workspace/stacked-line-milestone.md) | Accepted and published | Continue with the next bounded roadmap item |
| 7 | [Sankey](../.kiro/specs/analyst-workspace/sankey-milestone.md) (additional chart type) | Accepted and published; light/dark appearances approved | Tagged assets and public image pulls verified |
| 8 | [Theme Settings preview](../.kiro/specs/analyst-workspace/theme-preview-milestone.md) | Accepted and published; Padding works and both appearances approved | TP4 tagged assets and public image pulls verified |
| Later | Remaining caller/table obligations | Open | Follow the capability matrix and actual original reachability |

Renderer and control lanes may run concurrently after their shared contract is accepted. Shared application integration, local heavy checks and publication gates remain serialized. This queue does not mark planned tests or unsupported original paths complete.

- [x] Close the [first-login onboarding, catalog, preview and agent-discovery batch](../.kiro/specs/openbb-self-service/first-login-diagnostics.md) with the independently accepted published-image Compose journey and local installation rehearsal.
- [ ] Complete owner-server deployment evidence and the generic-widget empty-required-symbol guard; broader provider and analyst workflows retain separate acceptance.
- [ ] Complete [shared advanced image, gradient and pattern palettes](../.kiro/specs/analyst-workspace/advanced-palettes.md) with renderer, persistence and export acceptance. Owner decision on 2026-10-26: track this separately while Funnel proceeds with stock/plain CSS colors.

## Historical analyst gallery

The current [gallery milestone](../.kiro/specs/analyst-workspace/historical-gallery-milestone.md) packages fixed FMP observations around January 2025 into reusable dashboards. It adds no chart renderer. The [analyst guide](chart-gallery.md) explains the questions, dimensions and transformations for all 36 chart types.

- [x] Verify native saved states and deterministic historical projections.
- [x] Implement packaged snapshot lookup and discovery without replacing the existing catalogs.
- [x] Verify all rendered examples and retained-state recreation in the assembled application.
- [x] Capture and review the README overview and all 36 per-chart screenshots.
- [x] Publish the gallery in the prebuilt images.

First data batch progress ([tasks](../.kiro/specs/market-data-integrations/tasks.md)):

- [x] Restore and characterize the existing provider verification baseline.
- [x] Implement typed financial metadata through the native result envelope.
- [x] Implement safe financial failures and separate query/result validation.
- [x] Harden FMP transport while preserving baseline consumers.
- [x] Preserve FRED acquisition times through versioned disk, memory and coalesced requests.
- [ ] Adopt these contracts in FMP/FRED fetchers and the running service; verify real-provider data.
