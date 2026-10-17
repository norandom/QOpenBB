import hashlib
import json
from pathlib import Path

root = Path('/mnt/d/Source/QOpenBB')
review = root / 'artifacts/parity/appearance-contract-review'
old = json.loads((review / 'corrected/reviewed-input-allowlist.json').read_text())
path = root / 'artifacts/parity/appearance-contract-close/publication-allowlist.json'
new = json.loads(path.read_text())
old_rows = {row['sourcePath']: row for row in old['files']}
changed = []
for row in new['files']:
    data = (root / row['sourcePath']).read_bytes()
    assert hashlib.sha256(data).hexdigest() == row['sha256']
    assert len(data) == row['bytes']
    if row != old_rows[row['sourcePath']]:
        changed.append(row['sourcePath'])
assert len(new['files']) == len(old['files'])
assert changed == ['.kiro/specs/openbb-self-service/chart-appearance-contract-close.md']
result = {'passed': True, 'files': len(new['files']), 'changed': changed,
          'allowlistSha256': hashlib.sha256(path.read_bytes()).hexdigest(),
          'specSha256': next(row['sha256'] for row in new['files'] if row['sourcePath'] == changed[0])}
(review / 'publication-link-check.json').write_text(json.dumps(result, indent=2) + '\n')
(review / 'publication-input-allowlist.json').write_bytes(path.read_bytes())
print(json.dumps(result))
