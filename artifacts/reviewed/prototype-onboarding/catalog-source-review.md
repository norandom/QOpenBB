# Installed catalog source repair

CAT1 and CAT2 source acceptance is complete on 2026-10-27. The assembled prototype exposed the gap: its health, readiness and OpenAPI routes worked, but `/data/widgets.json` and `/data/apps.json` returned 404. The repair packages the two existing committed catalog files and serves their exact bytes through fixed read-only JSON routes before the core API mount.

The existing runtime-input allowlist, hashes and provenance cover both assets. Dagger copies them into `/app/qopenbb_data/catalog`, matching the runtime's sibling-directory lookup. No generator, provider schema, catalog contents or readiness contract changed. The existing transitive route compatibility check against the running API reports no changes or revalidation requirement. Missing or tampered build inputs fail the existing staging checks.

Verification: 14 existing packaging cases pass in 5.12 seconds, including catalog tampering. Eight focused runtime cases pass in 3.99 seconds, including both exact-byte GETs, read-only method behavior and the four existing API regressions. The final runtime run uses explicit read-only code/test/catalog/tool mounts, no owner environment files, and disabled Docker networking. The two missing GET cases failed before the repair. Earlier raw-ASGI fixture and exact-405 assumptions were corrected without production workarounds; they are not additional product defects.

The existing syntax-unit checker measures `runtime_inputs.py` at 34 physical/25 logical/largest function 12; Dagger `data_api.py` at 43/12/3; runtime `app.py` at 48/24/10. All satisfy 400/300/50. An independent Sol review inspected the actual joined source, tests and final isolated output and returned APPROVED. The detailed local verification record was updated to the final 3.99-second explicit-mount run before publication.

This is source acceptance. Rebuilt-image catalog serving, first/later browser login and the live FMP Compose journey remain open until the same application test passes. No expanded provider coverage or owner-server deployment is claimed.
