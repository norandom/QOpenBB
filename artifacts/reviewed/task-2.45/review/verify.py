"""Freeze the current joined chart closure and run each prescribed gate once."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

ROOT = Path('/mnt/d/Source/QOpenBB')
OUT = ROOT / 'artifacts/task-2.45/review'
SOURCE = ROOT / 'vendor/workspace/terminalpro'
BASE = Path('/home/mc/qopenbb-work/task241-20261017135547/terminalpro')
STAGE = Path('/home/mc/qopenbb-work/task245-independent-review/terminalpro')
NODE = ROOT / 'artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node'
DIRS = ['src/components/General/Table/Chart/application',
        'src/components/General/Table/Chart/compatibility',
        'src/components/General/Table/Chart/echarts',
        'tests/unit/chart-application', 'tests/unit/chart-compatibility',
        'tests/e2e/chart-compatibility']

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git(*args):
    return subprocess.check_output(['git', '-C', str(SOURCE.parent), *args]).decode().strip()

assert not STAGE.exists(), 'Do not overwrite evidence from a previous run'
shutil.copytree(BASE, STAGE, symlinks=True, ignore=shutil.ignore_patterns('node_modules'))
(STAGE/'node_modules').symlink_to('/home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules', target_is_directory=True)
paths = sorted({p.relative_to(SOURCE).as_posix() for d in DIRS for p in (SOURCE/d).rglob('*') if p.is_file()} | {'package.json', 'biome.json', 'tsconfig.json', 'tsconfig.node.json'})
closure = []
for relative in paths:
    target = STAGE / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes((SOURCE/relative).read_bytes())
    closure.append({'path': relative, 'sha256': digest(target), 'currentSha256': digest(SOURCE/relative)})
manifest = {'stage': str(STAGE), 'baselineStage': str(BASE), 'workspaceHead': git('rev-parse', 'HEAD'),
            'scope': 'Every staged closure file is the current checkout byte sequence; no accepted-lane overlays.',
            'node': str(NODE), 'nodeSha256': digest(NODE), 'inputs': closure,
            'dependencies': str((STAGE/'node_modules').resolve())}
(OUT/'stage.json').write_text(json.dumps(manifest, indent=2)+'\n')
env = dict(os.environ)
env['PATH'] = str(NODE.parent) + ':' + env.get('PATH', '')
commands = [
    ('versions', ['--version']),
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
    start = time.monotonic()
    with log.open('x') as stream:
        result = subprocess.run(command, cwd=STAGE, env=env, stdout=stream, stderr=subprocess.STDOUT, check=False)
    results.append({'name': name, 'command': command, 'cwd': str(STAGE), 'exit': result.returncode,
                    'seconds': round(time.monotonic()-start, 3), 'log': log.name, 'sha256': digest(log)})
    (OUT/'results.json').write_text(json.dumps(results, indent=2)+'\n')
    print(name, result.returncode, flush=True)
    if result.returncode:
        raise SystemExit('Failed check preserved; diagnose before any follow-up')
assert all(digest(STAGE/item['path']) == item['sha256'] == digest(SOURCE/item['path']) for item in closure)
(OUT/'closure-stability.json').write_text(json.dumps({'files':len(closure), 'current_and_staged_unchanged':True}, indent=2)+'\n')
print('Current and staged closure hashes unchanged', len(closure), flush=True)
