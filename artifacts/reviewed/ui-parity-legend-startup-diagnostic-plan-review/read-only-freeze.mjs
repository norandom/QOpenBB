import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {syncBuiltinESMExports} from 'node:module';
const base=path.resolve('artifacts/ui-parity-legend-startup-diagnostic-plan');
const permitted=new Set(['verification.json','source-hashes.json','publication-allowlist.json'].map(n=>path.join(base,n)));
fs.writeFileSync=(file,data)=>{
  const target=path.resolve(file instanceof URL?fileURLToPath(file):file);
  if(!permitted.has(target))throw Error('Unexpected plan-freezer output');
  if(!Buffer.from(data).equals(fs.readFileSync(target)))throw Error('Frozen plan output differs: '+path.basename(target));
  process.stderr.write('Suppressed identical frozen '+path.basename(target)+' write.\n');
};
syncBuiltinESMExports();
