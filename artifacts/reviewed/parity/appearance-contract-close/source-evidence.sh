#!/bin/bash
set -eu
cd /mnt/d/Source/QOpenBB
pipeline/.venv/bin/python - <<'PY'
import hashlib,json,pathlib,subprocess
root=pathlib.Path('/home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules/ag-charts-community')
files=['package.json','LICENSE.txt','dist/package/main.cjs.js']
manifest={'installedDependency':{'name':'ag-charts-community','version':json.loads((root/'package.json').read_text())['version'],'license':'MIT','files':[{'path':str(root/f),'sha256':hashlib.sha256((root/f).read_bytes()).hexdigest()} for f in files]},'ownedSource':[]}
for f in ['terminalpro/package.json','terminalpro/src/components/General/Table/Chart/themes.tsx','terminalpro/src/components/General/Table/Chart/hooks/useChartOptions.tsx']:
 b=subprocess.check_output(['git','-C','vendor/workspace','show','38dffc33389aca0e4a87e0e88d42f7067aa220df:'+f]);manifest['ownedSource'].append({'path':f,'sha256':hashlib.sha256(b).hexdigest()})
pathlib.Path('artifacts/parity/appearance-contract-close/source-manifest.json').write_text(json.dumps(manifest,indent=2))
PY
