from pathlib import Path
import json, subprocess, hashlib, shutil
root=Path(__file__).resolve().parents[2]
repo=root/'vendor/workspace'
head=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD']).decode().strip()
base='f23cb786a946a6a996deedbe87be9c7ca86b221e'
paths=subprocess.check_output(['git','-C',str(repo),'diff','--name-only',base,head]).decode().splitlines()
allowed=('terminalpro/src/components/General/Table/Chart/application/', 'terminalpro/tests/unit/chart-application/')
assert all(p.startswith(allowed) for p in paths), paths
assert not subprocess.check_output(['git','-C',str(repo),'diff','HEAD','--',*allowed]).strip()
types=repo/allowed[0]/'types.ts'
assert hashlib.sha256(types.read_bytes()).hexdigest()=='5e01f153244005180a284d591f0732fd24f5b1bec804c4c59a8e831cb4e8696e'
result=dict(base=base,head=head,changed_paths=paths,scope='Only new application helpers and tests changed since pre-slice source. Existing reducers, mapper, snapshot, host, controls and flags have no committed changes.',frozen_types_sha256=hashlib.sha256(types.read_bytes()).hexdigest())
(root/'artifacts/task-2.37/boundary-audit.json').write_text(json.dumps(result,indent=2)+'\n')
for name in ('complexity.json','workspace-changes.json','data-api-changes.json','owned-source-hashes.json'):
    shutil.copyfile(root/'artifacts/chart-application-implementation'/name,root/'artifacts/task-2.37'/name)
print(json.dumps(dict(head=head,changed_files=len(paths))))
