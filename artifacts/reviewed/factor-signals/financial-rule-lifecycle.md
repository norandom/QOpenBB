# Financial rule execution and independent verification

Foundation task 5 evaluates preconditions on the supplied snapshot, passes eligible output IDs to the calculator, evaluates invariants and postconditions, and compares candidate values with independent references. The acceptance fixture uses test-only arithmetic. Factor-specific reference formulas belong to factor tasks 12–14.

The fixture withheld outputs affected by a blocking rule and preserved a separately verified sibling. When every output was blocked, the calculator received zero calls. A changed production multiplier produced a reference mismatch and withheld the result. A policy exception retained the failed check and prevented promotion to verified. Reusing verification evidence after changing the snapshot or assumptions failed wire validation.

Review regressions cover a callback claiming that 9 and 1 matched with zero tolerance, a passing callback with no comparison evidence, the recorded explanation for a successful check, and preservation of both operands after an exact-text mismatch. The tests exercise serialization through the frozen ModelRun contract.

Invalid reference values outside the supported scalar bounds produced unavailable evidence and preserved independent siblings. A text mismatch that exhausts the contract's trace capacity raises an explicit error.

Independent financial review approved the changes. The implementation suite passed 431 factor tests. The final portable gate, `bash pipeline/ci.sh check` with pinned Node 24.22.1, passed 992 tests with 13 skipped and one deselected. It staged and imported the runtime modules and checked 814 maintained files with zero complexity violations. Scoped Ruff passed. The base revision was 531d289. This evidence covers offline backend evaluation of supplied inputs.
