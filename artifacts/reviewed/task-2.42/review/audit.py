"""Audit only explicit synthetic task evidence and its frozen input closure."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path('/mnt/d/Source/QOpenBB')
OUT = ROOT / 'artifacts/task-2.42/review'
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

worker = json.loads((ROOT/'artifacts/task-2.42/implementation/publication-allowlist.json').read_text())
for item in worker['sourceFiles'] + worker['evidenceFiles']:
    assert digest(ROOT/item['path']) == item['sha256'], item['path']
controller = ['complexity-stale-manifest-failure.json', 'complexity.json',
              'data-api-changes.json', 'owned-source-hashes.json', 'workspace-changes.json']
quality = json.loads((ROOT/'artifacts/task-2.42/controller/complexity.json').read_text())
assert quality['errors'] == [] and quality['violations'] == []
metric = next(f for f in quality['files'] if f['path'].endswith('/appearanceComposition.ts'))
assert metric['physical'] <= 400 and metric['logical'] <= 300
assert all(f['logical'] <= 50 for f in metric['functions'])
fixture = ROOT/'vendor/workspace/terminalpro/tests/unit/chart-application/appearanceFixtures.json'
provenance = json.loads(fixture.read_text())['provenance']['files']
for path, expected in provenance.items():
    assert digest(ROOT/path) == expected, path
stage = json.loads((OUT/'stage.json').read_text())
assert all(digest(Path(stage['stage'])/p['path']) == p['sha256'] for p in stage['inputs'])
source = subprocess.check_output(['git', '-C', str(ROOT/'vendor/workspace'), 'show',
    '38dffc33389aca0e4a87e0e88d42f7067aa220df:terminalpro/src/components/General/Table/Chart/hooks/useChartOptions.tsx'])
assert b'chartOptions.common = options.common;' in source
assert b'return merge(options, chartOptions)' in source
owned_text = '\n'.join((ROOT/p['path']).read_text() for p in worker['sourceFiles'])
assert not re.search(r'\b(TBD|TODO|FIXME|HACK|XXX)\b', owned_text)
paths = [p['path'] for p in worker['evidenceFiles']]
paths.append('artifacts/task-2.42/implementation/publication-allowlist.json')
paths.extend('artifacts/task-2.42/controller/'+p for p in controller)
review_names = ['verify.py', 'audit.py', 'stage.json', 'results.json',
                'application-strict.log', 'compatibility-strict.log', 'application-suite.log',
                'compatibility-suite.log', 'scoped-lint.log', 'review.md', 'audit.json']
dependency_versions = {}
for package in ['vitest', 'typescript', 'lodash.merge', '@biomejs/biome']:
    path = Path(stage['dependencies'])/package/'package.json'
    dependency_versions[package] = {'version': json.loads(path.read_text())['version'], 'packageSha256': digest(path)}
audit = {'workerHashesMatch': True, 'fixtureProvenanceHashesMatch': True,
         'immutableClosureUnchanged': True, 'placeholderScan': 'CLEAN',
         'qualityErrors': quality['errors'], 'qualityViolations': quality['violations'],
         'qualityFileCount': len(quality['files']), 'compositionMetrics': metric,
         'dependencyVersions': dependency_versions,
         'scope': 'Task 2.42 against accepted bc42d60 sibling closure; no current tooltip acceptance'}
(OUT/'audit.json').write_text(json.dumps(audit, indent=2)+'\n')
paths.extend('artifacts/task-2.42/review/'+p for p in review_names)
secret = re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----|\bsk-(?:ant-)?[A-Za-z0-9_-]{24,}|\bgh[pousr]_[A-Za-z0-9]{20,}')
for path in paths:
    assert not secret.search((ROOT/path).read_text()), path
allow = {'task': '2.42', 'reviewVerdict': 'APPROVED', 'verificationStatus': 'VERIFIED',
         'sourceFiles': worker['sourceFiles'],
         'evidenceFiles': [{'path': p, 'sha256': digest(ROOT/p)} for p in paths],
         'omittedHistoricalEvidence': [],
         'review': 'Independent review of explicit completed synthetic scripts, logs, JSON and report; all worker failures and controller stale-manifest failure retained.',
         'exclusions': ['credentials', 'environment files', 'dependency caches', 'user accounts and database state', 'browser profiles', 'image archives', 'unowned source content'],
         'scope': 'Explicit files only, no full repository traversal. No source file is copied to the evidence mirror by this allowlist.'}
(OUT/'publication-allowlist.json').write_text(json.dumps(allow, indent=2)+'\n')
print(json.dumps(audit, indent=2))
