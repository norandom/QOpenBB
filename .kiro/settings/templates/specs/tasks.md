# Implementation Plan

## Task Format Template

Before generating tasks, read `.kiro/steering/complexity.md` and `.kiro/steering/delegation.md`. Plan the complexity inventory/checker foundation task before capped production work. Add a scope-specific complexity completion bullet to every executable task; for non-code/generated-only work, state why the production caps do not apply. The checker command must come from the implemented toolchain, not an invented command.

Use whichever pattern fits the work breakdown:

### Major task only
- [ ] {{NUMBER}}.{{PARALLEL_MARK}} {{TASK_DESCRIPTION}}
  - {{DETAIL_ITEM_1}} (Include details only when needed. If the task stands alone, omit bullet items.)
  - {{COMPLEXITY_COMPLETION}} (For an executable task: verify applicable 400 physical lines/file, 300 logical units/file, and 50/function caps, or state the scoped exclusion.)
  - _Requirements: {{REQUIREMENT_IDS}}_

### Major + Sub-task structure
- [ ] {{MAJOR_NUMBER}}. {{MAJOR_TASK_SUMMARY}}
- [ ] {{MAJOR_NUMBER}}.{{SUB_NUMBER}}{{SUB_PARALLEL_MARK}} {{SUB_TASK_DESCRIPTION}}
  - {{DETAIL_ITEM_1}}
  - {{DETAIL_ITEM_2}}
  - {{OBSERVABLE_COMPLETION_ITEM}} (At least one detail item should state the observable completion condition for this task.)
  - {{COMPLEXITY_COMPLETION}} (Verify applicable caps for this task's maintained code and record evidence; document any scoped exclusion.)
  - _Boundary: {{COMPONENT_NAMES}}_ (Only for (P) tasks. Omit when scope is obvious.)
  - _Depends: {{TASK_IDS}}_ (Only for non-obvious cross-boundary dependencies. Most tasks omit this.)
  - _Requirements: {{REQUIREMENT_IDS}}_ (IDs only; do not add descriptions or parentheses.)

> **Parallel marker**: Insert ` (P)` immediately after the task number for tasks that can be executed in parallel. Omit the marker when running in `--sequential` mode.
>
> **Optional test coverage**: When a sub-task is deferrable test work tied to acceptance criteria, mark the checkbox as `- [ ]*` and explain the referenced requirements in the detail bullets.
