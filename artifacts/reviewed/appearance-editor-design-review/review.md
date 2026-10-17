# Source contracts are ready for human review

VERDICT: GO for human review of the scoped appearance/editor design amendment. After human design approval, generate bounded tasks for saved-option composition, explicit derived-color tokens, grouped-column tooltip events and their independent source-level join. This is not approval to implement, activate the application, or declare full B2, C, renderer, persistence or release readiness.

Reviewed 2026-10-17 against candidate Workspace `76edf85a46298f7bc5212ff9944e4b66e9baa4af`. The reviewed draft is `.kiro/specs/openbb-self-service/chart-appearance-editor-integration-design.md`, SHA-256 `05d12b46374cfaf1bf9986da24efc8e8fed7ded9b0b13eee333518285926d76b`. The verdict applies to those bytes. The original source is `38dffc33389aca0e4a87e0e88d42f7067aa220df`.

The reviewer used the kiro-spec-design design-review gate, with read-only source review. Production tests, RED evidence, browser journeys, installs and builds are not applicable to this documentation decision and were not run. No production source, approval state, breadth map or inventory was edited by this reviewer. Only `artifacts/appearance-editor-design-review/**` was written. Concurrent catalog, Perspective and controller documentation work was preserved.

## Findings and repaired contracts

No blocker remains for the stated source-contract task boundary. One local repair pass resolved the following issues before final review:

1. The original draft required an unresolved stacked-column tooltip outcome without specifying how to cross the existing `ValidationResult<RuntimeOptions>` interface. Actual `editorEvents.ts` accepts grouped and stacked columns; actual `sessionState.ts` maps all mapper errors to invalid. The repaired design preserves that interface, rejects stacked tooltip at the mapper, and adds a descriptor-safe exact valid-event precheck after stamp validation in `applyColumnEdit`. Only the valid stacked tooltip combination returns unresolved. Malformed events remain invalid; the four existing event kinds remain accepted for both families. Neither failure path reaches storage reduction.
2. Derived-color validation needed a precise boundary rather than a claim to recognize arbitrary valid CSS. The repair freezes structural invalid outcomes, unsupported string/base unresolved outcomes, six-digit case-insensitive hex admission, lowercase output, diagnostic paths and hostile-input containment. Aliases are already resolved by a later caller; the helper does not infer them or claim that caller is implemented.
3. The composition handoff now names `baseline.options` as the saved operand and `generated` as the other operand. It expressly keeps the reducer's `resolvedOptions` argument on the latest selected `baseline.options`; composed rendering options never become the stored source model. This matches the existing reducer ownership and avoids dropping saved common fields during an unrelated event.
4. The main `design.md` is now explicitly linked as the owner of all 69 active requirement criteria. The application design and this amendment are scoped supplements. Read-only baseline, reducer, validation, financial formatting and host dependencies now have concrete file ownership alongside proposed files.

## Source and evidence assessment

The pinned original `useChartOptions.tsx:406-434` replaces `chartOptions.common` with `options.common`, then invokes `merge(options, chartOptions)`. Its source hash matches the reviewed saved-composition manifest. Detached output and nonmutation are suitable pure-boundary requirements; the saved/default precedence is unchanged. The narrow helper does not reproduce the unrelated scatter-axis preprocessing or claim general AG inheritance.

The actual `OptionBaseline` holds both `model` and separately selected `options`; initialize and synchronize differ. The proposed explicit operand rule therefore matters. Current `reduceIntegratedState` clones and merges its supplied resolved options with the event, strips only root theme and preserves the existing partition/model ordering. The design preserves this state path and existing latest-storage semantics. Unit tasks must verify this composition with deliberately different `baseline.options` and `baseline.model.chartOptions`, not merely matching fixtures.

The three reviewed finding documents and their independent reviews support only the finite contracts stated: 44 appearance assertions plus 262,144 normalized color comparisons; four saved-input cases with 99 assertions; seven original editor edits with 30 assertions and six Sum raster bars. These are accepted historical reference results, not reruns by this review. The corrected normalized operation order and explicit text/chart-background separation appear in the draft. The tooltip family patch is `bar.tooltip.mode`, with Multiple mapped to `shared`; no series-level replacement is introduced.

The architecture has no additional state owner or runtime dependency. New composition/colors files and tooltip/session files form disjoint implementation lanes after controller-owned types and test scope freeze. Every component has a current or proposed path; later effective appearance, mapper and editor paths remain blocked until their named contracts are frozen. Shared types, inventory, breadth and test configuration remain controller-owned. The 400 physical / 300 logical / 50 per-function caps, existing executable checker, explicit fork scope and final shared-module audit are retained. Existing production file physical counts inspected here range from 25 to 278; this is not a fresh logical/function gate.

## Mechanical verification

Run from `D:/Source/QOpenBB`:

| Command or check | Result |
| --- | --- |
| `py artifacts/appearance-editor-design-review/audit.py` | Final exit 0; 16 checks pass. Draft/source hashes, requirements, populated sections, concrete paths, relative links, placeholders and inspected physical counts are recorded in checks.json. |
| `git -C vendor/workspace rev-parse HEAD` | Exit 0; candidate matches the pinned revision. |
| `git -C vendor/workspace show <original>:<path>` for each of four paths in the reviewed saved-composition source manifest | All four SHA-256 values match; audit.py records the exact paths and revision. |
| `git diff --name-only` and `git -C vendor/workspace diff --name-only` | Read-only boundary inspection. Existing root changes were preserved; no tracked Workspace source diff was introduced by this review. |
| Design file-plan/component audit | PASS by source inspection: composition, colors, baseline, reducer, event mapping, session, financial formatting, host and later mapper owners have concrete paths; no orphan replacement component. |

The traceability extractor finds 69 active criteria and 12 direct criterion references in this amendment. The remaining 57 IDs are enumerated in [checks.json](checks.json), and all 69 occur in the main design. Direct omissions are intentional scoped ownership, not deleted requirements or proof of implementation. All relative draft links exist; no placeholder markers remain.

The initial audit run exited 1 because the reviewer script stopped a level-two section at its first level-three subsection and therefore misclassified the populated Boundary Commitments section as empty. The script was corrected to retain nested subsections. The draft hash did not change between that failed audit and the final passing run. This is a reviewer mechanical-parser correction, not a hidden design or runtime retry.

## Gates that remain open

The complete B2 field manifest, palette allocation/reordering, custom line/stacked behavior and unresolved axis/legend leaves still block their consuming projections. Tooltip rendering needs the remaining missing-value, ordering, hit-testing and keyboard evidence. Numeric transpose/aggregation requires a separate transformed-snapshot contract. Original controls, full family/conditional coverage, actual light/dark candidate interaction, export freshness, table return and backend save/reopen/restart remain application acceptance obligations. The amendment neither hides controls nor turns unresolved engineering results into shipped product restrictions.

Tasks must freeze exact commands, fixture hashes and ownership before implementation. The current decision establishes source contracts, not working UI. No task can cite this review as permission to remove application guards or declare full requirements 4.8/4.9 met. Anthropic-before-Excel remains unchanged.

## Publication boundary

The exact safe publication set is [publication-allowlist.json](publication-allowlist.json): the reviewed design plus this report, the audit script and its result. All contain source paths, synthetic contract descriptions and hashes only. No credentials, account state, browser traces, dependency caches, raw runtime captures or unrelated changes belong in the set. The manifest itself should accompany its listed entries. Verify hashes before copying or staging; preserve original paths and hashes in any mirror manifest. Controller synthesis documents and approval records require their own review and are not implicitly covered by this allowlist.
