# Normalized columns and bars design review

PASS for the scoped design amendment, reviewed 2026-10-18 against [the draft](design-draft.md). This is design readiness, not implementation or renderer acceptance.

Applied the design-review gate to approved criteria 4.7-4.9 and 10.1-10.6. All nine IDs have concrete evidence mappings. Boundary, exclusions, allowed dependencies, revalidation triggers and file ownership are populated. The sole mechanical repair expanded abbreviated production paths to their actual subdirectories; the second pass confirms that repair. No blocking issues remain.

The financial contract separates raw observations from normalized geometry, uses max(positive sum, absolute negative sum), preserves missing values and raw formatting, and keeps overview normalization independent of main legend selection. Native signed stacking is an appropriate existing dependency. The horizontal overview deviation is explicit for owner approval, not represented as observed original behavior.

The lifecycle contract is executable through the existing application projection, host and lifecycle owners. Stable column IDs already serve as native series names. Callback, legendScope, options and revision must travel as one accepted request; the current host update forwards only options/revision and therefore needs the stated change. Scope changes reset transient selection, ordinary revisions retain it, failures invalidate export, and disposal prevents revival. No second selection store is needed.

The existing navigator clones main series, so its stated full-source overview seam is necessary. The renderer lane owns that change; the application join supplies the independent projection. Frozen interfaces precede disjoint Sol implementation lanes and the controller join. Whole-file 400/300/50 caps, existing checker/inventory and focused tests are explicit.

The original runtime prerequisite remains mandatory before implementation dispatch: formatter precedence/crosshair, zero/missing domain, legend lifetime and actual miniature outcomes must be frozen. A contradiction or further visible deviation returns for a concrete decision. Browser evidence, export/reopen behavior and breadth status remain planned. No tests, browser sessions or builds were run for this document review.
