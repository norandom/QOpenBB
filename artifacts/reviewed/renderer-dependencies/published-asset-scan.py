import pathlib,re,json
root=pathlib.Path('/usr/share/nginx/html')
patterns={'highcharts_word':r'highcharts','cdn':r'(?:code[.]highcharts[.]com|highcharts[.]com/(?:js|stock|maps|gantt)|cdn[^\s"\x27]{0,100}highcharts)','license_banner':r'Highcharts (?:JS|Stock|Maps|Gantt)|Highcharts (?:license|License)|@license[^\n]{0,100}Highcharts','init_import':r'(?:Highcharts[.]|highcharts/highcharts|highcharts[.]js|highstock[.]js)','ag_enterprise':r'ag-grid-enterprise|ag-charts-enterprise|LicenseManager[.]setLicenseKey'}
files=[p for p in root.rglob('*') if p.is_file() and p.suffix in ('.js','.html','.txt','.json','.css','.map')]
out={'root':str(root),'files_scanned':len(files),'bytes_scanned':sum(p.stat().st_size for p in files),'patterns':{}}
for name,pat in patterns.items():
 matches=[]
 for p in files:
  t=p.read_text(errors='replace')
  found=list(re.finditer(pat,t,re.I))
  if found: matches.append({'file':str(p.relative_to(root)),'count':len(found),'contexts':[t[max(0,m.start()-90):m.end()+130] for m in found[:8]]})
 out['patterns'][name]={'count':sum(x['count'] for x in matches),'files':matches}
out['matching_filenames']=[str(p.relative_to(root)) for p in root.rglob('*') if re.search('highcharts|highstock|highmaps|highgantt',p.name,re.I)]
print(json.dumps(out,indent=2))


