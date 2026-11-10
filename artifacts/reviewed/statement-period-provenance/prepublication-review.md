# Prepublication catalog review

Selective promotion of the eight proposed outputs is safe as the accepted local candidate baseline. No blocking catalog defect was found. This review does not accept publication: replace the candidate image provenance with evidence captured from the actual published image and recompute its hashes before closing task 7.

Reviewed 2026-11-10, root HEAD 23d35aa, proposal `task6/corrected/catalog-utf8`, against root contracts, clean controller generator and sources.lock. No live calls, image builds, repository edits or commits were performed. Generated outputs are exempt from 400/300/50 production caps; this proposal changes no generator code.

## Independent evidence

- All eight entries in hashes.json match SHA-256 of exact proposal file bytes. datasets.json is byte-identical to the root inventory; its hash is 714994fd425b8ee02a4c3d5489614b0b556e800274a68c615647503ecc1d4d8c. Preserve that tracked file.
- All five maintained generator hashes match both clean controller files after LF normalization and committed HEAD blobs. The accepted catalog_runtime.py hash is 338dd60463273f728b51f98689ad20bf9ebfab503aa155b9e4f35877721bbbb7. No dirty catalog_cli, renderer or inventory input is needed.
- The three upstream generator/asset file hashes match Git blobs at API a965f70c164fe477ce9c99654b9be48e2f1bc9fd. Provenance revision and API label agree with sources.lock; Workspace label agrees with e1a12c3a031a23598f41166a0f91b8fb24ac2387.
- OpenAPI local references validate using the clean accepted validator. compatibility.json recomputes exactly from current root routes and proposed routes using the clean accepted compatibility function.
- Proposal provenance identifies local image sha256:9b1649810b0d83500f5bb1219adcb6aed8eeb6e674163f1b1d72f6d0f98f63e0. That is candidate evidence, not an anonymous registry pull receipt.

## Semantic comparison

No paths or widget identities were added or removed. OpenAPI changes comprise 47 structural leaf changes: statement descriptions/query text, one optional statement_provenance member and four referenced strict statement schema definitions. Existing metadata remains shared across all eleven routes, explaining compatibility flags on unrelated consumers without implying changed FRED data behavior. Old strict readers require the approved migration note.

widgets.json changes only the three statement widgets, with eleven text/tooltip changes. Parameter choices, defaults and table structures remain stable. apps.json is semantically unchanged. catalog-report.json changes only served_schema_hash, retaining eleven mappings and existing sanitizer omissions. The compatibility report correctly requires review by Workspace, agent and future Excel consumers.

## Promotion and remaining checks

Promote only contracts/{openapi,routes,widgets,apps,catalog-report,compatibility,provenance,hashes}.json from the reviewed directory. Preserve datasets.json and unrelated working-tree changes. Stage explicit paths and inspect the index before the controller-owned commit.

Parent reports fresh clean-controller test_catalog_financial plus test_catalog_runtime: 59 passed, one opt-in image test skipped. This report independently verified hashes, source identities, references and compatibility; it did not repeat that pytest run. A focused test_catalog.py run is useful for sanitizer/mapping regression if not already covered by retained acceptance evidence; no live provider suite is required for this promotion.

After milestone completion, verify anonymous published image identities and source labels, run the existing opt-in catalog runtime check against the exact pulled data image, regenerate with the same five-module generator and preserved inventory, and compare openapi/routes/widgets/apps/catalog-report/compatibility semantics with this accepted baseline. Image/provenance/hash differences are expected; source/schema/consumer drift must leave publication acceptance open. Retain actual portable Linux results, manifest and prerelease evidence, and distinguish published images from the local candidate. No owner-server deployment claim is supported here.
