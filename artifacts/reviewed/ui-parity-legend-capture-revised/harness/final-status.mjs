export function assessFinal({incoming,cleanup,browser,eventDrain,eventOverflow,lateEvents,failure}){
  const cleanupVerified=cleanup?.status==='cleaned'&&cleanup?.networkAbsent===true&&cleanup?.browser?.identityRecorded===true&&cleanup?.browser?.browserProcessAbsent===true&&browser?.browserIdentityRecorded===true&&browser?.browserClosed===true&&browser?.contextClosed===true&&!browser?.closeError;
  const eventAccountingVerified=!eventOverflow&&!lateEvents&&eventDrain?.verified===true&&!failure;
  const status=cleanupVerified?(incoming===0&&eventAccountingVerified?'observed':'capture-failed'):'cleanup-unverified';
  return {exitCode:incoming,status,cleanupVerified,eventAccountingVerified,candidateExecuted:false};
}
