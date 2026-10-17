"""Review the frozen composition lane against accepted sibling dependencies."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

ROOT = Path('/mnt/d/Source/QOpenBB')
OUT = ROOT / 'artifacts/task-2.42/review'
SOURCE = ROOT / 'vendor/workspace/terminalpro'
BASE = Path('/home/mc/qopenbb-work/task241-20261017135547/terminalpro')
STAGE = Path(f'/home/mc/qopenbb-work/task242-review-{time.time_ns()}/terminalpro')
REV = 'bc42d604855a6b5d943ce05ee9fcce11e356435a'
NODE = ROOT / 'artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node'
OWNED = ['src/components/General/Table/Chart/application/appearanceComposition.ts',
         'tests/unit/chart-application/appearanceComposition.test.ts']
SIBLING = ['src/components/General/Table/Chart/compatibility/optionStateTypes.ts',
           'src/components/General/Table/Chart/compatibility/editorEvents.ts',
           'src/components/General/Table/Chart/application/sessionState.ts',
           'src/components/General/Table/Chart/application/types.ts',
           'tests/unit/chart-compatibility/editorEvents.test.ts',
           'tests/unit/chart-application/sessionState.test.ts']
DIRS = ['src/components/General/Table/Chart/application',
        'src/components/General/Table/Chart/compatibility',
        'src/components/General/Table/Chart/echarts',
        'tests/unit/chart-application', 'tests/unit/chart-compatibility',
        'tests/e2e/chart-compatibility']

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def accepted(relative):
    return subprocess.check_output(['git', '-C', str(SOURCE.parent), 'show',
                                    REV + ':terminalpro/' + relative])

shutil.copytree(BASE, STAGE, symlinks=True, ignore=shutil.ignore_patterns('node_modules'))
(STAGE / 'node_modules').symlink_to('/home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules', target_is_directory=True)
paths = sorted({p.relative_to(SOURCE).as_posix() for d in DIRS for p in (SOURCE/d).rglob('*') if p.is_file()} | {'package.json', 'biome.json'})
closure = []
for relative in paths:
    target = STAGE / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    current = (SOURCE / relative).read_bytes()
    if relative in OWNED:
        data = current
        origin = 'current owned frozen bytes'
    else:
        data = accepted(relative)
        origin = REV
        if relative not in SIBLING:
            assert current.replace(b'\r\n', b'\n') == data.replace(b'\r\n', b'\n'), relative
            data = current
            origin = 'current immutable dependency, compared with ' + REV
    target.write_bytes(data)
    closure.append({'path': relative, 'origin': origin, 'sha256': digest(target),
                    'currentSha256': digest(SOURCE / relative), 'siblingOverlay': relative in SIBLING})
manifest = {'stage': str(STAGE), 'baselineStage': str(BASE), 'acceptedRevision': REV,
            'node': str(NODE), 'nodeSha256': digest(NODE), 'inputs': closure,
            'dependencies': str((STAGE/'node_modules').resolve())}
(OUT/'stage.json').write_text(json.dumps(manifest, indent=2)+'\n')
env = dict(os.environ)
env['PATH'] = str(NODE.parent) + ':' + env.get('PATH', '')
commands = [
    ('application-strict', ['node_modules/typescript/bin/tsc', '--project', 'tests/unit/chart-application/tsconfig.json', '--noEmit']),
    ('compatibility-strict', ['node_modules/typescript/bin/tsc', '--project', 'tests/unit/chart-compatibility/tsconfig.json', '--noEmit']),
    ('application-suite', ['node_modules/vitest/vitest.mjs', 'run', '--config', 'tests/unit/chart-application/vitest.config.mjs']),
    ('compatibility-suite', ['node_modules/vitest/vitest.mjs', 'run', '--config', 'tests/unit/chart-compatibility/vitest.config.mjs']),
    ('scoped-lint', ['node_modules/@biomejs/biome/bin/biome', 'check', 'src/components/General/Table/Chart/application', 'src/components/General/Table/Chart/compatibility/editorEvents.ts', 'src/components/General/Table/Chart/compatibility/optionStateTypes.ts', 'tests/unit/chart-application', 'tests/unit/chart-compatibility/editorEvents.test.ts']),
]
results = []
for name, args in commands:
    command = [str(NODE), *args]
    log = OUT / (name + '.log')
    with log.open('x') as stream:
        stream.write('cwd: '+str(STAGE)+'\ncommand: '+' '.join(command)+'\n')
        stream.flush()
        result = subprocess.run(command, cwd=STAGE, env=env, stdout=stream, stderr=subprocess.STDOUT, check=False)
        stream.write('\nexit: '+str(result.returncode)+'\n')
    results.append({'name': name, 'command': command, 'exit': result.returncode, 'log': log.name, 'sha256': digest(log)})
    (OUT/'results.json').write_text(json.dumps(results, indent=2)+'\n')
    print(name, result.returncode, flush=True)
assert all(digest(STAGE/item['path']) == item['sha256'] for item in closure)
assert all(digest(SOURCE/p) == next(i['sha256'] for i in closure if i['path']==p) for p in OWNED)
print('Immutable closure and owned source hashes unchanged', flush=True)
