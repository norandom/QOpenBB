# Candidate 3 bounded browser evidence review

Verdict: the five recorded checks and the bounded stage-label screenshot inspection pass. This is partial F4 evidence, not F4 completion or owner appearance approval. The owner's qView appearance decision remains pending.

## Identity and evidence

All three qualified runs identify Workspace source `6c7632329bbddc89f8986b0183d7b3a8750dd5eb`, image `sha256:4ae3695d4c691f3da326ad2310b2e60ed7ee6fc254d4de9b46fe8c8798437814`, and loopback origin `http://127.0.0.1:55606`, with a running container and only a disposable data mount. Each run used one worker and zero retries. Each retained post-run source-integrity report contains only OK entries. The frozen candidate spec independently hashes to `e147eb68a038722b7a4752b7d1c2d90ad8277f800aedf61b49fa662c0f6bd7af` in all three run copies. The retained financial CSV hash is `c6b74bd3da1bca8d74438cf441e5b784c40ca27cc4e70d11da42cb34d7b206e8`.

Raw evidence is retained locally in these ignored directories, including results, command, runtime qualification, frozen hashes, source-integrity reports and observation JSON:

- `artifacts/chart-funnel/f4/browser/candidate3-defaults-1`: 3 passed, exit 0, 135.0 seconds.
- `artifacts/chart-funnel/f4/browser/candidate3-controls-1`: 1 passed, exit 0, 47.0 seconds.
- `artifacts/chart-funnel/f4/browser/candidate3-recovery-1`: 1 passed, exit 0, 25.9 seconds.

Results contain no unexpected, skipped or flaky tests. All five observation records retain empty errors, failures, consoleErrors and requestFailures arrays; the tests invoke application diagnostic assertions, including the separately authenticated reopen. These are evidence review findings; no tests or builds were rerun for this review.

## Verified scope

The three defaults checks exercise Funnel, Cone Funnel and Pyramid with the retained AAPL financial levels, light/dark default captures, stage/value tooltip checks, ordinary saved settings and export smoke checks. The controls check exercises ordinary control exposure and final Pyramid numeric-label mode persistence across reload and authenticated reopen. Its existing limited geometry assertions remain limited.

The recovery check starts from visible valid Pyramid geometry (144244 nonuniform pixels on the 619 by 593 canvas), records the real First / Valid USD: 100 tooltip at normalized point (0.5, 0.2), directly reorders the invalid series first, and verifies zero nonuniform pixels and no tooltip after dwelling at that prior hit. Correcting the selection restores labels. Removing the final series again leaves zero nonuniform pixels and no tooltip, and restoring the valid series recovers labels and the saved selection. This supports stale-paint and stale-tooltip clearing for this fixture.

I visually inspected all six matched light/dark original/replacement pairs in `artifacts/chart-funnel/f4/comparison-3`, against the retained native visual-2 captures. All three families' stage labels now share the native right-aligned left-strip placement. All five Cone labels, including Revenue at the first endpoint and Net income at the last endpoint, are fully visible in both themes. The earlier centered-strip alignment and clipped endpoint glyph defects are absent in these captures. Numeric labels are absent in the matched default views. Small raster and segment-boundary differences remain visible; this review does not assert pixel identity or broader appearance acceptance.

## Remaining boundaries

Owner appearance approval is outstanding. These five tests do not close the complete F4 control/geometry matrix, custom theme and common appearance behavior, refresh and gallery/table/Cartesian transitions, missing/zero coverage across all families, or export content fidelity. The export smoke helper verifies PNG structure/dimensions rather than matching exported chart content. Horizontal long-label fit and all alternate placements are not proven by these vertical default screenshots. Source unit checks remain separate evidence.

The earlier first-login onboarding 404 at `/api/pro/pro-developer-onboarding-info` remains separately recorded; successful chart checks do not erase that failure. Earlier display-label fixture corrections and blank-capable recovery instrumentation are test corrections, not additional production fixes. F4 and subsequent publication acceptance remain open.
