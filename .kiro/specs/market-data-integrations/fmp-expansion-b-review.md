# Batch B independent design review

**GO for owner design review.** On 17 November 2026 an independent gpt-6-astra reviewer checked the [bounded design](fmp-expansion-b-design.md) against the accepted root, data API and Workspace sources. The design retains the native Fetcher and OBBject path, distinguishes acquisition from presentation, and gives each of the eight operations a bounded request. The owner decision covers design readiness for task generation. Task execution and live budget approval are later decisions.

## Required contract-freeze evidence

- Override the inherited date conversion in core/openbb_core/provider/standard_models/company_filings.py for source acceptance time. The transcript standard is also date-only. Verify public serialization with a non-midnight timestamp, offsets where supplied and timezone uncertainty where absent.
- The root HTTP financial_query_policy.py parses bare integers. The standard transcript query declares quarter as a Literal. Freeze a provider-specific constrained integer or a reviewed narrow admission change. Test valid quarters via actual HTTP and verify zero sends on invalid input through each public surface.
- Assign the Workspace widget type, validation, registry, catalog and storage changes before adapter/UI fan-out. Inspect terminalpro/src/components/Widgets/index.ts, lib/types/app/widgetTypes.ts and utils/zodForms.ts beneath terminalpro/src where applicable. Keep authenticated endpoint-backed acquisition, stale-response protection and saved context. Apply whole-file complexity checks to every shared edit.

This was a read-only design review. Installed behavior, financial responses, consumer rendering and the proposed 36-request budget await the appropriate implementation and owner gates.
