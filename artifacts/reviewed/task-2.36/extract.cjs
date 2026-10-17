const fs = require('node:fs');
const crypto = require('node:crypto');
const ts = require('/home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules/typescript');
const { execFileSync } = require('node:child_process');
const root = require('node:path').resolve(__dirname, '../..');
const hash = s=>crypto.createHash('sha256').update(s).digest('hex');
const specs=[['utils.ts','terminalpro/src/lib/utils/utils.ts',['formatNumber','formatNumberMagnitude','formatNumberNoMagnitude','formatNumberThousands','toFixedString']],['AgGridUtils.tsx','terminalpro/src/components/General/Table/AgGridUtils.tsx',['datePattern','dateTimePattern','isDate','isDateTime']],['chart.tsx','terminalpro/src/components/General/Table/Chart/utils.tsx',['getFiscalPeriodString']]];
const sources=specs.map(([file,path,names])=>{
 const full=execFileSync('git', ['-C', root+'/vendor/workspace', 'show', '38dffc33389aca0e4a87e0e88d42f7067aa220df:'+path], {encoding:'utf8'});
 const ast=ts.createSourceFile(file,full,ts.ScriptTarget.Latest,true);
 const snippets=ast.statements.filter(n=>ts.isFunctionDeclaration(n)?names.includes(n.name?.text):ts.isVariableStatement(n)&&n.declarationList.declarations.some(d=>names.includes(d.name.getText(ast)))).map(n=>n.getText(ast));
 if(snippets.length!==names.length)throw Error(file);
 const code=snippets.join('\n');
 return {path,fullSourceSha256:hash(full),names,code,codeSha256:hash(code)};
});
fs.writeFileSync(root+'/vendor/workspace/terminalpro/tests/unit/chart-application/financialFormatting.sources.json',JSON.stringify({pin:'38dffc33389aca0e4a87e0e88d42f7067aa220df',extraction:'TypeScript '+ts.version+' top-level function/variable AST getText; exact source snippets joined LF; export removed only at execution',notice:'OpenBB Workspace source, OpenBB Inc. Preserve upstream vendor/workspace/LICENSE and notices. Test-only original helper excerpts, no maintained production copy.',sources},null,2)+'\n');
