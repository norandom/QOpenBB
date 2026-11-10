# Inventory split amendment

Owner-approved controller-owned addition to task 2 (2026-11-10). The native entry implementation has passed independent review, but its combined gate fails because the central inventory grows from 398 to 410 physical lines. The three new production files themselves pass their limits.

## Change

Extract the complete Workspace repository inventory object into `.kiro/complexity/workspace.json`. Keep limits, exceptions and the other repositories in `.kiro/complexity-budgets.json`. Add a one-level repository reference to the root inventory; existing inline repository objects remain supported.

Extend the existing inventory reader in `tools/quality/scope.py` to load that reference. `tools/quality/exceptions.py` and the portable `pipeline/qopenbb_ci/quality_cli.py` entry use the same reader so all consumers see identical resolved configuration. A reference is confined to the repository, cannot traverse a symlink or escape the root, and cannot recursively include other files. Missing, malformed or ambiguous references fail closed. Existing duplicate repository, source-lock, ownership and exception validation remains authoritative.

The extracted JSON remains maintained production configuration, explicitly inventoried and subject to the same 400-line cap. No size limit, financial assertion, runtime behavior or test obligation is relaxed. No new checker framework or size exception is introduced.

## Ownership and verification

A bounded Sol implementer owns the loader change and focused existing inventory tests. The controller owns the configuration extraction and selective staging. Independent Astra review checks the new loading boundary and unchanged enforcement.

Verify equivalent inline/referenced inventory results, missing/invalid/escaping/reparse/recursive references, duplicate repository rejection and consistent exception resolution. Run the existing combined gate against the exact accepted source plus task 2 changes. Do not modify or absorb unrelated renderer/inventory edits; retain their semantic delta and stage only the reviewed split and native additions.

## Task integration

This is a prerequisite completion within task 2's controller-owned inventory integration, covering existing requirements 6.4 and 5.4. Task 2 remains unchecked until its implementation, split and combined gate are accepted. The remaining task graph and approvals are unchanged; this amendment does not start another application workstream.

## Review basis

Independent Astra investigation confirmed that no supported include mechanism or redundant mapping can fix the current gate without changing its loading contract. A metadata-only exception is also incompatible with the existing maintained-tree exception rules. The recommended split preserves the rules and avoids formatting changes intended only to evade the counter.
