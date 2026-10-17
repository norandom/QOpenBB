import json,hashlib,re
from pathlib import Path
root=Path(__file__).resolve().parents[3];out=Path(__file__).resolve().parent
controller=['check.sh','check.log','check.exit','identity.py','identity.json','identity.log','identity.exit','boundary.py','boundary-audit.json','commands.md','complexity.json','workspace-changes.json','data-api-changes.json','owned-source-hashes.json','quality.log','quality.exit','prepare-records.py','exception-byte-audit.py','exception-byte-audit.json']
review=['check.sh','check.log','check.exit','identity.py','identity.json','identity.log','identity.exit','scope.py','scope.log','scope.exit','workspace-changes.json','data-api-changes.json','owned-source-hashes.json','quality.sh','quality.log','quality.exit','complexity.json','exception-byte-audit.py','exception-byte-audit.json','exception-byte-audit.log','exception-byte-audit.exit','audit.py','audit.json','audit.log','audit.exit','verdict.md','publication.py']
paths=['artifacts/task-2.40/'+p for p in controller]+['artifacts/task-2.40/review/'+p for p in review]+['artifacts/grid-capture-implementation/'+p for p in ['scope.py','quality.sh','advance.py']]
records=[]
for p in paths:
 data=(root/p).read_bytes();text=data.decode('utf-8-sig')
 assert not re.search(r'(?:gh[pousr]_[A-Za-z0-9]{25,}|sk-ant-[A-Za-z0-9_-]{20,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----)',text),p
 records.append({'source':p,'sha256':hashlib.sha256(data).hexdigest(),'sanitization':'none; reviewed synthetic/source identity evidence'})
(out/'publication-allowlist.json').write_text(json.dumps({'files':records,'additional_manifest':'artifacts/task-2.40/review/publication-allowlist.json','excluded':['stage-path.txt','inventory-index.json','scratch audit','active/shared outputs','environment/private data','dependencies'],'note':'Controller records final source and published hashes, including this manifest, before staging.'},indent=2)+'\n')
print(f'{len(records)} reviewed finished files allowlisted; no concrete credential patterns.')
