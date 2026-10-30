# Company selector source progress

Eight of ten tasks are accepted as of 2026-10-30. The existing FMP widgets now have linked Company name and Symbol controls in source. Packaged real-data, save/reopen and retained-state acceptance remain open; these changes are not yet published in images.

The selector reuses the connected data API, native widget execution, original Profile comparison editor and dashboard groups. It applies only to the eight approved immediate FMP definitions. Period/Limit, raw Symbol correction and ineligible/manual-run controls remain available. Selecting an unchanged symbol updates listing metadata without requesting financial data again.

The joined six native suites passed **287 cases**. Portable schema/catalog checks passed **157 cases**: 156 initially, then the one case blocked by a missing Node path passed after the existing pinned toolchain was exposed in the clean snapshot. The generated widget contracts agree with the eight selector bindings; the data API and generator source are unchanged. Metadata stays beside parameters in storage and outside financial requests.

The exact-source size gate passed **680 maintained files**, with no errors or violations. QueryParams measures 993 physical lines, 364 logical units and a maximum 38 units per function, within its owner-approved 1000/390/50 exception. Other changed production code retains 400/300/50 limits.

CI41088351983 exposed an evidence defect: the local gate had minified the inventory while its committed form contained404 lines. This supersedes the earlier task5.2 full-gate conclusion. Removing seven blank lines preserves the JSON exactly and brings the inventory to397 lines. The corrected check measures exact inventory bytes. [Source join review](task6-review.md) records the failure and repair; [source identities](source.json) bind the accepted inputs and corrected receipt.

| Accepted scope | Independent review |
| --- | --- |
| Contract and inventory foundation | [Contract](task1-review.md), [scope correction](task1-inventory-review.md) |
| Connected search and pure group guard | [Search](task2-review.md), [group safety](task3-review.md) |
| Selection lifecycle and paired controls | [Lifecycle](task4.1-review.md), [controls](task4.2-review.md) |
| Reactive groups and native header | [Group context](task5.1-review.md), [header](task5.2-review.md) |
| Source/catalog join and exact-byte gate | [Join](task6-review.md) |

Next: extend the existing financial browser case, build the packaged candidate, and verify real FMP selection with independent group/FRED sentinels and saved state. Full native TypeScript/build remains unverified under the reused dependency cache; unit tests do not replace that application gate. See the [task plan](../../../.kiro/specs/analyst-workspace/company-selector-tasks.md).
