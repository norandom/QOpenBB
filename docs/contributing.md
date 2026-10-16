# Contributing

Make each contribution easy for a financial engineer to review: state the result, identify the data or runtime contract it affects, and supply evidence that could expose a wrong assumption. Read [AGENTS.md](../AGENTS.md) and the owning specification before changing scope or implementation.

## Work within the approved phase

Requirements, design, and tasks each require human review before the next phase. Check [spec.json](../.kiro/specs/openbb-self-service/spec.json) and keep acceptance criteria in the [requirements](../.kiro/specs/openbb-self-service/requirements.md), rather than inventing a second checklist in the docs. Research can narrow uncertainty without implying implementation approval.

Application source belongs in the owned [Workspace](https://github.com/norandom/openbb-workspace) and [data API](https://github.com/norandom/openbb-data-api) forks. Record revisions and adaptations. QOpenBB coordinates their contracts, delivery, documentation, and verification. Preserve upstream licenses and notices.

For design or code work, load [complexity](../.kiro/steering/complexity.md), [testing](../.kiro/steering/testing.md), [CI](../.kiro/steering/ci.md), and [delegation](../.kiro/steering/delegation.md) steering. Future tasks must establish executable complexity checks, not just repeat the caps. Read the [documentation policy](../.kiro/steering/documentation.md) for prose and code comments.

## Write for the next decision

Lead with what the reader can do or conclude. Put the reason and evidence beside the action; link detailed source research instead of repeating it. Assume the reader understands financial engineering, and explain project-specific conventions such as which backend owns authentication or which period a dataset represents.

Separate observed behavior, proposed design, and untested assumptions. For an experiment, state what would invalidate the claim. A useful entry is: "The direct FRED request returned GDP observations; the self-hosted API and Workspace journey remain untested." A statement such as "FRED works" hides the boundary that a reviewer needs.

For financial-data contracts, document applicable period/date conventions, units, currency, frequency, missing-value behavior, provenance, and entitlement limits. State transformations explicitly, with a source or formula and a reproducible comparison where relevant. Do not infer financial correctness from an HTTP status or a rendered chart.

## Put rationale beside the code

Comments should explain a financial constraint, a non-obvious decision, a failure boundary, or an invariant that a future edit could break. Names and code should explain routine mechanics. Keep a comment next to the decision it governs; link a durable spec section when the rationale needs more space.

Illustrative comments, not implemented behavior:

```python
# Preserve the provider's fiscal period; calendar-year relabeling changes comparisons.
# Keep a missing observation distinct from zero so growth rates remain meaningful.
```

Avoid comments such as `# Loop through rows` or a COBESY rubric on every function. When a contract changes, update or remove the old explanation. Comments count toward physical production-file limits.

## Report verification precisely

Record the command, source revision or image digest, exit code, and artifact path. Link actual checks and evidence in [.kiro/breadth.toml](../.kiro/breadth.toml). Report failures, skips, and untested paths explicitly. A parser check, static import scan, or provider probe supports only the boundary it exercised.

Use synthetic fixtures or disposable accounts for ordinary tests. Real credentials stay in ignored `.env`; [.env.sample](../.env.sample) stays empty. Keep secrets out of snippets, browser artifacts, source contexts, image layers, and diagnostic output. Never read or copy credentials into documentation.

## Keep navigation current

Add or move reader-facing pages through [docs/index.md](index.md). Keep the README focused on purpose, status, operating constraints, and entry points. When evidence changes, update the owning report and breadth map first, then revise summary claims and roadmap gates. Add an executable startup or deployment runbook only after its commands have been exercised against the recorded baseline.
