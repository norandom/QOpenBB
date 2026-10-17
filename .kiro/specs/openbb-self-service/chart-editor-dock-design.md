# Connect the gallery to the original editor dock

Build the production dock around the accepted gallery: the original 260 px right-hand panel, Chart / Set Up / Customize tabs, collapse action, and retained navigation state. The owner authorized this next UI step with "yes, go". This closes the dock component boundary; complete panel controls and application chart activation remain separate work in the UI parity worklist.

## Component contract

Own `terminalpro/src/components/General/Table/Chart/editor/ChartEditorDock.tsx` and cohesive dock styling/navigation helpers if needed. Reuse the accepted `ChartTypeGallery` and existing design-system tabs where suitable. Do not change global styling, dependencies, widget state, storage schemas, flags or table/chart guards.

The caller controls `open`, `activeTab` (`chart`, `setup`, `customize`), `onOpenChange`, `onTabChange`, gallery props, and a `themeResetKey` identifying a live theme rebuild. Require caller-provided Set Up and Customize React elements; provide no empty or fake production defaults. The dock owns navigation and presentation only. Supplied panel components retain ownership of their fields and chart commands. The gallery continues to emit exact supplied model types without filtering.

Keep the mounted dock and active content when closing it. Hide the entire dock from layout, keyboard navigation and accessibility traversal while closed. Preserve its active tab, expanded child state and scroll across close/reopen. When reopened, focus the selected tab header. If closing while focus is inside, return focus to a caller-supplied opener ref when available; do not steal unrelated external focus.

Switching away from Customize destroys that tab's inner component state, matching the observed return with collapsed groups. A changed live theme key rebuilds Customize contents while preserving the selected outer tab. Do not infer additional family-change resets from the original capture: it mixed family changes with a tab detour. Remounting the whole editor starts on the caller's initial Chart state; persisted openness remains a caller responsibility.

Use accessible tabs with selected state, associated panels, roving keyboard focus and visible focus styling. Keep the original short labels and collapse chevron. Match the existing dark/light tokens and accepted gallery spacing; make no new toolbar or product navigation surface.

## Verification and limits

Reuse the existing original navigation screenshots and findings. Focused component tests cover all three tab destinations with supplied interactive test panels, exact gallery callbacks, hide/reopen state and scroll retention, focus, tab switching and live-theme resets. Test panels are explicitly fixtures, not implementations of the remaining product controls. A scoped preview shows the dock and accepted gallery; any displayed fixture panel is labeled outside the component. No inert buttons or pretend complete editor are permitted.

Run scoped types/lint and the existing complexity checker: 400 physical lines/file, 300 logical units/file, 50/function. Tests and stories remain documented development-only exclusions. Use existing pinned dependencies and isolated headless verification; no installation or original-reference capture workstream. Independent review checks the actual component and limited integration claim. Ask the owner if the shown dock differs materially from the original.

Task 2.48 depends on accepted task 2.47 and implements requirements 4.8, 4.9, 10.1, 10.4, 10.5 and 10.6 within this boundary. A working dock component does not complete UI-04/05 controls, UI-06 session composition or UI-07 table/chart entry.
