const fs = require('node:fs');
const cp = require('node:child_process');
const crypto = require('node:crypto');
const ts = require('/home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules/typescript');
const root = '/mnt/d/Source/QOpenBB';
const repo = root + '/vendor/workspace';
const sha = data => crypto.createHash('sha256').update(data).digest('hex');
const git = (...args) => cp.execFileSync('git', ['-C', repo, ...args]);
const fixturePath = 'terminalpro/tests/unit/chart-application/financialFormatting.sources.json';
const fixture = JSON.parse(fs.readFileSync(repo + '/' + fixturePath, 'utf8'));
const originals = fixture.sources.map(item => {
  const original = git('show', fixture.pin + ':' + item.path);
  const ast = ts.createSourceFile(item.path, original.toString(), ts.ScriptTarget.Latest, true);
  const excerpts = ast.statements.filter(n => ts.isFunctionDeclaration(n)
    ? item.names.includes(n.name?.text)
    : ts.isVariableStatement(n) && n.declarationList.declarations.some(d => item.names.includes(d.name.getText(ast))));
  const code = excerpts.map(n => n.getText(ast)).join('\n');
  if (excerpts.length !== item.names.length || code !== item.code || sha(original) !== item.fullSourceSha256 || sha(code) !== item.codeSha256) throw Error(item.path);
  return {path: item.path, fullSourceSha256: sha(original), codeSha256: sha(code), exactAstMatch: true};
});
const prior = JSON.parse(fs.readFileSync(root + '/artifacts/task-2.36/identity.json', 'utf8'));
const identities = prior.exact_source_and_config_bytes.map(item => {
  const current = sha(fs.readFileSync(repo + '/' + item.path));
  const staged = sha(fs.readFileSync('/home/mc/qopenbb-work/task236/' + item.path));
  if (current !== staged || current !== item.sha256) throw Error(item.path);
  return {path: item.path, sha256: current, sourceStageWorkerMatch: true};
});
const production = repo + '/terminalpro/src/components/General/Table/Chart/application/financialFormatting.ts';
const measured = JSON.parse(cp.execFileSync(process.execPath, [root + '/tools/quality/syntax_units.ts'], {input: JSON.stringify([production]), encoding: 'utf8'}))[0];
measured.physical = fs.readFileSync(production, 'utf8').replace(/\r\n?/g, '\n').replace(/\n$/, '').split('\n').length;
measured.maximumFunction = Math.max(...measured.functions.map(f => f.logical));
if (measured.physical > 400 || measured.logical > 300 || measured.maximumFunction > 50) throw Error('caps');
console.log(JSON.stringify({head: git('rev-parse','HEAD').toString().trim(), originalPin: fixture.pin, originals, identities, measured}, null, 2));
