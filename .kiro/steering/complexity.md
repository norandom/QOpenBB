# Complexity caps and task planning

User-requested on 2026-10-16 for later task generation. Adapted from the sibling because-security-quant-terminal project's complexity policy; its application-specific architecture limits do not transfer.

## Production code limits

| Metric | Cap |
| --- | --- |
| Physical lines per maintained production file | 400 |
| Logical syntax units per maintained Python/JavaScript/TypeScript file | 300 |
| Logical syntax units per function | 50 |

Physical lines include comments and blank lines; normalize LF/CRLF/CR and do not count a terminal newline as an extra line. Templates, styles, build definitions, and configuration receive physical counts only unless a language-specific logical metric is explicitly defined.

Use the reference project's `project-syntax-units-v1` convention: Python AST statements excluding docstrings, plus lambdas; TypeScript/JavaScript parser statements/declarations and expression-bodied functions. Nested callable bodies are measured separately for function caps but remain in file totals. This measures code size, not cyclomatic complexity or financial correctness. Document supported syntax and parser versions when implementing the checker.

## Scope

- Apply caps to new or modified maintained production code in QOpenBB and its owned forks, including provider adapters, agent services, frontend/Excel changes, and Dagger code. A modified maintained file is checked as a whole, not only its changed lines.
- Unchanged upstream source is outside the initial enforcement scope. Do not turn baseline integration into an unrelated upstream-wide rewrite.
- Deterministically generated widgets/functions, dependency lockfiles, vendored assets, tests, and documentation are outside production size caps. Record generated/vendor exclusions and their source/generator; hand-maintained logic must not hide in excluded files. Generator code remains capped.
- For an oversized upstream file that must change, plan a cohesive extraction/refactor before accepting the change, or record a narrowly scoped, reviewed design exception with its measured baseline and reason. No implicit grandfathering of modified maintained code.
- Split by responsibility. Do not compress statements, create arbitrary forwarding helpers, duplicate state owners, or introduce parallel replacement implementations to pass a counter.

## Required in later tasks

1. Every executable production-code task identifies the affected ownership scope and includes an observable completion bullet requiring the applicable caps to pass. Non-code/generated-only tasks explicitly state why production caps do not apply.
2. Include a foundation task to implement the scope inventory and executable checks before accepting capped feature work. Proposed inventory: `.kiro/complexity-budgets.json`, with repository/revision, feature ownership, maintained paths, and documented exclusions.
3. The design defines component responsibilities; task generation splits oversized work into cohesive units. Each worker receives its task's caps, allowed files, and verified check command along with functional acceptance criteria.
4. Add checks to the same Dagger closing gate used locally and in GitHub. Supply an explicit pinned base/head or changed-file manifest for fork changes; do not assume Git metadata is present inside build containers. Missing scope input must fail rather than silently skip checks.
5. Require per-task size evidence and a final cross-task audit of shared modules. Update breadth mapping and inventory when adding files or responsibilities. Keep the Anthropic-before-Excel dependency and reviewed fan-out lanes intact.

Current state: policy and task-template requirements only. No complexity checker, budget inventory, or implementation task list exists yet. Do not claim enforcement until those checks are implemented and verified.
