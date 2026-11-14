import { execFile } from 'node:child_process';
import { isAbsolute, relative } from 'node:path';
import { checkedOutput, outputRoot } from './evidence.ts';

export interface RuntimeDescriptor {
  schema_version: 1;
  session_id: string;
  backend: 'compose';
  phase: 'ready';
  name: string;
  origin: string;
  container: string;
  credentials: { email: string; password: string };
  images: Record<'workspace' | 'data-api', string>;
  packaged_image_only: true;
  source_overlay: null;
  release_image_verified: false;
}

function object(value: unknown): value is Record<string, unknown> {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}
function readyDescriptor(value: unknown): value is RuntimeDescriptor {
  if (!object(value) || !object(value.credentials) || !object(value.images)) return false;
  const images = value.images;
  const origin = typeof value.origin === 'string' ? value.origin : '';
  const match = /^http:\/\/127\.0\.0\.1:([1-9][0-9]*)$/.exec(origin);
  return value.schema_version === 1 && value.backend === 'compose' && value.phase === 'ready'
    && typeof value.session_id === 'string' && /^[a-f0-9]{32}$/.test(value.session_id)
    && value.name === `qopenbb-browser-${value.session_id}`
    && typeof value.container === 'string' && /^[a-f0-9]{64}$/.test(value.container)
    && !!match && Number(match[1]) <= 65535
    && typeof value.credentials.email === 'string' && !!value.credentials.email
    && typeof value.credentials.password === 'string' && !!value.credentials.password
    && Object.keys(images).sort().join(',') === 'data-api,workspace'
    && ['workspace', 'data-api'].every(key => typeof images[key] === 'string'
      && /^sha256:[a-f0-9]{64}$/.test(images[key] as string))
    && value.packaged_image_only === true && value.source_overlay === null
    && value.release_image_verified === false;
}

export async function readRuntimeDescriptor(path: string): Promise<RuntimeDescriptor> {
  const python = process.env.QOPENBB_RUNTIME_PYTHON;
  if (!python || !isAbsolute(python) || !path || !isAbsolute(path))
    throw new Error('Runtime descriptor read refused');
  try {
    const payload = await new Promise<string>((accept, reject) => {
      execFile(python, ['-B', '-m', 'qopenbb_ci.session_files', 'read', '--private-ipc', '--path', path],
        { shell: false, windowsHide: true, encoding: 'utf8', maxBuffer: 1024 * 1024, timeout: 20000 },
        (error, stdout) => error ? reject(new Error('Runtime descriptor read refused')) : accept(stdout));
    });
    const value: unknown = JSON.parse(payload);
    if (!readyDescriptor(value)) throw new Error('Runtime descriptor read refused');
    return value;
  } catch {
    throw new Error('Runtime descriptor read refused');
  }
}

export function checkpointPath(value: string): string {
  const root = outputRoot();
  const path = checkedOutput(value);
  const suffix = relative(root, path);
  if (!suffix || suffix.startsWith('..') || isAbsolute(suffix))
    throw new Error('Checkpoint must be beneath the owned evidence root');
  return path;
}

export async function writeResearchCheckpoint(path: string, value: unknown): Promise<void> {
  try {
    const python = process.env.QOPENBB_RUNTIME_PYTHON;
    const runtime = process.env.WORKSPACE_RUNTIME_PRIVATE;
    if (!python || !isAbsolute(python) || !runtime || !isAbsolute(runtime))
      throw new Error('Checkpoint write refused');
    const target = checkpointPath(path);
    const payload = `${JSON.stringify(value, null, 2)}\n`;
    if (Buffer.byteLength(payload, 'utf8') > 1024 * 1024) throw new Error('Checkpoint write refused');
    await new Promise<void>((accept, reject) => {
      const child = execFile(python, ['-B', '-m', 'qopenbb_ci.checkpoint_cli', '--runtime', runtime, '--path', target],
        { shell: false, windowsHide: true, encoding: 'utf8', maxBuffer: 1024, timeout: 20000 },
        error => error ? reject(new Error('Checkpoint write refused')) : accept());
      if (!child.stdin) { child.kill(); reject(new Error('Checkpoint write refused')); return; }
      child.stdin.on('error', () => reject(new Error('Checkpoint write refused')));
      child.stdin.end(payload, 'utf8');
    });
  } catch {
    throw new Error('Checkpoint write refused');
  }
}

