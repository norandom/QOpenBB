# Company Research readiness reconciliation

2026-11-13. The acquisition prerequisites have advanced; full IA-B financial readiness remains false. This addendum preserves the [2026-11-06 assessment](research-input-assessment.md) and its [machine-readable receipts](../../../docs/reference/research-input-readiness.json) as dated evidence. No provider requests or new runtime tests were performed for this reconciliation.

## What is closed and what remains open

| Finding | Current evidence | Remaining boundary |
| --- | --- | --- |
| Missing effective TTM selector in Metrics/Ratios | The accepted [periodic-query repair](../../../artifacts/reviewed/periodic-query-provenance/accepted.md) emits `ttm: exclude` for default annual and explicit quarter requests. | Periodic selection does not prove a calculation window, denominator validity or comparable periods. |
| Unattributed statement fiscal facts | The accepted [statement milestone](../../../artifacts/reviewed/statement-period-provenance/publication.md) preserves row/source attribution, supplied fiscal facts, conflicts, null versus absence and duplicate rows. | Unknown coverage/start/duration, restatement and point-in-time availability remain unknown; the historical reporting-basis finding is not converted into a pass. |
| Instant/flow distinctions | Balance and closing cash retain observation dates; beginning cash has no inferred date. | This does not define cash conversion or align market prices, shares, debt, cash and other claims. |
| Native optional statement limits | Omitted limits work for existing statement widgets; [local browser acceptance](../../../artifacts/reviewed/statement-period-provenance/packaged.md) covers annual/quarter, refresh and saved reopening. | A curated multi-widget research App and its complete saved context have not been accepted. |
| Accounting metadata export | The dated assessment already distinguishes surviving comparisons from pinned source annotations. | Do not rewrite the historical sanitized receipts or attribute their repair to these provenance releases. |
| Peer financial compatibility | Provider observations and their provenance are available. | Currency, fiscal windows, price/share dates, denominator scope and enterprise-to-equity claims still require financial-method acceptance. |
| House modeling and macro/DCF | Existing foundation requirements preserve acquisition/model separation. | Cash-conversion definitions, adjusted earnings, peer aggregates, DCF/WACC and sensitivities remain separately specified work. |

The accepted statement alpha is `alpha-42878062405-1`, built from QOpenBB `e09024aa965757d23937ed0472ccce05d9666aea`, Workspace `e1a12c3a031a23598f41166a0f91b8fb24ac2387` and data API `a965f70c164fe477ce9c99654b9be48e2f1bc9fd`. Publication identities and offline CI-image checks are separate from local candidate browser acceptance. No owner-server deployment is inferred.

## Reuse before new implementation

| Need | Reuse | Work still required |
| --- | --- | --- |
| Readable company selection | Accepted [company selector](../../../docs/company-selection.md), Symbol groups and widget-owned selection state | Bind the complete research layout and verify stale-response/clearing behavior across its views. |
| Statements and price context | Existing Income/Balance/Cash and historical-price definitions in the native catalog | Coherent layout, explicit independent statement/price controls and inspectable financial meaning. |
| Peer editing | Existing Profile multi-symbol comparison editor and independent comparison group | Candidate rationale and aligned presentation of single-symbol statement observations; existing multi-symbol Profile behavior does not establish a peer financial matrix. |
| Saved research | Existing dashboard/widget/group persistence and retained-bind lifecycle | Verify all proposed context together. Existing template export excludes company-selection storage; saved dashboard persistence does not establish template export/import round-trip. Requirement 5.6 carries that remaining acceptance obligation. |
| App delivery | Existing App layouts, tabs, parameters and groups | Curate the new App; the current eleven-table starter with mixed company defaults is not a finished research layout. |

The [capability inventory](../../../docs/capability-reuse.md) remains a historical foundation reference; current catalog and acceptance records supersede its earlier missing-widget observations. Existing metadata transport is not evidence that an inspectable metadata consumer already exists.

## Next approval

Review [Company Research dashboard requirements](company-research-requirements.md) for a useful, explicitly limited IA-B increment. Observations remain available when compatibility is unknown. House methods remain in the [financial-modeling specification](../financial-modeling/requirements.md); no calculation engine moves into widgets or provider adapters.

IA-A assessment completion stays true. Full IA-B input readiness and workflow implementation stay false. The bounded dashboard can expose these limitations without claiming a validated comparable set; full IA-B still requires its cash-conversion, multiples and financial-method contracts. This is a proposed delivery boundary for owner approval, not a waiver of the investment-analysis contract.
