import React, { useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import { ChartEditorDock } from "/@fs/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro/src/components/General/Table/Chart/editor/ChartEditorDock.tsx";
import { chartTypeGalleryGroups } from "/@fs/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro/src/components/General/Table/Chart/editor/chartTypeGalleryCatalog.ts";
import "/@fs/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro/src/styles/tokens.css";
function Fixture({ name }) {
  const [expanded, setExpanded] = useState(false);
  return <div style={{ padding: 12, height: 1200 }}><button onClick={() => setExpanded(!expanded)}>{name} group</button>{expanded && <input aria-label={`${name} value`} defaultValue="Fixture value" />}</div>;
}
function PreviewDock({ theme }) {
  const [open, setOpen] = useState(true);
  const [activeTab, setActiveTab] = useState("chart");
  const [selectedType, setSelectedType] = useState("groupedColumn");
  const [themeKey, setThemeKey] = useState(0);
  const opener = useRef(null);
  return <section className={theme === "dark" ? "dark" : ""} data-theme={theme} style={{ background: "var(--surface-page)", color: "var(--text-heading)", padding: 20, width: 300 }}>
    <h1 style={{ fontSize: 14 }}>{theme}: Dock component preview</h1>
    <p style={{ fontSize: 12 }}>Set Up / Customize are interactive fixtures. Application wiring remains pending.</p>
    <button ref={opener} onClick={() => setOpen(true)}>Chart settings</button>
    <button onClick={() => setThemeKey(themeKey + 1)}>Rebuild fixture theme</button>
    <div style={{ height: 343, marginTop: 12 }}><ChartEditorDock open={open} activeTab={activeTab} onOpenChange={setOpen} onTabChange={setActiveTab} openerRef={opener} themeResetKey={themeKey} galleryProps={{ groups: chartTypeGalleryGroups, selectedType, onSelect: setSelectedType }} setup={<Fixture name="Setup" />} customize={<Fixture name="Customize" />} /></div>
    <p style={{ fontSize: 12 }}>Selected model: <output>{selectedType}</output></p>
  </section>;
}
createRoot(document.getElementById("root")).render(<main style={{ display: "flex", gap: 32, padding: 24, fontFamily: "Arial" }}><PreviewDock theme="light" /><PreviewDock theme="dark" /></main>);

