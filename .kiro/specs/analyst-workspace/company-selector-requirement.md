# Company selection by name and symbol

Owner requirement recorded on 2026-10-30: analysts need a searchable **Company name** field with a linked **Symbol** field beside it. Knowing a provider's ticker convention must not be a prerequisite for selecting a company. The owner accepts the deployed technical baseline; this note defines a subsequent analyst UX requirement, not a shipped feature or implementation approval.

## Expected interaction

- **1.1** Typing a company name offers matching listings with company name and symbol. Show exchange information to distinguish share classes, listings and similarly named companies; retain currency and provider attribution when available.
- **1.2** Selecting a result fills both fields from the same selected listing. Keep name, symbol and listing identity together rather than storing two unrelated text values.
- **1.3** Analysts who know a symbol can search through the adjacent Symbol field and select a result that also resolves the company name. Changing the selection updates the linked research context; the bounded design must define the affected widget group and preserve independent groups.
- **1.4** Keep the chosen listing's source-qualified identity. Do not infer that equal ticker strings, different share classes or provider peer suggestions identify the same security or a curated peer group.
- **1.5** Save/reopen must restore the selected name, symbol and listing consistently. A failed search or unresolved input must not silently retain a different company as if selection succeeded.

FRED should follow the same human-readable display principle in its later selector work: series name alongside series ID, with units and frequency visible where relevant. The current generic FRED widget still accepts series IDs; no series-name search is implemented by this note.

## Existing acquisition contract

Reuse the owned OpenBB discovery route `GET /api/v1/equity/search` with explicit `provider=fmp`. Company-name search uses `query` with `is_symbol=false`; ticker search uses `is_symbol=true`. The accepted adapter returns names, symbols, exchange information and source-qualified listing identifiers, retaining alternatives instead of guessing one company. These acquisition capabilities are part of the published market-data baseline; connecting them to the two-field selector is analyst-workspace work.

The selector design must assess existing Workspace selection controls and parameter groups before adding another mechanism. Exact component wiring, asynchronous search behavior, shared-group propagation and verification belong in a bounded design/task amendment. Keep provider acquisition separate from financial modeling; this control introduces no valuation calculations.

## Acceptance boundary

The current native Profile/Income Symbol inputs remain plain text. AAPL and GDP are starter defaults, not limits on supported companies or series. The deployed starter is a technical example, while a curated investment-research dashboard remains the separate [investment-analysis contract](investment-analysis-contract.md).

Before implementation, review the bounded design and tasks under the project's Kiro flow. Test actual user-visible name/symbol selection, ambiguous listings, failure/recovery, linked-group behavior and saved reopening against the existing API contract. Do not label the control complete based on discovery schema or API-only tests.

The [technical design proposal](company-selector-design.md) and [independent review](company-selector-design-review.md) are available. Independent design readiness passed and the owner approved the design/exception on 2026-10-30. The owner also approved the [reviewed task plan](company-selector-tasks.md) and implementation on 2026-10-30. Source work is in progress; the selector is not yet shipped. [Discovery and trade-offs](company-selector-research.md) explain the reuse decisions.
