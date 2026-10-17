import hashlib
import json
import os
import pathlib
import shutil
import subprocess

ROOT = pathlib.Path('/mnt/d/Source/QOpenBB')
OUT = ROOT / 'artifacts/task-2.41/implementation'
path = OUT / 'source-stage-manifest.json'
manifest = json.loads(path.read_text())
stage = pathlib.Path(manifest['stage'])
owned = ['src/components/General/Table/Chart/application/appearanceContracts.ts',
         'tests/unit/chart-application/appearanceContracts.types.ts',
         'tests/unit/chart-application/appearanceFixtures.json']
for relative in owned:
    shutil.copyfile(ROOT / 'vendor/workspace/terminalpro' / relative, stage / relative)
for record in manifest['files']:
    if record['path'] in owned:
        record['sourceSha256'] = record['stageSha256'] = hashlib.sha256((stage / record['path']).read_bytes()).hexdigest()
path.write_text(json.dumps(manifest, indent=2) + '\n')
env = dict(os.environ, PATH=str(ROOT / 'artifacts/task-1.2/node-v24.22.0-linux-x64/bin') + ':' + os.environ['PATH'])
commands = [
    ['node', 'node_modules/typescript/bin/tsc', '--project', 'tests/unit/chart-application/tsconfig.json', '--noEmit'],
    ['node', 'node_modules/@biomejs/biome/bin/biome', 'check', 'src/components/General/Table/Chart/application', 'src/components/General/Table/Chart/compatibility/editorEvents.ts', 'src/components/General/Table/Chart/compatibility/optionStateTypes.ts', 'tests/unit/chart-application', 'tests/unit/chart-compatibility/editorEvents.test.ts'],
]
results = []
for index, command in enumerate(commands):
    result = subprocess.run(command, cwd=stage, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    log = OUT / f'final-check-{index}.log'
    log.write_text(result.stdout)
    results.append({'command': command, 'exitCode': result.returncode, 'log': str(log.relative_to(ROOT))})
    print(index, result.returncode, flush=True)
(OUT / 'final-command-status.json').write_text(json.dumps(results, indent=2) + '\n')
relevant = [r for r in manifest['files'] if r['path'].startswith(('src/components/General/Table/Chart/', 'tests/unit/chart-application/', 'tests/unit/chart-compatibility/')) or r['path'] in ['package.json', 'bun.lockb', 'biome.json']]
(OUT / 'frozen-scope.json').write_text(json.dumps({**{k: v for k, v in manifest.items() if k != 'files'}, 'files': relevant, 'ownedPaths': owned}, indent=2) + '\n')
