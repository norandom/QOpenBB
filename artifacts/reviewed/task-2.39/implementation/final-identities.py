import pathlib,json,hashlib,subprocess
root=pathlib.Path('/mnt/d/Source/QOpenBB');out=root/'artifacts/task-2.39/implementation'
man=json.loads((out/'source-stage-manifest.json').read_text());stage=pathlib.Path(man['stage']);source=root/'vendor/workspace/terminalpro'
for entry in man['files']:
 entry['sourceSha256']=hashlib.sha256((source/entry['path']).read_bytes()).hexdigest()
 entry['stageSha256']=hashlib.sha256((stage/entry['path']).read_bytes()).hexdigest()
 entry['matched']=entry['sourceSha256']==entry['stageSha256']
man['rootHead']=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
man['workspaceStatus']=subprocess.check_output(['git','-C',str(source.parent),'status','--short'],text=True)
(out/'source-stage-manifest.json').write_text(json.dumps(man,indent=2)+'\n')
assert all(entry['matched'] for entry in man['files']), 'Source/stage mismatch; inspect manifest'
