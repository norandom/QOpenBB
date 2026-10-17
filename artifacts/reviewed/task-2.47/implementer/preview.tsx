import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import { ChartTypeGallery } from "/@fs/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro/src/components/General/Table/Chart/editor/ChartTypeGallery.tsx";
import { chartTypeGalleryGroups } from "/@fs/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro/src/components/General/Table/Chart/editor/chartTypeGalleryCatalog.ts";
import "/@fs/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro/src/styles/tokens.css";

function Preview() {
  const [selectedType, setSelectedType] = useState("groupedColumn");
  return <main style={{ display: "flex", gap: 48, padding: 24, fontFamily: "Arial" }}>
    {["light", "dark"].map((theme) => <section className={theme === "dark" ? "dark" : ""} key={theme} style={{ background: "var(--surface-page)", color: "var(--text-heading)", padding: 20 }}>
      <h1 style={{ fontSize: 14 }}>{theme}: Gallery component preview only</h1>
      <div style={{ height: 315, width: 260 }}><ChartTypeGallery groups={chartTypeGalleryGroups} selectedType={selectedType} onSelect={setSelectedType} /></div>
      <p style={{ fontSize: 12 }}>Selected model: <output>{selectedType}</output></p>
    </section>)}
  </main>;
}
createRoot(document.getElementById("root")!).render(<Preview />);



