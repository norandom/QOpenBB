import json,tomllib,re,subprocess,hashlib
from pathlib import Path
root=Path('/mnt/d/Source/QOpenBB'); out=root/'artifacts/task-4.9/review'
spec=json.loads((root/'.kiro/specs/openbb-self-service/spec.json').read_text()); breadth=tomllib.loads((root/'.kiro/breadth.toml').read_text()); json.loads((root/'.kiro/complexity-budgets.json').read_text()); pins=json.loads((root/'sources.lock.json').read_text())
s=spec['persistence_repair_slice']; assert s['implementation_accepted'] and s['phase']=='implementation-complete' and s['source_revision']==pins['workspace']['revision'] and spec['ready_for_implementation'] is False
cap=next(c for c in breadth['capabilities'] if c['id']=='sqlite-query-and-storage-compatibility'); assert cap['status']=='passed' and len(cap['test_paths'])==4
for path in cap['test_paths']: assert (root/path).is_file()
assert '- [x] 4.9 ' in (root/'.kiro/specs/openbb-self-service/tasks.md').read_text()
paths=subprocess.check_output(['git','-C',str(root),'diff','--name-only'],text=True).splitlines(); checked=[]; bad=[]
for path in paths:
 if not path.endswith('.md'): continue
 for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',(root/path).read_text()):
  target=target.strip('<>').split('#')[0]
  if not target or re.match(r'^[a-z]+:',target): continue
  resolved=(root/path).parent/target
  checked.append({'source':path,'target':target})
  if not resolved.exists(): bad.append({'source':path,'target':target})
assert not bad,bad
fresh=json.loads((out/'full.json').read_text()); assert all(hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in fresh['sources'].items())
record={'json_toml':'PASS','slice_accepted':True,'overall_ready':False,'four_actual_tests':True,'task49_checked':True,'local_link_targets_checked':len(checked),'broken_links':bad,'runtime_hashes_unchanged':True,'source_pin':s['source_revision']};(out/'metadata.json').write_text(json.dumps(record,indent=2)+'\n'); print(json.dumps(record))
