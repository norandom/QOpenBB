from pathlib import Path
import json,hashlib,subprocess
root=Path(__file__).resolve().parents[3];repo=root/'vendor/workspace'
base='945e438a9a65c3eeef7073dbce64a03b02f0ff6f'
head=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD']).decode().strip()
inv=json.loads((root/'.kiro/complexity-budgets.json').read_text())
paths=sorted({x['path'] for x in inv['exceptions'] if x['repository']=='workspace'})
sha=lambda b:hashlib.sha256(b).hexdigest()
rows=[]
for name in paths:
 original=subprocess.check_output(['git','-C',str(repo),'show',f'{base}:{name}'])
 committed=subprocess.check_output(['git','-C',str(repo),'show',f'{head}:{name}'])
 current=(repo/name).read_bytes()
 assert original==committed==current,name
 rows.append(dict(path=name,base_sha256=sha(original),head_sha256=sha(committed),working_sha256=sha(current)))
(root/'artifacts/task-2.40/review/exception-byte-audit.json').write_text(json.dumps(dict(base=base,head=head,files=rows),indent=2)+'\n')
print(f'{len(rows)} exception target files unchanged byte for byte')
