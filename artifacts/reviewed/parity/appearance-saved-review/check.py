import hashlib
import json
import math
import pathlib
import re
import subprocess

root = pathlib.Path('/mnt/d/Source/QOpenBB')
source = root / 'artifacts/parity/appearance-saved-composition'
out = root / 'artifacts/parity/appearance-saved-review'
checks = []
def record(name, passed, detail):
    checks.append(dict(name=name, passed=passed, detail=detail))
def sha(data):
    return hashlib.sha256(data).hexdigest()
allowlist = json.loads((source / 'publication-allowlist.json').read_text())
for row in allowlist['files']:
    data = (root / row['sourcePath']).read_bytes()
    record('publication/' + row['sourcePath'], sha(data) == row['sha256'] and len(data) == row['bytes'], dict(sha256=sha(data), bytes=len(data)))
manifest = json.loads((source / 'source-manifest.json').read_text())
for row in manifest['files']:
    data = subprocess.check_output(['git', '-C', str(root / 'vendor/workspace'), 'show', manifest['source'] + ':' + row['path']])
    record('original/' + row['path'], sha(data) == row['sha256'], sha(data))
rows = json.loads((source / 'cases.json').read_text())
def finite(v):
    if isinstance(v, dict):
        return all(isinstance(k, str) and finite(x) for k, x in v.items())
    if isinstance(v, list):
        return all(finite(x) for x in v)
    if isinstance(v, float):
        return math.isfinite(v)
    return v is None or isinstance(v, (str, int, bool))
record('finite-data', finite(rows), len(rows))
record('unique-case-ids', {r['actionId'] for r in rows} == {'bar-common', 'bar-family', 'line-common', 'line-family'}, [r['actionId'] for r in rows])
for row in rows:
    effective = row['effective']
    record(row['actionId'] + '/series-identities', [s['yKey'] for s in effective['series']] == ['revenue', 'operatingIncome'], [s['yKey'] for s in effective['series']])
    record(row['actionId'] + '/two-axes', {a['type'] for a in effective['axes']} == {'category', 'number'} and len(effective['axes']) == 2, len(effective['axes']))
    family = 'line' if row['requestedFamily'] == 'line' else 'bar'
    if row['actionId'].endswith('family'):
        branch = row['hookCombined'][family]
        saved = row['syntheticSavedFixture'][family]
        record(row['actionId'] + '/hook-family-title', branch['title']['text']['value'] == saved['title']['text'], branch['title']['text'])
        record(row['actionId'] + '/hook-family-left-label', branch['axes']['number']['left']['label']['color']['value'] == saved['axes']['number']['left']['label']['color'], branch['axes']['number']['left']['label'])
        record(row['actionId'] + '/hook-family-stroke', branch['series']['stroke']['value'] == saved['series']['stroke'], branch['series']['stroke'])
record('fresh-assertions-identical', (out / 'offline/assertions.json').read_bytes() == (source / 'assertions.json').read_bytes(), sha((out / 'offline/assertions.json').read_bytes()))
record('callback-markers-absent', '[callback]' not in json.dumps(rows), 'data-only projections')
patterns = re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:ghp|github_pat|sk_live)_[A-Za-z0-9_]{15,}|\bBearer\s+[A-Za-z0-9._-]{20,}')
matches = [r['sourcePath'] for r in allowlist['files'] if pathlib.Path(r['sourcePath']).suffix != '.png' and patterns.search((root / r['sourcePath']).read_text())]
record('secret-pattern-scan', not matches, matches)
record('excluded-private-paths', not any(re.search(r'credential-private|(?:^|/)\.env|(?:^|/)state-|runtime\.json|widget-writes|diagnostics\.json|\.log$', r['sourcePath']) for r in allowlist['files']), len(allowlist['files']))
result = dict(passed=all(c['passed'] for c in checks), checks=checks, allowlistSha256=sha((source / 'publication-allowlist.json').read_bytes()))
(out / 'checks.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(dict(passed=result['passed'], checks=len(checks), allowlistSha256=result['allowlistSha256'])))
raise SystemExit(0 if result['passed'] else 1)
