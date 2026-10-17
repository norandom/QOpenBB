export const ownerLabel='org.qopenbb.capture.owner';
export function networkOwnership(runtime,network){
  if(network?.Id!==runtime.networkId||network?.Name!==runtime.networkName||network?.Labels?.[ownerLabel]!==runtime.ownership)throw Error('network-isolation-unresolved: network ownership');
}
export function networkGuard(runtime,network){
  networkOwnership(runtime,network);
  if(network?.Driver!=='bridge'||network?.Internal!==true||network?.EnableIPv6!==false)throw Error('network-isolation-unresolved: internal owned bridge');
  return {internal:true,driver:network.Driver,ipv6:false,owned:true};
}
export function containerNetworkGuard(runtime,container){
  const networks=container?.NetworkSettings?.Networks,keys=Object.keys(networks??{}),ports=container?.NetworkSettings?.Ports?.['3000/tcp'];
  if(container?.Id!==runtime.container||container?.Config?.Labels?.[ownerLabel]!==runtime.ownership||keys.length!==1||keys[0]!==runtime.networkName||networks[keys[0]].NetworkID!==runtime.networkId)throw Error('network-isolation-unresolved: extra or wrong attached network');
  if(!Array.isArray(ports)||ports.length!==1||ports[0].HostIp!=='127.0.0.1'||!/^\d+$/.test(ports[0].HostPort))throw Error('network-isolation-unresolved: loopback publication');
  return {onlyOwnedNetwork:true,loopbackOnly:true,port:ports[0].HostPort};
}
export function ownedNetworkIds(docker,runtime){
  const lines=docker('network','ls','--no-trunc','--filter','name='+runtime.networkName,'--format','{{.ID}} {{.Name}}').trim().split('\n').filter(Boolean);
  if(lines.length>4)throw Error('Owned network listing bound');
  const matches=lines.map(line=>line.trim().split(/\s+/)).filter(([,name])=>name===runtime.networkName);
  if(matches.length>1)throw Error('Ambiguous owned network');return matches.map(([id])=>id);
}
