"""Audit frozen scope, whole-file metrics and explicitly selected public evidence."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path('/mnt/d/Source/QOpenBB')
OUT = ROOT / 'artifacts/task-2.44/review'
IMPL = ROOT / 'artifacts/task-2.44/implementation'
STAGE = Path('/home/mc/qopenbb-work/task244-independent-review/terminalpro')
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
manifest = json.loads((OUT / 'stage-manifest.json').read_text())
for entry in manifest['files']:
    assert sha(STAGE / entry['path']) == entry['sha256']
    assert sha(ROOT / 'vendor/workspace/terminalpro' / entry['path']) == entry['sha256']
owned = json.loads((IMPL / 'source-manifest.json').read_text())['files']
production = [ROOT / e['source'] for e in owned if '/src/' in e['source']]
command = [str(ROOT / 'artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node'), str(ROOT / 'tools/quality/syntax_units.ts')]
result = subprocess.run(command, input=json.dumps([str(p) for p in production]), capture_output=True, text=True, cwd=ROOT)
assert result.returncode == 0, result.stderr
measurements = json.loads(result.stdout)
for entry, path in zip(measurements, production):
    entry.update(physical=len(path.read_text().splitlines()), sha256=sha(path))
    entry['max_function'] = max([fn['logical'] for fn in entry['functions']], default=0)
    assert entry['physical'] <= 400 and entry['logical'] <= 300 and entry['max_function'] <= 50
(OUT / 'size.json').write_text(json.dumps({'command': command, 'exit_code': 0, 'files': measurements}, indent=2) + '\n')
diff = (OUT / 'actual-owned.diff').read_text()
additions = '\n'.join(line for line in diff.splitlines() if line.startswith('+') and not line.startswith('+++'))
assert not re.search(r'\b(TBD|TODO|FIXME|HACK|XXX)\b', additions)
secret = re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:sk-[A-Za-z0-9]{24,}|ghp_[A-Za-z0-9]{30,}|AKIA[A-Z0-9]{16})\b')
assert not secret.search(additions)
controller_names = ['complexity-stale-manifest-failure.json', 'complexity.json', 'data-api-changes.json', 'owned-source-hashes.json', 'workspace-changes.json']
quality = json.loads((ROOT / 'artifacts/task-2.44/controller/complexity.json').read_text())
assert not quality['errors'] and not quality['violations'] and quality['coverage']['combined_acceptance'] == 'passed'
for measurement in measurements:
    rel = str(Path(measurement['path']).relative_to(ROOT / 'vendor/workspace'))
    shared = next(e for e in quality['files'] if e['repository'] == 'workspace' and e['path'] == rel)
    assert (shared['physical'], shared['logical']) == (measurement['physical'], measurement['logical'])
selected = json.loads((IMPL / 'publication-allowlist.json').read_text())['files']
selected += [{'path': 'artifacts/task-2.44/implementation/publication-allowlist.json', 'sha256': sha(IMPL / 'publication-allowlist.json')}]
selected += [{'path': 'artifacts/task-2.44/controller/' + name, 'sha256': sha(ROOT / 'artifacts/task-2.44/controller' / name)} for name in controller_names]
review_names = ['prepare.py', 'repair-stage.py', 'staging-failure.md', 'run_check.py', 'audit.py', 'actual-owned.diff', 'stage-manifest.json', 'input-audit.json', 'size.json', 'report.md']
for label in ['compatibility', 'compatibility-complete', 'application', 'strict-compatibility', 'strict-application', 'lint']:
    review_names += [label + '.log', label + '.json']
    expected = 1 if label in ['compatibility', 'application'] else 0
    assert json.loads((OUT / (label + '.json')).read_text())['exit_code'] == expected
selected += [{'path': 'artifacts/task-2.44/review/' + name, 'sha256': sha(OUT / name)} for name in review_names]
for entry in selected:
    path = ROOT / entry['path']
    assert path.is_relative_to(ROOT / 'artifacts/task-2.44')
    assert sha(path) == entry['sha256']
    assert path.suffix in {'.md', '.json', '.log', '.txt', '.py', '.ts', '.diff'}
    assert not secret.search(path.read_text()), entry['path']
(OUT / 'publication-allowlist.json').write_text(json.dumps({'scope': 'Independently inspected synthetic source, test, deterministic script, failure and successful verification evidence; no environment files, credentials, private state, dependency caches or image archives.', 'files': selected}, indent=2) + '\n')
print(f'All {len(manifest["files"])} closure hashes remain current; whole-file caps pass; {len(selected)} safe evidence hashes frozen.')
