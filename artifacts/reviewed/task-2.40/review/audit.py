import json,hashlib,re,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[3];out=Path(__file__).resolve().parent;repo=root/'vendor/workspace'
def git(*args):return subprocess.check_output(['git','-C',str(repo),*args]).decode().strip()
head='76edf85a46298f7bc5212ff9944e4b66e9baa4af';base='945e438a9a65c3eeef7073dbce64a03b02f0ff6f'
assert git('rev-parse','HEAD')==head
prefix='terminalpro/'
paths=['src/components/General/Table/Chart/application/gridCapture.ts','tests/unit/chart-application/gridCapture.fixtures.json','tests/unit/chart-application/gridCapture.grid.test.ts','tests/unit/chart-application/gridCapture.test.ts','tests/unit/chart-application/tsconfig.json']
assert set(git('diff','--name-only',base,head).splitlines())=={prefix+p for p in paths}
assert not git('diff','HEAD','--',*[prefix+p for p in paths])
sha=lambda b:hashlib.sha256(b).hexdigest()
frozen={'src/components/General/Table/Chart/application/types.ts':'5e01f153244005180a284d591f0732fd24f5b1bec804c4c59a8e831cb4e8696e','tests/unit/chart-application/gridCapture.fixtures.json':'7d6a08a2360b241b0d1edd60ece10069cbd2d38295cdbfc87b979a53b429a3f4','tests/unit/chart-application/tsconfig.json':'4d8000a97707c3c82cfa0011d31e3ba72ba39a17a05c79753405bc077b948e1a'}
for p,h in frozen.items():assert sha((repo/prefix/p).read_bytes())==h,p
for p in paths:assert not re.search(r'\b(TBD|TODO|FIXME|HACK|XXX)\b',(repo/prefix/p).read_text()),p
quality=json.loads((out/'complexity.json').read_text());assert not quality['errors'] and not quality['violations']
assert len(quality['files'])==173
assert json.loads((root/'sources.lock.json').read_text())['workspace']['revision']==head
for name in ['workspace-changes.json','data-api-changes.json','owned-source-hashes.json']:
 assert json.loads((out/name).read_text())==json.loads((root/'artifacts/task-2.40'/name).read_text()),name
result={'head':head,'base':base,'changed_paths':[prefix+p for p in paths],'frozen_hashes':frozen,'maintained_file_count':len(quality['files']),'errors':quality['errors'],'violations':quality['violations'],'capture_measurement':next(x for x in quality['files'] if x['path'].endswith('/gridCapture.ts')),'current_manifests_match_controller':True}
(out/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
print('Five paths; frozen bytes, current manifests and pins match; 173 maintained files without errors/violations.')
