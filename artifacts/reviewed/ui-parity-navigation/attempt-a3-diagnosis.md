# Create the finite selection with a real drag after recording click behavior

Attempt `run-20261017-r1-a3` resized Revenue from 281 to 347 pixels through the original visible handle, then recorded zero cell ranges after Q2 Revenue click and Q3 Operating Income Shift-click. It stopped at the N01 selection discriminator. Browser/container/state/credential cleanup succeeded; all failed-attempt bytes remain unchanged.

Original `terminalpro/src/components/General/Table/AgGrid.tsx:764-765` at `38dffc33389aca0e4a87e0e88d42f7067aa220df` calls `clearCellSelection(params)` on each cell click. Original `Table/utils.tsx:350-353` unconditionally invokes the grid clear method. This explains the actual captured empty range; it is an original click effect, not evidence that range selection is unavailable.

The bounded a4 correction preserves and captures those same clicks, then drags from the center of Q2 Revenue into Q3 Operating Income using Playwright's page mouse. It reads the resulting actual range and never invokes a selection API. It also projects focused-cell column identity through the named read-only column getter instead of attempting to serialize the Column object, and records bounded original chart event identities. The 12 navigation cases, data and transition assertions are unchanged.
