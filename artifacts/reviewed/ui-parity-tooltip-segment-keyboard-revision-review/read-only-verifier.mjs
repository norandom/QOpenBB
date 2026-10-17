import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {syncBuiltinESMExports} from 'node:module';
const source=path.resolve('artifacts/ui-parity-tooltip-segment-keyboard-revised');
const owned=path.resolve('artifacts/ui-parity-tooltip-segment-keyboard-revision-review');
const temporary=path.join(source,'offline-io');
const target=path.join(source,'verification.json');
const original=Object.fromEntries(['readFileSync','writeFileSync','mkdirSync','rmdirSync','unlinkSync','existsSync','statSync','readdirSync'].map(k=>[k,fs[k].bind(fs)]));
const resolve=file=>path.resolve(file instanceof URL?fileURLToPath(file):file);
const map=file=>{if(typeof file==='number')return file;const p=resolve(file);return p===temporary||p.startsWith(temporary+path.sep)?path.join(owned,'verifier-io',path.relative(temporary,p)):file;};
for(const name of ['readFileSync','existsSync','statSync','readdirSync'])fs[name]=(file,...args)=>original[name](map(file),...args);
for(const name of ['writeFileSync','mkdirSync','rmdirSync','unlinkSync'])fs[name]=(file,...args)=>{
  if(name==='writeFileSync'&&resolve(file)===target){
    const actual=Buffer.isBuffer(args[0])?args[0]:Buffer.from(args[0]);
    if(!actual.equals(original.readFileSync(target)))throw Error('Verifier receipt changed');
    process.stderr.write('Read-only wrapper: identical frozen receipt write suppressed.\n');return;
  }
  const redirected=map(file);
  if(!path.resolve(redirected).startsWith(owned+path.sep))throw Error('Unexpected verifier mutation: '+file);
  return original[name](redirected,...args);
};
syncBuiltinESMExports();
