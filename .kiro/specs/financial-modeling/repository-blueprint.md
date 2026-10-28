# Separate modeling repository: blueprint and extension rules

Status: design input, not an approved design or runtime implementation. The owner requests a separate repository; its name and remote are not yet assigned. This QOpenBB specification is a handoff stub. At bootstrap, move authoritative model specs and implementation evidence into that repository and retain pinned integration references here; do not maintain two editable copies of the same model definition.

## Dependency direction

Use ports and adapters for service boundaries, Adapter for explicit source-to-model input mapping, Strategy for selectable versioned methods, and a small registry for installed extensions. Begin with trusted Python modules, not a general plugin host or runtime-loaded user code.

```text
QOpenBB Workspace -> data API -> FMP, later expanded FRED/EconDB adapters
                 -> modeling service -> data API (explicit input acquisition)
                                    -> domain models (supplied inputs only)
```

The modeling service can acquire and snapshot inputs through the published data API. The domain package cannot fetch provider data, read provider credentials, import OpenBB adapters or depend on the UI. Provider APIs and widgets do not import the calculation package. Boundary checks enforce that direction.

Recommend one independently released modeling container on the existing Compose network. Keep provider widgets on their data routes. A presentation adapter exposes model results in Workspace-compatible shapes without duplicating calculations. Separate method versions, schema versions and image versions: each answers a different compatibility question.

## Proposed repository layout

```text
AGENTS.md                    Agent entry point and extension workflow
.kiro/steering/               House methods, architecture, testing, security and delivery
.kiro/specs/<capability>/     Requirements, design, tasks, decision and review records
src/<package>/contracts/     Versioned domain inputs, results and check outcomes
src/<package>/models/        Cohesive financial model modules
src/<package>/validation/    Shared rule execution and validation result types
src/<package>/service/       HTTP orchestration, authentication and snapshot handling
contracts/                  Exported API schemas and public contract examples
tests/                      Numerical reference, boundary and contract tests
docs/index.md               Navigation, supported methods and extension guide
pyproject.toml + uv.lock     Independent pinned Python environment
```

This is a layout proposal, not a package namespace reservation. Module-local financial rules stay close to their model; the shared validation code owns result handling, not a centralized catalogue of every formula. Reuse schema validators rather than inventing a rules language.

## Design by contract, applied to finance

Use explicit runtime validation functions with typed outcomes. Do not rely on Python's bare `assert` for production guards: optimized execution can remove assertions. Test assertions remain appropriate inside verification suites.

| Contract kind | Example obligation | Failure meaning |
| --- | --- | --- |
| Input schema | Required field, numeric type, date shape and nullability | Malformed input; do not invoke the model |
| Financial precondition | Compatible currency/period basis; required opening balance present | Input cannot support the selected method |
| Invariant | Balance sheet reconciles; capital weights reconcile under the method's declared scope | Broken financial relationship or incomplete input |
| Postcondition | Cash closing ties to the corresponding balance; signed EV/equity bridge reconciles | Calculated result cannot be accepted |
| Independent numerical check | Separately expressed Python reference agrees within declared tolerance | Numerical mismatch or incomplete verification |
| House-policy check | Selected growth/terminal assumptions satisfy the chosen policy | Warning or blocking rule according to approved policy |
| Consumer contract | Widget accepts the response types, semantics and validation states | API/consumer incompatibility |

The house standard explicitly requires an independent Python recalculation. Record reference implementation/version and actual compared inputs/results. This is distinct from structural validation and must not be satisfied by calling the production model twice.

Proposed rule-result contract: stable rule ID/version; method and run IDs; applicability; referenced inputs/outputs; expected condition; observed values; units; tolerance; severity; outcome (`pass`, `fail`, `unknown`, `error`, `not_applicable`); explanation; optional separately recorded policy exception. Exact types and encoding await design.

A required unknown/error blocks verification of dependent outputs. A warning remains visible. A policy exception never turns failed arithmetic into a pass. The UI can display unaffected source data while identifying withheld calculations. There is no blanket rule that every provider discrepancy blocks every model; applicability and dependency determine the affected outputs.

## Schemas and consumer contracts

Use OpenAPI and JSON Schema for published request/result structures, with versioned semantic definitions for financial fields. Model results retain their rich evidence; the widget adapter exposes the required projections and check details. Consumer contracts specify field bindings and meanings; generated client types alone do not prove runtime compatibility.

QOpenBB owns Workspace consumer expectations and their renderer checks. The modeling repository owns model/provider contract verification and numerical rules. Exchange immutable schema and consumer-contract artifacts or pinned Git revisions in CI. The design must choose the artifact mechanism before implementation; no contract broker is required merely to start.

Build breadth relationships as:

`spec criterion -> model/rule -> API operation/schema -> consumer binding -> test -> revision-specific evidence`

Do not duplicate the same truth manually in several manifests. Generate derivable references and retain explicit financial semantics where needed. Existing QOpenBB breadth mapping remains the integration index; the model repository owns its detailed method checks.

## Agent-first extension workflow

The future repository's AGENTS.md shall direct agents to:

1. Read core steering, the owning model spec and the pinned house-standard reference. Identify the finance action and supported entity/period scope before coding.
2. Write requirements with formula definitions, inputs, assumptions, failure cases, validation obligations and affected consumers. Distinguish reported data, provider calculations and house outputs.
3. Obtain requirements approval; design cohesive modules, contracts and extension boundaries; obtain design approval; generate bounded tasks and obtain task approval. Use explicit fast-track only when authorized.
4. Assign disjoint implementation lanes after contracts are frozen. Use the QOpenBB role-based fan-out rules initially: bounded implementers, independent financial review, at most four active slots and one heavy verification/build process.
5. Implement each task with financial preconditions/invariants/postconditions, meaningful numerical and contract checks, and maintained-file inventory. Apply 400 physical lines/file, 300 logical units/file and 50/function, with the executable checker rather than policy text alone.
6. Independently review the formula, signs, units, time bases, reconciliation and consumer failures. Recalculate material outputs in Python. No success claim from synthetic data alone where actual provider integration is promised.
7. Update spec checkboxes, docs, breadth and actual evidence, then commit the accepted task. Keep untouched provider/UI work out of the model repository.
8. Publish at an accepted feature milestone. Dagger builds images only; portable checks and publication commands keep CI movable from GitHub to Gitea. QOpenBB adopts an explicit compatible image/contract version after integration checks.

Carry COBESY documentation conventions, uv/uvx and the protected package workflow into the new repository. Keep secrets out of fixtures and public artifacts. No Excel implementation before the separately required Anthropic acceptance.

## Python and table conventions

The owner selected Polars for the modeling layer. Transfer [financial Python conventions](python-finance-conventions.md) into the future repository steering and each model task: financial-domain dataframe/table names, explicit grain/schema/precision, idiomatic typed Python and comments explaining financial rationale. The data-provider layer remains separately owned.

## Current session boundary

Only the stub specification and cross-project roadmap/breadth links are delivered. There is no model API, executable validator, fixture acceptance, plugin runtime, published package or Docker image yet. Requirements review is not implementation verification. Broad FMP work remains the active implementation lane; later FRED/EconDB expansion follows the same provider-versus-model boundary.
