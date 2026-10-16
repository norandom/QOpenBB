import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { test } from 'node:test';
import { measure } from '../../tools/quality/syntax_units.ts';

const parserPath = fileURLToPath(new URL('../../tools/quality/syntax_units.ts', import.meta.url));
const root = fileURLToPath(new URL('../../', import.meta.url));

function run(input, cwd = root) {
  return spawnSync(process.execPath, [parserPath], {
    input, cwd, encoding: 'utf8', windowsHide: true,
  });
}

function withFiles(files, action) {
  const artifacts = resolve(root, 'artifacts/task-1.4');
  mkdirSync(artifacts, { recursive: true });
  const directory = mkdtempSync(resolve(artifacts, 'parser-fixture-'));
  try {
    for (const [name, source] of Object.entries(files)) {
      writeFileSync(resolve(directory, name), source);
    }
    action(directory);
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
}

test('formatting, comments, newline styles and empty statements do not add units', () => {
  for (const newline of ['\n', '\r\n', '\r']) {
    assert.equal(measure(`// doc${newline}${newline}let x=1;${newline}x++; x++;;;`).logical, 3);
  }
  assert.deepEqual(measure('/* empty */;;;'), { path: 'fixture.ts', logical: 0, functions: [] });
});

test('declarations, class members and type signatures count as units', () => {
  const source = `interface X { a: number; f(): void; (): void; new(): X; [k:string]: unknown }
    class C { a=1; constructor(){} m(){return;} get value(){return 1;} set value(v){a(v);} }`;
  const result = measure(source);
  assert.equal(result.logical, 15);
  assert.deepEqual(result.functions.map(({ name, logical }) => [name, logical]),
    [['constructor', 0], ['m', 1], ['value', 1], ['value', 1]]);
});

test('nested arrow and class method bodies have separate callable budgets', () => {
  const result = measure('function outer(){ const f=()=>{a();b();}; class C { m(){c();d();} } return f; }');
  assert.equal(result.logical, 9);
  assert.deepEqual(result.functions.map(({ name, logical }) => [name, logical]),
    [['outer', 4], ['f', 2], ['m', 2]]);
});

test('nested expression-bodied arrows remain in file totals and outside parent bodies', () => {
  const result = measure('const outer = () => () => 42;');
  assert.equal(result.logical, 3);
  assert.deepEqual(result.functions.map(({ name, logical }) => [name, logical]),
    [['outer', 1], ['<anonymous>', 1]]);
});

test('callable source positions are one-based and names are stable', () => {
  assert.deepEqual(measure('\nconst f=()=>42;').functions,
    [{ name: 'f', line: 2, column: 9, logical: 1 }]);
  assert.deepEqual(measure('function named(){}\nconst obj={m(){},get x(){return 1;}};').functions,
    [{ name: 'named', line: 1, column: 1, logical: 0 },
      { name: 'm', line: 2, column: 12, logical: 0 },
      { name: 'x', line: 2, column: 18, logical: 1 }]);
});

test('file and callable thresholds are measured exactly', () => {
  for (const count of [300, 301]) assert.equal(measure('a();'.repeat(count)).logical, count);
  for (const count of [50, 51]) {
    assert.equal(measure(`function f(){${'a();'.repeat(count)}}`).functions[0].logical, count);
  }
});

test('all eight explicit script extensions parse their supported syntax', () => {
  for (const extension of ['js', 'jsx', 'mjs', 'cjs', 'ts', 'tsx', 'mts', 'cts']) {
    const path = `input.${extension}`;
    const source = ['jsx', 'tsx'].includes(extension)
      ? 'const View = () => <main><span value={1}/></main>;'
      : ['ts', 'mts', 'cts'].includes(extension)
        ? 'const value: number = 1; const f = (): number => value;'
        : 'const value = 1; const f = () => value;';
    const result = measure(source, path);
    assert.equal(result.path, path);
    assert.equal(result.logical, ['jsx', 'tsx'].includes(extension) ? 2 : 3);
    assert.equal(result.functions[0].logical, 1);
  }
});

test('JSX and TSX retain callable units inside JSX expressions', () => {
  for (const path of ['view.jsx', 'view.tsx']) {
    const result = measure('const View = () => <div>{items.map(x => <span>{x}</span>)}</div>;', path);
    assert.equal(result.logical, 3);
    assert.deepEqual(result.functions.map(({ logical }) => logical), [1, 1]);
  }
});

test('invalid syntax and unsupported file extensions fail with path context', () => {
  assert.throws(() => measure('function broken( {', 'broken.ts'), /broken\.ts:/);
  assert.throws(() => measure('const view = <div/>;', 'broken.ts'), /broken\.ts:/);
  assert.throws(() => measure('const value=1;', 'unsupported.vue'), /unsupported\.vue.*[Uu]nsupported/);
});

test('JavaScript files reject TypeScript-only syntax', () => {
  for (const path of ['input.js', 'input.jsx', 'input.mjs', 'input.cjs']) {
    assert.throws(() => measure('const value: number = 1;', path), /TypeScript/);
    assert.throws(() => measure('interface X {}', path), /TypeScript/);
  }
});

test('empty CLI path array returns an empty JSON array', () => {
  const result = run('[]');
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stderr, '');
  assert.deepEqual(JSON.parse(result.stdout), []);
});

test('CLI validates the entire path array and emits no partial result', () => {
  for (const input of ['', 'null', '{}', '"file.ts"', '[1]', '["file.ts", null]', '{']) {
    const result = run(input);
    assert.equal(result.status, 2, input);
    assert.equal(result.stdout, '');
    assert.notEqual(result.stderr, '');
  }
});

test('CLI preserves relative, absolute and duplicate paths in deterministic input order', () => {
  withFiles({ 'one.ts': 'const f = () => 1;', 'two.jsx': 'const v = <div/>;' }, (directory) => {
    const paths = ['two.jsx', resolve(directory, 'one.ts'), 'two.jsx'];
    const first = run(JSON.stringify(paths), directory);
    const second = run(JSON.stringify(paths), directory);
    assert.equal(first.status, 0, first.stderr);
    assert.equal(first.stderr, '');
    assert.equal(first.stdout, second.stdout);
    const records = JSON.parse(first.stdout);
    assert.deepEqual(records.map(({ path }) => path), paths);
    assert.deepEqual(records.map(({ logical }) => logical), [1, 2, 1]);
    assert.deepEqual(records[0], records[2]);
  });
});

test('CLI read, parse and extension failures emit stderr with exit 2 and no partial JSON', () => {
  withFiles({ 'valid.ts': 'const a=1;', 'broken.ts': 'function broken( {', 'unsupported.vue': '' }, (directory) => {
    for (const invalid of ['missing.ts', 'broken.ts', 'unsupported.vue']) {
      const result = run(JSON.stringify(['valid.ts', invalid]), directory);
      assert.equal(result.status, 2, invalid);
      assert.equal(result.stdout, '');
      assert.match(result.stderr, new RegExp(invalid.replace('.', '\\.')));
    }
  });
});

test('production parser passes strict no-emit checking with the pinned TypeScript compiler', () => {
  const compiler = resolve(root, 'verification/node_modules/typescript/bin/tsc');
  const result = spawnSync(process.execPath, [compiler, '--project', 'tools/quality/tsconfig.json'], {
    cwd: root, encoding: 'utf8', windowsHide: true,
  });
  assert.equal(result.status, 0, result.stdout + result.stderr);
});
