# Role-based models and bounded fan-out

2026-10-19 owner amendment: [prototype-first delivery](delivery-workflow.md) replaces whole-spec phase gating with bounded agile slices. Role models, independent review and Anthropic-before-Excel remain. Successor feature lanes must not delay deployment.

User-requested policy, 2026-10-16, adapted from ../because-security-quant-terminal/AGENTS.md and its terminal-control-surface/parallel-execution-proposal.md. The reference project's historical task approvals and run budgets do not transfer.

## Team and models

| Role | Model | Responsibility |
| --- | --- | --- |
| Controller | Current parent model | Contracts, dependency queue, joins, status, heavy-check queue, selective commits |
| Bounded implementer / routine reviewer | gpt-6.1-sol | One well-defined task per worker; focused evidence |
| Architecture / difficult integration / financial review | gpt-6-astra | Independent review of hard contracts and failure modes |
| Mechanical auditor | gpt-6-luna | Inventories, mapping and documentation checks; no sole acceptance of complex behavior |

Use at most four active slots: controller + up to two independent implementers + one reviewer/auditor. Free a slot when a task needs a fresh independent reviewer. Model overrides require fresh-context dispatch (fork_turns=none); pass exact task/spec references, boundaries, commands, and acceptance criteria. If a requested model is unavailable, report the fallback rather than claiming it was used.

## Execution rules

- Freeze shared interfaces before fan-out. Each lane has explicit prerequisites, exclusive writable paths, outputs, and join criteria in the reviewed task plan. A (P) label alone is insufficient.
- One bounded task per worker; independent tasks may run concurrently. The controller owns shared contract edits and serializes coupled work. Stop affected lanes if ownership overlaps or contracts change.
- Pass the task's applicable complexity caps and inventory scope from complexity.md to each worker/reviewer. Fan-out does not relax file/function caps or the final shared-module audit.
- Each task retains implement -> independent review -> fresh verification -> acceptance. A reviewer must not rubber-stamp the implementer's report. Keep exact evidence/revision references.
- One heavy build/suite at a time, with up to three independent verification processes only under testing.md. Serialize installs, shared fixture mutations, integration gates, and commits.
- Freeze worker edits before selective staging/commit. Never commit another lane's unfinished work; preserve unrelated changes.
- Phase approvals remain requirements -> design -> tasks -> implementation. This delegation request authorizes the workflow policy and independent research, not automatic approval of future runtime tasks.

## Intentional local workflow override

For QOpenBB, this explicit user-requested policy supersedes kiro-impl's sequential-only iteration and informational-only (P) defaults when the reviewed task plan defines independent lanes. It does not waive per-task review, dependency checks, evidence, or parent-owned commits. Without a lane plan, run sequentially. Cross-spec review uses gpt-6-astra rather than the older model named in the generic kiro-spec-batch text; this project policy is the override.

## Proposed lanes and joins (not implementation approval)

1. Research/design: Workspace/HTTP routing and data/provider contracts can be investigated independently; reviewer checks seams and sources.
2. After contract approval: data API/FMP/FRED work and Full Workspace adaptation may run in separate owned forks. Join at real dashboard discovery, data, save/reopen, and bind-state checks.
3. Dagger/release work may overlap application tasks only after source/image/runtime contracts are frozen and files are disjoint. A publishable release waits for its acceptance gates.
4. Anthropic agent implementation and independent review follow the dashboard contract; join at actual Workspace discovery, model access, streaming, selected-data answer, and failure recovery.
5. Excel implementation is BLOCKED until Anthropic acceptance. Excel may not be started as a spare parallel lane. Afterward regenerate functions and verify Office/Cloudflare Access behavior against the frozen API.
6. Final pull-only Linux deployment, origin HTTP routing, Cloudflare Access client behavior, and backup/restore are controller-owned integration gates.

No Jupyter, notebook image, or wheel-distribution lane. PostgreSQL integration remains deferred.
