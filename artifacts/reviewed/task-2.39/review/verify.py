import pathlib, json, hashlib, subprocess
root = pathlib.Path('/mnt/d/Source/QOpenBB')
out = root/'artifacts/task-2.39/review'
manifest = json.loads((root/'artifacts/task-2.39/implementation/source-stage-manifest.json').read_text())
stage = pathlib.Path(manifest['stage'])
source = root/'vendor/workspace/terminalpro'
bad = []
for item in manifest['files']:
    for base, key in [(source, 'sourceSha256'), (stage, 'stageSha256')]:
        if hashlib.sha256((base/item['path']).read_bytes()).hexdigest() != item[key]:
            bad.append(str(base/item['path']))
(out/'identity.json').write_text(json.dumps({'workspaceHead': subprocess.check_output(['git','-C',str(source.parent),'rev-parse','HEAD'],text=True).strip(), 'stage':str(stage), 'checkedFiles': len(manifest['files']), 'mismatches':bad},indent=2)+'\n')
assert not bad, bad
node = root/'artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node'
commands = []
for suite in ['chart-application','chart-compatibility']:
    commands += [(suite, [str(node),'node_modules/vitest/vitest.mjs','run','--config',f'tests/unit/{suite}/vitest.config.mjs']), (suite+'-tsc',[str(node),'node_modules/typescript/bin/tsc','--project',f'tests/unit/{suite}/tsconfig.json','--noEmit'])]
commands += [('biome',[str(node),'node_modules/@biomejs/biome/bin/biome','check','src/components/General/Table/Chart/application','tests/unit/chart-application'])]
results=[]
for name, command in commands:
    with (out/(name+'.log')).open('w') as log:
        result = subprocess.run(command,cwd=stage,stdout=log,stderr=subprocess.STDOUT)
    results.append({'name':name,'command':command,'exit':result.returncode})
    print(name,result.returncode,flush=True)
(out/'commands.json').write_text(json.dumps(results,indent=2)+'\n')
