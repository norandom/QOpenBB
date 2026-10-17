import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
names = ['review.md', 'check.py', 'checks.json', 'reviewed-input-allowlist.json',
         'offline/assertions.json', 'freeze-publication.py']
rows = []
for name in names:
    data = (root / name).read_bytes()
    rows.append({'sourcePath': 'artifacts/parity/appearance-saved-review/' + name,
                 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)})
result = {'frozen': True, 'reviewRequired': False, 'files': rows,
          'excluded': ['copied offline inputs already present in the approved capture publication set']}
(root / 'publication-allowlist.json').write_text(json.dumps(result, indent=2) + '\n')
print(hashlib.sha256((root / 'publication-allowlist.json').read_bytes()).hexdigest())
