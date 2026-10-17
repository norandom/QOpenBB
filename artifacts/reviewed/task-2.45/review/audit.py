"""Audit explicit review inputs and create limited publication derivatives."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path('/mnt/d/Source/QOpenBB')
OUT = ROOT/'artifacts/task-2.45/review'
SOURCE = ROOT/'vendor/workspace/terminalpro'
WORKER = ROOT/'artifacts/task-2.43/implementation'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text())

def git_bytes(revision, path):
    return subprocess.check_output(['git', '-C', str(SOURCE.parent), 'show', revision+':'+path])

stage = read(OUT/'stage.json')
closure = {item['path'] for item in stage['inputs']}
assert all(digest(SOURCE/item['path']) == item['sha256'] for item in stage['inputs'])
worker = read(WORKER/'publication-allowlist.json')
assert len(worker['files']) == 29
for item in worker['files']:
    assert digest(ROOT/item['path']) == item['sha256'], item['path']
omissions = []
for name in ['red-stage-manifest.json', 'source-manifest.json']:
    original = WORKER/name
    data = read(original)
    selected = [item for item in data['files'] if item['path'] in closure]
    target = OUT/('task243-'+name)
    derived = {key:value for key,value in data.items() if key != 'files'}
    derived.update({'derivative':True, 'source_path':original.relative_to(ROOT).as_posix(),
                    'source_sha256':digest(original), 'original_file_entries':len(data['files']),
                    'transformation':'Retain only the reviewed chart source/test/config closure; omit unrelated full-stage traversal entries.',
                    'files':selected})
    target.write_text(json.dumps(derived, indent=2)+'\n')
    omissions.append({'path':original.relative_to(ROOT).as_posix(), 'sha256':digest(original),
                      'reason':'Full-stage traversal; replaced by labeled closure derivative.',
                      'derivative':target.relative_to(ROOT).as_posix()})
fixture = read(SOURCE/'tests/unit/chart-application/appearanceFixtures.json')
references = []
for path, expected in fixture['provenance']['files'].items():
    assert digest(ROOT/path) == expected, path
    references.append({'path':path, 'sha256':expected})
normalized = read(ROOT/'artifacts/reviewed/parity/appearance-contract-close/normalized-color-evidence.json')
assert fixture['normalizedColors'] == normalized
assert sum(item['channelPairs'] for item in normalized['ratios']) == 262144
assert all(item['normalizedMismatches'] == 0 for item in normalized['ratios'])
frozen = []
for path in ['src/components/General/Table/Chart/application/appearanceContracts.ts',
             'tests/unit/chart-application/appearanceContracts.types.ts',
             'tests/unit/chart-application/appearanceFixtures.json']:
    expected = git_bytes('bc42d60', 'terminalpro/'+path)
    assert expected == (SOURCE/path).read_bytes(), path
    frozen.append({'path':path, 'sha256':digest(SOURCE/path)})
assert digest(SOURCE/'tests/unit/chart-application/gridCapture.grid.test.ts') == '47c9793abc7d528d15b3fce807e669d6ef168b88d2c6f213ac316bfe5d4e41b0'
quality_path = ROOT/'artifacts/task-2.45/controller/complexity.json'
quality = read(quality_path)
assert not quality['errors'] and not quality['violations']
assert len(quality['files']) == 176
owned = read(ROOT/'artifacts/task-2.45/controller/owned-source-hashes.json')
for path, expected in owned.items():
    assert digest(ROOT/path) == expected, path
exceptions = []
for path in sorted({item['path'] for item in quality['exceptions']}):
    expected = git_bytes('0a4b2ea', path)
    actual = SOURCE.parent/path
    assert expected == actual.read_bytes(), path
    exceptions.append({'path':path, 'sha256':digest(actual), 'exact_matches_revision':'0a4b2ea'})
production = ['application/appearanceContracts.ts', 'application/appearanceComposition.ts',
              'application/appearanceColors.ts', 'application/sessionState.ts',
              'compatibility/editorEvents.ts', 'compatibility/optionStateTypes.ts']
prefix = 'src/components/General/Table/Chart/'
metrics = []
for path in production:
    row = next(item for item in quality['files'] if item['repository']=='workspace' and item['path']=='terminalpro/'+prefix+path)
    assert row['physical'] <= 400 and row['logical'] <= 300
    assert all(item['logical'] <= 50 for item in row['functions'])
    assert len((SOURCE/prefix/path).read_text().splitlines()) == row['physical']
    metrics.append(row)
changed = subprocess.check_output(['git','-C',str(SOURCE.parent),'diff','--name-only','76edf85..HEAD']).decode().splitlines()
assert all(path.startswith('terminalpro/src/components/General/Table/Chart/') or path.startswith('terminalpro/tests/unit/chart-') for path in changed)
preserved = ['src/components/General/Table/Chart/compatibility/optionState.ts',
             'src/components/General/Table/Chart/compatibility/integratedState.ts',
             'src/components/General/Table/Chart/application/types.ts','package.json','bun.lock']
for path in preserved:
    assert git_bytes('76edf85', 'terminalpro/'+path) == (SOURCE/path).read_bytes(), path
markers = []
secrets = []
for path in [prefix+p for p in production] + ['tests/unit/chart-application/appearanceColors.test.ts']:
    contents = (SOURCE/path).read_text()
    if re.search(r'\b(?:TBD|TODO|FIXME|HACK|XXX)\b', contents): markers.append(path)
    if re.search(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:api_key|password|secret|token)\s*=\s*[\"\'][^\"\']{12,}', contents, re.I): secrets.append(path)
assert not markers and not secrets
dependencies = []
deps = Path(stage['dependencies'])
for name in ['typescript','vitest','@biomejs/biome','lodash.merge','lodash','ag-grid-community','echarts']:
    path = deps/name/'package.json'
    dependencies.append({'name':name,'version':read(path)['version'],'package_sha256':digest(path)})
result = {'worker_allowlist_entries_verified':len(worker['files']), 'frozen_contracts':frozen,
          'reference_artifacts_verified':references, 'historical_normalized_comparisons':262144,
          'current_closure_entries':len(closure), 'workspace_head':stage['workspaceHead'],
          'controller_complexity':{'path':quality_path.relative_to(ROOT).as_posix(),'sha256':digest(quality_path),
                                  'files':len(quality['files']),'errors':[],'violations':[],
                                  'note':'Measured before tooltip commit at 0a4b2ea; eight owned source identities match current bytes. Parent reconciles final revision pins separately.'},
          'owned_source_identities_verified':owned,'exception_bytes_verified':exceptions,'task_metrics':metrics,
          'preserved_dependency_paths':preserved, 'changed_committed_paths':changed,
          'placeholder_matches':markers,'concrete_secret_matches':secrets,'dependencies':dependencies,
          'publication_omissions':omissions}
(OUT/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'worker_hashes':len(worker['files']),'closure':len(closure),'references':len(references),
                  'quality_files':len(quality['files']),'exception_files':len(exceptions),'status':'PASS'}))
