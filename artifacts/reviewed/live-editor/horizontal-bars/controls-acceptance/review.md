# Horizontal control acceptance

Task 2.80 connects existing Horizontal/Vertical controls to physical axis direction while preserving semantic category/number identities. Independent Sol review approved the change. Application activation and browser acceptance remain task 2.81.

Horizontal remains first. Bar titles and typography select numeric-X/category-Y metadata from concrete bindings; latest-state title intents rehydrate against current bindings even when rendered metadata is stale. Original option types and both directional positions are preserved, as are unknown and inactive settings. Category-only controls follow the category axis. No saved axes, controls or flags were added.

Independent pinned Node/Vitest application-config run: 90/90 passed across editorHorizontalAxes, editorBindings and editorSavedLeaves, exit 0. Six-file Biome lint passed without fixes. Combined explicit-manifest complexity gate passed 400 physical / 300 logical / 50 function limits with no errors or violations. RED tool transcript records five pre-edit failures and is honestly labeled as a transcript excerpt. Compatibility TypeScript retains existing typography TS2578; broader application compiler failures remain unaccepted.

Local evidence and independent review: artifacts/live-editor/horizontal-bars/controls. Base Workspace de5e419e9de596e38e3357e61c3309f22a98b700 plus exact files below. Browser and release readiness are not claimed.

| File | SHA-256 |
| --- | --- |
| `terminalpro/src/components/General/Table/Chart/editor/ApplicationAxisEditor.tsx` | `aecbf7d6ff712772f03dfb19a74ed4f402bd620eab7984e258c2715f77fe663e` |
| `terminalpro/src/components/General/Table/Chart/editor/ApplicationCustomizeEditor.tsx` | `882572b7738ca8a11f3abe88fed748268d7603be86f9e4e98a25a453a5ab9b7b` |
| `terminalpro/src/components/General/Table/Chart/compatibility/editorBindings/metadata.ts` | `f12f9b16905477528858954522def6d931e0971af6489d2419c6a4d8daaf6b93` |
| `terminalpro/src/components/General/Table/Chart/compatibility/editorBindings/selectApplicationEditorState.ts` | `9b42a5d5e4568fc6b8efdc2164634064a31eceb1074646b17b5f21775323c34e` |
| `terminalpro/src/components/General/Table/Chart/compatibility/editorBindings/rehydrateApplicationEditorEvent.ts` | `97e7f65d0c6c80145f026e57aab020a6e5f038755fbcd569e36ae16a14c06066` |
| `terminalpro/src/components/General/Table/Chart/compatibility/editorBindings/mapApplicationEditorEvent.ts` | `e71aded857953e4372a36e30305a79e95bbe04b03a2f2abf38b50e29ff7f8dfe` |
| `terminalpro/tests/unit/chart-application/editorHorizontalAxes.test.tsx` | `5245b781a2b93a98bf42388f04b4132a6a0e59b99f525669def5c7fac5ee1f0b` |
| `terminalpro/tests/unit/chart-application/editorBindings.test.ts` | `a5ffc0aad250063283c1ba5c98112db85ff9eff94b447fe75717d70bb5f1713f` |
| `terminalpro/tests/unit/chart-application/editorSavedLeaves.test.ts` | `2b638e290511ea32daff13618c555e29d7952c15e800808f559f7acb9e54b2cc` |
