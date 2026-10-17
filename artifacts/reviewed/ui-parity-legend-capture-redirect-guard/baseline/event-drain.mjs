export function acceptDrain(envelope,{save,persist,expected=null}){
  if(!envelope||!Array.isArray(envelope.events)||envelope.events.length>256)throw Error('event-drain-unresolved: envelope');
  save(envelope.events);
  if(envelope.overflow){persist('event-overflow',envelope.overflow);throw Error('event-overflow: '+String(envelope.overflow.reason??'unknown').slice(0,512));}
  const count=envelope.events.length;
  if(expected!==null&&count!==expected){persist('late-events',{expectedSettledSequence:expected,actualDrainedSequence:count,status:'late-events-unresolved'});throw Error('late-events-unresolved: settled '+expected+' drained '+count);}
  return {count,overflow:null,listenerRemoved:envelope.listenerRemoved===true};
}
