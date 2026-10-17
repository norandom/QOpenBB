import hashlib
import importlib.metadata as metadata
import json
from pathlib import Path
import platform
import subprocess
import sys

root = Path('/mnt/d/Source/QOpenBB')
backend = root / 'vendor/workspace/backend-api/backend'
out = root / 'artifacts/task-4.6/review/round2'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

commands = {
    'tests': [sys.executable, str(backend / 'tests_sqlite/run.py')],
    'lint': [str(Path(sys.executable).parent / 'ruff'), 'check', str(backend / 'tests_sqlite')],
    'format': [str(Path(sys.executable).parent / 'ruff'), 'format', '--check', str(backend / 'tests_sqlite')],
}
results = {}
for name, command in commands.items():
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    (out / (name + '-final.log')).write_text(result.stdout)
    results[name] = {'command': command, 'exit_code': result.returncode}
record = {
    'python': sys.version, 'executable': sys.executable, 'platform': platform.platform(),
    'workspace_revision': subprocess.check_output(['git','-C',str(root / 'vendor/workspace'),'rev-parse','HEAD'],text=True).strip(),
    'source_hashes': {str(path.relative_to(root)): digest(path) for path in [backend / 'poetry.lock', backend / 'pyproject.toml', backend / 'api/crud.py', backend / 'utilities/config.py', *sorted((backend / 'tests_sqlite').glob('*.py'))]},
    'runtime_distributions': {item.metadata['Name']: item.version for item in metadata.distributions()},
    'restoration_inputs': {str(path): digest(path) for path in [Path('/home/mc/qopenbb-work/sqlite-runtime/requirements.txt'), Path('/home/mc/qopenbb-work/sqlite-runtime/build-tools.txt')]},
    'results': results,
}
(out / 'evidence.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(results, indent=2))
sys.exit(any(result['exit_code'] for result in results.values()))
