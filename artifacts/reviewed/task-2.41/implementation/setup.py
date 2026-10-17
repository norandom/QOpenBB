import datetime
import hashlib
import json
import pathlib
import shutil
import subprocess

ROOT = pathlib.Path('/mnt/d/Source/QOpenBB')
OUT = ROOT / 'artifacts/task-2.41/implementation'
SOURCE = ROOT / 'vendor/workspace/terminalpro'
REFERENCE = ROOT / 'artifacts/reviewed/parity'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text())

def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')

provenance = {}
for folder, names in {
    'appearance-saved-composition': ['source-manifest.json', 'case-inputs.json', 'cases.json', 'assertions.json'],
    'appearance-contract-close': ['source-manifest.json', 'cases.json', 'normalized-color-evidence.json'],
}.items():
    for name in names:
        path = REFERENCE / folder / name
        provenance[str(path.relative_to(ROOT))] = digest(path)

saved = read(REFERENCE / 'appearance-saved-composition/case-inputs.json')
observations = read(REFERENCE / 'appearance-saved-composition/cases.json')
composition = []
for item, captured in zip(saved, observations, strict=True):
    assert item['id'] == captured['actionId']
    assert item['saved'] == captured['syntheticSavedFixture']
    # This data-only projection uses the observed generated legend winner.
    assert captured['hookCombined']['common']['legend']['position']['value'] == 'top'
    common = {'legend': {'position': 'top'}}
    composition.append({
        'id': item['id'],
        'referenceActionId': captured['actionId'],
        'baseline': {'stateAddress': 'synthetic', 'chartType': item['family'],
                     'model': captured['model'], 'options': item['saved']},
        'generated': {'common': common},
        'expected': {'common': common, **{k: v for k, v in item['saved'].items() if k != 'common'}},
        'observedCommonLegendPosition': 'top',
    })

captured_colors = read(REFERENCE / 'appearance-contract-close/cases.json')[-1]
assert captured_colors['id'] == 'explicit-derived-tokens'
color = {
    'id': 'explicit-derived-tokens',
    'tokens': {'base': 'ag-default-dark', 'foregroundColor': '#123456',
               'backgroundColor': '#26394a', 'textColor': '#123456', 'chartBackgroundColor': '#26394a'},
    'expected': {'status': 'resolved',
                 'gridLineColor': captured_colors['effective']['axes'][1]['gridLine']['style'][0]['stroke'],
                 'subtleTextColor': captured_colors['effective']['subtitle']['color']['value']},
}
fixture = {
    'provenance': {'files': provenance,
                   'savedCompositionSource': read(REFERENCE / 'appearance-saved-composition/source-manifest.json'),
                   'colorSource': read(REFERENCE / 'appearance-contract-close/source-manifest.json')},
    'scope': 'Finite data-only projections; expected composition follows the pinned owned common-replacement operation. No final theme inheritance is inferred.',
    'composition': composition,
    'colors': [color],
    'normalizedColors': read(REFERENCE / 'appearance-contract-close/normalized-color-evidence.json'),
    'invalidInputPolicy': {'basis': 'Approved design policy, not runtime reference observation',
        'composition': ['accessors', 'nonplain objects', 'cycles', 'throwing proxies'],
        'colorsInvalid': ['missing field', 'non-string token', 'unknown own field', 'accessor', 'nonplain object', 'throwing proxy'],
        'colorsUnresolved': ['unsupported string base', 'string outside opaque six-digit hex']},
}
write(SOURCE / 'tests/unit/chart-application/appearanceFixtures.json', fixture)

base = pathlib.Path('/home/mc/qopenbb-work/task241-' + datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
stage = base / 'terminalpro'
stage.mkdir(parents=True)
records = []
paths = [p for folder in ['src', 'tests'] for p in (SOURCE / folder).rglob('*') if p.is_file()]
paths += [p for p in SOURCE.iterdir() if p.is_file() and (p.suffix in ['.json', '.jsonc', '.mjs', '.js', '.ts'] or p.name == 'bun.lockb')]
for path in paths:
    relative = path.relative_to(SOURCE)
    dest = stage / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, dest)
    records.append({'path': str(relative), 'sourceSha256': digest(path), 'stageSha256': digest(dest)})
deps = pathlib.Path('/home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules')
(stage / 'node_modules').symlink_to(deps, target_is_directory=True)
packages = {}
for package in ['typescript', 'vitest', '@biomejs/biome', 'jsdom', 'lodash', 'echarts']:
    path = deps / package / 'package.json'
    packages[package] = {'version': read(path)['version'], 'packageSha256': digest(path)}
write(OUT / 'source-stage-manifest.json', {'stage': str(stage), 'workspaceHead': subprocess.check_output(['git', '-C', str(SOURCE.parent), 'rev-parse', 'HEAD'], text=True).strip(), 'dependencies': packages, 'files': records})
(OUT / 'stage-path.txt').write_text(str(stage) + '\n')
print(stage)
