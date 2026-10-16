import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { extname } from 'node:path';
import { pathToFileURL } from 'node:url';
import type * as TypeScript from '../../verification/node_modules/typescript/lib/typescript.js';

export interface FunctionMeasurement {
  name: string;
  line: number;
  column: number;
  logical: number;
}

export interface FileMeasurement {
  path: string;
  logical: number;
  functions: FunctionMeasurement[];
}

type Callable = TypeScript.FunctionLikeDeclaration & { readonly body: TypeScript.ConciseBody };

// Resolve the pinned parser from its owning project, independent of npm hoisting.
const ts: typeof TypeScript = createRequire(new URL('../../verification/package.json', import.meta.url))('typescript');
const scriptKinds = new Map([
  ['.js', ts.ScriptKind.JS], ['.jsx', ts.ScriptKind.JSX],
  ['.mjs', ts.ScriptKind.JS], ['.cjs', ts.ScriptKind.JS],
  ['.ts', ts.ScriptKind.TS], ['.tsx', ts.ScriptKind.TSX],
  ['.mts', ts.ScriptKind.TS], ['.cts', ts.ScriptKind.TS],
]);
const extraKinds = new Set([
  ts.SyntaxKind.MethodDeclaration, ts.SyntaxKind.Constructor,
  ts.SyntaxKind.GetAccessor, ts.SyntaxKind.SetAccessor,
  ts.SyntaxKind.PropertyDeclaration, ts.SyntaxKind.PropertySignature,
  ts.SyntaxKind.MethodSignature, ts.SyntaxKind.CallSignature,
  ts.SyntaxKind.ConstructSignature, ts.SyntaxKind.IndexSignature,
]);
const unit = (node: TypeScript.Node): boolean => (ts.isStatement(node) && !ts.isBlock(node)
  && !ts.isEmptyStatement(node)) || extraKinds.has(node.kind);
const callable = (node: TypeScript.Node): node is Callable => ts.isFunctionLike(node)
  && 'body' in node && node.body !== undefined;

function validateSyntax(ast: TypeScript.SourceFile): void {
  // Public syntactic diagnostics also reject TypeScript-only syntax in JS inputs.
  // The host serves only this AST so imports cannot widen the measured scope.
  const options: TypeScript.CompilerOptions = { allowJs: true, noLib: true, noResolve: true };
  const host = ts.createCompilerHost(options);
  host.getSourceFile = path => path === ast.fileName ? ast : undefined;
  const diagnostics = ts.createProgram([ast.fileName], options, host).getSyntacticDiagnostics(ast);
  if (diagnostics.length) {
    const diagnostic = diagnostics[0];
    const position = ast.getLineAndCharacterOfPosition(diagnostic.start ?? 0);
    const message = ts.flattenDiagnosticMessageText(diagnostic.messageText, ' ');
    throw new Error(`${ast.fileName}:${position.line + 1}:${position.character + 1}: ${message}`);
  }
}

function ownBody(node: Callable): number {
  if (!ts.isBlock(node.body)) return 1;
  let count = 0;
  function visit(child: TypeScript.Node): void {
    if (unit(child)) count++;
    // A nested declaration counts here; its body belongs to its own function budget.
    if (callable(child)) return;
    ts.forEachChild(child, visit);
  }
  ts.forEachChild(node.body, visit);
  return count;
}

function functionRecord(node: Callable, ast: TypeScript.SourceFile): FunctionMeasurement {
  const position = ast.getLineAndCharacterOfPosition(node.getStart(ast));
  const owner = node.name ?? (ts.isVariableDeclaration(node.parent) ? node.parent.name : undefined);
  const name = owner?.getText(ast) ?? (ts.isConstructorDeclaration(node) ? 'constructor' : '<anonymous>');
  return { name, line: position.line + 1, column: position.character + 1, logical: ownBody(node) };
}

export function measure(source: string, path = 'fixture.ts'): FileMeasurement {
  const scriptKind = scriptKinds.get(extname(path));
  if (scriptKind === undefined) throw new Error(`${path}: Unsupported script extension`);
  const ast = ts.createSourceFile(path, source, ts.ScriptTarget.Latest, true, scriptKind);
  validateSyntax(ast);
  let logical = 0;
  const functions: FunctionMeasurement[] = [];
  function visit(node: TypeScript.Node): void {
    if (unit(node)) logical++;
    if (callable(node)) {
      functions.push(functionRecord(node, ast));
      if (!ts.isBlock(node.body)) logical++;
    }
    ts.forEachChild(node, visit);
  }
  visit(ast);
  return { path, logical, functions };
}

function pathsArray(value: unknown): value is string[] {
  return Array.isArray(value) && value.every((path: unknown) => typeof path === 'string');
}

function main(): void {
  try {
    const paths: unknown = JSON.parse(readFileSync(0, 'utf8'));
    if (!pathsArray(paths)) {
      throw new Error('Expected a JSON array of file-path strings');
    }
    const results = paths.map(path => measure(readFileSync(path, 'utf8'), path));
    process.stdout.write(`${JSON.stringify(results)}\n`);
  } catch (error) {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 2;
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) main();
