import pathlib,json,hashlib,subprocess
root=pathlib.Path('/mnt/d/Source/QOpenBB'); out=root/'artifacts/task-2.38/implementation'; src=root/'vendor/workspace/terminalpro'; stage=pathlib.Path((out/'stage-path.txt').read_text().strip()); fixture=json.loads((src/'tests/unit/chart-application/gridCapture.fixtures.json').read_text()); ref=root/'artifacts/parity/grid-runtime-next'
assert fixture['rows']==json.loads((ref/'rows.json').read_text())
for item in fixture['reference']['inputs']: assert hashlib.sha256((root/item['path']).read_bytes()).hexdigest()==item['sha256']
ordinary=json.loads((ref/'ordinary.json').read_text()); bounded=json.loads((ref/'filtered-sorted-bounds.json').read_text()); getter=json.loads((ref/'synthetic-value-getter.json').read_text())
for key in ['revenue','operatingIncome']:
 assert [r[key] for r in ordinary['chart']['effective']['data']]==fixture['ordinary'][key]
 assert [r[key] for r in bounded['chart']['effective']['data']]==fixture['bounded'][key]
assert [r['revenue'] for r in getter['chart']['effective']['data']]==fixture['experiments']['getter']['revenue']
manifest=json.loads((out/'source-stage-manifest.json').read_text()); assert all(x['sourceSha256']==x['stageSha256'] for x in manifest['files'])
owned=['tests/unit/chart-application/gridCapture.fixtures.json','tests/unit/chart-application/gridCapture.grid.test.ts','tests/unit/chart-application/tsconfig.json','tests/unit/chart-application/vitest.config.mjs']
identities=[]
for name in owned:
 a=hashlib.sha256((src/name).read_bytes()).hexdigest(); b=hashlib.sha256((stage/name).read_bytes()).hexdigest(); assert a==b; identities.append({'path':name,'sourceSha256':a,'stageSha256':b})
packages={p:json.loads((stage/'node_modules'/p/'package.json').read_text())['version'] for p in ['ag-grid-community','ag-grid-react','vitest','jsdom','typescript','@biomejs/biome']}
(out/'identity.json').write_text(json.dumps({'workspaceHead':manifest['workspaceHead'],'stage':str(stage),'node':'v24.22.0','packages':packages,'ownedAndConfigIdentities':identities,'referenceAssertions':'original rows, both series baseline/bounded arrays and synthetic getter arrays independently compared; all input hashes match','scope':'Tests/fixture only; production caps excluded; no adapter, application, browser, build or renderer acceptance'},indent=2)+'\n')
