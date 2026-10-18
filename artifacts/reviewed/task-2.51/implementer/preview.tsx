import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import { ChartLegendPanel } from "/@fs/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro/src/components/General/Table/Chart/editor/legend/ChartLegendPanel.tsx";
import "/@fs/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro/src/styles/tokens.css";
const bounds = { min: 0, max: 40, step: 1 };
const base = { enabled: true, font: "Verdana", weight: "predefined", size: 11, position: "top", spacing: 20, markerSize: 11, markerStroke: 0, itemSpacing: 5, horizontalSpacing: 32, verticalSpacing: 8 };
function Preview({ theme }) {
  const [value, setValue] = useState({ ...base, color: theme === "dark" ? "#FFFFFF" : "#000000" });
  const [edit, setEdit] = useState(null);
  return <section className={theme === "dark" ? "dark" : ""} data-theme={theme} style={{ background: "var(--surface-page)", color: "var(--text-heading)", padding: 20 }}>
    <h1 style={{ fontSize: 14 }}>{theme}: Legend component</h1><p style={{ width: 260, fontSize: 12 }}>Controlled Legend only. Menu choices are examples. Renderer and storage integration remain pending.</p>
    <div style={{ width: 260, background: "var(--surface-card)", border: "1px solid var(--general-border-primary)" }}><ChartLegendPanel value={value}
      fonts={[{ value: "Verdana", label: "Verdana, sans-serif" }, { value: "Arial", label: "Arial" }]}
      weights={[{ value: "predefined", label: "Predefined" }, { value: "400-italic", label: "Italic" }]}
      sizes={[11, 18, 24].map((value) => ({ value, label: String(value) }))}
      positions={["top", "right", "bottom", "left"].map((value) => ({ value, label: value[0].toUpperCase()+value.slice(1) }))}
      bounds={{ spacing: { ...bounds, max: 200 }, markerSize: bounds, markerStroke: { ...bounds, max: 10 }, itemSpacing: bounds, horizontalSpacing: bounds, verticalSpacing: bounds }}
      onEdit={(next) => { setEdit(next); setValue((previous) => ({ ...previous, [next.field]: next.value })); }} /></div>
    <output style={{ display: "block", width: 260, overflowWrap: "anywhere", fontSize: 11 }}>{JSON.stringify(edit)}</output>
  </section>;
}
createRoot(document.getElementById("root")).render(<main style={{ display: "flex", gap: 24, fontFamily: "Arial" }}><Preview theme="light" /><Preview theme="dark" /></main>);
