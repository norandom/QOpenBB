import hashlib,json,subprocess,sys,re
from pathlib import Path
root=Path('/mnt/d/Source/QOpenBB'); out=root/'artifacts/task-4.9/review'; ws=root/'vendor/workspace'; base='b96d36d16ba87db2dd595d5796507d473dd0c0c6'; head='f23cb786a946a6a996deedbe87be9c7ca86b221e'; crud='backend-api/backend/api/crud.py'
def git(*args): return subprocess.check_output(['git','-C',str(ws),*args])
changes=git('diff','--name-only',base,head).decode().splitlines()
diff=git('diff',base,head,'--',crud).decode(); (out/'production.diff').write_text(diff)
assert len(changes)==9 and sum('func.concat' in l for l in diff.splitlines() if l.startswith('-'))==6
assert sum('.join(User, User.uuid == DashboardItem.creator_uuid)' in l for l in diff.splitlines() if l.startswith('+'))==1
assert git('diff',head,'--',crud,'backend-api/backend/tests_sqlite')==b''
assert git('diff',base,head,'--','backend-api/backend/poetry.lock','backend-api/backend/pyproject.toml')==b''
assert git('rev-parse','HEAD').decode().strip()==head
before=hashlib.sha256(git('show',base+':'+crud)).hexdigest(); after=hashlib.sha256((ws/crud).read_bytes()).hexdigest()
assert after=='575b2cdeb0f04aab81af60b34074e4b9c2c6e21cfb6559c695e502361defc6e9'
inv=json.loads((root/'.kiro/complexity-budgets.json').read_text()); exc=[x for x in inv['exceptions'] if x['path']==crud]
assert len(exc)==2 and {x['metric'] for x in exc}=={'physical','logical'} and all(x['revision']==head and x['expires_on']=='2026-11-17' for x in exc)
rebound=[]
for path in sorted({x['path'] for x in inv['exceptions'] if x['path']!=crud}):
 assert git('diff',base,head,'--',path)==b''; rebound.append(path)
assert json.loads((root/'sources.lock.json').read_text())['workspace']['revision']==head
added=[l[1:] for l in git('diff',base,head).decode().splitlines() if l.startswith('+') and not l.startswith('+++')]
markers=[l for l in added if re.search(r'\b(TBD|TODO|FIXME|HACK|XXX)\b',l)]
assert not markers
format_results=[]
for label,content in [('baseline',git('show',base+':'+crud)),('patched',(ws/crud).read_bytes())]:
 cmd=[sys.executable,'-m','ruff','format','--check','--stdin-filename',str(ws/crud),'-']
 p=subprocess.run(cmd,input=content,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (out/(label+'-format.log')).write_bytes(p.stdout);format_results.append({'label':label,'command':cmd,'exit':p.returncode})
record={'root_revision':subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip(),'baseline':base,'workspace':head,'changed_files':changes,'crud_before':before,'crud_after':after,'exceptions':exc,'unchanged_rebound_exception_files':rebound,'markers':markers,'secrets_review':'Only explicitly synthetic test configuration introduced; no real secrets. No private configuration read.','format':format_results}
(out/'audit.json').write_text(json.dumps(record,indent=2)+'\n'); print(json.dumps(record,indent=2))
