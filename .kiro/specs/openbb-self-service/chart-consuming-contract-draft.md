# Connect appearance, editor and session through explicit contracts

The next integration has concrete draft interfaces and evidence ledgers. It is not ready for implementation: the session write scheduler, original appearance/control behavior and settled export acknowledgement still need their named contracts. Preserve the full original Workspace journey; do not activate a partial editor or remove chart guards from this draft.

The controller's [contract draft](../../../artifacts/reviewed/consuming-contract-freeze/controller/draft.md) joins the appearance and session proposals against Workspace `ea02ec15956dee8d2c8a06825387a570757db12d`. The original reference remains `38dffc33389aca0e4a87e0e88d42f7067aa220df`. This follows the approved [readiness work](chart-consuming-integration-readiness.md), without changing prior task acceptance or granting a new implementation phase.

## Review the handoffs

| Handoff | Concrete result | Remaining prerequisite |
| --- | --- | --- |
| Appearance to existing mapper | [Appearance proposal](../../../artifacts/reviewed/consuming-contract-freeze/appearance/draft.md), [types](../../../artifacts/reviewed/consuming-contract-freeze/appearance/proposed-types.ts) and [field manifest](../../../artifacts/reviewed/consuming-contract-freeze/appearance/field-manifest.json) define selected theme/generated/baseline inputs, canonical role styles and trusted formatting. | Resolve named original behavior and geometry; available ECharts members alone do not prove visual parity. |
| Session to original storage and host | [Session proposal](../../../artifacts/reviewed/consuming-contract-freeze/session/draft.md) defines unstamped selection, explicit render inputs, five admitted commands, revision ownership and applied-revision receipts. | Freeze the existing widget owner's replay-safe completion port and continuous-edit scheduler; distinguish applied options from settled pixels. |
| Original editor to session | [Field ledger](../../../artifacts/reviewed/consuming-contract-freeze/session/editor-field-ledger.json) records observed controls, predicates, payloads and missing capture queries. | Complete typed controls, family/Set Up/transform contracts and focus/tab/scroll transitions. Five commands cannot substitute for the complete panel. |

The appearance manifest contains 127 observed pointer groups covering 908 historical leaves, plus four supplemental gates. The editor ledger contains 202 runtime capture rows, 88 inventory rows and five supported-command rows. These counts describe evidence coverage, not independently verified product features.

## Preserve current owners

Use the existing composition/color helpers, Cartesian mapper, original reducers, widget storage owner and ECharts host. Canonical styles replace overlapping aliases; financial formatting comes from `ChartDisplayPolicy`. Keep original baseline options for persistence. Root category-fill state and ordered source bindings are explicit render inputs, not hidden store reads.

Review found that `Widget.hooks.tsx` changes a captured functional request into an object inside React's updater, then schedules persistence/context effects there. A replay can reuse the first result. A pure chart callback does not repair the surrounding owner. Adapt that owner before session writes, with replay/rebase, unchanged/rejected completion and continuous-edit checks. This is an existing source finding; no new failing runtime test or production fix is claimed here.

## Next acceptance boundary

Complete the named original captures and the transaction/export contracts, then review the full consuming design before generating bounded implementation tasks. All modified production files must satisfy 400 physical lines, 300 logical units and 50/function, including the whole existing widget owner. Reference captures and design artifacts do not satisfy the real candidate journey: table -> chart -> full editor -> edit/theme -> fresh export -> table -> save/reopen/restart.

No production code, renderer activation, task completion or deployment acceptance is claimed by this document.
