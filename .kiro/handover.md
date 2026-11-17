# QOpenBB session handover

Updated 2026-11-17. Active work is the reviewed FMP expansion plan and Batch A design described below. The bounded Company Research milestone remains complete: 13 executable tasks accepted, all 29 requirements mapped, and publication independently verified. No further build or provider run is needed for that milestone.

## Active FMP expansion

Seven shared prerequisite tasks and 2 offline adapters are accepted (9 of 26 tasks). Accepted adapters: historical_market_cap, analyst_estimates. Latest API commit e79eb68b82dc8f0a8f62602b28e0e16cc424e937. See [task evidence](specs/market-data-integrations/fmp-expansion-a-tasks.md). SDK/HTTP admission and the explicit allow_empty acquisition correction are independently accepted; shared interfaces remain frozen. Continue the approved two-lane adapter queue. Production registration, native result/discovery joins, live/browser verification and publication remain pending. No live Batch A requests have been used.

The owner requested substantial FMP endpoint coverage alongside the financial-modeling input/bootstrap plan. The [reviewed plan](specs/market-data-integrations/fmp-expansion-plan.md) names 24 additional candidate operations: A11 financial/valuation, B8 events/content, C5 DCF/as-reported. The [inventory](specs/market-data-integrations/fmp-expansion-inventory.md) distinguishes 19 retained-adapter candidates, five new-contract candidates and the unchanged ten-model baseline.

The [Batch A design](specs/market-data-integrations/fmp-expansion-a-design.md) and [26-task plan](specs/market-data-integrations/fmp-expansion-a-tasks.md) are owner-approved as of 2026-11-17, including the 48-request ceiling. The independently reviewed task artifact had SHA-256 `dad09e093184ef53a53ceecc569ed4b4e8119358f20e82d51c47087957fcadea`; later status/checkbox updates do not change that approval record. Execution has started with source/complexity setup; two characterization groups, one contract freeze and public input-admission prerequisites precede eleven disjoint adapters. Registration, exact-source runtime, live/browser verification and actual milestone publication follow. Preserve existing native SDK provider resolution versus explicit REST provider selection; use the reviewed admission addendum, preserving the oversized CommandRunner.

Use `D:/BuildArtifacts/QOpenBB/fmp-expansion-a/root` and sibling `data-api`, both on `work/fmp-expansion-a`. The planning/approval commit is `4a85a27`; unchanged Workspace source is at `D:/BuildArtifacts/QOpenBB/company-research/workspace`. Preserve the completed Company Research source/runtime/evidence and unrelated canonical work. New raw task evidence belongs under `D:/BuildArtifacts/QOpenBB/fmp-expansion-a/evidence`; earlier planning drafts remain under `D:/BuildArtifacts/QOpenBB/fmp-expansion-planning`. Approved allocation: 22 direct/native, ten contrasts, eight browser and eight shared diagnosed reruns. Freeze the exact matrix and initialize its ledger before candidate startup; every unexpected startup, failure or background request counts. Do not reuse the historical Company Research ledger.

The separate modeling foundation retains its approved 18-task plan. Repository coordinates and selected-method input/definition gates remain open; proposed repository name is `qopenbb-financial-modeling`, not an owner decision. No new repository was created. Full FMP completion, DCF and FRED/WACC are not prerequisites for a narrowly selected historical cash-conversion method.

## Published milestone

- Release: [alpha-43604526965-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-43604526965-1).
- CI run: [43604526965, attempt 1](https://github.com/norandom/QOpenBB/actions/runs/43604526965). Both candidate and publish-alpha passed after one dispatch.
- Release source: root `fbd81eaf11d82b47043592f60736009304f198c8`; Workspace `bf180ef506286886da224df9ff184cd1ace2397e`; API `a965f70c164fe477ce9c99654b9be48e2f1bc9fd`. The later documentation-only closure does not change this build identity.
- Workspace source is available on `qopenbb/company-research`. The unchanged API source remains remotely reachable on `qopenbb/statement-period-provenance`.
- Three public assets and six anonymous digest/tag/latest image pulls passed. The public environment asset is `default.env.sample`; installation instructions save it locally as `.env.sample`.

See [Company Research](../docs/company-research.md), [publication review](../artifacts/reviewed/company-research/publication-review.md) and [final integration review](../artifacts/reviewed/company-research/final-integration-review.md). Publication review SHA-256 is `0d6e2258ac66cb03bae66c5190bd31d55103f1b0479136e29ccc36b57782ccd4`.

## Verification and limits

The local packaged financial journey, export/import, explicit foreign-source recovery, fresh authentication and retained-directory recreation passed at root `4736c31` and browser hash prefix `c9a267`. Its local image pair differs from the CI rebuild. Publication checks establish the public images' identities and accessibility, not a second financial browser run against those bytes.

All 54 required captures matched. Cumulative usage was 291 FMP requests under the reviewed 320 ceiling, zero FRED and zero denials. Twelve additional requested-only entries were not consumed by the required capture assertions. Failed attempts and their cumulative ledgers remain preserved externally.

The checkpoint's ACL/content review is closed. Historical broader access, absence of a pre-correction payload hash and absence of an independent initial Workspace inventory snapshot remain disclosed. Future checkpoint creation now uses the checked private writer; this separate post-run harness change passed 39 tests with one existing platform skip and six independent checks.

Source verification passed 509 joined Workspace tests and 135 supported root checks, with one skip and three deselections; the separate peer-adapter suite passed ten tests. Final complexity covered 741 files with zero violations. Release CI passed 461 tests, with 12 skips and one deselection. Existing unrelated compiler/chart/schema baseline failures are not declared green. Full IA-B, house modeling, validated rankings, live macro coverage, backup/restore and owner-server deployment are outside this milestone.

## Checkout continuity

The clean published implementation checkout is `D:/BuildArtifacts/QOpenBB/company-research/root`; the corresponding Workspace and API checkouts are sibling directories. Release evidence and private failed-run records remain under `D:/BuildArtifacts/QOpenBB/company-research`.

The original `D:/Source/QOpenBB` checkout remains on its prior source commit with pre-existing dirty inventories/catalog work and `.openidea/` preserved. Only reviewed feature metadata, documentation, sanitized evidence and this handover are synchronized there. Do not reset, blanket-checkout, stash or overwrite unrelated work to make it resemble the published checkout. Use the isolated checkout or the tagged release for the accepted implementation.

Company Research requires no further implementation. A follow-on workstream needs its own explicit scope; do not infer authorization to implement house modeling, AI/Excel or server deployment from this completed milestone.
