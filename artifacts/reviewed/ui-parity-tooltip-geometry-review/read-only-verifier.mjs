import fs from 'node:fs';
import path from 'node:path';
import {syncBuiltinESMExports} from 'node:module';
const target=path.resolve('artifacts/ui-parity-tooltip-geometry-diagnosis/verification.json');
fs.writeFileSync=(file,data)=>{
  if(path.resolve(file)!==target) throw Error('Unexpected verifier output');
  const bytes=Buffer.isBuffer(data)?data:Buffer.from(data);
  if(!bytes.equals(fs.readFileSync(target))) throw Error('Verifier receipt differs from frozen bytes');
  process.stderr.write('Read-only wrapper: identical frozen receipt write suppressed.\n');
};
syncBuiltinESMExports();
