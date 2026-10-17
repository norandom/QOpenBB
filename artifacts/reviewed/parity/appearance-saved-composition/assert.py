import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
rows=json.loads((ROOT/'cases.json').read_text());inputs={c['id']:c for c in json.loads((ROOT/'case-inputs.json').read_text())};checks=[]
def eq(name,actual,expected):checks.append({'name':name,'actual':actual,'expected':expected,'passed':actual==expected})
def value(x,k):return x[k].get('value')
for c in rows:
    name=c['actionId'];family='line' if c['requestedFamily']=='line' else 'bar';has_family=name.endswith('family');e=c['effective'];combined=c['hookCombined']
    eq(name+'/exact-saved-input',c['syntheticSavedFixture'],inputs[name]['saved'])
    eq(name+'/native-family',c['model']['chartType'],c['requestedFamily'])
    eq(name+'/native-selected-namespace-projection-empty',c['model']['chartOptions'],{})
    eq(name+'/generated-common-legend',value(combined['common']['legend'],'position'),'top')
    eq(name+'/saved-common-title-removed',combined['common']['title']['text']['presence'],'absent')
    eq(name+'/title-enabled',value(e['title'],'enabled'),has_family)
    eq(name+'/effective-title',value(e['title'],'text'),'SAVED '+family.upper() if has_family else 'Title')
    eq(name+'/legend',value(e['legend'],'position'),'right' if has_family else 'top')
    axis=next(a for a in e['axes'] if a['type']=='number')
    eq(name+'/number-position',axis['position'],'left');eq(name+'/number-label',value(axis['label'],'color'),'#abcdef' if has_family else '#fff')
    for i,s in enumerate(e['series']):
        eq(name+f'/series{i}/type',s['type'],family)
        if family=='bar':
            eq(name+f'/series{i}/fill',value(s,'fill'),'#abcdef' if has_family else ['#5090dc','#ffa03a'][i]);eq(name+f'/series{i}/stroke',value(s,'stroke'),'#fedcba' if has_family else ['#74a8e6','#ffbe70'][i]);eq(name+f'/series{i}/width',value(s,'strokeWidth'),3 if has_family else 0)
        else:
            eq(name+f'/series{i}/fill-not-line-color',s['fill']['presence'],'absent');eq(name+f'/series{i}/stroke',value(s,'stroke'),'#fedcba' if has_family else ['#5090dc','#ffa03a'][i]);eq(name+f'/series{i}/width',value(s,'strokeWidth'),5 if has_family else 2)
            eq(name+f'/series{i}/marker-fill',value(s['marker'],'fill'),'#789abc' if has_family else ['#5090dc','#ffa03a'][i]);eq(name+f'/series{i}/marker-stroke',value(s['marker'],'stroke'),'#cba987' if has_family else ['#74a8e6','#ffbe70'][i]);eq(name+f'/series{i}/marker-enabled',value(s['marker'],'enabled'),has_family);eq(name+f'/series{i}/marker-width',value(s['marker'],'strokeWidth'),2 if has_family else 0);eq(name+f'/series{i}/marker-shape',value(s['marker'],'shape'),'circle');eq(name+f'/series{i}/marker-size',value(s['marker'],'size'),7)
eq('four-cases',len(rows),4);eq('owned-cleanup',json.loads((ROOT/'cleanup-report.json').read_text())['remainingOwnedState'],[]);eq('journey-exit',(ROOT/'journey-exit.txt').read_text().strip(),'0')
result={'passed':all(x['passed'] for x in checks),'assertions':len(checks),'checks':checks};(ROOT/'assertions.json').write_text(json.dumps(result,indent=2));print(json.dumps({'passed':result['passed'],'assertions':len(checks)}));raise SystemExit(0 if result['passed'] else 1)
