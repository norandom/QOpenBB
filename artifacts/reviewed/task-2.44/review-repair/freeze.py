"""Verify the repaired closure and freeze old failures plus new review evidence."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path('/mnt/d/Source/QOpenBB')
OUT = ROOT / 'artifacts/task-2.44/review-repair'
STAGE = Path('/home/mc/qopenbb-work/task244-independent-review-repair/terminalpro')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
manifest = json.loads((OUT / 'stage-manifest.json').read_text())
for item in manifest['files']:
    assert sha(STAGE / item['path']) == item['sha256'] == sha(ROOT / 'vendor/workspace/terminalpro' / item['path'])
selected = {}
for manifest_path in ['artifacts/task-2.44/review/publication-allowlist.json', 'artifacts/appearance-grid-teardown/allowlist.json']:
    for item in json.loads((ROOT / manifest_path).read_text())['files']:
        assert sha(ROOT / item['path']) == item['sha256'], item['path']
        selected[item['path']] = item['sha256']
    selected[manifest_path] = sha(ROOT / manifest_path)
repair = ROOT / 'artifacts/appearance-grid-teardown'
probe_text = re.sub(r'\x1b\[[0-9;]*m', '', (repair / 'callback-lifecycle-probe.log').read_text())
callbacks = [json.loads(line.split('TEARDOWN_PROBE ', 1)[1]) for line in probe_text.splitlines() if line.startswith('TEARDOWN_PROBE ')]
assert sum(c.get('delay') == 400 and 'RowRenderer.destroyRowCtrls' in c['origin'] for c in callbacks) == 6
assert sum(c.get('delay') == 0 and 'RowRenderer.dispatchDisplayedRowsChanged' in c['origin'] and 'LocalEventService.dispatchAsync' in c['origin'] for c in callbacks) == 4
assert all(c['windowAlive'] and c['destroyed'] for c in callbacks)
assert probe_text.count('TEARDOWN_PENDING_DRAINED 0') == 11
summary = json.loads((repair / 'lifecycle-summary.json').read_text())
assert sha(Path('/home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules/ag-grid-community/dist/package/main.esm.mjs')) == summary['ag_grid_bundle_sha256']
names = ['prepare.py', 'run_check.py', 'freeze.py', 'freeze-parser-corrections.txt', 'stage-manifest.json', 'fixture.diff', 'gridCapture.grid.test.ts', 'report.md']
for label in ['compatibility', 'application', 'strict-compatibility', 'strict-application', 'lint']:
    assert json.loads((OUT / f'{label}.json').read_text())['exit_code'] == 0
    names += [label + '.json', label + '.log']
for name in names:
    selected['artifacts/task-2.44/review-repair/' + name] = sha(OUT / name)
additions = '\n'.join(line for line in (OUT / 'fixture.diff').read_text().splitlines() if line.startswith('+') and not line.startswith('+++'))
assert not re.search(r'\b(TBD|TODO|FIXME|HACK|XXX)\b', additions)
secret = re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:sk-[A-Za-z0-9]{24,}|ghp_[A-Za-z0-9]{30,}|AKIA[A-Z0-9]{16})\b')
for rel, expected in selected.items():
    path = ROOT / rel
    assert not Path(rel).is_absolute() and '..' not in Path(rel).parts
    assert sha(path) == expected
    assert path.suffix in {'.md', '.json', '.log', '.txt', '.py', '.ts', '.diff'}
    assert not secret.search(path.read_text()), rel
(OUT / 'publication-allowlist.json').write_text(json.dumps({'scope': 'Original implementation, controller quality, frozen failed review, authorized test repair and fresh independent passing review; synthetic source/evidence only.', 'files': [{'path': rel, 'sha256': expected} for rel, expected in sorted(selected.items())]}, indent=2) + '\n')
print(f'Verified {len(manifest["files"])} current closure hashes and froze {len(selected)} safe artifact/source hashes.')
