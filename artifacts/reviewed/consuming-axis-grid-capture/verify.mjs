import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';

const root=path.dirname(new URL(import.meta.url).pathname);
const read=name=>JSON.parse(fs.readFileSync(root+'/'+name+'.json'));
const checks=[];
function equal(name,actual,expected){assert.deepEqual(actual,expected,name);checks.push(name);}
const axis=(snapshot,position)=>snapshot.state.effective.axes.find(value=>value.position===position);
const live=(snapshot,position)=>snapshot.state.live.find(value=>value.position===position);
const names=['baseline','ui-axis-thickness-3','ui-grid-thickness-4','ui-grid-dash-5',
  'synthetic-width-3-style-1','synthetic-width-1-style-4','synthetic-opacity-quarter','synthetic-opacity-one'];
try{
  for(const name of names){
    const snapshot=read(name);
    equal(name+' animation complete',snapshot.state.settled.animationActive,false);
    equal(name+' left grid node count',live(snapshot,'left').gridNodes.length,5);
    equal(name+' image signature',fs.readFileSync(root+'/'+name+'.png').subarray(0,8),
      Buffer.from([137,80,78,71,13,10,26,10]));
  }
  const baseline=read('baseline');
  for(const position of ['bottom','left']){
    equal(position+' baseline processed stroke',axis(baseline,position).line.stroke,'#c1c1c2');
    equal(position+' baseline color absent',axis(baseline,position).line.presence.color.kind,'absent');
    equal(position+' baseline scene stroke',live(baseline,position).lineNode.stroke,'#c1c1c2');
  }
  equal('bottom baseline scene width',live(baseline,'bottom').lineNode.strokeWidth,1);
  equal('left baseline disabled',axis(baseline,'left').line.enabled,false);
  equal('left baseline scene width zero',live(baseline,'left').lineNode.strokeWidth,0);
  equal('left baseline node visible flag',live(baseline,'left').lineNode.visible,true);
  const thickness=read('ui-axis-thickness-3');
  for(const position of ['left','right']){
    const patch=thickness.state.model.chartOptions.bar.axes.number[position].line;
    equal(position+' axis model enabled',patch.enabled,true);
    equal(position+' axis model width',patch.width,3);
  }
  equal('UI axis live width',live(thickness,'left').lineNode.strokeWidth,3);
  equal('UI axis live stroke',live(thickness,'left').lineNode.stroke,'#c1c1c2');
  const grid=read('ui-grid-thickness-4');
  for(const position of ['left','right'])equal(position+' grid model width',
    grid.state.model.chartOptions.bar.axes.number[position].gridLine.width,4);
  equal('UI grid processed style width',axis(grid,'left').gridLine.style[0].strokeWidth,4);
  equal('UI grid all scene widths',live(grid,'left').gridNodes.map(value=>value.node.strokeWidth),[4,4,4,4,4]);
  const dashed=read('ui-grid-dash-5');
  for(const position of ['left','right'])equal(position+' UI dash model',
    dashed.state.model.chartOptions.bar.axes.number[position].gridLine.style[0].lineDash,[5]);
  equal('UI dash all scene values',live(dashed,'left').gridNodes.map(value=>value.node.lineDash),[[5],[5],[5],[5],[5]]);
  equal('UI event count',dashed.state.events.length,3);
  for(const [name,width,styleWidth] of [[names[4],3,1],[names[5],1,4],[names[6],1,4],[names[7],1,4]]){
    const snapshot=read(name),effective=axis(snapshot,'left').gridLine,nodes=live(snapshot,'left').gridNodes;
    equal(name+' labelled synthetic',snapshot.kind,'synthetic-reference-public-update-no-ui-proof');
    equal(name+' root grid width',effective.width,width);
    equal(name+' style width',effective.style[0].strokeWidth,styleWidth);
    equal(name+' all live style widths',nodes.map(value=>value.node.strokeWidth),Array(5).fill(styleWidth));
    equal(name+' all live dash values',nodes.map(value=>value.node.lineDash),Array(5).fill([2,7]));
    equal(name+' all live strokes',nodes.map(value=>value.node.stroke),Array(5).fill('#123abc'));
    equal(name+' UI events unchanged',snapshot.state.events,dashed.state.events);
  }
  for(const name of [names[6],names[7]]){
    const snapshot=read(name);
    equal(name+' processed opacity rejected',axis(snapshot,'left').gridLine.style[0].presence.strokeOpacity.kind,'absent');
    equal(name+' live opacity unchanged',live(snapshot,'left').gridNodes.map(value=>value.node.strokeOpacity),[1,1,1,1,1]);
  }
  equal('unknown grid opacity warning',read('diagnostics').errors.some(value=>
    value.text?.includes('Unknown option `theme.overrides.bar.axes.number.left.gridLine.style[0].strokeOpacity`')),true);
  equal('synthetic opacity screenshot identity',fs.readFileSync(root+'/'+names[6]+'.png'),
    fs.readFileSync(root+'/'+names[7]+'.png'));
  equal('baseline plus bounded cases',read('summary'),{completed:true,uiActions:3,baseline:1,syntheticCases:4,
    scope:'Original runtime only. No candidate, persistence, provider or pixel-equivalence claim.'});
  for(const attempt of ['', 'attempt1/']){
    equal(attempt+'cleanup complete',read(attempt+'cleanup-report'),{containerAbsent:true,stateAbsent:true,
      credentialAbsent:true,remainingOwnedState:[]});
    equal(attempt+'browser closed',read(attempt+'browser-cleanup').closed,true);
    equal(attempt+'cleanup exit',read(attempt+'cleanup-status').exitCode,0);
  }
  equal('final run exit',read('run-status').exitCode,0);
  equal('attempt1 failure preserved',read('attempt1/run-status').exitCode,1);
  for(const file of read('source-manifest').scripts){
    equal('script/source hash '+path.basename(file.path),
      createHash('sha256').update(fs.readFileSync(file.path)).digest('hex'),file.sha256);
  }
  const result={status:'VERIFIED',claim:'Recorded bounded original axis/grid runtime observations and cleanup',
    checks:checks.length,passed:checks,gaps:['No onboarding acceptance','No candidate rendering',
      'No save/reopen or backend persistence','Synthetic update cases do not prove UI reachability',
      'Node visible is a local scene flag; ancestor visibility was not established']};
  fs.writeFileSync(root+'/verification.json',JSON.stringify(result,null,2));
  console.log(JSON.stringify({status:result.status,checks:checks.length}));
}catch(error){
  fs.writeFileSync(root+'/verification.json',JSON.stringify({status:'NOT_VERIFIED',checks:checks.length,
    passed:checks,error:error.message},null,2));throw error;
}
