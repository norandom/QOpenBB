# Preserve the selected date axis

Owner amendment, 2026-10-19: the owner approved the proposed next step to retain the Time-axis selection after save/reopen. This is a deliberate improvement over the upstream runtime-only behavior documented in chart-live-editor-integration-design.md and chart-live-editor-contracts.md. It does not change the visible controls, themes, flags, axis positions or rotation contract.

## 1. Acceptance

For an ordinary chart with date observations, selecting Time and a date format, saving and reopening in a fresh session must restore both the selected type and format and the rendered date spacing. Changing back to Category or Number must replace the saved preference. Older dashboards without this preference retain their current defaults. Stale or invalid edits must not write storage. Unrelated model fields, theme options and data remain intact. Requirement 4.9 and UI-09 own this continuation.

## 2. Storage and restoration

Use an optional namespaced JSON field in the existing selected chartModel: qopenbbAxisSettings = {version: 1, categoryType: 'category' | 'number' | 'time', timeFormat?: string}. No additional store, API, database table or persistence envelope is introduced. Time stores its current format, including the normal default when entering Time. Leaving Time omits timeFormat.

A missing extension uses the caller's existing initial axes. A malformed present extension, unsupported version or invalid type/format produces the existing invalid saved-chart diagnostic; it must not be partially applied or silently discarded. Restore only the semantic category axis type and label.format, preserving family-derived direction/position, the numeric axis and other runtime options.

Successful type or time-format edits write the extension through currentModel and the existing integrated reducer in the same transaction as transferred theme options. Position and rotation edits do not serialize runtime axes. Initial session creation and caller construction use one pure codec. External changes to the selected extension synchronize the existing session consistently. Unknown unrelated model fields survive.

Changing chart family intentionally drops this extension, preserving the established family-transition reset behavior. Re-selecting the same family retains it. No inactive-family preference registry is introduced.

## 3. Bounded implementation and verification

Task 2.96 owns one pure axis-preference codec; the existing session edit/initialization/synchronization paths; caller initialization and actual family transition; directly affected comments; focused caller/session/codec tests; one existing-harness browser regression. Keep each production file within 400 physical lines, 300 logical units and 50 per function; register the new codec in the existing complexity inventory without staging unrelated changes.

Use the existing chart-application Vitest and strict TypeScript configurations, with one worker. Verify JSON round-trip, legacy initialization, malformed extension, orientation, same/different family transitions, stale edits and preservation of unrelated fields. An independent reviewer checks the diff before the source commit. Build the identified Workspace image through pinned Dagger, then verify the actual save/fresh-session reopen journey with animation enabled. Replace the local preview only after verification, preserving its account/data. Public evidence is one sanitized report; real provider data and credentials remain local.
