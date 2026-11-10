# Statement period provenance: design findings

2026-11-10. Integration-focused discovery for the owner-approved bounded contract. No provider requests, builds or tests were run. Findings come from source inspection, not a new FMP convention assertion.

## Source identity and existing seams

Sol inspected D:/Source/QOpenBB/vendor/data-api at Git HEAD `2e60c0a7aff039eda5f14a9d494beaec822fb9c4` and the staged data-api source under D:/BuildArtifacts/QOpenBB/native-app-build/data-api-stage/sources/data_api. The stage has no Git metadata; its core financial_metadata.py matches the checkout SHA-256 `559814782feb4b83dca4712faf2bac8e2f52da27328d5ed3bbd00f59cc0fbfd6`. This is not an independent hash audit of the entire stage.

- FMPAcquisition retains decoded payload and original acquisition time. No original row ordinal is attached.
- Income validates rows in provider order without clipping, preserving baseline limit/overflow behavior. Its common period basis currently comes from the query.
- Balance and Cash stably sort by period end descending and clip. Cash derives a common flow classification from FY/Q labels and preserves instant field templates. Neither proves duration from source evidence.
- Source row models map date, calendarYear, period, fillingDate and acceptedDate. Before-validators give fiscalYear and filingDate precedence, including supplied null. Capture relevant source facts before these normalizations; do not reconstruct raw alias evidence afterward.
- No explicit start, duration, YTD or restatement-history fields are modeled. Unmodeled provider extras are not validated financial evidence.
- Core FinancialResultMetadata is strict, outer version 1. Its observation_provenance is FRED-specific. The existing safe financial validation utility converts validation failures into INVALID_RESPONSE without retaining provider inputs in exception context.
- Root financial_openapi.py projects the core model schema. The catalog projection wrapper has its own version and is not the runtime envelope version.
- Existing live_financial_support helpers already compare duplicate source ordinals, preserve absent/null distinctions and export sanitized selected comparisons. The accounting sanitizer repair is accepted; no replacement is needed.

## Design synthesis

The three statement routes share one need: retain each returned row's evidence without changing its financial values. Adopt existing OpenBB/Pydantic contracts and use one narrowly typed statement sidecar and one FMP builder. No new dependency or external API change is proposed, so no package-selection research is needed.

Do not reuse the FRED series map for fiscal rows. Do not add a generic provenance registry or a service between API and widgets. Keep matching by original ordinal through each route's existing transformations; matching by date afterward loses duplicate identity.

Use unknown flow coverage until observation or reviewed provider-convention evidence supports more. Fiscal labels and query frequency remain available, but they do not supply actual start/duration. No current convention is asserted from external documentation in this design. Future evidence must be reviewed before enabling a known classification.

Retain outer version 1 with a separately versioned optional member and explicit coordinated core/provider migration, following the existing contract evolution practice. Old strict validators reject the extension; do not call it transparently backward compatible. New consumers can still read old envelopes, and absent extensions must not change unrelated provider payloads.

## Scope and verification constraints

Source physical counts: financial_metadata 193; Income adapter 133, Balance 148, Cash 138; row models Income 262, Balance 356, Cash 336. These are inspected physical counts, not a new logical/function gate result. Place typed contracts and cohesive provider construction in separate owned modules; implementation must pass the existing 400/300/50 gate without hiding logic in tests or generated files.

Kiro light-discovery/design-synthesis/review rules guided this extension. Corporate-finance and project documentation guidance require period, unit and evidence distinctions, and forbid presenting the metadata change as completed financial comparability. Native Compose/Dagger/Playwright acceptance is already established; use it for affected checks rather than opening another infrastructure workstream.
