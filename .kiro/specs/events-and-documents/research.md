# Events and Documents integration findings

Use one native story widget with four independently bound receipts. Existing Batch B widgets establish the provider contracts. The composed story still needs to prove that company changes, empty results, charts and reopened dashboards tell a consistent story. The inspection on 2026-11-27 used QOpenBB at `3fd072a` and its pinned Workspace and data API sources. [Source revisions](../../../sources.lock.json) · [Approved requirements](requirements.md)

## Research log

| Question | Source finding | Design implication |
|---|---|---|
| Can the existing story be used directly? | The research story declares its own native widget and saves model run references. Its chart groups points by axis label. | Reuse the catalog admission pattern, shell and ECharts host. Give this App its own native identity and key chart observations by source ordinal so same-date rows remain distinct. [Research story](../research-stories/design.md) |
| Where does the market cap apply? | The installed earnings adapter reports the count after its 250-row local cap. Observed overflow sets truncated to true. A null flag leaves wider coverage unknown. Field availability aggregates across all returned listings. | Filter an accepted market receipt locally and derive availability per row. Reuse the same current receipt for a listing-only change. [Calendar contract tests](../../../tests/providers/test_fmp_calendar_earnings.py) |
| Does an empty result have retrieval metadata? | The installed HTTP join exercises 204 with an empty body as well as successful envelopes and typed denial. Workspace's ordinary query rejection path loses distinctions needed here. | Classify the response at the status boundary. Use provider retrieval time only when supplied, retain the validated request tuple and distinguish a failed request from an empty result. [Installed join](../../../tests/providers/test_fmp_batch_b_installed_join.py) |
| Which document claims survive normalization? | News distinguishes site from publisher. Filings carry separate report and index URLs. An exact transcript has its own timestamp and period. Unsafe or missing required fields can cause adapter rejection before rendering. | Inspect documents independently. Show the typed failure when the adapter rejects the response; suppress unsafe link actions for metadata that reaches the view. [Document serialization examples](../../../tests/providers/fixtures/fmp_batch_b/documents/serialization_examples.json) |
| What can the existing browser evidence establish? | The prior journey verifies ordinary widgets with guarded provider captures. The composed App has a different permission, chart, lifecycle and persistence boundary. | Reuse the harness and compare each displayed fact to its own acquisition. Keep the new journey and entitlement status distinct in breadth tracking. [Batch B browser journey](../../../tests/e2e/fmp-batch-b-workspace.spec.mts) |

## Architecture decisions

Four independent readers embedded in unrelated widget instances would leave the conclusion without a single view of current evidence. One controller can bind effective choices, suppress stale completions and assemble the conclusion while keeping each input independent. The common receipt contract covers source identity, bounds and freshness. Each input retains its own content decoder. The design introduces no financial calculation or server aggregation.

Use the installed query policies, shared financial parser, authorized session transport, literal document presentation and chart host. Keep the story reader narrow because the existing query hook collapses a bodyless 204 and discards the installed error code. Retain source rows only in transient authorized state. The positive saved-state schema is shared between dashboard and template paths. [Batch B catalog policy](../../../pipeline/qopenbb_ci/catalog_batch_b.py)

Use the Kiro integration discovery and design review gate. The project-specific Workspace, complexity, verification and delivery steering govern this extension. The conventional product, tech and structure steering files are absent from this checkout; the pinned source and existing story establish the concrete integration boundaries. [Workspace steering](../../steering/workspace-experience.md) · [Complexity policy](../../steering/complexity.md)

## Risks and disproof conditions

A delayed response that can change the conclusion for a different query, an export containing response-derived text, or a chart mark that cannot be traced to its row and field disproves the design's acceptance claim. Exercise each with controlled inputs and verify the normal catalog, provider and persistence path on the candidate. No live provider calls or application acceptance tests were run during design.
