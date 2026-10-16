import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';

// Only synthetic observations are served; no operator configuration is loaded.
export async function startFixture(port = 0) {
  const observation = JSON.parse(await readFile('tests/providers/fixtures/observation.json', 'utf8'));
  const server = createServer((request, response) => {
    if (request.url?.startsWith('/failure')) {
      response.writeHead(503).end('unavailable');
      return;
    }
    response.setHeader('Content-Type', 'text/html');
    response.end(`<main><output>${observation.value} ${observation.unit}</output></main>`);
  });
  await new Promise<void>((resolve, reject) => {
    const timer = setTimeout(() => { server.close(); reject(new Error('fixture readiness timeout')); }, 5000);
    server.once('error', error => { clearTimeout(timer); reject(error); });
    server.listen({ host: '127.0.0.1', port, exclusive: true }, () => { clearTimeout(timer); resolve(); });
  });
  const address = server.address();
  if (!address || typeof address === 'string') throw new Error('fixture address unavailable');
  return { url: `http://127.0.0.1:${address.port}`, port: address.port,
    close: () => new Promise<void>((resolve, reject) => {
      server.close(error => error ? reject(error) : resolve());
      server.closeAllConnections();
    }) };
}
