# Sankey data and presentation source acceptance

SK1 and SK2 are independently accepted on 2026-10-27. They remain inactive until the Table/File application join; this record does not establish browser, appearance or release acceptance.

- Data source: `b146da6b0f248d039aad14d3e5c29313edac01c5`. Independent Astra review verified 27 graph and 6 capture checks, read-only lint and unchanged inherited typing diagnostics. Typed identities, duplicate-link provenance, metadata conflicts, invalid/zero/cyclic input, finite aggregation and internal-node reconciliation are covered. A recorded zero counterpart remains distinct from an absent counterpart and produces the appropriate imbalance warning.
- Presentation source: `5190f5f1764d2a26117cf1b4eeb2d47fbc00d2a8`. Independent Sol review verified 16 renderer and 5 setup checks, read-only lint and unchanged inherited typing diagnostics. Native ECharts SVG checks cover financial widths, escaped tooltips, subnormal values, compact layouts and recovery. Internal layout normalization preserves the retained financial values; an unrepresentable positive ratio produces an explicit diagnostic.
- Both lanes pass the existing combined complexity gate: no errors or violations against 400 physical lines, 300 logical units/file and 50/function. The largest new file is 274 physical lines. Initial review findings and their failing regressions remain in local evidence.
- The retained financial example has 12 links from AAPL FY2025 revenue to quarterly cost of revenue and gross profit, in USD at scale 1. The annual root of 416,161,000,000 is a derived sum. Links are income allocations, not cash flows or links supplied by FMP. SK0 independently verified the retained records and quarterly identities.

Next is the existing editor integration: selection, recoverable diagnostics, theme controls, refresh, saved mappings and PNG export. A real-FMP application journey, owner appearance review and completed-milestone publication remain open. No new images were built for these inactive modules.

Evidence identities (SHA256):

- Data review: `6381a8481e5394504ce583a51565837f8834cad4829ff45f1e3b6a2f3e5a6e0f`.
- Presentation review: `95c6c72e6881b9e5031bacc84c19a9ca5f6e293bd4c30cd598bc1ec198f0ad81`.
- Combined size report: `4b0389866902a40beca85e75f98360243a892a193a2e374ecc72015d8ee42f5d`.
