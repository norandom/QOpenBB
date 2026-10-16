import { mkdtemp, mkdir, writeFile, rm } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { execFileSync } from 'node:child_process';

export function browserEnvironment(): Record<string, string> {
  const result: Record<string, string> = {};
  for (const key of ['PATH', 'SYSTEMROOT', 'WINDIR', 'LD_LIBRARY_PATH']) {
    if (process.env[key]) result[key] = process.env[key]!;
  }
  return result;
}
export async function runRoot() {
  const base = resolve('artifacts/task-1.7/runs');
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
