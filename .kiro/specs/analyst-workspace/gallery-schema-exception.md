# Preserve sparse chart-family selections on first open

Proposed bounded correction, 2026-10-28: change only the `cellRangeCols` record constructor in `terminalpro/src/lib/types/app.ts` so native parsing preserves absent chart-family keys. Keep chart vocabulary, selected column arrays, explicit nullish values and all other widget schema behavior unchanged.

The first-open gallery currently acquires own undefined entries for absent chart families. The integrated chart-state validator rejects those entries, so a native Custom Combination edit silently retains the previous series type. Saving and reloading drops those entries through JSON serialization and permits the same edit. The correction belongs at schema parsing; weakening the chart validator or requiring a reload would leave inconsistent application state.

The existing file has 927 physical lines and an accepted exception for the Sankey vocabulary addition. Extend that exception solely for this additional one-line sparse-record correction, with no physical growth and the existing 2026-11-27 expiry. The 300 logical-unit and 50 function-unit caps remain enforced. A wider schema extraction is disproportionate to this isolated constructor correction and is not covered here.

Acceptance requires independent review of the exact diff, a regression that fails before the correction and passes afterward using native schema parsing and chart editing, checks that explicit supported entries and invalid chart names retain their intended behavior, and fresh whole-file size measurements. The packaged application must accept the first edit without save/reload before the user-facing issue can be closed. This document does not itself establish source or runtime acceptance.

## Source acceptance, 2026-10-28

Independent review approved fork `d6208dd3d44e46760d39c80da47c0b681b91e151`: exactly one `.record` to `.partialRecord` substitution. The focused native-template suite failed two new assertions before the correction (15 existing tests passed), then passed all 17. Explicit nullish selections remain supported; unknown family keys and numeric column entries remain rejected. Native integrated reduction retains the area edit and EPS secondary axis. The integrated validator is unchanged.

Whole-file measurements remain 927 physical lines, 144 logical units and maximum function size 16. The accepted physical exception is therefore extended to this correction, with the same expiry. The two changed source/test files pass scoped Biome and whitespace checks. The new bounded persistence browser test received separate independent source review; runtime execution is still required. Detailed local evidence is retained under `artifacts/historical-gallery/first-mount/`.
