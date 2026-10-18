# Ordinary chart integration acceptance

Task 2.77 closes the ordinary grouped-column, stacked-column and line integration milestone. Existing editor controls, displayed observations, saving and reopening now have joined application evidence. UI-10 through UI-16 and release-image deployment remain pending; this is not full renderer acceptance.

## Evidence

The actual Full Workspace browser journey passed 1/1 with one headless worker, zero retries and no skips. It exercises the three families, representative editor sections, visible tooltip and vertical-axis stroke, native navigator and miniature dragging, light/dark rendering, failed-save recovery, fresh-session and backend-restart reads, current PNG export and table return. Unknown model fields, unknown options and the inactive pie branch survive those saves and reads. Miniature endpoints remain at full extent while the main plot changes.

Earlier independently reviewed checkpoints cover filtered/sorted observations, series removal/addition, Sum/Avg and category/series switching. The owner accepted the refined default light line view. Those records remain under the adjacent browser-checkpoint, filter-repair, visual-refinement, manual-rotation, series-add and setup-transformations directories; they are not rerun merely to duplicate evidence.

Command: pinned Node 24.22.0 runs `verification/node_modules/@playwright/test/cli.js test application.spec.ts --config vendor/workspace/terminalpro/tests/e2e/live-chart/playwright.config.ts` with the existing owned runtime and evidence environment. Raw report: `artifacts/live-editor/runtime/ordinary-closeout-final/browser-results.json`. Duration: 85.1 seconds. Strict application diagnostics retain their existing exclusions; no new failure is allowlisted.

The combined complexity command (`python -m tools.quality.complexity --check`, explicit Workspace/data-api manifests) passed. Its Workspace scope includes 84 changed production files selected by `git diff --no-renames --name-status bc202e457087794e984b1bd4d44518a868560811 6db2fb96db507a604541114e8bf0841276e6794e -- terminalpro/src`. Manifest base/head both identify the current inventory pin, as required by the checker; `scope_selection_base` separately records the historical comparison. These changes add tests only, exempt from production caps.

## Findings and limits

Fixture corrections were required before this pass: unload the old editor before seeding backend fields, open the Quick actions submenu, expand Chart Style before reading padding, and drag the actual handle rather than a plot-derived coordinate inside the slider. Backend readback verifies the fixture before edits. These are test repairs, not production data-loss or navigator repairs.

The historical CSV cancellation remains unexplained, as recorded in setup-transformations/review.md. Original numeric-rotation/Auto Rotate and structural-axis restore limitations remain disclosed; this does not claim broader round-trip parity. Representative controls are covered, not every possible option combination.

Runtime: owned source-overlaid backend image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`, backend overlay SHA-256 `23b6323e40a2edaa7267e25f72d032da8e92ccef09cc09545cb749fe2d2a15de`, 43 files. This is not a verified release image. Provider entitlement, other chart families, advanced callers and deployment are outside this acceptance.

## Source identity and review

Workspace base `6db2fb96db507a604541114e8bf0841276e6794e`, plus the following files under `terminalpro/tests/e2e/live-chart/`:

| File | SHA-256 |
| --- | --- |
| `application.spec.ts` | `840167a556636ccf02295082ba4be6095417ee71039de4dac8e6a11590ec414b` |
| `diagnostics.ts` | `b013ace34c2caed90076083b89439f389cbeb6b0fd9b9ef77bbb194a1da6aca4` |
| `effects.ts` | `4f0da86ce2d200d016f748da5e479c2a60abfd0e0442c3d076235bf9de9de1c5` |
| `saved-compatibility.ts` | `ae973fd6b6ee0aeb3efdd4f3a7584af6ef4cf11307f18843410b7e8706de8217` |

Independent Astra review: APPROVED and VERIFIED for the ordinary task 2.77 milestone. The reviewer inspected the current light/dark screenshots and exported PNG, decoded application diagnostics, verified the four source hashes and checked the zero-error/violation size audit. The export shows the updated saved title, Revenue 10/20/30 and Cost 4/8/12. See [current export](saved-ordinary-observations.png).
