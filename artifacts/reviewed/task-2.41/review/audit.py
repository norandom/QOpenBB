import hashlib
import json
import re
from pathlib import Path

ROOT = Path('/mnt/d/Source/QOpenBB')
OUT = ROOT / 'artifacts/task-2.41/review'
IMPL = ROOT / 'artifacts/task-2.41/implementation'
SOURCE = ROOT / 'vendor/workspace/terminalpro'

def read(path):
    return json.loads(path.read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

fixture = read(SOURCE / 'tests/unit/chart-application/appearanceFixtures.json')
for path, expected in fixture['provenance']['files'].items():
    assert digest(ROOT / path) == expected, path
refs = ROOT / 'artifacts/reviewed/parity'
inputs = read(refs / 'appearance-saved-composition/case-inputs.json')
captures = read(refs / 'appearance-saved-composition/cases.json')
for case, original, captured in zip(fixture['composition'], inputs, captures, strict=True):
    assert case['id'] == original['id'] == captured['actionId']
    assert case['baseline']['options'] == original['saved'] == captured['syntheticSavedFixture']
    assert case['baseline']['model'] == captured['model']
    assert case['baseline']['options'] != case['baseline']['model']['chartOptions']
    assert case['baseline']['chartType'] == original['family']
    assert case['generated'] == {'common': {'legend': {'position': 'top'}}}
    assert captured['hookCombined']['common']['legend']['position']['value'] == 'top'
    assert case['expected']['common'] == case['generated']['common']
    assert {k: v for k, v in case['expected'].items() if k != 'common'} == {k: v for k, v in original['saved'].items() if k != 'common'}
assert fixture['provenance']['savedCompositionSource'] == read(refs / 'appearance-saved-composition/source-manifest.json')
assert fixture['provenance']['colorSource'] == read(refs / 'appearance-contract-close/source-manifest.json')
assert fixture['normalizedColors'] == read(refs / 'appearance-contract-close/normalized-color-evidence.json')
captured = next(c for c in read(refs / 'appearance-contract-close/cases.json') if c['id'] == 'explicit-derived-tokens')
color = fixture['colors'][0]
assert color['expected']['gridLineColor'] == captured['effective']['axes'][1]['gridLine']['style'][0]['stroke']
assert color['expected']['subtleTextColor'] == captured['effective']['subtitle']['color']['value']
assert fixture['invalidInputPolicy']['basis'] == 'Approved design policy, not runtime reference observation'
for item in read(IMPL / 'publication-allowlist.json')['files']:
    assert digest(IMPL / item['path']) == item['sha256'], item['path']
for path, expected in read(ROOT / 'artifacts/task-2.41/controller/frozen-hashes.json').items():
    assert digest(ROOT / path) == expected, path
quality = read(ROOT / 'artifacts/task-2.41/controller/complexity.json')
assert quality['errors'] == [] and quality['violations'] == []
measurement = next(f for f in quality['files'] if f['path'].endswith('/appearanceContracts.ts'))
contract = SOURCE / 'src/components/General/Table/Chart/application/appearanceContracts.ts'
assert measurement['physical'] == len(contract.read_text().splitlines()) == 34
assert measurement['logical'] <= 300 and not measurement['functions']
inventory = read(ROOT / '.kiro/complexity-budgets.json')
assert 'terminalpro/src/components/General/Table/Chart/application/appearanceContracts.ts' in json.dumps(inventory)
owned = read(IMPL / 'frozen-scope.json')['ownedPaths']
markers = []
secrets = []
for path in owned:
    content = (SOURCE / path).read_text()
    markers += [(path, m.group()) for m in re.finditer(r'\b(?:TBD|TODO|FIXME|HACK|XXX)\b', content)]
    secrets += [(path, m.group()) for m in re.finditer(r'(?:-----BEGIN .*PRIVATE KEY-----|sk-ant-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{30,})', content)]
assert not markers and not secrets
status = read(OUT / 'command-status.json')
assert all(c['exitCode'] == 0 for c in status)
ansi = re.compile(r'\x1b\[[0-9;]*m')
assert '88 passed (88)' in ansi.sub('', (OUT / 'check-3.log').read_text())
assert '260 passed (260)' in ansi.sub('', (OUT / 'check-4.log').read_text())
assert 'Unhandled Errors' not in (OUT / 'check-3.log').read_text()
result = {'status': 'PASS', 'referenceHashes': len(fixture['provenance']['files']), 'compositionFixtures': len(inputs), 'colors': 'Captured explicit tokens and normalized evidence match', 'productionMeasurement': measurement, 'maintainedFiles': len(quality['files']), 'markers': markers, 'secretPatterns': secrets, 'allCommandsExitZero': True}
(OUT / 'audit.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
