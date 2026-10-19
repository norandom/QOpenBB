# Area axis repair review

APPROVED. The final application matches the original six-row axis scales requested by the owner: ordinary area -10/0/10, stacked area -5/0/5/10, normalized area -50%/0%/50%/100%.

The bounded cartesianAxes.ts change applies the existing 1/2/5 scale rule to projected area extents, refits after outward rounding, and reserves category label/tick/title space before choosing numeric density. The reserve accounts for ECharts grid containment using resolved text measurement and rotation, not a fixture-specific constant. Original line behavior, bars and explicit intervals remain unchanged; no financial observations or persisted state change.

Independent review required two corrections. Finite signed +/-1e308 and subnormal inputs initially produced invalid rounded bounds; the area-only finite/positive guard now retains the original finite extent. The first scale repair also used the pre-containment pixel budget and left extra ordinary-area ticks in the browser. The final category-occupancy reserve removes those ticks in the actual application.

Mechanical evidence inspected: scale-layout-regression.log passes 80/80 affected checks; scale-representative-final.log passes 19/19 final native area tests; scoped Biome passes. RED logs demonstrate domain, extreme-value and layout-density failures. Compatibility TypeScript retains baseline typography.ts TS2578 and is not reported green. Final combined caps have zero errors/violations: cartesianAxes.ts is 229 physical lines, 88 logical units, largest function 9, below 400/300/50. Diff inspection found no placeholder, secret or boundary spillover.

The native regression uses an explicitly representative 640x300 source-default layout and checks full mapper output plus actual native grid density. Substituting the browser's 359x284 dimensions into that different synthetic theme/legend setup failed two expectations; that attempt is not passing evidence and was reverted. Actual 359x284 application acceptance comes from the fresh area-layout-final browser run: 1 passed in 86.127 seconds, zero skipped/flaky/unexpected results, one isolated worker. The reviewer inspected all final screenshots and exported PNG; original domains/ticks and corrected zero valley agree. Both sessions have no application exceptions; the known allowlisted datafeed bundle 404 remains.

Reviewed SHA-256 identities:

- cartesianAxes.ts: 0a0b066690e42e8d718ddda6c4942e07f27a30e3e7a5879f3e05d0a318559c74
- cartesian.area.test.ts: 1beabd61078053fec1eb90b5b088be6cb0fee7544639f16ac80f4fde41549730
- join-complexity.json: 305188e3e63e462f98c2c3b37089f4f4aa287088e691cfbdf203ea89b1c12b66
- area-layout-final/browser-results.json: f8914acb1f2bb26e6a1057aa51f9006709d9ac620d50f33e86902f391e00118f

No remediation remains for this bounded repair. Earlier browser runs are superseded. Broader UI-10, mobile parity and release-image acceptance remain outside this verdict.

Publication review: area-layout-final area-default.png, stackedArea-default.png and normalizedArea-default.png contain only synthetic observations and ordinary UI; all three are approved for selective publication with this review. No credentials or private account data are visible.
