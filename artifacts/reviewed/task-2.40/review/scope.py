"""Declare current maintained fork scope without claiming a clean checkout."""
import hashlib
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[3]
out = Path(__file__).resolve().parent
inventory = json.loads((root / '.kiro/complexity-budgets.json').read_text())
for repo in inventory['repositories']:
    if repo['id'] == 'qopenbb':
        continue
    base = root / repo['root']
    def git(*args):
        return subprocess.check_output(['git', '-C', str(base), *args]).decode().strip()
    names = {p for owner in repo['owners'] for p in owner['files'] if (base / p).is_file()}
    names.update(git('diff', '--name-only', 'HEAD').splitlines())
    names.update(git('ls-files', '--others', '--exclude-standard').splitlines())
    names.discard('')
    result = dict(repository=repo['repository'], base=repo['revision'], head=git('rev-parse', 'HEAD'),
                  changes=[dict(path=p, status='M' if (base / p).is_file() else 'D') for p in sorted(names)])
    (out / (repo['id'].replace('_', '-') + '-changes.json')).write_text(json.dumps(result, indent=2) + '\n')
paths = sorted((root / 'vendor/workspace/terminalpro/src/components/General/Table/Chart/application').glob('*.ts'))
hashes = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
(out / 'owned-source-hashes.json').write_text(json.dumps(hashes, indent=2) + '\n')
print('Explicit current manifests and application hashes recorded')
