# RC2 independent implementation review

- VERDICT: APPROVED
- TASK: inactive Radial controls/selection lane, 2026-10-24. This is source acceptance only; full RC0, activation and visible parity remain pending.
- Scope: six exclusive production files and radialSession.test.ts. All seven actual SHA256 values freshly match source-evidence.json. Corrected radialAppearance.ts is `e8c3136ffdb1ffbce31d82bfebd14f08c5723c309381a1274d74bab78cce0b4a`; test is `a1c3dab43cf52b11c4502a048bad8f5548aec3398196fd387a39203e14a5d023`.

## Mechanical results

- Fresh independent focused Vitest: exit 0, 11/11 tests. Command from terminalpro: pinned Node 24.22.0, node node_modules/vitest/vitest.mjs run tests/unit/chart-compatibility/radialSession.test.ts --config tests/unit/chart-compatibility/vitest.config.mjs --maxWorkers=1. Serialized after the geometry reviewer released the test slot.
- Retained Biome: exit 0 for six production files. Strict TypeScript exits 2 with the same four inherited typography/Zod errors; independently compared log bytes equal the imported-source baseline. No clean application compilation is claimed.
- Syntax evidence: exit 0; maximum 222 physical lines, 66 logical units/file and 23/function, within 400/300/50. Parent inventory-backed combined gate remains required for completion.
- Placeholder/credential scan: CLEAN. Boundary audit: WITHIN; no shared routing, renderer, declaration, fixture, persistence or inventory changes by the worker.
- RED phase: VERIFIED in stroke-red.log, two intended regression failures before the correction, followed by eleven passing tests.

## Findings and correction

Independent review found a concrete default error: an explicit user stroke without strokeWidth inherited zero instead of the original source fallback one. The worker repaired this before final freeze. User-stroke detection examines composed/theme common and family layers before injecting defaults. Palette strokes alone remain width zero; explicit zero/nonzero widths keep precedence. Regression cases cover both families, saved/generated/theme branches, inactive neighboring options and nonmutation. Shared generated-common replacement behavior is preserved rather than overridden locally.

No remaining blocking findings. Assignment admission rejects unknown families, malformed/duplicate IDs including unselected entries, nonboolean selection and throwing reads; valid selected order and empty selection survive. Preparation consumes the existing snapshot once and separates absent root grouping from explicit grouped. Raw/count display functions remain distinct from normalized numerical-axis formatting.

Appearance retains original family axis roles, independent axis values and the separate first-axis UI projection. Bar projected padding zero does not erase effective category padding 0.2. Palette fills/strokes remain supplied values. Transactions derive target authority from family, validate edits and return detached patches or a separate root mutation. Padding/orientation target restrictions match the independently inspected original saved paths, and predefined font edits use each target axis's own font context. Inactive/neighboring stored keys remain in the unchanged baseline. Ratio limits and unsupported-neighbor rejection are covered; the DOM regression checks reachable controls, 0.05 steps and emitted orientation intent.

## Limits and completion

This lane does not establish stale-command rejection by the shared session, actual rendering, save/reopen, export or packaged financial behavior; those belong to the join and browser gates. Column numerical/missing-value decisions remain unapproved. No browser, build or broad suite ran in this review.

REMEDIATION: None in the frozen RC2 source. Complete the controller combined inventory gate before marking RC2 done or committing its accepted boundary.
