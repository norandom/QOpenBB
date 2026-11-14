# Company Research

Open the installed Company Research App to inspect one company, its statements and dated price context, alongside an independent list of candidate peers. This guide describes the bounded local milestone accepted on 2026-11-14; image publication is still pending under task 5.3. See the [runtime review](../artifacts/reviewed/company-research/runtime-acceptance.md) for exact images and limitations.

## Use the App

Choose an explicit current-source listing by company name or Symbol. Profile, Income, Balance, Cash and price share the primary symbol. The statement period links only the three statements; the price window and peer settings are independent. Changing the primary company does not validate the peer set.

Add peers explicitly, record a rationale and reorder them. The peer widget requests periodic metrics and ratios with TTM excluded. Inspect original rows and fields, currency/unit/date basis, provider origin and limitations. A provider multiple without denominator evidence remains unverified; a visible value or apparently similar fiscal period does not establish financial comparability. No house valuation formula, ranking or peer aggregation is supplied.

Refresh observations through the existing controls. Failed or missing datasets should retain their own explained state without erasing unrelated choices. Treat stale evidence as stale. The reviewed evidence distinguishes live source observations from deterministic missing/incompatible/failure fixtures.

Save the dashboard and use template export/import to preserve research choices. An imported unavailable or foreign-source identity remains unresolved until explicitly selected from the current source. Same-symbol recovery is local to each affected widget; it does not broadcast corrected identity through an unchanged symbol group. Exported configuration excludes credentials and provider payloads.

## Accepted scope and evidence

The independently reviewed initial and retained-recreation journeys passed against the same accepted candidate. All 54 required response captures matched (45 initial and 9 reopened). Final cumulative provider usage was 291 FMP of 320 and zero FRED; the accepted attempt consumed 89 requests, including 12 during retained recreation. Twelve extra requested-only entries were not consumed by required capture assertions. The independently reviewed ACL-only correction closed checkpoint custody/content review; historical broader access and the absence of a pre-correction payload hash remain disclosed. No independent initial Workspace inventory snapshot was established. The subsequent [private checkpoint writer](../artifacts/reviewed/company-research/private-checkpoint-writer-review.md) passed separate source and offline verification; it was not part of the executed provider journey.

The initial journey included fresh authenticated reopening; the separate retained phase required a changed API container and restored exact saved choices before validating current observations. Historical failed attempts remain failed. The linked review records exact source/image/test identities, fixture labels, unsupported cases and artifact-permission closure.

Selected source checks passed 509 Workspace tests and 135 supported root tests; the root result includes one skip and three deselections. Whole-repository/typecheck limitations remain qualified in the source evidence. Full IA-B readiness, house modeling, macro integration, backup/restore and owner-server deployment remain separate. The historical [input assessment](../.kiro/specs/analyst-workspace/research-input-assessment.md) is a gap assessment, not acceptance of those broader methods.

See the [task plan](../.kiro/specs/analyst-workspace/company-research-tasks.md), [requirements](../.kiro/specs/analyst-workspace/company-research-requirements.md), [roadmap](roadmap.md) and [documentation index](index.md).
