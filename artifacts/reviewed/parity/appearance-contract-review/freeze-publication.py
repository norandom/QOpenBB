import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
names = [
    'review.md', 'review-initial.md', 'check.py', 'checks.json',
    'reviewed-input-allowlist.json', 'math-check.cjs', 'math-check.json',
    'corrected/check.py', 'corrected/checks.json',
    'corrected/reviewed-input-allowlist.json',
    'corrected/offline/assertions.json',
    'corrected/offline/normalized-color-evidence.json',
    'freeze-publication.py',
    'publication-link-addendum.md', 'publication-link-check.py',
    'publication-link-check.json', 'publication-input-allowlist.json',
]
files = []
for name in names:
    data = (root / name).read_bytes()
    files.append({'sourcePath': 'artifacts/parity/appearance-contract-review/' + name,
                  'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)})
result = {'frozen': True, 'reviewRequired': False, 'files': files,
          'excluded': ['copied offline inputs and scripts already in the reviewed capture allowlist',
                       'check-output.txt because it reproduces dependency source excerpts',
                       'preserve-initial.py because it only reconstructs a historical allowlist']}
(root / 'publication-allowlist.json').write_text(json.dumps(result, indent=2) + '\n')
print(hashlib.sha256((root / 'publication-allowlist.json').read_bytes()).hexdigest())
