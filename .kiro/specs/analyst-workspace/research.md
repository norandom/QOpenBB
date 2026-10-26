# Analyst Workspace research

## Stacked Line source assessment, 2026-10-26

Extend the existing Cartesian session rather than introduce a separate renderer or reuse bar stacking unchanged. This is a proposal informed by source inspection, not an accepted implementation contract. The [milestone](stacked-line-milestone.md) owns the bounded sequence; SL0 was open at this source checkpoint. The subsequent six-case characterization and independent review accepted that bounded assessment; see the milestone and artifacts/reviewed/chart-stacked-line/native-review.md.

The original gallery includes `stackedLine` and `normalizedLine`; Workspace source `0b2190354d2dc5f4175ffb989cf652ac36237c77` excludes them from replacement Cartesian admission. Broad analyst requirements remain unapproved; this assessment follows the owner-authorized chart-parity slice and prototype-first workflow.

| Requirement | Existing asset | Gap |
| --- | --- | --- |
| Preserve both visible Line variants | Gallery catalog and thumbnails | Missing family admission; union-only changes would fall through to bar rendering |
| Preserve financial meaning | Raw snapshots, unit admission and display callbacks | Original cumulative/normalized geometry needs a distinct numerical contract |
| Preserve editor and theme | Existing Line controls and appearance layers | Ordinary-Line-only predicates and saved namespaces need coordinated extension |
| Preserve state and lifecycle | Native session, stamped edits, Set Up and persistence | Variant transitions, legend reprojection and reload need evidence |
| Preserve appearance | Existing host, axes, legends and navigator | Original/reference screenshots and packaged candidate comparison pending |

### Options

1. Extend Cartesian modules directly. This has the fewest new owners, but scattered `family === "line"` decisions and cumulative geometry can enlarge existing functions.
2. Add a separate stacked-Line renderer. This isolates geometry but duplicates style/session integration and makes consistency harder; it is not preferred.
3. Extend shared Line-family admission and extract only cohesive cumulative projection logic where needed. This retains current owners while keeping financial transformations testable. It is the preferred design hypothesis, subject to original characterization and complexity measurements.

The original-source investigation identifies algebraic stacking in selected series order, with normalized scaling based on cumulative extrema. Existing bar normalization instead uses positive/negative masses and same-sign stacks. Area projection is a closer reuse candidate, but its missing-value and interpolation behavior must not be assumed identical to Line.

Estimated effort: medium, because the change crosses existing renderer, appearance, editor and session owners. Risk: medium, concentrated in signed/missing normalization, legend membership and saved namespaces. This is a relative planning estimate, not a delivery promise.

### Next evidence

Use the original ordinary Table/File journey for both variants, one retained additive FMP quarterly dataset and a small signed/zero/missing discriminator. Record selected series order, labels/tooltips, legend reflow, Connect Missing Data, native model fields and save/reopen. A different observed denominator or missing-value topology disproves any proposed shared projection that does not reproduce it.

Freeze interfaces and exclusive worker paths after that evidence. All touched production files retain the existing 400 physical/300 logical units per file and 50 logical units per function limits. No implementation, browser parity or new build is accepted by this research note.
