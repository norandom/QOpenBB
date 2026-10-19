# Build dashboards from reusable, named data widgets

Owner direction, 2026-10-19: provide parameterized widgets for equities, commodities and futures, inline news text, and readable names alongside provider-specific symbols. Apply the same discovery experience to FRED. This is a requirements draft; provider coverage and implementation are not yet accepted.

## Dashboard builder outcomes

1. Search instruments by name or symbol. Show the name, provider ID, provider and relevant exchange/currency; distinguish ambiguous matches. Keep the selected name visible after selection and dashboard reopen.
2. Resolve selections to explicit provider IDs for requests. Display names must not replace unique identifiers or silently map between providers. Preserve existing saved symbol-only selections, showing the ID when metadata is unavailable.
3. For FRED, search by series title or ID and show title, ID, units, frequency and seasonal adjustment when available. Users should not need to memorize series IDs. Changing transformations must keep displayed units and descriptions accurate.
4. Add multiple instances of each widget, independently edit their supported parameters, and save/reopen those choices. Reuse existing Workspace parameter controls and group bindings for linked dashboard selections. Preserve working controls and behavior while applying the owner's Bloomberg-inspired visual direction through widgets and theme.
5. Show loading, no matches, empty data, entitlement restrictions and provider failures distinctly. Do not substitute another instrument or stale results under a newly selected name.

## Research coverage

FMP is the broad primary source, not a price-only integration. The [provider coverage map](../../../docs/provider-coverage.md) and its endpoint inventory define the research scope: ETFs/funds, filings and annual reports, fundamentals, analyst expectations, ownership, COT, news and other published families. Yahoo supplements identified price gaps. The initial examples below are not the scope ceiling.

## Representative widget set

| Capability | Editable inputs | Visible financial context |
| --- | --- | --- |
| Equity price history | Named instrument, date range, supported interval | Currency, price field and adjustment convention |
| Company profile | Named equity | Company name, symbol, exchange and currency |
| Financial statements | Named equity, supported statement, annual/quarterly period, count | Reporting period, currency and scale |
| Commodity prices | Named supported commodity, date range | Spot versus futures-related series, units and currency |
| Futures prices | Named supported instrument, contract/series where supplied, date range and supported interval | Expiry for dated contracts; explicit continuous-series and roll semantics where applicable |
| News | Named equities, supported dates and result count | Headline, publisher, publication date, inline provider text and original link |
| FRED series | Named series, dates, supported frequency/aggregation/transformation | Series identity, units, frequency and adjustment |

News must expose readable provider text in the widget itself, reusing the existing newsfeed presentation where feasible. A headline-only table or article dialog alone does not meet this requirement. Provider summaries must be identified as summaries; do not claim complete article coverage when only excerpts are supplied. Preserve source links and handle missing text explicitly.

Futures coverage remains a provider discovery item. Commodity spot data is not futures data, and a futures-related provider symbol does not prove dated-contract or roll-history coverage. Confirm available instruments and account entitlements before promising a contract selector.

## Observed baseline and reuse

- `contracts/datasets.json` and `contracts/widgets.json` currently admit company profile, income statement and FRED series. These have editable parameters; the recent comprehensive dashboard instead uses uploaded snapshots.
- The installed FMP provider registers only `EquityInfo` and `IncomeStatement`. Prices and news need actual provider/API support before catalog entries can work.
- `contracts/openapi.json` includes FRED commodity spot data. This does not establish futures coverage.
- Existing `useParamGroupBindings` supports linked parameters. Existing `Widgets/custom/News.tsx` supports title, excerpt, date, author and body; assess its inline reading behavior before changing presentation.

## Meaningful acceptance

Verify one dashboard journey: search by name, add price/statement/news widgets, change the linked instrument, confirm the displayed identity and data change together, then reopen the saved dashboard. Include ambiguous names, metadata unavailable and provider errors in focused checks. FRED needs a corresponding named-series selection and units check when implemented. Keep provider credentials and raw licensed data out of public artifacts.

Next: review these requirements, then freeze the supported provider routes and lookup/identity contracts in the bounded design. Existing chart-parity obligations remain in the [UI worklist](ui-parity-worklist.md).

## Command line and dashboard time context

Owner direction: use Bloomberg as the workflow benchmark and [bloomberg_free](https://github.com/iconicvenom/bloomberg_free) as a visual reference, implemented through the existing widgets, theme and chart work. This supersedes OpenBB appearance as the target for this new research surface; it does not authorize removing working features or replacing the application foundation.

The [supplied Bloomberg command guide](https://web.stevens.edu/hfslwiki/images/b/b0/Bloomberg_Tutorial_Commands.pdf) informs function discovery and security-context commands. It is a reference, not evidence that QOpenBB implements Bloomberg datasets or services.

1. Provide a keyboard-first command line with name/identifier/function autocomplete, readable results, command history and visible help. Enter executes a selected command; Escape dismisses suggestions without changing the dashboard. These research commands must work without an LLM or Anthropic connection.
2. Resolve a security by name or identifier, explicitly disambiguating listing, asset class and provider. A function-only command uses the current security where required. Show the resolved name and scope before execution; an unresolved or unsupported command must not silently select another security or function.
3. Commands open or focus the corresponding reusable widget in the active dashboard. Expose whether the action adds a widget or targets the focused widget. Preserve existing widgets and saved layouts. The command bar and mouse controls operate on the same state.
4. Maintain an explicit function catalog linking command/aliases to widget, supported asset classes, required provider capabilities and parameters. Reference candidates include SECF (security discovery), FA (financial analysis), EEO (estimates), RV (peers), FUND (fund holdings), ECO (calendar), N (news) and G (charts). These are proposed mappings, not implemented commands. QOpenBB-specific time commands must be identified as additions, not claimed as Bloomberg syntax.
5. Each dashboard has a shared date range, timezone and optional selected timestamp. Widgets visibly opt into the dashboard or a named link group, or remain independent. Link instruments and time separately so different securities can share one comparison window. Updates must not leak to another dashboard.
6. Changing the shared range updates participating charts, news, filings, statements and positioning views according to their declared date semantics. A selected timestamp synchronizes chart crosshairs/event inspection without fetching on every pointer movement. Missing observations remain missing; show the actual observation date rather than inventing matching data.
7. Distinguish price observation time, news publication time, financial period end, filing/release time and COT reporting date. Define range-filter behavior per widget. Offer historical as-of behavior only where publication timestamps and any necessary vintages support it; otherwise clearly indicate that point-in-time reconstruction is unavailable. A shared range alone is not a historical-information guarantee.
8. Persist date range or relative-range intent, timezone, selected security, group memberships and independent overrides with the dashboard. Resolve relative ranges consistently at load/refresh. Hover state may remain transient. Slow earlier responses must not overwrite newer selections; show stale/loading/error status per widget.
9. A coordinated comparison view must expose source, units, frequency and alignment conventions. Do not silently resample, forward-fill or normalize. If a statistical correlation widget is added, its return/level transformation, sampling interval, missing-data rule, observation count and window must be explicit; synchronized widgets alone are not a correlation calculation.

Acceptance example: select a company by name through the command line, add financials, price and inline news views, and link them to one time group. Change the shared range and inspect an earnings date. Verify each widget's date semantics and source, preserve another dashboard and an unlinked comparison widget, then save/reopen. Repeat with commodity prices and weekly COT to prove frequency differences and reporting delays remain visible. Include rapid selection changes, ambiguous instruments and an unavailable function. Reuse existing browser fixtures; avoid a separate test suite for every command alias.
