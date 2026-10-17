import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import assert from 'node:assert/strict';
import * as candidate from '../ui-parity-legend-relay-mount-source/harness/admission.mjs';
import * as prior from '../ui-parity-legend-fixed-relay-revised/harness/admission.mjs';
const base=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(base,'../..');
const source=path.join(root,'artifacts/ui-parity-legend-relay-mount-source'),old=path.join(root,'artifacts/ui-parity-legend-fixed-relay-revised');
const read=file=>fs.readFileSync(file),text=file=>read(file).toString('utf8'),json=file=>JSON.parse(read(file));
const hash=file=>createHash('sha256').update(read(file)).digest('hex');
const pins={'harness-manifest.json':'b03ba2f0939a637d02937326caa24b1287514d6463efd369fa67361c53e99831','source-hashes.json':'64eecc7260f1c9a269cffe919f73405fda94d645b9667705072402a0ea4019c2','publication-allowlist.json':'514eef21dcad5d3cc2a1956eeee363abf33a3e6d86a39af8a7d9b0d5b52ae79e'};
const checks=[];
function check(name,fn){fn();checks.push(name);}
function frozen(){
  for(const [file,digest] of Object.entries(pins))assert.equal(hash(path.join(source,file)),digest);
  const manifest=json(path.join(source,'source-hashes.json')),selection=json(path.join(source,'publication-allowlist.json'));
  assert.equal(selection.length,20);assert.equal(new Set(selection.map(item=>item.sourcePath)).size,20);
  for(const entry of [...manifest.sourceInputs,...manifest.sourceFiles.map(item=>({...item,sourcePath:'artifacts/ui-parity-legend-relay-mount-source/'+item.path})),...selection]){
    assert(!entry.sourcePath.includes('..'));const file=path.join(root,entry.sourcePath);
    assert(!fs.lstatSync(file).isSymbolicLink());assert.equal(hash(file),entry.sha256,entry.sourcePath);assert.equal(read(file).length,entry.bytes,entry.sourcePath);
  }
  return manifest;
}
check('All frozen source/input/selection bytes',frozen);
check('Only mount behavior and revision paths changed',()=>{
  for(const file of ['harness/relay.py','harness/cleanup.mjs','harness/finalize.mjs','harness/io.mjs','harness/run.sh','test-relay.py','probe-contract.json'])assert(read(path.join(source,file)).equals(read(path.join(old,file))),file);
  for(const file of ['harness/probe.mjs','supervise.sh','prepare-run.mjs'])assert.equal(text(path.join(source,file)),text(path.join(old,file)).replaceAll('ui-parity-legend-fixed-relay-revised','ui-parity-legend-relay-mount-source'),file);
  const previous=text(path.join(old,'harness/admission.mjs')),current=text(path.join(source,'harness/admission.mjs'));
  assert.equal(current.slice(current.indexOf('export function admitContainer')),previous.slice(previous.indexOf('export function admitContainer')));
});
const commands=[];
function run(file,args=[],expected=0){
  const result=spawnSync(process.execPath,[path.join(source,file),...args],{cwd:root,encoding:'utf8',windowsHide:true,maxBuffer:262144});
  assert.equal(result.status,expected,result.stderr);
  const entry={command:'node artifacts/ui-parity-legend-relay-mount-source/'+file+(args.length?' '+args.join(' '):''),exitCode:result.status};
  if(expected===1){assert(result.stderr.includes('valid-three-bind-layout-rejected'));entry.reason='valid-three-bind-layout-rejected';}
  else entry.result=JSON.parse(result.stdout);
  commands.push(entry);return entry;
}
check('Actual baseline RED and complete offline matrix',()=>{
  run('test-mounts.mjs',['--baseline'],1);
  assert.deepEqual(run('verify-offline.mjs').result,{status:'passed',javascriptTests:25,mountTests:11,pythonTests:10,syntaxFiles:10,runtimeExecuted:false});
  assert.deepEqual(run('verify-freeze.mjs').result,{status:'passed',frozenPins:64,runtimeFiles:8,runtimeExecuted:false});
});
const runtime={name:'review-relay',ownership:'PRIVATE_OWNER_SENTINEL',relayId:'1'.repeat(64),internalNetworkId:'2'.repeat(64),ingressNetworkId:'3'.repeat(64),relaySourcePath:'/PRIVATE_SOURCE_SENTINEL/a',configPath:'/PRIVATE_CONFIG_SENTINEL/b',statsPath:'/PRIVATE_STATS_SENTINEL/c'};
const option='rw,nosuid,nodev,size=1048576';
function fixture(){return {
  Id:runtime.relayId,Name:'/'+runtime.name+'-relay',Image:candidate.image,
  Config:{Labels:{[candidate.ownerLabel]:runtime.ownership},User:'65534:65534',Entrypoint:['/opt/.venv/bin/python'],Cmd:['-B','-I','-S','-u','/relay/relay.py','/relay/config.json'],Healthcheck:{Test:['NONE']}},
  HostConfig:{RestartPolicy:{Name:'no'},Privileged:false,PublishAllPorts:false,NetworkMode:runtime.name+'-ingress',ReadonlyRootfs:true,CapDrop:['ALL'],SecurityOpt:['no-new-privileges'],Sysctls:{'net.ipv4.ip_forward':'0','net.ipv6.conf.all.forwarding':'0'},Tmpfs:{'/data':option},PortBindings:{'3100/tcp':[{HostIp:'127.0.0.1',HostPort:''}]}},
  Mounts:[['/relay/relay.py',runtime.relaySourcePath,false],['/relay/config.json',runtime.configPath,false],['/evidence/relay-stats.json',runtime.statsPath,true]].map(([Destination,Source,RW])=>({Destination,Source,RW,Type:'bind'})),
  NetworkSettings:{Networks:Object.fromEntries(['internal','ingress'].map(kind=>[runtime.name+'-'+kind,{NetworkID:runtime[kind+'NetworkId'],IPAddress:'172.30.0.2'}])),Ports:{'3100/tcp':[{HostIp:'127.0.0.1',HostPort:'43210'}]}},
  State:{Status:'running',Running:true,Restarting:false,Dead:false,ExitCode:0,OOMKilled:false}};}
let independentCases=0;
function observe(raw,expected){const saved=[];const result=candidate.observeContainer(raw,runtime,'relay',value=>saved.push(structuredClone(value)));assert.equal(saved.length,1);assert.deepEqual(saved[0],result.receipt);assert.equal(result.decision.kind,expected);independentCases++;return saved[0];}
check('Six bind orders admit; each exact tuple field and duplicate rejects',()=>{
  for(const order of [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]]){const raw=fixture();raw.Mounts=order.map(index=>raw.Mounts[index]);observe(raw,'relay-admitted');}
  assert.equal(prior.admitContainer(prior.projectContainer(fixture(),runtime,'relay')).kind,'security-unresolved');
  for(let index=0;index<3;index++)for(const field of ['Destination','Source','RW','Type']){const raw=fixture();raw.Mounts[index][field]=field==='RW'?!raw.Mounts[index].RW:'wrong';assert.equal(observe(raw,'security-unresolved').security.exactMounts,false);}
  const duplicate=fixture();duplicate.Mounts[2]=duplicate.Mounts[0];observe(duplicate,'security-unresolved');
});
check('Malformed entries persist and destination coercion is never called',()=>{
  let coercions=0;
  for(const value of [null,undefined,false,0,'entry',{}, {Destination:{toString(){coercions++;throw Error('unexpected coercion');}}}]){
    const raw=fixture();raw.Mounts[1]=value;const receipt=observe(raw,'security-unresolved');assert.equal(receipt.selected.Mounts.entries.length,3);
  }
  assert.equal(coercions,0);
  const arrayLike=fixture();arrayLike.Mounts={0:arrayLike.Mounts[0],1:arrayLike.Mounts[1],2:arrayLike.Mounts[2],length:3};observe(arrayLike,'security-unresolved');
});
check('Only own sole configured data survives; private key/source sentinels excluded',()=>{
  const inherited=fixture();inherited.HostConfig.Tmpfs=Object.create({'/data':option});assert.equal(observe(inherited,'security-unresolved').selected.Tmpfs.dataOwn,false);
  const ownProto=fixture();ownProto.HostConfig.Tmpfs=JSON.parse('{"/data":"'+option+'","__proto__":"PRIVATE_EXTRA_SENTINEL"}');
  const receipt=observe(ownProto,'security-unresolved');assert.equal(receipt.selected.Tmpfs.keyCount,2);assert.equal(receipt.selected.Tmpfs.unexpectedKeyCount,1);assert(!JSON.stringify(receipt).includes('PRIVATE_'));assert(!JSON.stringify(receipt.selected.Tmpfs).includes('__proto__'));
  const noPrototype=fixture();noPrototype.HostConfig.Tmpfs=Object.assign(Object.create(null),{'/data':option});observe(noPrototype,'relay-admitted');
  const missing=fixture();delete missing.HostConfig.Tmpfs;const absent=observe(missing,'security-unresolved').selected.Tmpfs;
  const scalar=fixture();scalar.HostConfig.Tmpfs=false;const falseParent=observe(scalar,'security-unresolved').selected.Tmpfs;
  assert.equal(absent.presence.kind,'absent');assert.equal(falseParent.presence.value,false);assert.equal(absent.keyCount,null);assert.equal(falseParent.keyCount,null);
  const raw=fixture();raw.Mounts.push({Destination:'/data',Type:'tmpfs',RW:true});observe(raw,'security-unresolved');
});
check('Safe exact selection, links and final frozen preservation',()=>{
  assert(read(path.join(base,'reviewed-source-publication-allowlist.json')).equals(read(path.join(source,'publication-allowlist.json'))));
  for(const item of json(path.join(source,'publication-allowlist.json'))){
    assert(!/attempt-|-private\.json$|\.log$/.test(item.sourcePath));const value=text(path.join(root,item.sourcePath));
    assert(!/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:gh[pousr]_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9]{32,}|AKIA[A-Z0-9]{16})\b/.test(value));
    assert(!/\b(?:TODO|TBD|FIXME|HACK|XXX)\b/.test(value));
  }
  for(const report of [path.join(source,'handoff.md'),path.join(base,'review.md')])for(const match of text(report).matchAll(/\]\(([^)]+)\)/g)){
    if(/^https:\/\//.test(match[1]))continue;
    if(process.argv.includes('--record')&&path.resolve(path.dirname(report),match[1])===path.join(base,'verification.json'))continue;
    assert(fs.existsSync(path.resolve(path.dirname(report),match[1])),match[1]);
  }
  frozen();
});
const receipt={verdict:'APPROVED',scope:'Exact mount-source correction only; separate runtime grant required',inputHashes:pins,checks,groupedChecks:checks.length,commands,independentCases,
  sourceFiles:19,publicationFiles:20,runtimeFiles:8,frozenInputsPreserved:true,runtimeExecuted:false,networkOpened:false,prepareOrFreezeExecuted:false,
  scanScope:'Selected safe source and synthetic offline evidence; bounded common-token/private-key markers and placeholders plus manual review',
  complexity:'Research exclusion; future maintained400 physical/file,300 logical/file,50/function with inventory/checker'};
if(process.argv.includes('--record'))fs.writeFileSync(path.join(base,'verification.json'),JSON.stringify(receipt,null,2)+'\n');
else assert.deepEqual(json(path.join(base,'verification.json')),receipt);
console.log(JSON.stringify({verdict:receipt.verdict,groupedChecks:checks.length,independentCases,runtimeExecuted:false,frozenInputsPreserved:true}));
