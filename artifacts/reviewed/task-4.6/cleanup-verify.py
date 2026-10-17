from pathlib import Path
import json
import subprocess
import sys

root = Path('/mnt/d/Source/QOpenBB')
out = root / 'artifacts/task-4.6'
removed = []
for index in (0, 1, 2):
    directory = Path(f'/tmp/pytest-of-mc/pytest-{index}/test_real_fixture_roundtrip0')
    observed = [{'name': item.name, 'bytes': item.stat().st_size} for item in directory.iterdir()]
    if observed != [{'name': 'workspace.db', 'bytes': 180224}]:
        raise RuntimeError(f'Unexpected residue in {directory}: {observed}')
    database = directory / 'workspace.db'
    with database.open('rb') as stream:
        assert stream.read(16) == b'SQLite format 3\x00'
    database.unlink()
    removed.append({'directory': str(directory), 'observed': observed, 'database_removed': not database.exists()})
    directory.rmdir()
    removed[-1]['task_directory_removed'] = not directory.exists()
commands = {
    'success': [sys.executable, str(root / 'vendor/workspace/backend-api/backend/tests_sqlite/run.py')],
    'nonzero': [sys.executable, str(root / 'vendor/workspace/backend-api/backend/tests_sqlite/run.py'), '-k', 'does_not_exist_task46_cleanup'],
}
results = {}
for name, command in commands.items():
    process = subprocess.run(command, capture_output=True, text=True)
    log = process.stdout + process.stderr
    (out / f'cleanup-{name}.log').write_text(log)
    lines = [line for line in log.splitlines() if line.startswith('Removed sandbox: ')]
    assert len(lines) == 1, log
    sandbox = Path(lines[0].removeprefix('Removed sandbox: '))
    assert not sandbox.exists()
    results[name] = {'command': command, 'exit': process.returncode, 'sandbox': str(sandbox), 'removed': not sandbox.exists()}
assert results['success']['exit'] == 0
assert results['nonzero']['exit'] == 5
(out / 'cleanup-evidence.json').write_text(json.dumps({'prior_residue': removed, 'fresh_runs': results}, indent=2) + '\n')
print(json.dumps(results, indent=2))