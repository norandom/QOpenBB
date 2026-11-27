import type { Page, Request } from '../../verification/node_modules/@playwright/test/index.mjs';
import type { Slot } from './events-documents-browser.mts';

type Scope = { stage: string; slot: Slot };
const expectedFailures: Record<string, number> = { 'listing/news': 403, 'timeout-news/news': 400 };
type Counts = Record<string, number>;

function add(counts: Counts, label: string) {
  counts[label] = (counts[label] ?? 0) + 1;
}

export function controlledDiagnostics(origin: string, fixtureHost: string, live = false) {
  const scopes = new WeakMap<Request, Scope>();
  const external = new Set<string>();
  const expectedConsole = new Map<string, Set<number>>();
  const result = {
    fixtureExternal: 0, abortedData: 0, errors: {} as Counts,
    httpErrors: {} as Counts, consoleErrors: {} as Counts, externalBlocks: 0,
    abortedSlots: {} as Counts,
  };

  function scopeLabel(request: Request) {
    const scope = scopes.get(request);
    return scope && scope.stage + '/' + scope.slot;
  }

  function observe(page: Page) {
    page.on('response', response => {
      const status = response.status();
      if (status < 400 || new URL(response.url()).origin !== origin) return;
      const label = scopeLabel(response.request());
      if (label && (live || expectedFailures[label] === status)) add(result.httpErrors, label + '/' + status);
      else add(result.errors, 'unexpected-same-origin-http-' + Math.trunc(status / 100) + 'xx');
    });
    page.on('requestfailed', request => {
      const target = new URL(request.url());
      if (target.origin !== origin) return;
      const label = scopeLabel(request);
      const reason = request.failure()?.errorText;
      if (label?.includes('-away/') && reason === 'net::ERR_ABORTED') {
        result.abortedData++;
        add(result.abortedSlots, label);
      } else if (target.pathname.startsWith('/data/api/v1/') || reason !== 'net::ERR_ABORTED') {
        add(result.errors, 'unexpected-same-origin-transport-failure');
      }
    });
    page.on('console', message => {
      if (message.type() !== 'error') return;
      const url = message.location().url;
      const status = /^Failed to load resource: the server responded with a status of (\d{3})\b/.exec(message.text());
      const aborted = /^Failed to load resource: net::ERR_/.test(message.text());
      if (status && expectedConsole.get(url)?.has(Number(status[1]))) {
        add(result.consoleErrors, 'expected-fixture-http-' + status[1]);
      } else if (aborted && external.has(url)) {
        add(result.consoleErrors, 'blocked-cross-origin-resource');
      } else {
        add(result.errors, status ? 'unexpected-http-console-error' : aborted
          ? 'unexpected-transport-console-error' : 'application-console-error');
      }
    });
  }

  function register(request: Request, scope: Scope, status: number) {
    scopes.set(request, scope);
    if (live ? status < 400 : expectedFailures[scope.stage + '/' + scope.slot] !== status) return;
    const statuses = expectedConsole.get(request.url()) ?? new Set<number>();
    statuses.add(status);
    expectedConsole.set(request.url(), statuses);
  }

  function blockExternal(target: URL) {
    result.externalBlocks++;
    external.add(target.href);
    if (target.hostname === fixtureHost) result.fixtureExternal++;
  }

  function recordTransportFailure() {
    add(result.errors, 'devtools-transport-failure');
  }

  return { result, observe, register, blockExternal, recordTransportFailure };
}
