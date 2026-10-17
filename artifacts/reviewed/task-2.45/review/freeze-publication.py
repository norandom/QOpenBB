"""Freeze only inspected source-contract evidence for controller publication."""
import hashlib
import json
from pathlib import Path
import re

root = Path('/mnt/d/Source/QOpenBB')
out = root/'artifacts/task-2.45/review'
worker = root/'artifacts/task-2.43/implementation/publication-allowlist.json'
audit = json.loads((out/'audit.json').read_text())
omitted = {item['path'] for item in audit['publication_omissions']}
paths = {item['path'] for item in json.loads(worker.read_text())['files']} - omitted
paths.add(worker.relative_to(root).as_posix())
paths.update('artifacts/task-2.45/controller/'+name for name in [
    'complexity.json','workspace-changes.json','data-api-changes.json','owned-source-hashes.json'])
paths.update(path.relative_to(root).as_posix() for path in out.iterdir()
             if path.is_file() and path.name != 'publication-allowlist.json')
files = []
for relative in sorted(paths):
    path = root/relative
    assert not any(part in {'.env','node_modules','__pycache__'} for part in path.parts)
    content = path.read_text()
    assert not re.search(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', content), relative
    files.append({'path':relative,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
allowlist = {'scope':'Task 2.43 and joined task 2.45 source-contract review; frozen safe outputs only.',
             'omissions':audit['publication_omissions'],
             'notes':'Worker allowlist is retained as historical inventory. Its two full-stage manifest entries are deliberately omitted and replaced by labeled derivatives. This allowlist controls publication.',
             'files':files}
(out/'publication-allowlist.json').write_text(json.dumps(allowlist,indent=2)+'\n')
print(json.dumps({'files':len(files),'omissions':len(omitted),'status':'FROZEN'}))
