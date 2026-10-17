import React from "react";
import { createRoot } from "react-dom/client";
import { ChartEditorControlsPreview } from "/@fs/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro/src/components/ds/organisms/ChartEditorControls.stories.tsx";
import "/@fs/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro/src/styles/tokens.css";
createRoot(document.getElementById("root")).render(<main style={{display:"flex",gap:32,padding:24,fontFamily:"Arial"}}>{["light","dark"].map(theme=><section key={theme} className={theme === "dark" ? "dark" : ""} data-theme={theme} style={{width:300,padding:20,background:"var(--surface-card)",color:"var(--text-heading)",fontSize:12}}><h1 style={{fontSize:14}}>{theme}: Controlled editor preview</h1><ChartEditorControlsPreview /></section>)}</main>);
