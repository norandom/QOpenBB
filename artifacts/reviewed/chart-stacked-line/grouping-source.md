# Original stacked-line grouping identity

Ordinary ordinal categories retain row identity even when their displayed labels repeat. Number and time axes group repeated coordinate values. `projectLineStack` therefore needs the effective category coordinate type rather than grouping every row by its display label.

Confirmed by source inspection on 2026-10-26, without runtime execution. Exact original Workspace is `38dffc33389aca0e4a87e0e88d42f7067aa220df`; the cache identities and hashes are recorded in [original-source.md](original-source.md). Grid below is cached `ag-grid-enterprise@34.1.1@@@1/dist/package/main.esm.mjs`; Charts is cached `ag-charts-community@12.1.1@@@1/dist/package/main.esm.mjs`, both under `/home/mc/.bun/install/cache`. Relevant exact cache snippets were freshly read through WSL. Windows retained dependency copies identify the same package versions and provided navigation into the cache.

## Grid changes the key before Charts groups it

Grid `ChartProxy.transformCategoryData`, lines 41885-41893, maps each row at index `i` to a shallow copy whose category is `{id:i,value:original,toString:()=>valueString}`. The string is `value && value.toString ? value.toString() : ""`. This presentation string is not the grouping key.

`CartesianChartProxy.getDataTransformedData`, lines 42002-42017, selects this wrapping for axis type `category`; `time` calls `transformTimeData`; other types return raw data. `getXAxisType`, 42019-42029, chooses grouped-category for grouping, then time, then number, else category. Explicit `chartDataType` controls the choice; absent it, first datum Date can infer time. `transformTimeData`, 42041-42054, leaves all data alone when the first value is Date; otherwise each string coordinate becomes `new Date(value)` and nonstrings remain unchanged.

Consequences for ordinary, ungrouped Table/File charts:

- Two ordinal rows labelled `A` get different wrapper IDs. They retain separate category bands and separate accumulators even though the labels look identical.
- Numeric coordinates are unwrapped. Repeated numeric values share the same stack key.
- Time coordinates are grouped after the above conversion. Equal Date instants serialize identically and share the stack group. A string time coordinate becomes Date only under the transformation rule above; do not infer grouping from an axis label formatter.

Original Workspace selection/capture and transpose remain authoritative. Grid `getChartUpdateParams`, 45672-45695, supplies `chartDataType` from model category-axis override or original field type. Transpose, 45696-45718, creates one synthetic category row per selected numeric field and distinct series IDs from each former row. These existing transformations must run before projection.

## Charts equality and accumulation

Charts `toKeyString`, 13934-13936, maps object keys to `JSON.stringify(key)` and other keys to themselves, then joins with `"-"`. `DataModel.groupData` uses this string in its group Map (the cached CJS navigation equivalent is 14495-14564). This is serialized equality, not JavaScript object reference equality or a typed Map key:

- The Grid ordinal wrapper serializes its `id` and `value`; its function is omitted. Its unique row ID prevents repeated labels collapsing.
- A primitive number `1` and string `"1"` would collide if both reached grouping raw. Ordinal data never reaches it raw; numeric/time admission determines which primitive values survive. Do not broaden this observation into support for invalid mixed-coordinate inputs.
- Date keys serialize as quoted ISO instants, so equal timestamps match despite distinct Date instances. A raw millisecond number is not the same serialized key as a Date instant. Preserve admitted original coordinate representation when reproducing this boundary.

`buildGroupAccFn`, Charts 29390 onward, iterates series outermost, then every row index within the x-key group; it adds finite values algebraically with one accumulator when `separateNegative` is false. Therefore repeated numeric/time coordinates accumulate all first-series rows before second-series rows. They are not independent rowwise stacks.

Category scale source, Charts 18282-18340 and 18378-18400, deduplicates categories using `Set` on `dateToNumber(value)` and uses a Map for indices. `dateToNumber`, 18200-18202, converts only Date to epoch. Grid wrapper objects retain distinct object identity, so its repeated ordinal rows do not deduplicate. Naked primitive duplicate labels would deduplicate, but that is not the original integrated Grid path.

## Minimal projection contract

Pass an explicit effective category coordinate discriminator, such as `category | number | time`, resolved from existing application axis selection and defaulting to ordinal category for the legacy row-index Cartesian path. No additional state owner is needed.

For category coordinates, use existing ordered row identity/index as accumulator key. For number/time coordinates, group by the processed original coordinate representation, reproducing the exact serialization boundary if matching engine behavior on admitted mixed representations is required. Never key on formatted labels. Preserve each original row and its source values for tooltip/export; grouping determines cumulative geometry rather than aggregating away source observations.

Grouped-category/pivot and cross-filtering behavior was not characterized here and is outside this ordinary ungrouped source conclusion. Invalid-coordinate admission is still owned by existing validation. No new runtime or acceptance evidence is claimed.
