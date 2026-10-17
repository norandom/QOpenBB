import fs from 'node:fs';
import zlib from 'node:zlib';
import {root,json} from './io.mjs';
function decode(file){
  const b=fs.readFileSync(file);if(!b.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10])))throw Error('PNG signature');
  let width,height,channels;const data=[];
  for(let o=8;o<b.length;){const length=b.readUInt32BE(o),type=b.toString('ascii',o+4,o+8),d=b.subarray(o+8,o+8+length);o+=12+length;
    if(type==='IHDR'){width=d.readUInt32BE(0);height=d.readUInt32BE(4);if(d[8]!==8||![2,6].includes(d[9])||d[12]!==0)throw Error('Unsupported PNG');channels=d[9]===6?4:3;}
    if(type==='IDAT')data.push(d);}
  const scan=zlib.inflateSync(Buffer.concat(data)),stride=width*channels,out=Buffer.alloc(height*stride);
  const paeth=(a,b,c)=>{const p=a+b-c,pa=Math.abs(p-a),pb=Math.abs(p-b),pc=Math.abs(p-c);return pa<=pb&&pa<=pc?a:pb<=pc?b:c;};
  for(let y=0;y<height;y++){const filter=scan[y*(stride+1)];for(let x=0;x<stride;x++){
    const i=y*stride+x,left=x>=channels?out[i-channels]:0,up=y?out[i-stride]:0,corner=y&&x>=channels?out[i-stride-channels]:0;
    const predictor=[0,left,up,Math.floor((left+up)/2),paeth(left,up,corner)][filter];if(predictor===undefined)throw Error('Unknown PNG filter');
    out[i]=(scan[y*(stride+1)+1+x]+predictor)&255;}}
  return {width,height,channels,data:out};
}
function crc(buffer){let n=0xffffffff;for(const byte of buffer){n^=byte;for(let bit=0;bit<8;bit++)n=(n>>>1)^((n&1)?0xedb88320:0);}return (n^0xffffffff)>>>0;}
function chunk(type,data){const name=Buffer.from(type),len=Buffer.alloc(4),sum=Buffer.alloc(4);len.writeUInt32BE(data.length);sum.writeUInt32BE(crc(Buffer.concat([name,data])));return Buffer.concat([len,name,data,sum]);}
function crop(image,r,file){
  const header=Buffer.alloc(13);header.writeUInt32BE(r.width);header.writeUInt32BE(r.height,4);header[8]=8;header[9]=image.channels===4?6:2;
  const rows=[];for(let y=r.y;y<r.y+r.height;y++)rows.push(Buffer.from([0]),image.data.subarray((y*image.width+r.x)*image.channels,(y*image.width+r.x+r.width)*image.channels));
  fs.writeFileSync(file,Buffer.concat([Buffer.from([137,80,78,71,13,10,26,10]),chunk('IHDR',header),chunk('IDAT',zlib.deflateSync(Buffer.concat(rows))),chunk('IEND',Buffer.alloc(0))]));
}
function compare(a,b,r){
  if(a.width!==b.width||a.height!==b.height)throw Error('Screenshot dimensions differ');let changed=0;const absolute=[0,0,0],signed=[0,0,0];
  for(let y=r.y;y<r.y+r.height;y++)for(let x=r.x;x<r.x+r.width;x++){
    let any=false;for(let c=0;c<3;c++){const d=b.data[(y*b.width+x)*b.channels+c]-a.data[(y*a.width+x)*a.channels+c];absolute[c]+=Math.abs(d);signed[c]+=d;if(d)any=true;}if(any)changed++;}
  return {pixels:r.width*r.height,changedPixels:changed,unchangedPixels:r.width*r.height-changed,absoluteChannelDifferences:absolute,signedChannelDifferences:signed};
}
const shots=JSON.parse(fs.readFileSync(root+'/screenshots.json')),ledger=JSON.parse(fs.readFileSync(root+'/action-ledger.json'));
const records=[],caseRegions=new Map();let previous=null;
for(const name of shots){
  const s=JSON.parse(fs.readFileSync(root+'/'+name+'.json')),image=decode(root+'/'+name+'.png'),chart=s.geometry.chart,plot=s.geometry.plot;
  if(!chart||!plot)throw Error('Recorded chart/plot geometry unavailable');
  const make=(kind,x,y,width=96,height=48)=>{const raw={x:Math.floor(x),y:Math.floor(y),width,height};
    const r={x:Math.max(0,Math.min(image.width-width,raw.x)),y:Math.max(0,Math.min(image.height-height,raw.y)),width,height};return {kind,rect:r,raw,clippedToViewport:r.x!==raw.x||r.y!==raw.y};};
  const first=s.live.series[0].nodes[0],x=chart.x+plot.x+first.x.value,y=chart.y+plot.y+first.y.value;
  const caseId=ledger.find(a=>a.image===name+'.png')?.id.split('.')[0]||'C01';
  const regions=caseRegions.get(caseId)||[make('bottom-axis',chart.x+plot.x+plot.width/2-48,chart.y+plot.y+plot.height-12),
    make('number-grid',chart.x+plot.x+plot.width/2-48,chart.y+plot.y+plot.height/2-24),
    make('bar-top-left-halo',x-20,y-20,Math.min(128,Math.max(48,Math.ceil(first.width.value)+40)),64),
    make('bar-interior',x+Math.max(1,first.width.value/2-4),y+Math.min(30,first.height.value/2),8,8)];caseRegions.set(caseId,regions);
  const selected=regions.map((r,index)=>{const file=name+'-region-'+index+'.png';crop(image,r.rect,root+'/'+file);return {...r,file,
    source:'recorded chart/plot + first actual bar rect geometry',outsideEdgeExtentCss:20,
    plotEdgeClipping:{left:r.raw.x<chart.x+plot.x,top:r.raw.y<chart.y+plot.y,right:r.raw.x+r.raw.width>chart.x+plot.x+plot.width,bottom:r.raw.y+r.raw.height>chart.y+plot.y+plot.height},
    previous:previous?{checkpoint:previous.name,...compare(previous.image,image,r.rect)}:null};});
  records.push({checkpoint:name,case:caseId,regions:selected});previous={name,image};
}
json('raster-measurements',{policy:'Exact RGB byte differences in finite regions; no universal tolerance or candidate equivalence asserted',records});
