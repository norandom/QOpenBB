import pathlib,json,hashlib,subprocess,shutil
r=pathlib.Path('/mnt/d/Source/QOpenBB'); o=r/'artifacts/task-2.38/review'; src=r/'vendor/workspace/terminalpro'; imp=r/'artifacts/task-2.38/implementation'; m=json.loads((imp/'source-stage-manifest.json').read_text()); stage=pathlib.Path(m['stage']); h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bad=[]
for x in m['files']:
 if h(src/x['path'])!=x['sourceSha256'] or h(stage/x['path'])!=x['stageSha256']: bad.append(x['path'])
assert bad==['tests/unit/chart-application/tsconfig.json'],bad
shutil.copyfile(src/bad[0],stage/bad[0])
f=json.loads((src/'tests/unit/chart-application/gridCapture.fixtures.json').read_text()); read=lambda n:json.loads((r/'artifacts/parity/grid-runtime-next'/n).read_text())
assert f['rows']==read('rows.json')
for x in f['reference']['inputs']: assert h(r/x['path'])==x['sha256']
for key,name in [('ordinary','ordinary.json'),('bounded','filtered-sorted-bounds.json')]:
 a=read(name)
 assert f[key]['ids']==[next(row['id'] for row in a['table']['rows'] if row['raw']['rowKey']==f['rows'][int(node)]['rowKey']) for node in f[key]['ids']]
 assert f[key]['categories']==[row['period']['value'] for row in a['chart']['effective']['data']]
 for col in ['revenue','operatingIncome']: assert f[key][col]==[row[col] for row in a['chart']['effective']['data']]
 assert f[key]['selectedColumnIds']==a['chart']['model']['cellRange']['columns']
a=read('filtered-sorted-bounds.json'); assert f['bounded']['displayedIds']==[row['id'] for row in a['table']['rows']]
for k in ['rowStartIndex','rowEndIndex']: assert f['bounded'][k]==a['chart']['model']['cellRange'][k]
assert f['hidden']['selectedColumnIds']==read('hidden-selected.json')['chart']['model']['cellRange']['columns']
assert f['experiments']['getter']['revenue']==[row['revenue'] for row in read('synthetic-value-getter.json')['chart']['effective']['data']]
assert f['experiments']['normalizedPercent']['raw']==read('formatted-margin.json')['chart']['effective']['data'][0]['margin']
allow=json.loads((imp/'publication-allowlist.json').read_text())
for x in allow['files']: assert h(r/x['path'])==x['sha256']
result={'stageVerifiedFiles':len(m['files']),'override':'Controller normalized tsconfig CRLF to LF; copied current config to stage; all other manifest bytes unchanged','referenceInputsVerified':len(f['reference']['inputs']),'publicationFilesVerified':len(allow['files']),'stage':str(stage),'ownedHashes':{x['path']:h(src/x['path']) for x in json.loads((imp/'identity.json').read_text())['ownedAndConfigIdentities']}}
(o/'identity-audit.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result))

