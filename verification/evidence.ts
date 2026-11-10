import { mkdtemp, mkdir, writeFile, rm } from 'node:fs/promises';
import { lstatSync } from 'node:fs';
import { resolve, join, parse, dirname, relative, isAbsolute } from 'node:path';
import { tmpdir } from 'node:os';
import { execFileSync } from 'node:child_process';

const cacheKeys = ['TEMP', 'TMP', 'TMPDIR', 'PLAYWRIGHT_BROWSERS_PATH', 'UV_CACHE_DIR',
  'CARGO_HOME', 'CARGO_TARGET_DIR', 'npm_config_cache', 'PIP_CACHE_DIR',
  'BUN_INSTALL_CACHE_DIR', 'PNPM_STORE_DIR', 'npm_config_store_dir'];

export function checkedOutput(value: string): string {
  const path = resolve(value);
  if (!isAbsolute(value) || path === parse(path).root) throw new Error('Absolute non-root output required');
  if (process.platform === 'win32') {
    const child = relative('D:/BuildArtifacts', path);
    if (!child || child.startsWith('..') || isAbsolute(child)) throw new Error('Output must be beneath D:/BuildArtifacts');
  } else if (/^\/mnt\/[cd](\/|$)/.test(path)) throw new Error('Linux outputs require Linux storage');
  for (let part = path; part !== dirname(part); part = dirname(part)) {
    try {
      if (lstatSync(part).isSymbolicLink()) throw new Error('Linked output paths forbidden');
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== 'ENOENT') throw error;
    }
  }
  return path;
}

export function outputRoot(): string {
  if (resolve('.') === parse(resolve('.')).root) throw new Error('Repository working directory required');
  return checkedOutput(process.env.QOPENBB_VERIFICATION_ROOT ?? (process.platform === 'win32'
    ? 'D:/BuildArtifacts/QOpenBB/verification' : join(tmpdir(), 'qopenbb-verification')));
}

export function browserEnvironment(): Record<string, string> {
  const result: Record<string, string> = {};
  const systemKeys = ['PATH', 'SYSTEMROOT', 'WINDIR', 'COMSPEC', 'PATHEXT', 'SYSTEMDRIVE', 'LD_LIBRARY_PATH'];
  for (const [key, value] of Object.entries(process.env)) {
    if (!value) continue;
    if (cacheKeys.some(item => item.toUpperCase() === key.toUpperCase())) {
      checkedOutput(value); result[key] = value;
    } else if (systemKeys.includes(key.toUpperCase())) result[key] = value;
  }
  if (process.platform === 'win32' && !result.PLAYWRIGHT_BROWSERS_PATH) {
    throw new Error('Explicit PLAYWRIGHT_BROWSERS_PATH required on Windows');
  }
  result.QOPENBB_VERIFICATION_ROOT = outputRoot();
  return result;
}
export async function runRoot() {
  const base = join(outputRoot(), 'runs');
  browserEnvironment();
  await mkdir(base, { recursive: true });
  return mkdtemp(join(base, 'run-'));
}
export function revision() {
  return execFileSync('git', ['rev-parse', 'HEAD'], { encoding: 'utf8', windowsHide: true,
    env: browserEnvironment() }).trim();
}
export async function retain(root: string, record: object) {
  await writeFile(join(root, 'evidence.json'), JSON.stringify(record, null, 2));
}
export async function clearProfile(root: string) {
  await rm(join(root, 'profile'), { recursive: true, force: true });
}
