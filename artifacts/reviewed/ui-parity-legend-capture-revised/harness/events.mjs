// Retain the last successful page read when a deadline disposes the page.
export function createEventStore(json){
  const serialized=new Map();let last=[];
  function save(values){
    if(values.length<last.length)throw Error('Event prefix regression');
    for(let i=0;i<values.length;i++){
      if(values[i].sequence!==i+1)throw Error('Event sequence discontinuity');
      if(i<last.length&&JSON.stringify(values[i])!==JSON.stringify(last[i]))throw Error('Event prefix mutation');
    }
    const files=[];
    for(let offset=0;offset<values.length;offset+=16){
      const name='events-p'+String(offset/16).padStart(2,'0'),chunk=values.slice(offset,offset+16),bytes=JSON.stringify(chunk);
      if(serialized.get(name)!==bytes){json(name,chunk);serialized.set(name,bytes);}files.push(name+'.json');
    }
    const index={count:values.length,files,chunkSize:16},bytes=JSON.stringify(index);
    if(serialized.get('event-index')!==bytes){json('event-index',index);serialized.set('event-index',bytes);}
    last=structuredClone(values);
  }
  return {save,last:()=>structuredClone(last),count:()=>last.length};
}
