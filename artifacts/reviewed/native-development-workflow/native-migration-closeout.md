# Native development migration accepted

All 15 executable tasks in the native-development-workflow spec are accepted on 2026-11-10. Development now uses native Windows tools with Podman Compose for application runtime, Dagger for image builds and native Playwright for browser verification. Historical WSL evidence remains available; WSL is not required for this accepted path.

The [financial acceptance](financial-browser-acceptance.md) records exact application sources/images, execution and request counts. [Independent Astra review](financial-browser-review.md) accepted both financial behavior and migration technical gates. Task 11.3 was committed as `538a822`; the underlying production pins are unchanged from root `0f4a8c9`, with test-only AAP guard correction `e96d0e5`.

| Gate | Observed result |
| --- | --- |
| Native Dagger image export, load and packaged runtime | Both images qualified; actual widget discovery, login and private-file checks passed |
| Financial Playwright | Income, company selection, failure recovery and fresh-login retained recreation passed; 58 FMP/6 FRED attempted sends |
| [Linux CI](https://github.com/norandom/QOpenBB/actions/runs/42845332176) | Portable check entry exited successfully: 459 passed, 12 skipped, one live-provider case deselected |
| [CodeQL](https://github.com/norandom/QOpenBB/actions/runs/42845332580) | Passed on e96d0e5 |
| Source/inventory complexity gate | Final reviewed production pins passed with no errors/violations; no later production edits |
| Owned runtime cleanup | Exit 0; all six sessions stopped, zero owned containers/networks; state preserved |

Cleanup used the checked Compose lifecycle for old failed sessions and checked status for already stopped sessions. Private state and evidence remain under D:/BuildArtifacts/QOpenBB. The owned Dagger engine/cache and unrelated projects were retained. Cleanup receipt SHA-256: `61880b0ed3a2f731532d83e7d62b96c7ebc7bf740718d666021272dbfb352d06`.

Only selected sanitized Markdown is synchronized into reviewed artifacts. Private descriptors, environment files, credentials, databases, financial bodies and raw browser logs remain local. README, developer guidance, roadmap, spec checkboxes and breadth mapping identify the accepted scope.

This closes the development-environment migration. It does not publish these local images, deploy the owner's Linux server, establish every provider endpoint, or complete the analyst-workspace roadmap. Linux CI intentionally skipped image publication. Future product work follows its owning spec and the existing milestone image-build policy.
