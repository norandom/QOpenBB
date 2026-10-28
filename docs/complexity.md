# Check maintained code size

Run the combined quality gate before accepting maintained production changes. It measures whole files against 400 physical lines, 300 logical syntax units per Python/JavaScript/TypeScript file and 50 units per callable. These limits measure code size; financial correctness still requires the owning feature's checks.

## Run the portable gate

The pinned command below is historical foundation evidence. For current adaptation work, supply explicit changed-file manifests for both forks as described below, or current clean base/head revisions. Do not reuse the historical heads against changed checkouts.

Restore the pinned [development toolchain](development.md) first. From the repository root in WSL or Linux, put Node 24.22.1 on PATH and use the locked Python environment:

```sh
export PATH="$PWD/artifacts/task-1.2/node-v24.22.1-linux-x64/bin:$PATH"
mkdir -p artifacts/task-1.4
pipeline/.venv/bin/python -m tools.quality.complexity --check \
  --base workspace=be00e95019a55d57af146919ee46b7e1a4859226 \
  --head workspace=be00e95019a55d57af146919ee46b7e1a4859226 \
  --base data_api=5a7517ae8bc74ecdcd1a549ed26df8ad131b02d0 \
  --head data_api=5a7517ae8bc74ecdcd1a549ed26df8ad131b02d0 \
  --output artifacts/task-1.4/combined-foundation.json
```

The historical variant of this command, using Node 24.22.0, was exercised on 2026-10-16 against the unchanged acquired forks and the task 1.2-1.4 foundation working tree. It checked 23 maintained files with no errors, violations or applied exceptions. The report records CPython 3.13.15, Node 24.22.0 and TypeScript 6.0.3. Application behavior and future fork modifications remain outside this evidence.

For a changed fork, retain the approved inventory base and supply its actual full head SHA. Git mode verifies the fork origin, exact HEAD and clean worktree, then measures the whole changed files. `--repository-root REPOSITORY=PATH` supports an explicit checkout location. The base and repository identity must match [the inventory](../.kiro/complexity-budgets.json) and source lock; changing these is a reviewed source decision.

When Git metadata is unavailable, supply `--changes REPOSITORY=MANIFEST.json` for each fork instead of its base/head options. A manifest declares the snapshot and changed paths explicitly:

```json
{
  "repository": "https://github.com/norandom/openbb-workspace.git",
  "base": "be00e95019a55d57af146919ee46b7e1a4859226",
  "head": "be00e95019a55d57af146919ee46b7e1a4859226",
  "changes": []
}
```

Use the actual snapshot SHA and entries such as `{"status":"M","path":"frontend/src/example.tsx"}`. Added, modified, deleted, renamed, copied and type-changed paths use A/M/D/R/C/T; R and C also require `old_path`. The report labels manifest provenance as declared. An empty changes array explicitly declares no fork modifications; omitting scope input fails. No scope is inferred from absent container Git metadata.

Exit 0 means the requested measurement completed; with `--check`, it also means no unsuppressed cap violations remain. Exit 1 reports exceeded caps under `--check`. Exit 2 reports invalid scope, unreadable files, parser failures or invalid exception data. Inspect `errors`, `violations`, `exceptions`, `scope` and `coverage.combined_acceptance` in the JSON report. `--python-only` is an explicit partial report and always leaves combined acceptance unverified.

## Understand the counts

Physical counts normalize LF, CRLF and CR. Comments and blank lines count; a terminal newline adds no extra line. Other maintained text files receive physical measurements only.

The `project-syntax-units-v1` metric counts Python AST statements excluding docstrings, plus lambdas. JavaScript/TypeScript counts parser statements except blocks and empty statements, plus method, constructor, accessor, property and type-signature members. Expression-bodied callables add one unit. Nested callable implementations have their own budgets and remain included in file totals. Callable names and source positions are reported with one-based lines and columns.

The TypeScript 6.0.3 parser supports `.js`, `.jsx`, `.mjs`, `.cjs`, `.ts`, `.tsx`, `.mts` and `.cts`; JSX and TSX use their respective script kinds. JavaScript inputs reject TypeScript-only declarations and annotations. Parse failures stop the parser batch without partial JSON results. Its dependency resolves from `verification/package.json`, independently of package hoisting or the measured repository's location. No module imports from measured source are followed.

The inventory maps maintained paths to owning specifications. Add ownership mappings before introducing files. Tests, documentation, generated outputs, dependencies and unchanged upstream sources have recorded exclusions with a source or generator; maintained generator logic remains capped. The QOpenBB `vendor/` exclusion does not exempt changed files inside an owned fork. The recorded Excel output exclusion authorizes no generation before Anthropic acceptance. Task 2.7 has seven reviewed no-growth metric exceptions for three type-import-only changes; see the [exact review and expiry conditions](../.kiro/specs/openbb-self-service/task-2.7-exception-review.md). Task acceptance still requires the joined implementation checks.

## Review an oversized fork file

Prefer a cohesive extraction. If an extraction must wait, record a reviewed exception in the inventory's `exceptions` array. Each entry requires these fields:

| Field | Contract |
| --- | --- |
| `repository`, `path` | Exact inventory repository ID and repository-relative file path; no globs |
| `metric` | `physical`, `logical` or `function` |
| `baseline` | Measured integer above the cap; growth above this value still fails |
| `revision` | Full fork head SHA matching the current scope report |
| `rationale`, `review` | Explanation and reference to the review approving that measured baseline |
| `expires_on` | Current or future ISO date, checked when the gate runs |
| `function` | Required only for a function exception: exact `name`, `line` and `column` |

Exceptions apply only to the matching metric and callable, with the observed count at or below the reviewed baseline. Duplicate targets, expired entries, mismatched revisions and malformed values fail the gate. The report retains applied exceptions beside their actual measurements and review references. Reviewers verify the referenced approval; the checker validates its presence and the matching bounds.

## Reproduce the regression checks

```sh
pipeline/.venv/bin/python -m pytest -c pipeline/pyproject.toml tests/quality -n0 --maxprocesses=2
node --test tests/quality/test_syntax_units.mjs
node verification/node_modules/typescript/bin/tsc --project tools/quality/tsconfig.json
```

These checks cover scope provenance, exact limits, Python and TypeScript conventions, real JSX/TSX, parser response validation, failure reporting and reviewed exceptions. The Node suite also runs strict no-emit checking against the actual TypeScript AST declarations and pinned `@types/node` 24.10.1; the configuration permits only Node's erasable TypeScript syntax. Task-local RED/GREEN logs and the combined foundation report are retained under ignored `artifacts/task-1.4/`. Breadth evidence and task acceptance remain controlled by the owning specification.

The parser subprocess has a bounded 180-second deadline for the complete maintained scope. The 2026-10-28 Node 24.22.1 join measured 549 JavaScript/TypeScript files; the previous 60-second bound expired on the WSL filesystem. The gate still fails closed on timeout and validates every returned file record.
