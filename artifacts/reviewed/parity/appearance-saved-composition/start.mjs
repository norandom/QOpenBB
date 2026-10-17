import fs from 'node:fs'; import {randomBytes} from 'node:crypto'; import {execFileSync} from 'node:child_process';
const out='/mnt/d/Source/QOpenBB/artifacts/parity/appearance-saved-composition';
const docker=(...args)=>execFileSync('docker',args,{encoding:'utf8',stdio:['ignore','pipe','pipe']});
const image='sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f';
const info=JSON.parse(docker('image','inspect',image))[0];
if(info.Id!==image||info.Config.Labels['org.qopenbb.source.workspace']!=='38dffc33389aca0e4a87e0e88d42f7067aa220df')throw Error('Identity mismatch');
const name='qopenbb-appearance-saved-composition-20261017-stock';
const credential={email:'appearance-saved-synthetic@example.com',password:'Aa1!'+randomBytes(24).toString('hex')};fs.writeFileSync(out+'/credential-private.json',JSON.stringify(credential),{mode:0o600});
const statePath=out+'/state-'+randomBytes(6).toString('hex');fs.mkdirSync(statePath);
const cid=docker('run','-d','--name',name,'--mount',`type=bind,src=${statePath},dst=/data`,'-p','127.0.0.1::3000','-e',`OPENBB_ADMIN_PASSWORD=${credential.password}`,'-e','PUBLIC_URL=http://localhost','-e','OPENBB_ADMIN_EMAIL=appearance-saved-synthetic@example.com',image).trim();
let ins; for(let i=0;i<60;i++){ins=JSON.parse(docker('inspect',cid))[0];if(ins.State.Running && ins.NetworkSettings.Ports['3000/tcp']?.[0]?.HostPort)break;await new Promise(r=>setTimeout(r,1000));} const port=ins.NetworkSettings.Ports['3000/tcp'][0].HostPort;
const result={image,source:info.Config.Labels['org.qopenbb.source.workspace'],name,container:cid,origin:`http://127.0.0.1:${port}`,port,health:null};
fs.writeFileSync(out+'/runtime.json',JSON.stringify(result,null,2));
for(let i=0;i<60;i++){try{const current=JSON.parse(docker('inspect',cid))[0];const bound=current.NetworkSettings.Ports['3000/tcp']?.[0]?.HostPort;if(bound){result.port=bound;result.origin=`http://127.0.0.1:${bound}`;}const r=await fetch(result.origin+'/api/health');if(r.status===200){result.health=200;break;}}catch{}await new Promise(r=>setTimeout(r,1000));}
fs.writeFileSync(out+'/runtime.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result));
if(result.health!==200)throw Error('Original container did not become healthy');






