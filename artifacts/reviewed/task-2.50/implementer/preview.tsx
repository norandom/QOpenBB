import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import { ChartTitlesPanel } from "/@fs/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro/src/components/General/Table/Chart/editor/titles/ChartTitlesPanel.tsx";
import "/@fs/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro/src/styles/tokens.css";
const base = { enabled: true, text: "Revenue", font: "Verdana", weight: "predefined", size: 18, color: "rgba(39, 198, 160, 0.502)", spacing: 10 };
function Preview({ theme }) {
  const [value, setValue] = useState({ title: { ...base }, subtitle: { ...base, text: "USD million", size: 14 }, horizontalAxisTitle: { ...base, text: "Period", size: 12 }, verticalAxisTitle: { ...base, text: "USD million", size: 12 } });
  const [edit, setEdit] = useState(null);
  return <section className={theme === "dark" ? "dark" : ""} data-theme={theme} style={{ background: "var(--surface-page)", color: "var(--text-heading)", padding: 20 }}>
    <h1 style={{ fontSize: 14 }}>{theme}: Titles component</h1><p style={{ width: 260, fontSize: 12 }}>Titles only. Other Customize groups, storage and dashboard wiring remain pending. Menu choices and bounds are candidate examples.</p>
    <div style={{ width: 260, background: "var(--surface-card)", border: "1px solid var(--general-border-primary)" }}><ChartTitlesPanel value={value}
      fonts={[{ value: "Verdana", label: "Verdana" }, { value: "Arial", label: "Arial" }]}
      weights={[{ value: "predefined", label: "Predefined" }, { value: "400-italic", label: "Italic" }]}
      sizes={[12, 14, 18, 24].map((value) => ({ value, label: String(value) }))} spacingBounds={{ min: 0, max: 100, step: 1 }}
      onEdit={(next) => { setEdit(next); setValue((previous) => ({ ...previous, [next.caption]: { ...previous[next.caption], [next.field]: next.value } })); }} /></div>
    <output style={{ display: "block", width: 260, overflowWrap: "anywhere", fontSize: 11 }}>{JSON.stringify(edit)}</output>
  </section>;
}
createRoot(document.getElementById("root")).render(<main style={{ display: "flex", gap: 24, fontFamily: "Arial" }}><Preview theme="light" /><Preview theme="dark" /></main>);
