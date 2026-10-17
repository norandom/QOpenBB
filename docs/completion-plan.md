# Complete the original Workspace experience

The next milestone is a working chart journey inside the existing Workspace table widget. The accepted renderer modules do not yet reach that application entry point. Completion requires the original controls, themes and outcomes, followed by a verified image-pull installation. Three working chart families are an intermediate integration milestone, not a reduced release scope.

This plan records source findings on 2026-10-17 at Workspace `b96d36d16ba87db2dd595d5796507d473dd0c0c6`, compared with original `38dffc33389aca0e4a87e0e88d42f7067aa220df`. It does not claim a new runtime test or approve new implementation tasks. [Phase status](../.kiro/specs/openbb-self-service/spec.json) owns approvals; [appearance verification](../.kiro/specs/openbb-self-service/chart-appearance-verification.md) owns the latest accepted renderer evidence.

## What must connect next

| Work | Concrete missing connection | Completion evidence |
| --- | --- | --- |
| Real table-to-chart journey | `ChartViewButton` returns null, `createChartData` is undefined, saved chart state is rejected and chart-option hooks are stubs | Original table selection, filter/sort, chart entry, edits, theme changes, export and return to table work through actual Workspace contexts |
| Effective appearance | The mapper accepts explicit styles; it does not resolve active original light/dark/custom themes | Matched original/candidate captures establish palette, typography, legend, axes, spacing and actual control effects |
| Persistence | The query/storage repair is independently accepted through task 4.9; the browser journey remains open | 60 file-backed SQLite tests pass; real application save and environment restart/reopen must still prove the full journey |
| Remaining renderer parity | Accepted Cartesian helpers cover only part of the original capability inventory | Every applicable row in the [capability matrix](renderer-capability-matrix.md) has working replacement behavior and evidence |
| Runtime and delivery | Controlling Compose and publication commands are not implemented; the Workspace image remains provisional | Matching source/catalog/image identities, real dashboard acceptance and pull-only WSL/Linux operation |

The existing Plotly widget keeps its rendering path. Detached charts, AI chart artifacts, advanced table actions and other chart families remain required; acceptance of an integrated table chart does not count as their verification.

The original per-chart Customize panel is supplied by AG Grid Enterprise. Reconnecting a React component cannot restore it: the compatibility work must reproduce its original control placement and behavior. The separate entity theme settings UI is owned application code and can retain its controls while its preview renderer is replaced.

## Parallel work and joins

1. Review the [application integration design](../.kiro/specs/openbb-self-service/chart-application-integration-design.md). Independent review permits task planning for source-proven session/range state and financial formatting helpers; unresolved original-editor behavior gates only its consuming tasks. SQLite repair is already accepted.
2. After design and task approval, freeze shared types and give separate Sol workers session/range state (A1) and formatting helpers (B1). Continue finite original-runtime captures independently. Displayed-grid capture (A2), appearance (B2), editor (C) and application activation (D) join only after their named contracts are established. Keep application entry, controls and guard removal in one integration lane.
3. Join the [accepted SQLite repair](../.kiro/specs/openbb-self-service/sqlite-repair-verification.md) with the application lane at save/reopen. Keep environment restart evidence separate from engine recreation.
4. Restore and verify the remaining original capabilities against the matrix. No hidden feature flag, reduced menu or inactive button substitutes for an unfinished behavior. Compare actual application screenshots in light and dark modes as well as user outcomes and financial values.
5. Close final catalog/image identity and dashboard acceptance. Then delivery/publication work can run alongside Anthropic. Excel begins only after Anthropic acceptance.

The controller owns shared contracts, source pins, breadth mapping and selective commits. Astra independently reviews integration and financial correctness. Use at most four agents and one heavy build/suite at a time. Every maintained production file must meet 400 physical lines, 300 logical units and 50 units per function, or have a specific reviewed exception. These rules also apply to upstream files changed for compatibility.

## Deployment acceptance

The final installation uses one Compose file and pulled immutable images. Workspace publishes plain HTTP on `0.0.0.0:23003`; state stays in bind-mounted paths under `./data`. The owner supplies Cloudflare Access and cloudflared for `qbb.hanse-hedge.fund`. WSL and private Linux use the same topology. Dagger builds images; portable repository commands verify and publish them.

Before calling this deployable, verify original dashboard interactions, FMP/FRED results and failures, persistence across restart, Anthropic, the Excel journey and clean backup restoration against recorded image identities. Provider fixtures, a health endpoint or a successful image build cannot close these gates. Jupyter and PostgreSQL remain outside this baseline.

## Source findings

- [Grid capture and SQLite findings](../.kiro/specs/openbb-self-service/chart-next-discovery.md)
- [Owner-approved SQLite repair design](../.kiro/specs/openbb-self-service/sqlite-repair-design.md)
- [Effective style discovery](../.kiro/specs/openbb-self-service/chart-effective-style-discovery.md)
- [Original editor contract](../.kiro/specs/openbb-self-service/echarts-editor-contract.md)
- [Implementation dependencies](../.kiro/specs/openbb-self-service/tasks.md)
- [Parity requirements](../.kiro/steering/workspace-experience.md)

Read-only application and delivery audits are retained locally in `artifacts/completion-path/`. They establish source gaps, not passing application evidence.
