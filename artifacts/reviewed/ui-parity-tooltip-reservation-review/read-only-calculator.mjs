import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {syncBuiltinESMExports} from 'node:module';
const target=path.resolve('artifacts/ui-parity-tooltip-reservation-analysis/verification.json');
fs.writeFileSync=(file,data)=>{
  if(path.resolve(file instanceof URL?fileURLToPath(file):file)!==target)throw Error('Unexpected calculator mutation');
  if(!Buffer.from(data).equals(fs.readFileSync(target)))throw Error('Calculator receipt differs from frozen bytes');
  process.stderr.write('Identical frozen calculator receipt write suppressed.\n');
};
syncBuiltinESMExports();
