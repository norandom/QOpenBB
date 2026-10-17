import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path('/mnt/d/Source/QOpenBB')
OUT = ROOT / 'artifacts/task-2.41/review'
IMPL = ROOT / 'artifacts/task-2.41/implementation'
SOURCE = ROOT / 'vendor/workspace/terminalpro'
stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d%H%M%S')
stage = Path('/home/mc/qopenbb-work/task241-review-' + stamp) / 'terminalpro'
baseline = json.loads((IMPL / 'frozen-scope.json').read_text())
subprocess.run(['cp', '-a', baseline['stage'], str(stage.parent)], check=True)
# cp creates the parent with the copied contents; use that isolated directory.
stage = stage.parent

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')

# Check the entire copied source inventory against current workspace bytes.
# Refresh every difference, retaining no stale baseline source in this stage.
full = json.loads((IMPL / 'source-stage-manifest.json').read_text())
records = []
for item in full['files']:
    path = item['path']
    current = digest(SOURCE / path)
    target = stage / path
    if not target.is_file() or digest(target) != current:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SOURCE / path, target)
    assert digest(target) == current
    records.append({'path': path, 'sourceSha256': current, 'stageSha256': current})
write('full-stage-manifest.json', {'stage': str(stage), 'files': records})
selected = {r['path'] for r in baseline['files']}
selected.update(str(p.relative_to(SOURCE)) for p in (SOURCE / 'tests/e2e/chart-compatibility').rglob('*') if p.is_file())
packages = {}
for package in baseline['dependencies']:
    package_path = stage / 'node_modules' / package / 'package.json'
    packages[package] = {'version': json.loads(package_path.read_text())['version'], 'packageSha256': digest(package_path)}
assert packages == baseline['dependencies']
write('frozen-scope.json', {'stage': str(stage), 'workspaceHead': baseline['workspaceHead'], 'dependencies': packages, 'fullSourceCount': len(records), 'files': [r for r in records if r['path'] in selected]})
env = dict(os.environ, PATH=str(ROOT / 'artifacts/task-1.2/node-v24.22.0-linux-x64/bin') + ':' + os.environ['PATH'])
commands = [
    ['node', '--version'],
    ['node', 'node_modules/typescript/bin/tsc', '--project', 'tests/unit/chart-application/tsconfig.json', '--noEmit'],
    ['node', 'node_modules/typescript/bin/tsc', '--project', 'tests/unit/chart-compatibility/tsconfig.json', '--noEmit'],
    ['node', 'node_modules/vitest/vitest.mjs', 'run', '--config', 'tests/unit/chart-application/vitest.config.mjs'],
    ['node', 'node_modules/vitest/vitest.mjs', 'run', '--config', 'tests/unit/chart-compatibility/vitest.config.mjs'],
    ['node', 'node_modules/@biomejs/biome/bin/biome', 'check', 'src/components/General/Table/Chart/application', 'src/components/General/Table/Chart/compatibility/editorEvents.ts', 'src/components/General/Table/Chart/compatibility/optionStateTypes.ts', 'tests/unit/chart-application', 'tests/unit/chart-compatibility/editorEvents.test.ts'],
]
results = []
for index, command in enumerate(commands):
    result = subprocess.run(command, cwd=stage, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    log = OUT / f'check-{index}.log'
    log.write_text(result.stdout)
    results.append({'command': command, 'cwd': str(stage), 'exitCode': result.returncode, 'log': str(log.relative_to(ROOT)), 'sha256': digest(log)})
    write('command-status.json', results)
    print(index, result.returncode, flush=True)
