import fs from 'node:fs';
import path from 'node:path';
import ts from '/mnt/d/Source/QOpenBB/verification/node_modules/typescript/lib/typescript.js';
const root = '/home/mc/qopenbb-work/widget-246-stage/terminalpro';
const component = `${root}/src/components`;
const deps = `${root}/node_modules`;
const actualTypes = `${component}/types.d.ts`;
const boundaries = {
  'lodash.isequal': 'export default function isEqual(a: unknown,b: unknown): boolean;',
  '~/lib/contexts/TabContext': 'export function useTabContext(): { getWidget(id:string): WidgetT; isShared:boolean };',
  '~/lib/state/app': `export type Group = any; export type Ticker = any; export type AppState = any;
    export function useShallowAppStore<T>(selector:(state:{updateWidget:(id:string,w:WidgetT)=>void})=>T): T;
    export const useAppStore: { subscribe: { (listener:string):()=>void; (listener:number):()=>void } };`,
  '~/lib/state/sharedApp': 'export type SharedAppState=any; export const useSharedAppStore: {subscribe: { (listener:boolean):()=>void; (listener:symbol):()=>void }};',
  '~/components/General/Table/hooks/utils': 'export function useIsFirstRender():boolean;',
  '~/lib/utils': `export function getEndpointParamName(params:unknown[],id:string):string;
    export function getEndpointParamGroupByIds(w:WidgetT):Record<string,string>;
    export function getCellOnClickParams(w:WidgetT, flag:boolean):string[];
    export function getJsonWidget(w:WidgetT):WidgetT; export function getWidgetInfo(w:WidgetT):string;
    export function isOmniType(t:string):boolean; export function isSSRMType(t:string):boolean;
    export function useEventListener(name:string, callback: (...args:any[])=>void):void;
    export function triggerCustomEvent<T extends \`runParams-\${string}\` | \`updateQueryParams-\${string}\` | "saveWidgets" | "refreshQuery" | \`updateWidget-\${string}\` , DataT = unknown>(name:T,detail?:DataT):boolean;
    export function needsGroupValueUpdate(w:WidgetT,g:any):boolean;
    export function addToWidgetParamGroups(groups:Record<string,string>,g:any):Record<string,string>;
    export function updateWidgetGroupValues(w:WidgetT,groups:any[]):WidgetT;`,
};
const virtual = new Map(Object.entries(boundaries).map(([name, body], i) => [name,
  { path: `${root}/__widget_boundary_${i}.d.ts`, text: `import type { WidgetT } from "${actualTypes}";\n${body}` }]));
const roots = ['Widget.hooks.tsx','widgetSync/updates.ts','widgetSync/useWidgetUpdates.ts','widgetSync/useWidgetSubscriptions.ts'].map(p=>`${component}/${p}`);
const options = { noEmit:true, skipLibCheck:true, strict:false, target:ts.ScriptTarget.ESNext,
 module:ts.ModuleKind.ESNext, moduleResolution:ts.ModuleResolutionKind.Node10, jsx:ts.JsxEmit.ReactJSX,
 ignoreDeprecations:"6.0", allowSyntheticDefaultImports:true, lib:['lib.esnext.d.ts','lib.dom.d.ts'], types:[] };
const host=ts.createCompilerHost(options);
const originalGet=host.getSourceFile.bind(host);
host.getSourceFile=(file,...args)=> {
 const entry=[...virtual.values()].find(v=>v.path===file);
 return entry ? ts.createSourceFile(file,entry.text,options.target,true) : originalGet(file,...args);
};
host.resolveModuleNames=(names, containing)=>names.map(name=> {
 let file;
 if (virtual.has(name)) file=virtual.get(name).path;
 else if (name==='react') file=`${deps}/@types/react/index.d.ts`;
 else if (name==='~/hooks/useRefHooks') file=`${root}/src/hooks/useRefHooks.tsx`;
 else if (name.endsWith('General/Table/hooks/utils')) file=virtual.get('~/components/General/Table/hooks/utils').path;
 else if (name===actualTypes || name==='./types' || name==='../types') file=actualTypes;
 else if (name.startsWith('./')) {
   const base=path.resolve(path.dirname(containing),name);
   file=[base+'.ts',base+'.tsx',base+'.d.ts'].find(fs.existsSync);
 }
 return file ? { resolvedFileName:file, extension:file.endsWith('.tsx')?ts.Extension.Tsx:file.endsWith('.d.ts')?ts.Extension.Dts:ts.Extension.Ts } : undefined;
});
const program=ts.createProgram(roots,options,host);
const diagnostics=ts.getPreEmitDiagnostics(program).filter(d=>!d.file || roots.includes(d.file.fileName));
console.log(ts.formatDiagnosticsWithColorAndContext(diagnostics,{getCanonicalFileName:f=>f,getCurrentDirectory:()=>root,getNewLine:()=>"\n"}));
console.log(`Scoped actual production modules: ${roots.length}; diagnostics: ${diagnostics.length}. External declaration boundaries; not full application type certification.`);
process.exitCode=diagnostics.length?1:0;
