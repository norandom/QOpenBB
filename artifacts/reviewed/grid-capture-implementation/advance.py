"""Stage only accepted application ownership and source pins, preserving other edits."""
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[2]
fork = root / 'vendor/workspace'
def git(*args, cwd=root):
    return subprocess.check_output(['git', *args], cwd=cwd).decode().strip()
path = root / '.kiro/complexity-budgets.json'
working = path.read_text()
indexed = git('show', 'HEAD:.kiro/complexity-budgets.json')
head = git('rev-parse', 'HEAD', cwd=fork)
previous = json.loads((root / 'sources.lock.json').read_text())['workspace']['revision']
for target in {e['path'] for e in json.loads(working)['exceptions'] if e['repository'] == 'workspace'}:
    assert not git('diff', previous, head, '--', target, cwd=fork), target
    assert not git('diff', 'HEAD', '--', target, cwd=fork), target
names = ['types.ts', 'chartRange.ts', 'sessionState.ts', 'financialFormatting.ts', 'gridCapture.ts']
prefix = 'terminalpro/src/components/General/Table/Chart/application/'
accepted = [prefix + n for n in names if git('ls-files', '--', prefix + n, cwd=fork)]
def revise(text, old_revision):
    text = text.replace(old_revision, head)
    cache = '        {"patterns":["**/__pycache__/**", "**/*.pyc"],"reason":"Generated CPython bytecode caches; maintained Python sources remain measured","source":"CPython import cache"},\n'
    anchor_cache = '        {"patterns":["backend-api/backend/tests_sqlite/**"]'
    if cache not in text:
        assert text.count(anchor_cache) == 1
        text = text.replace(anchor_cache, cache + anchor_cache, 1)
    parsed = json.loads(text)
    files = next(r for r in parsed['repositories'] if r['id'] == 'workspace')['owners'][0]['files']
    anchor = '        "terminalpro/src/components/General/Table/Chart/echarts/cartesianStyle.ts",'
    for name in accepted:
        if name not in files:
            assert text.count(anchor) == 1
            text = text.replace(anchor, anchor + '\n        "' + name + '",', 1)
    json.loads(text)
    return text.rstrip() + '\n'
path.write_text(revise(working, previous), encoding='utf-8')
snapshot = root / 'artifacts/grid-capture-implementation/inventory-index.json'
snapshot.write_text(revise(indexed, json.loads(git('show', 'HEAD:sources.lock.json'))['workspace']['revision']), encoding='utf-8')
lock = root / 'sources.lock.json'
lock.write_text(lock.read_text().replace(previous, head), encoding='utf-8')
blob = git('hash-object', '-w', str(snapshot))
subprocess.run(['git', 'update-index', '--cacheinfo', '100644,' + blob + ',.kiro/complexity-budgets.json'], check=True)
print(json.dumps(dict(previous=previous, head=head, accepted_application_files=accepted)))
