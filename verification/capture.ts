export function capturePolicy(credentialEntry = false, requested = false) {
  if (credentialEntry && requested) throw new Error('capture forbidden during credential entry');
  return { trace: false, video: false, screenshot: false } as const;
}
