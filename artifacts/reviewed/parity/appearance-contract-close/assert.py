import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
cases={c['id']:c for c in json.loads((ROOT/'cases.json').read_text())}
checks=[]
def check(name,actual,expected):
    checks.append({'name':name,'actual':actual,'expected':expected,'passed':actual==expected})
def val(case,role,key):return cases[case]['effective'][role][key].get('value')
def blend(fg,bg,background_ratio):
    rgb=lambda h:[int(h[i:i+2],16) for i in (1,3,5)]
    return '#'+''.join(f'{math.floor(max(0,min(1,(a/255)*(1-background_ratio)+(b/255)*background_ratio))*255+0.5):02x}' for a,b in zip(rgb(fg),rgb(bg)))
for case,fg,bg,dark in [('stock','#ffffff','#151518',True),('background-only-dark','#ffffff','#26394a',True),('palette-only-dark','#ffffff','#151518',True),('background-only-light','#181d1f','#edf3d7',False),('explicit-derived-tokens','#123456','#26394a',True)]:
    e=cases[case]['effective']
    check(case+'/background',val(case,'background','fill'),bg)
    check(case+'/subtitle',val(case,'subtitle','color'),blend(fg,bg,.57 if dark else .38))
    for a in e['axes']:check(case+'/grid/'+a['type'],a['gridLine']['style'][0]['stroke'],blend(fg,bg,1-(.257 if dark else .1)))
for case,text,color,legend in [('common-family-collision','FAMILY','#654321','right'),('common-only','COMMON','#123456','bottom'),('family-only','FAMILY','#654321','right')]:
    check(case+'/title',val(case,'title','text'),text);check(case+'/titleColor',val(case,'title','color'),color);check(case+'/legend',val(case,'legend','position'),legend)
    number=next(a for a in cases[case]['effective']['axes'] if a['type']=='number')
    check(case+'/number-label',number['label']['color']['value'],'#123456' if case=='common-only' else '#abcdef')
for case,color in [('common-only','#5090dc'),('family-only','#abcdef'),('common-family-collision','#abcdef'),('palette-only-dark','#d12378')]:
    check(case+'/series-fill',cases[case]['effective']['series'][0]['style']['fill']['value'],color)
edge=json.loads((ROOT/'normalized-color-evidence.json').read_text())
check('source-rounding-edge',edge['edge']['actual'],'#8b0000')
for row in edge['ratios']:check('normalized-source-equivalence/'+row['role'],row['normalizedMismatches'],0)
check('cleanup',json.loads((ROOT/'cleanup-report.json').read_text())['remainingOwnedState'],[])
check('journey-exit',(ROOT/'journey-exit.txt').read_text().strip(),'0')
check('finite-cases',len(cases),8)
result={'passed':all(c['passed'] for c in checks),'assertions':len(checks),'checks':checks}
(ROOT/'assertions.json').write_text(json.dumps(result,indent=2))
print(json.dumps({'passed':result['passed'],'assertions':len(checks)}))
raise SystemExit(0 if result['passed'] else 1)
