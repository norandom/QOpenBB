from pathlib import Path
import json,subprocess,hashlib
root=Path(__file__).resolve().parents[2]
repo=root/'vendor/workspace'
def git(*args): return subprocess.check_output(['git','-C',str(repo),*args]).decode().strip()
base='945e438a9a65c3eeef7073dbce64a03b02f0ff6f'
head=git('rev-parse','HEAD')
allowed={
 'terminalpro/src/components/General/Table/Chart/application/gridCapture.ts',
 'terminalpro/tests/unit/chart-application/gridCapture.fixtures.json',
 'terminalpro/tests/unit/chart-application/gridCapture.grid.test.ts',
 'terminalpro/tests/unit/chart-application/gridCapture.test.ts',
 'terminalpro/tests/unit/chart-application/tsconfig.json',
}
changed=set(git('diff','--name-only',base,head).splitlines())
assert changed<=allowed,changed-allowed
assert not git('diff','HEAD','--',*sorted(allowed))
frozen=repo/'terminalpro/src/components/General/Table/Chart/application/types.ts'
assert hashlib.sha256(frozen.read_bytes()).hexdigest()=='5e01f153244005180a284d591f0732fd24f5b1bec804c4c59a8e831cb4e8696e'
result=dict(base=base,head=head,changed_paths=sorted(changed),frozen_types_sha256=hashlib.sha256(frozen.read_bytes()).hexdigest(),scope='Only ordinary capture and its fixture/tests/config changed. Existing helpers, reducers, mapper, snapshot, host, UI and flags unchanged from accepted base. Unrelated dirty work remains excluded from acceptance.')
(root/'artifacts/task-2.40/boundary-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
