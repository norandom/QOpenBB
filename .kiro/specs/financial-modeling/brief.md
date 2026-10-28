# Financial modeling repository stub

2026-10-28 owner direction: broad FMP acquisition first; house financial modeling second, in a separate Git repository. This session establishes the specification and repository blueprint only. No remote repository, calculation implementation, deployable stub service or image is created.

## Intended outcome

Financial engineers can extend independently versioned house methods without changing OpenBB provider adapters or duplicating formulas in widgets. Each extension carries executable validation rules and consumer contracts. Agents follow a repeatable Kiro requirements/design/tasks/implementation flow with independent financial review.

Read the [foundation requirements](requirements.md), [repository and extension blueprint](repository-blueprint.md), and [requirements review](requirements-review.md). Requirements are owner-approved. The [technical design](design.md) and [research](research.md) are independently reviewed and ready for owner design approval; no tasks or implementation are authorized by that review.

## Boundary candidates

- QOpenBB retains provider acquisition, catalog integration, Workspace widgets and deployment composition.
- A separate modeling repository owns domain input/result contracts, installed model modules, financial checks, calculation evidence and its service/image.
- FMP DCF remains an optional provider comparison. House DCF uses explicit assumptions and verified calculations.
- The same pattern supports later FRED/EconDB analytical work. No EconDB integration or interchangeability is claimed. Existing accepted FRED work remains intact.
- A three-year historical / five-year forecast company model is a later target, not part of this contract-foundation implementation stub.

The [house-standard reflection](../analyst-workspace/house-modeling-reflection.md) supplies financial-method findings and the earlier FM1-FM10 proposals. This stub develops its boundary and validation requirements; it does not settle the method ambiguities identified there.

## Sequence

1. Complete bounded FMP coverage slices in market-data-integrations, retaining broad family coverage and visible entitlement gaps. An initial endpoint set does not close the whole FMP workstream.
2. Approve this modeling foundation's requirements, then its design and tasks. Identify the first model's required datasets and verify them before its implementation; do not invent a requirement to finish every possible FMP endpoint.
3. Bootstrap the separate repository with the approved contracts, agent instructions and checks. Its name/remote and release coordinates remain unset until repository creation.
4. Deliver house methods in small model-specific specs, with independent financial review and contract-aware consumer acceptance.

This document does not authorize implementing the financial engine in the OpenBB fork or starting Excel work before Anthropic acceptance.

Design including Polars conventions is owner-approved. The [18-task implementation plan](tasks.md) has passed independent graph review and awaits task approval. FMP remains first and the modeling repository remains uncreated.
