import type { BrowserContext, Page } from '@playwright/test';

export interface Diagnostic { kind: 'console' | 'exception' | 'network'; failed: boolean; status?: number }

// Deliberately retain categories and status only: even paths and error text can carry keys.
export async function diagnostics(context: BrowserContext, page: Page) {
  const events: Diagnostic[] = [];
  const session = await context.newCDPSession(page);
  session.on('Runtime.consoleAPICalled', event => {
    if (event.type === 'error') events.push({ kind: 'console', failed: true });
  });
  session.on('Runtime.exceptionThrown', () => events.push({ kind: 'exception', failed: true }));
  session.on('Network.responseReceived', event => {
    if (event.response.status >= 400) events.push({ kind: 'network', failed: true, status: event.response.status });
  });
  session.on('Network.loadingFailed', () => events.push({ kind: 'network', failed: true }));
  await session.send('Runtime.enable');
  await session.send('Network.enable');
  return { events, close: () => session.detach() };
}
