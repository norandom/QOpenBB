# Workspace issuer FCF yield and saved results

Workspace main commit `74a495b929fb2da3facc306d0af887baaf049e49` and the QOpenBB integration pin `aa1a625e5d9478f023226b9ac9acd3bcfb71da4a` have identical widget changes. The underlying QOpenBB modeling service and its v1 bundle retain their prior method and contract versions.

The change enters the dashboard through the existing Widget dispatcher and app-widget catalog. The baseline at `cf344880` used Widget.tsx lines 177–185 for endpoint widgets, AgGridTable.tsx lines 99 and 128–129 for controls, and QueryParams.tsx lines 219–233 for Run and parameter persistence. Issuer FCF yield now sends one explicit authenticated evaluation. The saved-output reader and dashboard refresh use GET. Native widget parameters retain the input snapshot, assumption version, effective date, sign convention and selected run ID. Input edits mark a bound run stale and failed reads expose a service error.

The focused Workspace run passed 79 unit and integration cases. The exact widget-generated body also passed the Python service request contract and authenticated bridge. Cross-repository tests compare native widget declarations to pinned API operations, parameter bindings, output units and saved-output columns. The production change met the 400/300/50 complexity limits; maxima were 395 physical lines, 170 logical units and 36 units in a callable. The production Full runtime frontend built with the frozen Bun lock. Workspace-wide TypeScript checking still reports existing errors outside this feature.

Independent integration review approved the frozen source. Fresh review ran 19 UI checks and four pinned-contract adoption checks.
