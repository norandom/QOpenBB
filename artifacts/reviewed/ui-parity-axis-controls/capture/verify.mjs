import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
const base=path.resolve(new URL('.',import.meta.url).pathname),target=process.argv[2]?path.resolve(process.argv[2]):base;
const hash=f=>createHash('sha256').update(fs.readFileSync(f)).digest('hex'),checks=[];
const assert=(v,label)=>{if(!v)throw Error(label);checks.push(label);};
const manifest=JSON.parse(fs.readFileSync(target+'/'+(target===base?'harness-manifest.json':'source-manifest.json')));
for(const f of manifest.files)assert(hash(target+'/'+f.path)===f.sha256,'frozen '+f.path);
assert(hash(base+'/../plan.md')===manifest.plan.sha256,'reviewed plan identity');
if(target!==base){
  const load=n=>JSON.parse(fs.readFileSync(target+'/'+n+'.json'));
  const status=load('run-status'),cleanup=load('cleanup-report'),browser=load('browser-cleanup'),counts=load('counters');
  assert(status.exitCode===0,'run exit zero');assert(cleanup.containerAbsent&&cleanup.stateAbsent&&cleanup.credentialAbsent,'owned runtime removed');
  assert(browser.browserClosed&&browser.contextClosed&&browser.listenerRemovedOrDisposed,'owned browser removed');
  assert(counts.actions<=240&&counts.changes<=80&&counts.checkpoints<=96&&counts.screenshots<=64&&counts.events<=256,'actual counters bounded');
  assert(load('cases').map(c=>c.id).join()==='A01,A02,A03,A04,A05,A06,A07,A08,A09','nine planned cases observed');
  const index=load('event-index'),events=index.files.flatMap(n=>JSON.parse(fs.readFileSync(target+'/'+n)));
  assert(events.length===index.count&&events.every((e,i)=>e.sequence===i+1),'complete ordered events');
  const observed=fs.readdirSync(target).filter(n=>/^observations-.*\.json$/.test(n)).flatMap(n=>JSON.parse(fs.readFileSync(target+'/'+n)));
  const observations=new Map(observed.map(o=>[o.id,o])),actions=load('action-ledger');
  for(const a of actions.filter(a=>a.beforeEvidence))assert(a.completed&&observations.has(a.beforeEvidence)&&observations.has(a.afterEvidence),'action evidence '+a.id);
  for(const o of observed){const s=JSON.parse(fs.readFileSync(target+'/'+o.checkpoint)),{dom,settled,...state}=s;delete state.case;
    assert(createHash('sha256').update(JSON.stringify(state)).digest('hex')===o.chartSha256,'reference identity '+o.id);
    assert(!o.settled.animationActive&&o.settled.identicalFiniteSamples&&o.settled.sampleTimes.at(-1)-o.settled.sampleTimes.at(-2)>=100,'settlement '+o.id);
  }
}
console.log(JSON.stringify({status:'passed',scope:target===base?'frozen harness only':'nine-case original capture',checks:checks.length,runtimeClaim:target!==base}));
