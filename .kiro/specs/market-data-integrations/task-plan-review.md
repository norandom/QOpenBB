# Independent market-data task-graph review

PASS after one repair and the single permitted re-review. The first-batch task graph is executable within its declared scope; no unresolved sanity-review findings remain.

Review date: 2026-10-28. Mode: independent, fresh-context review. Scope: requirements.md, design.md, spec.json, artifacts/market-data-tasks/draft.md, task-generation/parallel rules, and relevant project steering. No implementation or existing-task merge was performed.

## Resolved finding and re-review

1. **Resolved: install the identified candidate before task 5.2 uses it.** The original draft had the following ordering issue: Task 5.1 ends with a committed fork and says to run route/model checks before advancing pins. Task 5.2 then requires ASGI checks against the actual installed first-batch models. Task 5.3, which depends on 5.2, is the first task explicitly owning root source/dependency pins. Neither 1.1's existing baseline environments nor 5.1's committed fork establishes that the service test environment imports the new fork revision. Following the graph literally can test the old installed model set or require unplanned dependency mutation during the runtime join.

   Make candidate source/dependency resolution and installation an explicit preceding controller-owned deliverable, within 5.1 if bounded or in a separate unit. Require evidence that the service environment imports the exact accepted fork and first-batch routes before 5.2. Distinguish isolated candidate resolution from final atomic promotion of source pins, installed-route snapshots and reviewed generated contracts in 5.3. Serialize the dependency mutation and update dependencies accordingly. This implements the approved design's identified installed assembly; it needs no design amendment.

The repaired task 5.1 explicitly prepares an isolated candidate source/dependency lock, serializes resolution and installation, and requires exact fork/import/dependency and installed-route identity checks. Task 5.2 explicitly consumes that environment. Final root pin/catalog promotion remains atomic in 5.3. The existing 5.1 -> 5.2 -> 5.3 edges now establish the required runtime prerequisite without introducing a cycle or new shared ownership. The change remains a bounded controller-owned integration task. Re-review was limited to this repair and its graph consequences; no implementation checks were run.

## Checks that passed

- Shared metadata and failures freeze before dependent FMP, FRED and consumer work. The provider registry and application joins have named controller ownership.
- Dataset restoration is divided by financial responsibility, with explicit enterprise-model/router integration and no blanket activation of retained source.
- FRED disk acquisition precedes memory/in-flight propagation, which precedes generic-series adaptation. Cache freshness and legacy payload/metadata compatibility have observable completion conditions.
- Catalog generation consumes one authoritative projection; policy and mounted error handling have separate writable modules. Shared fixtures, generated artifacts, installs and commits remain serialized.
- Every executable unit has an observable deliverable and applicable complexity treatment. The existing checker is reused through foundation scope/inventory work. The sizes are plausible as bounded adaptations; any whole-file extraction discovered by 1.1 must be split before worker dispatch as the plan already requires.
- Real-provider and packaged consumer acceptance are separate from deterministic fixtures. Entitlement blockers cannot be converted to passing gallery evidence.
- Later DCF, narrative, wider FMP and Yahoo/FRED obligations remain explicitly open. Bounded delivery follows the approved staged design and project delivery amendment; it does not claim umbrella completion.
- Publication and documentation reconciliation follow explicit project delivery rules. They do not add owner-server deployment or AI/Excel implementation.

No requirements/design contradiction requiring RETURN_TO_DESIGN was found. Core steering files product.md, tech.md and structure.md were absent at their configured paths; this review used the supplied spec and available governing steering without inventing their contents. This review establishes task-plan readiness only, not working provider integrations or test execution.
