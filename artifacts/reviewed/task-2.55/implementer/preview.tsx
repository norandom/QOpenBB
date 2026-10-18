import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import { ChartTooltipsPanel } from "/@fs/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro/src/components/General/Table/Chart/editor/tooltips/ChartTooltipsPanel.tsx";
import "/@fs/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro/src/styles/tokens.css";
const modes=[{value:'single',label:'Single'},{value:'shared',label:'Multiple'},{value:'compact',label:'Compact'}];
function Preview({theme}) {
 const [value,setValue]=useState({enabled:true,mode:'shared'});const [edit,setEdit]=useState(null);
 return <section className={theme==='dark'?'dark':''} data-theme={theme} style={{background:'var(--surface-page)',color:'var(--text-heading)',padding:20}}>
 <h1 style={{fontSize:14}}>{theme}: Tooltips within Series</h1><p style={{width:260,fontSize:12}}>Tooltips only. Other Series controls and live chart bindings remain pending.</p>
 <div style={{width:260,background:'var(--surface-card)',border:'1px solid var(--general-border-primary)'}}><ChartTooltipsPanel value={value} modes={modes} onEdit={next=>{setEdit(next);setValue(previous=>({...previous,[next.field]:next.value}));}}/></div>
 <output style={{display:'block',width:260,overflowWrap:'anywhere',fontSize:11}}>{JSON.stringify(edit)}</output>
 </section>;
}
createRoot(document.getElementById('root')).render(<main style={{display:'flex',gap:24,fontFamily:'Arial'}}><Preview theme="light"/><Preview theme="dark"/></main>);
