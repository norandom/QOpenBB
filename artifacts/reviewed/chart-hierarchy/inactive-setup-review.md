# H1c independent implementation review

VERDICT: APPROVED for inactive hierarchy selection, preparation and pure transitions. No blocking finding remains. This does not establish live renderer/control behavior, storage integration or H4 acceptance.

Reviewed against plan `e666341913dba00bdadab1896daed3310d69772d3ae2dba0966f0f628699ff5b`, starting Workspace `61d1475205bd6bd18799309e674cb6d96494ff15`. The seven exact source/test hashes are frozen in `frozen-files.json`, manifest SHA256 `936301e9033b1e08af2ccc07c659a20770a7e11811f5d55731cb787c54131f94`. Independently checked all seven before and after verification: zero mismatches.

## Verification

- Independent focused run: `wsl -d Debian -u mc -- bash /mnt/d/Source/QOpenBB/artifacts/chart-hierarchy/h1c/reviewerlogs/run.sh`, exit 0. Both suites pass: 7 projection and 6 transition tests, 13 total, one worker. Logs and exit are under `reviewerlogs/`.
- RED inspected: both new suites fail resolving the missing preparation/transition modules before implementation, exit 1; individual tests did not execute. This is missing-export RED evidence, not a behavioral pass.
- Static evidence independently checked: baseline and final logs have identical SHA256 `d724de88c6991f330ad09c549c2703a227e80766d215bff07ff266bc9fb70e0c`. Both retain 3476 inherited TypeScript diagnostics and exit 2. No clean-compile claim; no task-owned diagnostic is introduced.
- Worker scoped formatting/lint passes seven files. Direct source review found no credential literals or placeholders; targeted production TODO/FIXME/HACK/XXX search has no matches.
- Controller inventory-backed combined gate includes all five new production owners, errors 0 and violations 0. Maximum physical size 184, logical file size 84 and callable size 28 meet 400/300/50. Tests remain outside production caps.
- Only five new production modules and two new tests belong to this implementation. Existing H1a/H1b, ordinary/Box setup, session, renderer and control owners remain unchanged. Unrelated worktree paths were preserved.

## Resolved review findings

The initial reducer indexed numeric records without checking own properties. Missing numeric IDs such as `__proto__` could resolve inherited objects, fabricate observations and potentially freeze a shared prototype during deep freeze. The final reducer and weight reader use own-property checks; a dedicated regression covers absent/present prototype-like numeric IDs and confirms Object.prototype remains unfrozen.

The initial transition projected current arithmetic before applying edits, preventing recovery from an overflowing aggregate. Final transitions validate current capture/selection without requiring successful current arithmetic. Dedicated regressions demonstrate aggregate-off and numeric-removal recovery edits. H3 still owns projection and atomic commit of the resulting selection.

The retained-FMP regression initially depended on an ignored root artifact. It now embeds the exact eight retained component rows with provenance/hash information in the owned test, using independent expected revenue totals. Fork tests require no ignored runtime fixture.

## Numerical and boundary assessment

Raw source data and candidate row origins remain detached and immutable. Off/last chooses the last complete-path row; explicit operators preserve endpoints, missing/null distinctions and candidate provenance. Sum starts from the first numeric value; Average starts at positive zero; extrema preserve strict-comparison signed-zero ties. All-missing numerical reductions return null, Count counts rows and gives count units only when aggregation executes.

Canonical tuple identity preserves the owner-approved distinction between missing categories and literal "null", while numeric/string and boolean/string canonical equivalence remains explicit. No-category rows bypass every operator, remain independent unlabeled leaves and retain financial units. Size-selected missing/negative/zero observations have zero weight without rewriting their raw values; deliberate no-size mode assigns one per leaf. Color remains independently retained, including on zero-weight leaves. Bucket and subtree overflow return invalid without partial prepared output.

Stable node IDs, fixed-depth trees and synthetic zero-own-weight parents avoid double-counted internal amounts. The retained AAPL FY2025 fixture reconciles eight USD leaves to quarterly totals and 416161000000 overall; this is numerical fixture evidence, not real-FMP application execution.

Pure transitions preserve unrelated model options and bounds, delete aggregation's own flag when disabled, preserve its inactive state after category removal, enforce roles/numeric cap and return explicit recapture requirements. They neither write storage nor create stamps. H3 retains family/stamp guards, live union narrowing and atomic recapture/project/commit responsibility. No flag or live route was introduced.

No remediation is required. Controller acceptance, evidence sync, documentation/breadth reconciliation and selective commit remain the delivery owner's work. H2 renderer/control and H4 browser, geometry, refresh, export and persistence checks remain outstanding.
