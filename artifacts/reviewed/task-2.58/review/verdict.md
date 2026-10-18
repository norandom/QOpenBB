# Shadow subsection independent review

- VERDICT: APPROVED
- TASK: 2.58; reviewed 2026-10-18 against `chart-series-shadow-design.md`, requirements 4.8, 4.9, 10.1 and 10.4–10.6. Workspace base: `f52a895dae3b749ec02b3fd08c92321be2660048` plus the identified new files.
- Tests: fresh pinned Node v24.22.0, Debian WSL as mc, terminalpro working directory: `node node_modules/vitest/vitest.mjs run --config tests/unit/chart-editor/vitest.config.mjs tests/unit/chartShadowPanel.test.tsx` — exit 0, five tests passed, no skips. Controller's shared 41-test join is separate evidence.
- Static checks: fresh `node node_modules/@biomejs/biome/bin/biome lint` on panel, story, test and shared configuration — exit 0. Inspected scoped compiler evidence retains only established upstream `ds/plugins/typography.ts(1,1)` TS2578; clean typecheck is not claimed. Placeholder and credential spot checks are clean.
- Boundary audit: clean. Shadow emits discriminated controlled edits, orders Color/Blur/X Offset/Y Offset after the toggle, retains caller values when hidden, reuses accepted color/numeric controls, permits fractional negative offsets with minimum -10, supplies default/expanded maxima and correct steps. No flags, family eligibility, renderer or storage ownership were added. Source is 49 physical lines, 27 logical units, maximum function 1; within 400/300/50. Story/tests are non-production exclusions.
- RED phase: verified local missing-component import failure. Inspected isolated headless browser script/results and light/dark screenshot: alpha, invalid recovery, pointer/keyboard toggle retention, picker focus, negative numeric edit and slider keyboard effect; no recorded console/page errors or failed requests. Browser lane was reused as evidence, not rerun independently.
- Shared configuration and retention documentation: APPROVED. Includes editor panels, dock and gallery without application Vite configuration; one worker and disabled file parallelism bound execution. Documentation correctly limits this to component verification.
- Findings: none requiring remediation. Full application, family eligibility, rendering, storage and integrated dock acceptance remain outside this controlled subsection review.

SHA256 identities (actual reviewed bytes):

| File | SHA256 |
| --- | --- |
| `Chart/editor/shadow/ChartShadowPanel.tsx` | `60cd4470179de12e590645a21264433a2b22965b71b7a87cc5016636301ebd0a` |
| `ds/organisms/ChartShadowPanel.stories.tsx` | `9648327f5f21a0cc174c08cb01e5d08f29caef174455b76dead964c24f0df4d7` |
| `tests/unit/chartShadowPanel.test.tsx` | `20a4499a67483767df18a96393d10f8322933f32db05c3b8f749299f4f408a66` |
| `tests/unit/chart-editor/vitest.config.mjs` | `0ded201f30f09e66996d0c2a3e6870ddb8cac347e303dd85f35130fd8a0a8373` |

The controlled Shadow subsection satisfies its approved local contract; publish this verdict and the reviewed `shadow-light-dark.png` only.
