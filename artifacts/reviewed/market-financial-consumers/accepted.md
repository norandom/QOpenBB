# Reusable financial widgets and source pins accepted

Task 5.3 is accepted on 2026-10-30. The native catalog now contains eleven reusable widgets: company profile, income, balance sheet, cash flow, search, peers, daily prices, key metrics, financial ratios, enterprise values and FRED series. The three existing widget IDs and example inputs remain intact. New examples use Microsoft and January 2025 prices; company, series and period parameters remain editable.

The unchanged upstream widget utilities run against the exact local data image built through Dagger from data fork `28423762e8cc3faae978e770899834b41e7cde99`. The bridge gives those utilities an inline view of the financial response envelope, fixing the empty dataKey and missing column definitions found in the initial native generation. Served OpenAPI and frozen route contracts remain byte-identical. Financial field definitions and values are not rewritten.

Source pins and nine consumer snapshots advance together. Dependency manifests and locks are unchanged. Generator provenance binds the native utilities, bridge and financial validator; repeated native generation is identical. Drift is compared with the committed baseline and keeps affected consumers marked for revalidation. See the [independent review and checks](review.md) and [source identities](final-source.json).

This accepts generated contracts and a local generation image. Live provider entitlement, the packaged Workspace journey and published image promotion remain tasks 6.1-6.3. Existing alpha images are unchanged. Main progress: 23/26.
