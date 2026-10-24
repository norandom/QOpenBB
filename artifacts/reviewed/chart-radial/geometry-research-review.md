# Independent analytical Column review

APPROVED after the numerical-bound remediation recorded below, for a bounded RC0G geometry foundation task. The original all-finite contract was rejected; the revised supported plot-pixel contract resolves that finding. Review date: 2026-10-24. Typed production transfer still requires its own independent review and maintained-scope gate. This does not accept the Radial mapper, family activation or all of RC0.

## Remediation acceptance

Independently reread the frozen revision: every numeric geometry input must be finite and have absolute value at most 1,000,000 plot pixels, in addition to the existing structural radius/width constraints. Larger values throw RangeError; they are not clamped. This explicit programmer limit prevents overflow in the helper's squared circle intersections without changing supported viewport geometry.

New reviewed SHA256 identities:

- geometry.cjs: `671f92739f4314776374db64440bf33f3551e2cbebc832469766ff29060ca563`.
- contract.cjs: `694f0f4fbe71723a86ea60f37af5af35e1cb897dfce56cc2b36665172f7bd563`.
- report.md: `3fddd7c55e0d47dcb0814b375a0266596570c03cb7fd906eedbe851a9f4200ec`.

All nine updated evidence hashes match. Fresh contract and actual-path reruns exit 0: twelve invalid inputs rejected, exact-bound connected path finite, 18 cases/187,272 points/zero fill mismatches and zero zero-stroke differences. Independent added probes also verify finite output when outer radius, endpoint and width equal the maximum, and rejection when each of the five numeric fields individually exceeds the maximum. Output writes were intercepted to preserve frozen evidence. Fresh syntax measurement is 47 logical units, maximum function 36, within caps.

The numerical finding below is retained as historical rationale and is resolved. Proceed with the exact geometry-only ownership boundary below, carrying the 1,000,000-pixel limit into the typed interface documentation, invalid-input regression and caller error contract. No family or financial semantics are added by this approval.

## Fresh evidence

Read geometry, cases, oracle, runner, contract assertions, report and output evidence. All nine hashes in `hashes.json` match. Key identities:

- geometry.cjs: `b27d841ab11756b84e3bb60abc6df98fd89bd85e6ea02a1bf1c308d2ace9050b`.
- report.md: `f6cb55087ce0de020f25853de4bf2249ead938ae7d3c9a5899af5675ea343c68`.
- checks.json: `b874db431fba4b2be5cc11c0e3828a2c56dd66ade71f9f6f2970951ba2399c32`.
- comparison.svg: `207da458942360d77a818e302ebd2225be89f023c2cb012212980fc746f279be`.

Fresh pinned-Node execution of the unchanged `run.cjs` and `contract.cjs` exited 0. Intercepted only output-file writes in memory to preserve frozen artifacts. Results reproduce 18 cases, 187,272 offset-grid samples, zero fill disagreements, five zero centerline-stroke cases with zero differences, and nine invalid inputs rejected. The actual ECharts display-list paths, including their transforms, are used in the fill comparisons. This is stronger than the first spike's envelope-only comparison.

Fresh SVG parse: 780 by 1500, 18,252 bytes, 36 path elements, no standalone NaN/Infinity. Fresh existing syntax checker: geometry 46 logical units and largest function 36; the reported physical count is 55. Geometry is within 400 physical / 300 logical / 50 function caps before typed transfer. No production gate or browser acceptance is claimed.

## Required numerical remediation

Important: the validation accepts finite values whose squares overflow. Independently executed:

```js
columnPath({
  startRadius: 1e200, endRadius: 1.5e200,
  holeRadius: 1e200, outerRadius: 2e200,
  width: 1e199, connectBaseline: true
})
```

This passes every current precondition and returns a path containing NaN coordinates. The cause is `outerRadius**2 - radius**2` and similar calculations producing `Infinity - Infinity`. Real chart viewports will ordinarily be much smaller, but the proposed exact finite-input contract currently promises more than the helper provides. This matters at the programmer boundary and is cheap to resolve without changing family behavior.

Before production dispatch, explicitly restrict the supported numerical range to safe plot geometry or use overflow-safe circle intersections and guard all derived coordinates. Add a regression establishing rejection or finite correct output for the counterexample and a boundary case for the chosen numerical policy. Update the contract accordingly. Do not silently manufacture zero coordinates or silently clamp an invalid viewport. The independent runner's success above remains valid for its actual bounded cases.

## Approved responsibility boundary for RC0G

Once that numerical condition is explicit, the pure helper can be materialized independently as `echarts/radialColumnShape.ts` with exactly these responsibilities:

- Input: directed start/end radii, hole/outer plot radii, width and explicit baseline-connection flag, subject to the stated safe numerical preconditions. Input/output units are plot pixels.
- Output: local upward-facing path string and explicit zero flag. No translation, rotation, style, series, axes, data, normalization, missing treatment, aggregation, legend or session state.
- Caller duties: decide baseline connectivity from the original contract, filter missing observations, resolve finite pixel geometry, transform the local path and set zero fill to none while retaining appropriate stroke options.
- Errors: reject invalid programmer geometry visibly through the existing adapter error boundary; do not swallow RangeError and draw a misleading empty chart.

The helper is independently expressed through strip/circle intersections; it imports no original code and owns no financial rules. The explicit flag is deliberately broader than the source's usual width threshold, so the caller must retain the source decision. Reversed axes and out-of-plot endpoints remain outside this contract. The normalized-missing owner decision cannot affect this pure finite-pixel function and therefore need not block RC0G once its own input contract is frozen. It still blocks affected family activation and RC0 acceptance.

## Retain meaningful checks and limits

Keep the exact split arcs through the baseline's vertical extremum; their separation addresses a measured ECharts containment failure. Do not simplify them merely because one arc is geometrically equivalent. Preserve inward segments, outer shoulders, flat stack seams, threshold fixtures, rotation, zero hole, hole ratio one, thin and wide cases.

Production tests should import the production helper, assert independent known boundaries and actual ECharts containment, and retain zero-open/unfilled and invalid-input assertions. The retained AG oracle is useful independent research evidence; it must not become a runtime dependency or a generic decoder. If production tests use reduced frozen expected hit points, select points on both sides of the branch boundaries and preserve the failing arc-split regression. Include the overflow contract test. Avoid asserting only path command counts.

The zero-stroke comparison reparses the original numerical path through ECharts; it checks sampled centerline agreement, not independent AG Canvas stroke rendering or complete stroke-region/dash equality. Nonzero fill comparison does use AG's own numerical containment as its independent oracle. The current grid is sampled evidence, not mathematical equality of exact arcs, AG cubic approximations and rendered pixels. Browser tooltip picking, dashed borders, appearance, grouped widths, single-category placement, axes and persistence remain separate obligations.

The controller must freeze the production file and focused test ownership, inventory update and commands before dispatch. Require independent production review and fresh maintained-scope verification after typed transfer. No shared routing or activation belongs in RC0G. Only this ignored review file was written; no browser, build, install, production edit or commit occurred.
