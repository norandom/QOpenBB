# Preserve the original editor's measured navigation behavior

The original-reference run completed 12 navigation cases with 36 checkpoints. It establishes concrete behavior for close/reopen, direct dark/light switching, the column/line selection journey and table return. These are inputs to the replacement UI contract, not candidate parity or deployment acceptance.

The [capture report](../../../artifacts/reviewed/ui-parity-navigation/report.md) binds the observations to original Workspace `38dffc33389aca0e4a87e0e88d42f7067aa220df` and image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`. Candidate `ea02ec15956dee8d2c8a06825387a570757db12d` was not executed. The four synthetic quarterly rows retain their revenue and operating-income values in USD millions throughout.

| Journey | Observed original behavior | Replacement obligation for this path |
| --- | --- | --- |
| Dock close -> external Chart settings reopen | Retains tab, Vertical Axis expansion and scrollTop 547; focus moves to the active tab header. The same chart/dock nodes remain. | Keep the transient editor state through hiding and reopening; use the observed focus destination. |
| Focused field -> Ctrl+M dark/light | Retains chart/dock owners; Customize remains visually selected, inner groups rebuild collapsed and field focus is lost. Stored model theme stays dark while the live chart becomes light. | Separate live theme/render inputs from persisted model and inner-group lifetime from dock lifetime. |
| Customize -> Chart -> line/column thumbnail -> Customize | Returns collapsed groups while outer chart/dock owners remain. Family and stored model update; the resolved range stays unchanged in this fixture. | Reproduce the complete measured journey. This run does not isolate family-change effects from the Chart-tab detour. |
| Chart -> table | Restores widths 282/347/281 px and horizontal scroll 65; clears range selection. DOM focus returns to the toggle, although the grid's internal focused-cell record still identifies Q2 Revenue. | Keep column sizing, scroll, actual focus and grid focus as distinct state. Clipped Period text is not lost source data. |
| Table -> chart again | Creates new chart/editor identities and automatically opens stored settings on Chart, scrollTop 0. | Restore settings openness without carrying a destroyed editor's transient tab/group state into reentry. |

The real pointer drag created a partial two-row selection, but chart entry resolved all four rows and the three ordered columns in this fixture. Do not conflate source rows, selected cell range and the original chart's resolved range. Original cell clicks clear selection; the failed click/Shift-click prerequisite and its source explanation remain published.

The dock measured 260 px wide at the captured 1440 x 1000 viewport. Responsive behavior at other sizes remains unverified. The original tab elements lack `aria-selected`; selected-tab findings use actual visible content, focus and inspected screenshots, without inventing a missing machine-readable flag.

Fresh offline verification passed 571 checks. All four attempts removed their owned browser, container, state and credentials. Three diagnosed setup attempts, original console/API faults and projection omissions remain recorded. Save/reopen/restart, export, editing transactions, additional families and candidate light/dark comparisons remain open.

This narrows the navigation questions in the [consuming contract draft](chart-consuming-contract-draft.md). It does not authorize a reduced panel, new feature predicates or renderer activation. The owner requested autonomous UI/UX parity work with per-task commits; each following implementation still needs its concrete design, task and independent verification gates.
