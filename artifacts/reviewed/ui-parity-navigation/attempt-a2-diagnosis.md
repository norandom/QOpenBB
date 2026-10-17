# Hover the original header before locating its resize handle

Attempt `run-20261017-r1-a2` acquired the original GridApi and synthetic WidgetProvider getter, saved `N01-table-initial` and stopped at the resize prerequisite. The existing handle returned no bounding box before any pointer entered the header. It did not complete N01 or any later case. Browser, container, state and credential cleanup succeeded.

Original `terminalpro/src/index.css:757-762` at `38dffc33389aca0e4a87e0e88d42f7067aa220df` defines `.ag-header-cell-resize { display: none; }`, then `.ag-header:hover .ag-header-cell-resize { display: flex; }`. Original `AgGrid.tsx:749` enables resizing. The corrected a3 harness records a real hover on the exact Revenue header before reading and dragging its existing handle. It does not force CSS, change grid options or use an API resize. The four-row fixture and all 12 cases remain unchanged. Preserve a2 scripts, failure, initial synthetic screenshot/state and cleanup evidence.
