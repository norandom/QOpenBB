from pathlib import Path
import json,re,hashlib
root=Path(__file__).resolve().parents[2]
out=root/'artifacts/grid-capture-tasks'
source=(root/'.kiro/specs/openbb-self-service/tasks.md').read_text()
draft=(out/'draft.md').read_text()
lines=source.splitlines()
for i,line in enumerate(lines):
 if line.startswith('| A: Workspace |'):
  lines[i]='| A: Workspace | Source-safe 2.34-2.37 are accepted; approved A2 design proposes sequential 2.38 -> 2.39 -> 2.40, pending task approval | Controller owns shared test setup/inventory; one Sol worker owns actual-grid fixture, capture adapter and its tests per bounded leaf | No parallel writers within A2; disjoint appearance/editor research may continue, with separate runtime implementation gates |'
 if line.startswith('| A: blocked renderer/catalog join |'):
  lines[i]='| A: blocked renderer/catalog join | Remaining grid/category paths, B2, mapper, C/D and real-app joins require their named frozen contracts and separately reviewed/approved task graphs | Ownership in the application integration design; no dispatch from this table | Historical 2.8-2.11/2.9 bindings are not executable replacement plans; neither 2.37 nor 2.40 unblocks this row |'
 if line.startswith('| A2 gridCapture |'):
  lines[i]='| A2 gridCapture | Explicit-category flat capture now has approved chart-grid-capture-design.md and proposed tasks 2.38-2.40, pending implementation approval. The canonical typed signature is unchanged. Numeric-only synthetic categories, general multiple-category resolution, arbitrary getter configuration, hidden-after-entry and remote/transformed cases retain separate missing evidence. |'
merged='\n'.join(lines)+'\n'
merged=merged.replace('Source-safe 2.34-2.37 acceptance does not satisfy renderer-complete eligibility.', 'Source-safe 2.34-2.37 or bounded A2 2.40 acceptance does not satisfy renderer-complete eligibility.')
merged=merged.replace('Acceptance of 2.37 alone does not satisfy this prerequisite.', 'Acceptance of 2.37 or 2.40 alone does not satisfy this prerequisite.')
merged=merged.replace('source-safe 2.37 is insufficient.', 'source-safe 2.37 or bounded A2 2.40 is insufficient.')
anchor='### Blocked application followups'
assert merged.count(anchor)==1
merged=merged.replace(anchor,draft.rstrip()+'\n\n'+anchor,1)
(out/'merged-preview.md').write_text(merged)
ids=re.findall(r'^- \[[ x]\] (\d+(?:\.\d+)?)\b',merged,re.M)
assert len(ids)==len(set(ids))
requirements=set(); group=None
for line in (root/'.kiro/specs/openbb-self-service/requirements.md').read_text().splitlines():
 m=re.match(r'### Requirement (\d+):',line)
 if m:group=m[1]
 m=re.match(r'(\d+)\. ',line)
 if m and group:requirements.add(group+'.'+m[1])
coverage=set()
for block in re.findall(r'_Requirements:\s*([^_]+)_',merged):coverage.update(re.findall(r'\d+\.\d+',block))
missing=sorted(requirements-coverage); assert not missing,missing
unknown=sorted(coverage-requirements); assert not unknown,unknown
edges={}
for block in re.split(r'(?=^- \[[ x]\] \d)',merged,flags=re.M):
 m=re.match(r'- \[[ x]\] (\d+(?:\.\d+)?)\b',block)
 if m:edges[m[1]]=[d for b in re.findall(r'_Depends:\s*([^_]+)_',block) for d in re.findall(r'\d+(?:\.\d+)?',b)]
assert not [(a,b) for a,bs in edges.items() for b in bs if b not in ids]
visiting=set();done=set()
def visit(n):
 assert n not in visiting,('cycle',n)
 if n in done:return
 visiting.add(n)
 for child in edges.get(n,[]):visit(child)
 visiting.remove(n);done.add(n)
for n in edges:visit(n)
result={'scope':'Task-plan mechanical checks only; no implementation or tests accepted','task_count':len(ids),'new_tasks':['2.38','2.39','2.40'],'requirement_count':len(requirements),'missing_requirements':missing,'unknown_requirements':unknown,'duplicate_ids':[],'explicit_dependency_cycles':[],'base_tasks_sha256':hashlib.sha256((root/'.kiro/specs/openbb-self-service/tasks.md').read_bytes()).hexdigest(),'draft_sha256':hashlib.sha256((out/'draft.md').read_bytes()).hexdigest()}
(out/'mechanical.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
