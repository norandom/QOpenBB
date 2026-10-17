export async function settle({waitForUpdate,sample,now=Date.now,pause=ms=>new Promise(r=>setTimeout(r,ms)),deadlineMs=6000,updateMs=4000,maxSamples=10}){
  const started=now(),deadline=started+deadlineMs;
  let timer;
  try{await Promise.race([waitForUpdate(),new Promise((_,reject)=>{timer=setTimeout(()=>reject(Error('settlement-unresolved: waitForUpdate deadline')),Math.min(updateMs,deadlineMs));})]);}
  finally{clearTimeout(timer);}
  let prior=null,last=null,accepted=null,count=0,invalidCount=0;
  while(count<maxSamples&&now()<deadline){
    const at=now();let sampleTimer,value;
    try{value=await Promise.race([sample(),new Promise((_,reject)=>{sampleTimer=setTimeout(()=>reject(Error('settlement-unresolved: sample deadline')),Math.max(1,deadline-now()));})]);}
    finally{clearTimeout(sampleTimer);}
    count++;last={at,value};
    if(value.valid&&value.animationActive===false){
      const signature=JSON.stringify({live:value.live,geometry:value.geometry,effective:value.effective,fonts:value.fonts});
      if(prior&&prior.signature===signature&&at-prior.at>=100){accepted=[prior,last];break;}
      prior={at,value,signature};
    }else{prior=null;if(value.reason==='bbox-getter-operands-changed')invalidCount++;}
    if(count<maxSamples&&now()+100<deadline)await pause(110);else break;
  }
  if(!accepted||now()>deadline){const error=Error('settlement-unresolved: finite sample deadline');error.diagnostic={count,elapsedMs:now()-started,invalidCount,last};throw error;}
  return {snapshot:accepted[1].value,settled:{pair:accepted.map(x=>({at:x.at,operands:x.value.operands,animationActive:x.value.animationActive})),count,elapsedMs:now()-started,invalidCount}};
}
