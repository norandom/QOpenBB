# Periodic query provenance design review

APPROVED for owner design review and bounded task generation. This verdict does not authorize implementation or establish runtime acceptance.

- Reviewed draft: `artifacts/research-metadata/ttm-design-draft.md`
- Exact SHA-256: `9b5f25df813aaa5f203b5a8248bd32d1b38580c17a2c20b15fb73f5b949217c1`
- Review date: 2026-11-06
- Independent review scope: the three-file metadata repair, its contract migration, and existing verification/source/catalog/release seams.
- Production API baseline: `28423762e8cc3faae978e770899834b41e7cde99`; local fork HEAD matches and its worktree is clean.
- Gate: `.agents/skills/kiro-spec-design/rules/design-review-gate.md`
- Review passes: 1; repair rounds: 0. Blocking findings: none.

## Mechanical gate

The approved requirements contain 44 numeric criteria. The existing approved `market-data-integrations/design.md` contains every numeric ID. This amendment expressly preserves that design and narrows its new decision to 4.1, 4.2, 4.3, 6.1, 6.2 and 6.3, with 4.4 through 4.7 and 7.1 through 7.2 as constraints. All twelve scoped criteria are represented, expanding the written ranges.

The literal ID scan finds these absent from the amendment: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 3.1, 3.2, 3.3, 3.4, 3.5, 4.5, 4.6, 4.8, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6.4, 6.5, 7.3, 7.4, 7.5, 8.1, 8.2, 8.3, 8.4 and 8.5. Criteria 4.5 and 4.6 are covered by the explicit range; the others retain their approved base-design coverage. This is an amendment, not a replacement design, so these are not new coverage gaps.

Boundary Commitments, Out of Boundary, Allowed Dependencies and Revalidation Triggers are populated. The file plan names the three production files and existing focused/core/native/live verification files. Source-lock, generated contracts and documentation remain controller-owned join responsibilities; the draft requires task generation to freeze exact selections and source checks. No new component or adapter lacks an implementation home. No placeholder production component or independent responsibility is introduced.

## Source and architecture findings

1. The source diagnosis is correct. Core `financial_metadata.py:13-19` omits `ttm` from `QUERY_PARAMETERS`; its validator at lines 167-179 rejects unsupported keys and applies existing public-value checks. `key_metrics.py:44` and `financial_ratios.py:45` already enforce `Literal["exclude"]` with the same default. Their effective-query dictionaries at lines 125 and 126 omit the selector. Both upstream request dictionaries remain limited to symbol, period, limit and the private API credential.
2. Adding the safe key in core and emitting each validated `query.ttm` is a cohesive three-file repair. It preserves provider-neutral core validation and avoids raw-argument echoing, a second default table, TTM acquisition, synthetic rows and financial calculations.
3. The schema-version 1 decision has an explicit migration. Generic dictionary consumers can accept the new entry, while the older strict core validator rejects it. Shipping matching reviewed core/provider revisions and documenting that migration satisfies the amendment's 6.3 obligation; the draft does not claim older strict-validator compatibility.
4. Generated discovery already exposes the selector. The inspected `contracts/openapi.json` metrics and ratios operations each declare `const` and default `exclude`; both matching entries in `contracts/widgets.json` declare the same option/default. A new schema definition or UI component is unnecessary.
5. Production file sizes match the draft: 193, 140 and 141 physical lines. The design requires the existing checker against all modified production files, explicit fork scope and the 400 physical / 300 logical per file / 50 logical per function limits. It correctly reuses the accepted checker foundation rather than treating policy text as enforcement.

## Execution readiness

Acceptance is concrete: default and explicit exclusion in annual/quarter modes, unchanged source request routing and result values, rejected unsupported modes before transport, retained unsafe-key/value rejection, and the selector in the native result envelope. Existing focused tests and the named canonical pytest harness provide implementation locations. Source and installed-package identity precede behavioral acceptance; the source/catalog join precedes packaged acceptance and the single milestone pipeline.

The source pin, reviewed generator inputs, preserved widget identities, four-call live bound, historical receipt separation and once-per-feature image pipeline are explicit. Task generation must retain the already stated exact test/install/source checks and scope the generated-output paths and migration documentation before implementation. These are task elaboration details, not missing architecture or a reason to reopen requirements.

The accounting sanitizer/assessment correction remains separate under its existing approved work. Balance/Cash annotations, the four unrelated catalog/inventory files, house calculations, UI, AI and Excel are outside this repair. No broad API research, new verification framework, provider requests, installs, builds or test execution were necessary for this design review.

## Limits and next gate

This is a static design verdict against the exact draft and local source baseline. No repaired behavior exists yet, and no planned checks are represented as passing tests. Obtain owner design approval, generate the bounded task plan, and obtain task approval before production edits. Preserve unrelated worktree changes and historical evidence identities.
