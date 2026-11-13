# Company Research design research

Read-only integration discovery, 2026-11-13. No runtime tests, live provider calls or image builds were performed for this design. Findings identify implementation seams; they do not establish an accepted dashboard.

## Sources and parallel discovery

Two independent `gpt-6.1-sol` explorers inspected state/template integration and API/consumer integration. The controller synthesized the design. Workspace baseline: `e1a12c3a031a23598f41166a0f91b8fb24ac2387`. Data API baseline: `a965f70c164fe477ce9c99654b9be48e2f1bc9fd`. QOpenBB baseline: `d364d2fede419ae1ad528db2635d5e6b7d045bfc`.

Paths below are relative to the owned Workspace fork unless prefixed otherwise. The approved [requirements](company-research-requirements.md) and [readiness reconciliation](research-readiness-reconciliation.md) remain the scope authority. The dated IA-A assessment is unchanged.

## Reuse supported by source

| Concern | Observed integration | Consequence |
| --- | --- | --- |
| Dashboard persistence | `terminalpro/src/lib/state/app.ts` saves widget/group/layout state through `/pro/dash/sync` | Use existing persistence, no new DB or API |
| Shared company selection | `terminalpro/src/components/Widgets/Helpers/useParamGroupBindings.ts` supports safe plain parameter groups for exact eligible FMP table IDs | Link profile/statements/price only; peer controller stays outside group |
| Readable identity | `terminalpro/src/components/General/Table/NavBar/companySelection.contract.ts` validates source key, symbol and nullable listing/name evidence | Adapt existing identity rather than invent another search model |
| Template import | `terminalpro/src/lib/utils/createTemplates.ts` remaps named groups and merges loose storage | Versioned widget config can travel through existing import unchanged |
| Template export | `terminalpro/src/components/General/ExportTemplatePopup.tsx` has a narrow storage allowlist excluding company selection | Add safe projections; do not dump unrestricted storage |
| Existing comparison UI | `terminalpro/src/components/Widgets/GroupedComparison.tsx` clears secondary tickers on primary changes | Unsuitable unchanged for persistent analyst-curated peers |
| Financial response | Data API `openbb_platform/core/openbb_core/app/model/obbject.py` exposes metadata at `extra.results_metadata.__qopenbb_financial__` | Inspect the existing envelope; no extra metadata endpoint |
| Table consumer | `terminalpro/src/components/General/Table/AgGridTable.tsx` receives complete response but exposes processed rows and cache time | Extract query hook and preserve original evidence beside rendered rows |
| Row transformations | `terminalpro/src/components/Widgets/dataProcessors.ts` transforms selected results without carrying provenance | Original-row inspector avoids false attribution after transpose/grouping |
| Query lifecycle | `terminalpro/src/lib/api.tsx` keys by URL/params and refresh counter, uses cancellation and bounded retries | Add current-context retention/failed-attempt state; do not treat cache time as observation time |
| Catalog App discovery | Root `services/data-api/qopenbb_data/app.py` serves merged canonical Apps through `gallery.py` | Add a generated App; no new service |
| Provider App adaptation | Root `pipeline/qopenbb_ci/catalog.py` strips unsupported provider state to params | Emit the curated App directly after validation instead of relying on lossy adaptation |

## Financial boundaries confirmed

Data API `financial_metadata.py` defines nullable unit, scale, currency, period basis, value origin, dates and financial basis. Statement provenance retains row index/source ordinal, actual period end, supplied fiscal labels, coverage evidence, filing/acceptance dates and field-specific instant dates. Duration/start, restatement status and historical availability are not established merely by a fiscal label.

FMP metrics and ratios accept one nonblank symbol, with periodic query metadata and `ttm=exclude`. A peer universe therefore needs bounded per-listing requests. Candidate discovery provides names and listing evidence, not financial comparability. No separate model runtime is accepted, so the dashboard cannot claim validated peer aggregation or reconstruct missing denominators.

## Synthesis decisions

1. Adopt existing App, groups, table frames, query adapter and storage. Building another orchestration service would duplicate accepted responsibilities without solving a required gap.
2. Generalize only the immediate shared need: financial-envelope inspection and same-context refresh state. Keep this inside the Workspace consumer, not a new platform framework.
3. Build a focused peer widget because persistent order/rationale and independent identity are absent from the existing comparison behavior. Reuse company search and existing UI primitives.
4. Preserve original row attribution outside transformed grid data. A dedicated original-observation selector is more reliable than guessing how a grouped cell maps to source rows.
5. Keep raw/provider observations separate from house modeling. Evidence labels disclose limits; they are not financial-method validation.
6. Keep existing import/state schemas unchanged. Add safe export projection and consumer decoding, with explicit unresolved identity behavior. Independent review found that the existing selector auto-resolves an invalid saved identity against the current source and can overwrite it. A narrow hook/helper guard is therefore necessary: preserve unresolved identity until explicit reselection, without blocking normal same-source group changes or initial defaults.

## Size constraints and implementation risks

Measured physical lines on accepted Workspace: table 347; renderer registry 340; API adapter 310; export popup 384; company selector 394; group helper 356. Existing oversized modules include row processors 970, QueryParams 993, app utils 1,954, template creation 919, app schema 927 and global App state 2,146. These counts do not establish logical/function compliance.

The design avoids editing oversized shared modules. Export serialization and table query extraction are cohesive prerequisites, not arbitrary line-count splits. Subsequent tasks must measure complete touched files against 400 physical / 300 logical / 50 per-function caps with the existing checker and explicit fork manifests. No new exception is granted.

Falsification conditions: if ordinary App storage cannot retain validated identity/group state through export/import, if response provenance cannot remain bound to original rows, or if the proposed renderer cannot mount through existing registration, revise the design before implementation acceptance. Passing discovery or compilation alone would not establish those properties.
