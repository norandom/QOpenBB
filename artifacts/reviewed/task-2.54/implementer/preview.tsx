import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import { ChartBackgroundPanel } from "/@fs/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro/src/components/General/Table/Chart/editor/background/ChartBackgroundPanel.tsx";
import "/@fs/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro/src/styles/tokens.css";
function Preview({ theme }) {
 const [value, setValue] = useState({visible:true,fill:theme==='dark'?'#151518':'#ffffff'});
 const [edit,setEdit]=useState(null);
 return <section className={theme==='dark'?'dark':''} data-theme={theme} style={{background:'var(--surface-page)',color:'var(--text-heading)',padding:20}}>
 <h1 style={{fontSize:14}}>{theme}: Background subsection</h1><p style={{width:260,fontSize:12}}>Background only. Chart rendering, other Chart Style controls and storage remain pending.</p>
 <div style={{width:260,background:'var(--surface-card)',border:'1px solid var(--general-border-primary)',paddingTop:12}}><ChartBackgroundPanel value={value} onEdit={next=>{setEdit(next);setValue(previous=>({...previous,[next.field]:next.value}));}}/></div>
 <output style={{display:'block',width:260,overflowWrap:'anywhere',fontSize:11}}>{JSON.stringify(edit)}</output>
 </section>;
}
createRoot(document.getElementById('root')).render(<main style={{display:'flex',gap:24,fontFamily:'Arial'}}><Preview theme="light"/><Preview theme="dark"/></main>);
