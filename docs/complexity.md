# Check maintained file size

Run the Python and physical-file gate from the repository root with the locked pipeline interpreter. This partial gate checks every maintained QOpenBB production file and the explicitly supplied changed files in each owned fork. Task 1.4 owns combined JavaScript/TypeScript certification; a Python-only pass does not establish it.

The following command was exercised in WSL on 2026-10-16 with CPython 3.13.15. These base/head pairs describe the unchanged acquisition checkouts. Replace them with the actual reviewed snapshot inputs when a fork changes; do not use acquisition hashes to describe a later checkout.

```sh
pipeline/.venv/bin/python -m tools.quality.complexity --python-only --check \
  --base workspace=be00e95019a55d57af146919ee46b7e1a4859226 \
  --head workspace=be00e95019a55d57af146919ee46b7e1a4859226 \
  --base data_api=7c9d4221bdf66965e3f6c7f4dc6ee848073e5ae2 \
  --head data_api=7c9d4221bdf66965e3f6c7f4dc6ee848073e5ae2 \
  --output artifacts/task-1.3/inventory.json
```

Git input requires an exact origin identity, both full commit hashes, the declared head checked out and a clean worktree. For a source export without Git metadata or a working change set, supply a reviewed JSON manifest for each fork instead:

```json
{
  "repository": "https://github.com/norandom/openbb-workspace.git",
  "base": "be00e95019a55d57af146919ee46b7e1a4859226",
  "head": "be00e95019a55d57af146919ee46b7e1a4859226",
  "changes": []
}
```

Use `--changes workspace=/path/to/workspace-changes.json` and the corresponding `data_api` manifest, replacing the Git arguments. Each changed entry has `status` and repository-relative `path`; rename/copy entries also require `old_path`. Supported statuses are `A`, `M`, `D`, `R`, `C` and `T`. Deleted entries are tombstones; rename destinations are measured as whole files. `--repository-root workspace=/export/workspace` selects an exported root. Empty explicit changes are valid; missing inputs fail. Manifest provenance is reported as `manifest-declared`, without a claim that Git verified the snapshot.

Update the owning `files` list in [.kiro/complexity-budgets.json](../.kiro/complexity-budgets.json) when adding maintained files or changing fork code. Fork bases must match the inventory and [source lock](../sources.lock.json). Moving an acquisition baseline requires a separately reviewed source-lock update. The QOpenBB exclusion for `vendor/` does not exempt modified code inside a fork. Exclusions list their rationale and source/generator; generator implementations remain maintained code. The existing Excel output exclusion authorizes no generation before Anthropic acceptance.

The caps are 400 physical lines, 300 logical units per Python file and 50 per callable. Physical counts include comments and blank lines, normalize CRLF/CR, and ignore a terminal newline as an extra line. Unicode separators do not create physical lines. The `project-syntax-units-v1` Python metric counts AST statements excluding initial module/class/function docstrings, plus lambdas. Nested implementations remain in file totals, receive their own callable counts and do not inflate their enclosing callable. This is a size check, not financial or algorithmic correctness evidence.

Exit status is `0` for a valid inventory, `1` for exceeded caps with `--check`, and `2` for missing/invalid scope or unreadable/unparseable input. The JSON report contains `coverage`, `scope`, `files`, `errors`, `violations`, `deleted`, and declared and applied exclusions. Omit `--output` to write it to stdout. Preserve reports under ignored artifacts.

Run the focused regression fixtures serially:

```sh
pipeline/.venv/bin/python -m pytest -c pipeline/pyproject.toml \
  tests/quality/test_python_units.py tests/quality/test_scope.py tests/quality/test_cli.py \
  -n0 --maxprocesses=2
```
