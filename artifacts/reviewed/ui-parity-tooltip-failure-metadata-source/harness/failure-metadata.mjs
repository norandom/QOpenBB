const metadataBytes=512;
const bytes=value=>Buffer.byteLength(JSON.stringify(value));
const metadata=(reason,reasonCode,reasonOmitted,failureOrigin)=>({reason,reasonCode,reasonOmitted,failureOrigin});

export function failureMetadata(error,failureOrigin,credential){
  const unavailable=()=>metadata('Failure message unavailable','message-unavailable',true,failureOrigin);
  try{
    const message=error.message;
    if(typeof message!=='string')return unavailable();
    const reasonCode=message==='not-run-budget'?'not-run-budget':'exception';
    let reason=message;
    for(const secret of [credential.email,credential.password])if(typeof secret==='string'&&secret.length)reason=reason.replaceAll(secret,'[redacted]');
    const complete=metadata(reason,reasonCode,false,failureOrigin);
    if(bytes(complete)<=metadataBytes)return complete;
    return metadata('Failure message omitted: serialized metadata limit','message-over-byte-cap',true,failureOrigin);
  }catch{return unavailable();}
}
