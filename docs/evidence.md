# Validate evidence before using a release identity

Use `qopenbb-ci check` to validate artifact structure and compare it with an independently captured expected context. This command validates recorded claims; it does not run an application, infer a financial result, publish images or promote a release. The current source lock remains an acquisition record with no validated release or images.

From WSL/Linux at the repository root, after restoring the [locked development tools](development.md):

```sh
pipeline/.venv/bin/qopenbb-ci check --scope source \
  --input sources.lock.json --report artifacts/task-1.5/source-check.json
pipeline/.venv/bin/python -m qopenbb_ci.schemas --output schemas
pipeline/.venv/bin/python -m pytest -c pipeline/pyproject.toml tests/contracts -n0 --maxprocesses=2
```

These commands were exercised on 2026-10-16. Source validation accepts the acquired API revision `7c9d4221bdf66965e3f6c7f4dc6ee848073e5ae2` while retaining `5a7517ae8bc74ecdcd1a549ed26df8ad131b02d0` as an unvalidated candidate. Neither this result nor the synthetic contract tests establishes application acceptance.

## Select the check

| Scope | Input and result |
| --- | --- |
| `source` | Existing schema-2 acquisition lock; rejects altered ownership/provenance, noncommit pins and claims of a validated release |
| `manifest` | Candidate or release structure and matching identity; permits a dashboard checkpoint with Workspace and data API images |
| `acceptance` | Record structure and matching identity; retains passed, failed, skipped and unverified status without treating structural validity as a successful runtime check |
| `backup` | Stopped-state manifest, UTC time, archive checksum, private configuration reference and declared restore compatibility; does not inspect or restore the archive |
| `excel` | Workspace/data/agent checkpoint and matching actual Anthropic acceptance; does not require an Excel candidate or image |
| `release` | Explicit release status, complete selected image set and matching declared runtime checks including Linux/recovery and Excel when selected; does not perform promotion |

Every scope except `source` requires `--expected PATH`. This file follows [expected.schema.json](../schemas/expected.schema.json). Capture it from the intended checkout, selected immutable image set, lock/contract hashes and configured Anthropic model before evaluating supplied records. Deriving it from the records being checked defeats freshness validation. Review the provenance and actual result artifacts independently.

The gate syntax exercised by the contract suite is:

```sh
pipeline/.venv/bin/qopenbb-ci check --scope excel \
  --input checkpoint.json --expected expected.json \
  --evidence workspace-acceptance.json --evidence data-acceptance.json \
  --evidence anthropic-acceptance.json --report artifacts/acceptance/excel-gate.json
```

The gate requires one matching passed record for each declared capability/class check, successful exit codes, exact acceptance references and matching release/run IDs, source revisions, image digests/architecture, hashes and model. Actual checkpoint requirements cannot be weakened to fixture evidence or an empty required-check list. Capability IDs are `workspace`, `data_api` and `anthropic`; image service IDs are `workspace`, `data-api` and `agent`. Numeric checkpoint criteria are 4.3/4.7, 5.1/5.6 and 12.1/12.2/12.5 respectively. Final release validation additionally requires Workspace 4.1/4.2, `linux` 3.3/9.4 and `recovery` 8.2/8.4; an enabled Excel profile requires `excel` 6.1-6.4.

## Interpret the report

Exit 0 means the selected check passed; exit 1 means its validation gate failed; exit 2 means invocation, input loading/JSON parsing or report writing failed. Valid invocations write a JSON report to `--report` and stdout. Invalid command arguments use argparse diagnostics; an unwritable report produces a minimal stdout error. `issues` contains field paths and codes without input values. Unknown map/field names are redacted in diagnostics. `checks` retains each parsed record's path, status and evidence class without copying its command or result payload.

`valid` describes the selected check. `runtime_accepted` is always false for structural scopes and becomes true only when the Excel/release evidence gate passes. It is a decision over supplied evidence, not independent attestation of its truth. Missing, stale, failed, skipped, unverified or fixture-only records cannot unlock Excel or satisfy a required actual runtime check.

The [Python models](../pipeline/qopenbb_ci/contracts.py) and [source model](../pipeline/qopenbb_ci/source_contract.py) own validation, including cross-field checks. Generated [release](../schemas/release.schema.json), [acceptance](../schemas/acceptance.schema.json) and [backup](../schemas/backup.schema.json) schemas expose their structural contracts; regenerate them after model changes. Boolean values cannot stand in for integer versions or exit codes. Unknown fields are rejected. Configuration fields contain uppercase names, and private backup configuration is an opaque `private:` reference. Acceptance artifact references must remain under `artifacts/` and must identify sanitized outputs; backup archives can also use a relative `backups/` reference. Never supply `.env` contents or credential-bearing commands/results.

Run the [combined complexity gate](complexity.md) after changing maintained validators. Task-local RED/GREEN output and the combined report are retained under ignored `artifacts/task-1.5/`; the owning specification and breadth map retain acceptance ownership.
