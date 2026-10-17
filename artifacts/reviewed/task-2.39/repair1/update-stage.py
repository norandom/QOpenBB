import pathlib,json,shutil
root=pathlib.Path('/mnt/d/Source/QOpenBB');out=root/'artifacts/task-2.39/repair1'
stage=pathlib.Path(json.loads((out/'source-stage-manifest.json').read_text())['stage'])
for rel in ['src/components/General/Table/Chart/application/gridCapture.ts','tests/unit/chart-application/gridCapture.test.ts']:
 shutil.copyfile(root/'vendor/workspace/terminalpro'/rel,stage/rel)
