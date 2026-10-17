import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
const attempt=path.resolve(process.argv[2]);
if(!/^attempt-[a-zA-Z0-9-]+$/.test(path.basename(attempt))||path.basename(path.dirname(attempt))!=='capture')throw Error('Unsafe attempt');
const runtime=JSON.parse(fs.readFileSync(attempt+'/runtime-private.json')),lifecycle=JSON.parse(fs.readFileSync(attempt+'/lifecycle-private.json'));
const browser=JSON.parse(fs.readFileSync(attempt+'/owned-browser-private.json'));
const ids=execFileSync('docker',['ps','-a','--no-trunc','--filter','name=^/'+runtime.name+'$','--format','{{.ID}}'],{encoding:'utf8',timeout:10000,windowsHide:true}).trim();
const alive=pid=>{try{process.kill(pid,0);return true;}catch{return false;}};
const report={scope:'Fresh owned resources absence after completed failed attempt',containerAbsent:ids==='',stateAbsent:!fs.existsSync(runtime.statePath),
  credentialAbsent:!fs.existsSync(attempt+'/credential-private.json'),browserProcessAbsent:!alive(browser.pid),supervisorProcessAbsent:!alive(lifecycle.shellPid)};
report.passed=Object.entries(report).filter(([k])=>k.endsWith('Absent')).every(([,v])=>v===true);
fs.writeFileSync(attempt+'/owned-absence-verification.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report));if(!report.passed)process.exitCode=1;
