// Parent-space boxes already include each node's own transform.
export function geometryTools(){
  const fail=m=>{throw Error('scene-unresolved: '+m);};
  const value=(r,k)=>{const v=r?.[k]?.value;if(typeof v!=='number'||!Number.isFinite(v))fail('finite '+k);return v;};
  const box=r=>Object.fromEntries(['x','y','width','height'].map(k=>[k,value(r,k)]));
  const translate=(b,x,y)=>({...b,x:b.x+x,y:b.y+y});
  function identity(fields,plain=false){
    for(const [k,v] of [['rotation',0],['scalingX',1],['scalingY',1]]){
      const r=fields[k];if(r?.kind==='absent')continue;
      if(r?.value!==v)fail('nonidentity '+k);
    }
    if(plain)for(const k of ['translationX','translationY'])if(fields[k]?.kind!=='absent'&&fields[k]?.value!==0)fail('plain Group translation');
  }
  function convert(scene){
    if(!scene.chainValid)fail('exact parent identities');
    if(scene.root.className!=='Group'||scene.items.some(i=>i.symbols.className!=='Group'))fail('plain Group roles');
    if(!/^_?Group$/.test(scene.root.constructorName)||scene.items.some(i=>!/^_?Group$/.test(i.symbols.constructorName)))fail('plain Group constructors');
    identity(scene.root.fields,true);identity(scene.group.fields);
    const x=value(scene.group.fields,'translationX'),y=value(scene.group.fields,'translationY');
    return {legend:box(scene.boxes.group),items:scene.items.map((i,index)=>{
      identity(i.fields);identity(i.symbols.fields,true);identity(i.label.fields);identity(i.marker.fields);
      const ix=value(i.fields,'translationX'),iy=value(i.fields,'translationY'),b=scene.boxes.items[index];
      const marker=box(b.marker),label=box(b.label);
      return {item:translate(box(b.item),x,y),label:translate(label,x+ix,y+iy),marker:translate(marker,x+ix,y+iy),
        markerLabelGap:label.x-(marker.x+marker.width)};
    })};
  }
  function gap(legend,plot,position){
    if(position==='top')return plot.y-(legend.y+legend.height);
    if(position==='bottom')return legend.y-(plot.y+plot.height);
    if(position==='left')return plot.x-(legend.x+legend.width);
    if(position==='right')return legend.x-(plot.x+plot.width);
    fail('position');
  }
  return {value,box,identity,convert,gap};
}
