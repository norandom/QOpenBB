# Company selector: reuse and design decisions

## Summary

This is an extension of native FMP widget parameters at Workspace `c652b909627d7634241eee2ed13a561fbb4f177b`, using the published data API at `28423762e8cc3faae978e770899834b41e7cde99`. The owner confirmed the [name/symbol requirement](company-selector-requirement.md); the design remains a separate approval. No runtime changes, provider calls or browser experiments were made during discovery.

The project uses the bounded-slice exception in [delivery workflow](../../steering/delivery-workflow.md), not approval of the entire analyst umbrella. Numeric criteria 1.1-1.5 label the existing confirmed interaction without expanding it. Discovery follows kiro-spec-design's light extension process; synthesis and review remain controller-owned. Documentation follows COBESY framing and the project documentation policy. Core product/tech/structure steering files remain absent; the specific delivery, delegation, complexity, testing and CI policies supply the applicable constraints.

## Existing acquisition and controls

| Source | Finding | Design consequence |
| --- | --- | --- |
| `vendor/data-api/openbb_platform/providers/fmp/openbb_fmp/models/equity_search.py` | Name search uses `is_symbol=false`, ticker lookup uses `true`; query is trimmed/nonblank, up to 200 characters; limit defaults20, maximum100 | Reuse the route with explicit FMP and limit20; no new provider endpoint |
| FMP `models/discovery_data.py` | Name, symbol, nullable exchange/currency/identifiers; alternatives and ordering retained | Do not collapse rows by symbol or infer a globally unique security |
| Workspace `components/NewAdvancedSelect.tsx` | Local option filtering, no remote search-text callback; 476 physical lines | Leave unchanged; reuse its theme/input primitives rather than growing it into another remote search controller |
| `components/Widgets/Helpers/AdvancedSelectTicker.tsx` | Remote search exists but calls Workspace `/search/symbols`, reduces identity to symbol; 665 lines | Do not route owned FMP discovery through this legacy API |
| `General/Table/NavBar/QueryParams.tsx` | Native text parameter renderer and group wrapper; Profile already has a multi-symbol comparison control | One explicit integration seam; preserve original manual/multiple behavior |
| `components/Widgets/Helpers/useParamGroupBindings.ts` | Group UUID/membership scopes updates; plain group values are strings | Reuse exact group writes, inspect membership, and reject mixed equity/FRED groups visibly |
| `lib/types/app.ts` and `components/types.d.ts` | Storage permits sibling JSON metadata; all stored `params` can reach requests | Use a typed versioned decoder for `storage.companySelection`; never put identity metadata in `storage.params` |
| `components/widgetSync/useWidgetUpdates.ts` | Functional widget update can persist related local fields together | Reuse local atomic symbol/metadata updates; no claim of cross-widget atomic metadata transactions |

These paths are findings, not permission to modify the oversized source files. The proposed integration only changes QueryParams and the small group-binding hook, with new bounded modules.

## Synthesis and decisions

### Adopt acquisition; adapt the selector UI

The generalization is one selected provider-qualified company behind two visible editable fields. Name search and ticker search are two query modes, not two instrument stores. A small remote-combobox adapter is justified because the existing local selector cannot emit remote search text and the legacy ticker selector loses required listing information. Use installed React/Radix/design-system primitives and existing debounce/query tooling. Add no packages, database, API service, generic plugin framework or global instrument registry.

### Preserve the existing group contract

Parameter groups already have isolation by UUID. Keep that behavior. A company selection may update the one exact compatible FMP equity Symbol group; it must not sweep all dashboard symbols. Mixed FRED/equity groups and multiple competing Symbol bindings need an explicit inline explanation before this new selection can commit. Keep membership and original controls available.

A plain group cannot authoritatively carry exchange/listing metadata. Store that metadata locally and validate it against the effective source/provider/symbol before display. Other members resolve names only from an unambiguous exact-symbol lookup; they never inherit a guessed identity. A full typed instrument-group model is a separate future amendment, not an undocumented sidecar group store.

### Preserve multiple-symbol capability

Profile's existing comparison editor must remain reachable. A selected company produces one active symbol; when replacing an existing multi-symbol value, the result action must state that it replaces the list. A manually maintained list has a visible multiple-company state, not one falsely attributed name. This does not implement a new multi-security research model.

### Proposed legacy-file exception

Fresh pinned-parser measurements on the committed source: Node24.22.1, TypeScript6.0.3, project-syntax-units-v1. QueryParams SHA256 `7ef59836a84f39a052b658fd47e49db713c1576c24b7635ccdf132dff9223d7a` measures938 physical/345 logical/max38 per function. The group-binding hook measures142/69/max11. Raw measurement receipt is retained at `artifacts/company-selector-design/baseline.json`.

Extracting only the renderer leaves QueryParams over400 lines; a compliant full split would also move execution, endpoint-query and Period responsibilities. That is a broader behavior-sensitive refactor. Following the first independent design review, propose a bounded QueryParams-only ceiling of1000 physical/390 logical, with function cap50 unchanged. The62physical/45logical allowance covers imports, a dedicated auto-height below-navbar host and compound local-selection wiring, including the unchanged-symbol metadata branch. New logic belongs in capped modules. This exception needs explicit design approval, candidate-head binding and executable inventory enforcement; no exception is active yet. If integration cannot fit, return to design instead of enlarging it silently.

### First independent design review

The initial draft was rejected for four local executability gaps: typed ports/exact bindings, compound commit details, fresh local/shared membership and preview safety, and real header placement/authentication-cache invalidation. The repaired draft supplies concrete contracts and ordering. Source confirms the current contextOverride caller supplies isPreview; the existing context plus actual dashboard membership can guard group writes without adding a global capability API. The small group-binding hook needs reactive reads of both local/shared widgets and groups, not a stable shared getter alone. Preview invariants are an explicit future revalidation trigger.

The selector uses a dedicated auto-height below-navbar row; wrapping inside the legacy fixed22px parameter rows would clip it. Manual-run variants retain their original control/draft path. Per-selector opaque request generations invalidate cached suggestions when source headers/authentication change, without serializing credentials or adding a credential registry. Cross-widget coalescing is deliberately outside this bounded design.

The second bounded review correction aligns the response adapter with the pinned FMP metadata: effective_query contains query/limit, while search-name versus search-symbol is identified by source.endpoint. The client must validate those actual fields rather than require an is_symbol metadata field that the API does not return.

## Risks and verification focus

- Legacy manual/group/copilot changes can invalidate saved names. Guard metadata by source/provider/effective single symbol; unresolved display is preferable to a wrong company.
- Native FMP financial routes accept a provider symbol, not an exchange-qualified instrument object. Known contradictory listings sharing one request symbol must be reported as unresolved; metadata does not add query disambiguation support.
- Canceled or late search responses must not select a previous query's company. Selection is explicit, not the first result on blur.
- Header layout must wrap the additional field using existing theme tokens; preserve Group, Period, Limit and multi-symbol controls.
- Use focused decoder/transport/group tests and one real-FMP compound journey plus a bounded failure/keyboard journey. Reuse the maintained isolated harness and CDP; assert actual clipped-viewport financial values, save/reopen and retained-state recreation for this selection only.

## Reference

[W3C APG Combobox pattern](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/) consulted 2026-10-30 for editable search, explicit selection, keyboard navigation, focus and announced popup state. Existing source and frozen contracts are authoritative for QOpenBB integration; no external library upgrade is proposed.
