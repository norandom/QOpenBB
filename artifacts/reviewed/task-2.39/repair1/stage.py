import pathlib,shutil,hashlib,json,subprocess,datetime
root=pathlib.Path('/mnt/d/Source/QOpenBB'); source=root/'vendor/workspace/terminalpro'
base=pathlib.Path('/home/mc/qopenbb-work/task239repair1-'+datetime.datetime.now().strftime('%Y%m%d%H%M%S')); stage=base/'terminalpro'; stage.mkdir(parents=True)
records=[]
for folder in ['src','tests']:
 for p in (source/folder).rglob('*'):
  if p.is_file():
   rel=p.relative_to(source); dest=stage/rel; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(p,dest)
   records.append({'path':str(rel),'sourceSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'stageSha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
for p in source.iterdir():
 if p.is_file() and (p.suffix in ['.json','.jsonc','.mjs','.js','.ts'] or p.name=='bun.lockb'):
  dest=stage/p.name;shutil.copyfile(p,dest);records.append({'path':p.name,'sourceSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'stageSha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
(stage/'node_modules').symlink_to('/home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules',target_is_directory=True)
out=root/'artifacts/task-2.39/repair1';(out/'stage-path.txt').write_text(str(stage)+'\n');(out/'source-stage-manifest.json').write_text(json.dumps({'stage':str(stage),'workspaceHead':subprocess.check_output(['git','-C',str(source.parent),'rev-parse','HEAD'],text=True).strip(),'files':records},indent=2)+'\n')
