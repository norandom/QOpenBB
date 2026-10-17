import hashlib
import json
import math
import pathlib
import re
import subprocess

root = pathlib.Path('/mnt/d/Source/QOpenBB')
evidence = root / 'artifacts/parity/appearance-contract-close'
out = root / 'artifacts/parity/appearance-contract-review/corrected'
allowlist = json.loads((evidence / 'publication-allowlist.json').read_text())
checks = []
def record(name, passed, detail):
    checks.append(dict(name=name, passed=passed, detail=detail))
def sha(data):
    return hashlib.sha256(data).hexdigest()

for row in allowlist['files']:
    path = root / row['sourcePath']
    data = path.read_bytes()
    record('publication/' + row['sourcePath'], sha(data) == row['sha256'] and len(data) == row['bytes'], dict(sha256=sha(data), bytes=len(data)))
manifest = json.loads((evidence / 'source-manifest.json').read_text())
for row in manifest['installedDependency']['files']:
    data = pathlib.Path(row['path']).read_bytes()
    record('dependency/' + row['path'], sha(data) == row['sha256'], sha(data))
for row in manifest['ownedSource']:
    data = subprocess.check_output(['git', '-C', str(root / 'vendor/workspace'), 'show', '38dffc33389aca0e4a87e0e88d42f7067aa220df:' + row['path']])
    record('original/' + row['path'], sha(data) == row['sha256'], sha(data))

cases = json.loads((evidence / 'cases.json').read_text())
def finite(value):
    if isinstance(value, dict):
        return all(isinstance(k, str) and finite(v) for k, v in value.items())
    if isinstance(value, list):
        return all(finite(v) for v in value)
    if isinstance(value, float):
        return math.isfinite(value)
    return value is None or isinstance(value, (str, bool, int))
record('finite-case-data', finite(cases), len(cases))
record('unique-eight-case-ids', len({c['id'] for c in cases}) == len(cases) == 8, [c['id'] for c in cases])
record('no-callback-markers', '[callback]' not in json.dumps(cases), 'data-only derivative')
record('fresh-assertion-bytes', (out / 'offline/assertions.json').read_bytes() == (evidence / 'assertions.json').read_bytes(), sha((out / 'offline/assertions.json').read_bytes()))
patterns = re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:ghp|github_pat|sk_live)_[A-Za-z0-9_]{15,}|\bBearer\s+[A-Za-z0-9._-]{20,}')
matches = []
for row in allowlist['files']:
    path = root / row['sourcePath']
    if path.suffix != '.png' and patterns.search(path.read_text()):
        matches.append(row['sourcePath'])
record('concrete-secret-pattern-scan', not matches, matches)
record('no-private-publication-paths', not any(re.search(r'credential-private|(?:^|/)\.env|(?:^|/)state-|runtime\.json|raw-cases|diagnostics\.json|start\.log', x['sourcePath']) for x in allowlist['files']), len(allowlist['files']))
report = dict(passed=all(x['passed'] for x in checks), checks=checks, allowlistSha256=sha((evidence / 'publication-allowlist.json').read_bytes()))
(out / 'checks.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(dict(passed=report['passed'], checks=len(checks), allowlistSha256=report['allowlistSha256'])))
dep = pathlib.Path('/home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules/ag-charts-community')
pkg = json.loads((dep / 'package.json').read_text())
print(json.dumps(dict(version=pkg['version'], license=pkg['license'])))
lines = (dep / 'dist/package/main.cjs.js').read_text().splitlines()
for start, end in [(1185,1205),(1220,1243),(1370,1386),(1550,1565),(26223,26248),(26442,26457),(26888,26912),(33078,33100),(33135,33161)]:
    print('\n'.join(f'{i}: {lines[i-1]}' for i in range(start,end+1)))
raise SystemExit(0 if report['passed'] else 1)

