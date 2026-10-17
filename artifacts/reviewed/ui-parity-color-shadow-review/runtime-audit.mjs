import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import {createHash} from 'node:crypto';
const repo='/mnt/d/Source/QOpenBB',root=repo+'/artifacts/ui-parity-color-shadow/capture',run=root+'/attempt-20261017-r3-a2';
const read=p=>JSON.parse(fs.readFileSync(p)),state=n=>read(run+'/'+n+'.json');
const sha=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const checks=[],check=(name,value)=>checks.push({name,passed:!!value});
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b),v=f=>f?.value;
function png(file){
  const b=fs.readFileSync(file);let w,h,c;const compressed=[];
  if(!b.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10])))throw Error('PNG signature');
  for(let i=8;i<b.length;){const len=b.readUInt32BE(i),type=b.toString('ascii',i+4,i+8),d=b.subarray(i+8,i+8+len);i+=len+12;
    if(type==='IHDR'){w=d.readUInt32BE(0);h=d.readUInt32BE(4);c=d[9]===2?3:d[9]===6?4:0;if(!c||d[8]!==8||d[12]!==0)throw Error('PNG format');}
    if(type==='IDAT')compressed.push(d);
  }
  const raw=zlib.inflateSync(Buffer.concat(compressed)),stride=w*c,data=Buffer.alloc(h*stride);
  const paeth=(a,b,c)=>{const p=a+b-c,x=Math.abs(p-a),y=Math.abs(p-b),z=Math.abs(p-c);return x<=y&&x<=z?a:y<=z?b:c;};
  for(let y=0;y<h;y++)for(let x=0;x<stride;x++){
    const i=y*stride+x,a=x>=c?data[i-c]:0,b=y?data[i-stride]:0,d=y&&x>=c?data[i-stride-c]:0;
    const predictor=[0,a,b,Math.floor((a+b)/2),paeth(a,b,d)][raw[y*(stride+1)]];
    if(predictor===undefined)throw Error('PNG filter');data[i]=(raw[y*(stride+1)+x+1]+predictor)&255;
  }
  return {w,h,c,data};
}
const shots=state('screenshots'),raster=state('raster-measurements').records;let previous=null;
check('24-viewport-captures',shots.length===24&&raster.length===24);
for(const entry of raster){
  const image=png(run+'/'+entry.checkpoint+'.png');check('viewport:'+entry.checkpoint,image.w===1440&&image.h===1000);
  for(const [index,region]of entry.regions.entries()){
    const r=region.rect,crop=png(run+'/'+region.file);let valid=crop.w===r.width&&crop.h===r.height,changed=0;
    const absolute=[0,0,0],signed=[0,0,0];
    for(let y=0;y<r.height;y++)for(let x=0;x<r.width;x++){
      let any=false;
      for(let c=0;c<3;c++){
        const current=image.data[((r.y+y)*image.w+r.x+x)*image.c+c];
        valid&&=current===crop.data[(y*crop.w+x)*crop.c+c];
        if(previous){const delta=current-previous.data[((r.y+y)*previous.w+r.x+x)*previous.c+c];if(delta)any=true;absolute[c]+=Math.abs(delta);signed[c]+=delta;}
      }
      if(any)changed++;
    }
    check('lossless-crop:'+entry.checkpoint+':'+index,valid&&r.width<=128&&r.height<=128);
    if(previous)check('pixel-count:'+entry.checkpoint+':'+index,changed===region.previous.changedPixels&&same(absolute,region.previous.absoluteChannelDifferences)&&same(signed,region.previous.signedChannelDifferences));
  }
  previous=image;
}
const snapshots=fs.readdirSync(run).filter(n=>/^(C\d\d|setup\.s\d+).*\.json$/.test(n)&&n!=='C03-invalid-check.json');
const baseline=state('C01-baseline');
for(const name of snapshots){const s=read(run+'/'+name),nodes=s.live.series.flatMap(x=>x.nodes);
  check('finite-cardinality:'+name,s.live.axes.length===2&&s.live.series.length===2&&nodes.length===8&&s.live.series.every(x=>x.nodes.length===4));
  check('typed-ancestry:'+name,nodes.every(n=>n.parents.length>0&&n.parents.length<=8&&n.parents.every(p=>p.visible.presence==='value'&&typeof v(p.visible)==='boolean'&&p.opacity.presence==='value'&&Number.isFinite(v(p.opacity)))));
  check('settled-bound:'+name,s.settled.animationActive===false&&fs.statSync(run+'/'+name).size<=262144);
}
const axis=s=>s.effective.axes.find(a=>v(a.position)==='bottom'),grid=s=>s.effective.axes.find(a=>v(a.position)==='left');
check('axis-alpha',v(axis(state('C02.s08-after')).line.stroke)==='rgba(187, 189, 194, 0.971)');
check('grid-alpha',v(grid(state('C03.s05-after')).gridLine.style[0].stroke)==='rgba(39, 198, 160, 0.502)');
check('invalid-no-event',state('C03-invalid-check').eventsUnchanged===true&&state('C03-invalid-check').input.validity.customError===true&&same(grid(state('C03.s04-before')),grid(state('C03.s04-after'))));
const tuple=s=>Object.fromEntries(Object.entries(s).map(([k,f])=>[k,v(f)]));
const expected={enabled:true,color:'rgba(249, 195, 61, 0.6)',blur:12,xOffset:-7,yOffset:9};
for(const [name,enabled]of [['C08.s02-after',true],['C09.s02-after',false],['C09.s03-after',true]]){
  const s=state(name);check('complete-shadow:'+name,s.effective.series.every(x=>same(tuple(x.shadow),{...expected,enabled}))&&s.live.series.every(x=>same(tuple(x.properties.shadow),{...expected,enabled})&&x.nodes.every(n=>same(tuple(n.fillShadow),{...expected,enabled}))));
}
check('same-restored-halo',sha(run+'/C08.s02-after-region-2.png')===sha(run+'/C09.s03-after-region-2.png'));
const ledger=state('action-ledger-public'),summary=state('summary'),opens=ledger.filter(a=>/ open$/.test(a.label));
check('conservative-mutations',summary.actions===51&&summary.potentiallyChangingActions===13&&opens.length===4&&13+opens.length===17);
check('three-open-events',opens.filter(a=>a.eventSequence.to>a.eventSequence.from).length===3&&state('events').length===15);
check('no-grid-opacity',grid(state('C09.s03-after')).gridLine.style.every(s=>s.opacity.presence==='absent'&&s.strokeOpacity.presence==='absent'));
for(const n of [1,2]){const dir=root+'/attempt-20261017-r3-a'+n,c=read(dir+'/cleanup-report.json'),b=read(dir+'/browser-cleanup.json'),id=read(dir+'/runtime-identity.json');
  check('cleanup:'+n,c.containerAbsent&&c.stateAbsent&&c.credentialAbsent&&c.remainingOwnedState.length===0&&b.browserClosed&&b.listenerRemoved&&read(dir+'/cleanup-status.json').exitCode===0);
  check('identity:'+n,id.image==='sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f'&&id.source==='38dffc33389aca0e4a87e0e88d42f7067aa220df');
}
const manifest=root+'/publication-allowlist.json';
if(fs.existsSync(manifest)){
  const a=read(manifest),selected=new Set();
  for(const f of a.files){const p=f.source||f.sourcePath||f.path;const full=p.startsWith('artifacts/')?repo+'/'+p:root+'/'+p;selected.add(path.resolve(full));
    check('safe:'+p,(full.startsWith(root+'/')||full.startsWith(repo+'/artifacts/ui-parity-color-shadow-review/')||['artifacts/ui-parity-color-shadow/plan.md','artifacts/ui-parity-color-shadow/source-hashes.json'].includes(p))&&!/private|\.log$|\.env$|\/state-|\/diagnostics\.json$|\/action-ledger\.json$/.test(p));
    check('hash:'+p,sha(full)===f.sha256);
  }
  for(const f of a.metadataFiles||[])selected.add(path.resolve(repo,f.source));
  const report=fs.readFileSync(root+'/report.md','utf8');
  for(const match of report.matchAll(/\]\(([^)]+)\)/g)){const target=match[1].split('#')[0];if(/^[a-z]+:/.test(target))continue;const full=path.resolve(root,target);
    check('link-exists:'+target,fs.existsSync(full));if(full.startsWith(root+'/')&&full!==manifest)check('link-included:'+target,selected.has(full));
  }
}
const result={scope:'Independent offline original color/Shadow evidence and decoded-PNG audit; no runtime',checkCount:checks.length,failed:checks.filter(c=>!c.passed),checks};
fs.writeFileSync(repo+'/artifacts/ui-parity-color-shadow-review/runtime-verification.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({checks:checks.length,failed:result.failed}));if(result.failed.length)process.exitCode=1;
