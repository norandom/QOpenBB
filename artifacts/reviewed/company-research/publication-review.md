# Company Research publication review

## Review Verdict

- VERDICT: APPROVED for criterion 6.4 and task 5.3 publication verification. Together with the accepted source and local runtime evidence, this supports closing all 13 executable Company Research tasks within their bounded scope.

The [alpha-43604526965-1 release](https://github.com/norandom/QOpenBB/releases/tag/alpha-43604526965-1) is bound to root `fbd81eaf11d82b47043592f60736009304f198c8`. [Workflow 43604526965, attempt 1](https://github.com/norandom/QOpenBB/actions/runs/43604526965) completed both candidate and publish-alpha jobs successfully. Independent remote tag resolution matches that exact root. Application sources are Workspace `bf180ef506286886da224df9ff184cd1ace2397e` and Data API `a965f70c164fe477ce9c99654b9be48e2f1bc9fd`.

## Actual public assets and image checks

Three anonymous HTTP 200 asset downloads match their GitHub metadata, reviewed source bytes and final receipts. The public sample filename is default.env.sample; its contents match the released repository's .env.sample.

| Asset | Bytes | SHA256 |
| --- | --- | --- |
| compose.yaml | 1359 | 0dda6c229eac7e6c7a8c55fa717bf338acbc5cd5e1634b8e2702de5393344724 |
| default.env.sample | 1299 | 8958b109b85f8e818e5b6d595b422881ed2e611f45106bde2ec268afc552348b |
| manifest.json | 7061 | 569c3e62ccf8a688d5bfdffa2565cc477ad51e98366f38eea93bb68519e2c793 |

The approved v2 verifier completed successfully. Independent post-execution review reconciled six successful actual pull/inspect receipts with the frozen manifest: immutable digest, exact release tag and latest for each service. All 28 finite execution stages have the expected ordering, including both remote config checks and both final latest checks. The final receipt equals the accumulated six-pull progress; no failure receipt exists. All 60 frozen inputs still match their reviewed hashes. Strict private reads confirm both isolated auth files remain empty; no registry login or ambient credentials were used.

| Image | Manifest digest | Config/local image digest |
| --- | --- | --- |
| ghcr.io/norandom/qopenbb-workspace | sha256:5e456b5f84383f49eb3e9cbda85ec20c9006e31d18619be715e4743c7cc8b570 | sha256:647c196c7936c67f6feed0bf9b2d0f6c92d2e9299f181fe46cdc1341595781c3 |
| ghcr.io/norandom/qopenbb-data-api | sha256:fa113636cfb8a7df948053cfa39b8473e987ad68ab39ec54c0f079fa2909fac9 | sha256:aa606c71f1d12951468aeedd5b353854853237d5c0ce25bf9dfaffa0021c229a |

Raw remote manifest and config hashes, Linux/AMD64 platform, exact source/provenance labels and local inspected identities passed the reviewed fail-closed verifier. Local IDs were correctly classified as config digests; they were not confused with manifest digests. Both moving latest aliases matched the release pair at the end of verification. This establishes observed publication/access/identity at verification time, not permanent immutability of latest.

Downloaded Compose passed parser-only validation with immutable image overrides and noncredential provider markers. No build or container startup was issued by the verifier, and no provider requests or owner-server operation occurred. The public sample contains no configured credentials.

## Provenance and retained qualifications

Final verification receipt SHA256: `88396153f8285eb365fe9e2e98ff49545196a835c33e0d3d9347b05e45e6024d`. Six-pull progress: `3a7877dd0c835f8e0eb429a1424be40a4116a508a20fc6a9a0adf321ad0339d7`. Finite stages: `415a6802c3e5dee5b54ed446fe194613d64947284feb28eee7912e30b6a10226`. Reviewed v2 freeze: `2de830961035e90a8c3a61a9e1d04767e8ec731de3bee120a5cc28f7e6dfe7a2`.

The first verifier attempt remains failed and preserved. It omitted native home variables; local help-only reproduction confirmed the initialization defect. The reviewed v2 preserves the maintained home configuration while retaining explicit empty authentication. Missing first-attempt progress alone is not treated as proof of zero pulls. No automatic retry concealed that failure.

These public CI rebuilds are not the exact local d00c17/a91d48 image pair used by the accepted financial journey. They share the accepted application source pins. Publication verification does not claim another financial browser run on the public images. The earlier successful journey remains root 4736c31/browser c9a267; the later checkpoint writer remains separately verified offline. Historical checkpoint ACL exposure, its reviewed custody correction, no pre-correction payload hash and no independent initial Workspace inventory snapshot remain disclosed in the linked runtime evidence.

Full IA-B readiness, house valuation/aggregation/ranking, live macro integration, whole-application compiler/full-suite success, backup/restore and owner-server deployment remain outside this acceptance. Existing qualified test counts must not be summed into a new suite. Final task/breadth/documentation reconciliation should reference this publication receipt without rewriting historical pending or failed evidence. Only sanitized reports and finite receipts are suitable for the reviewed mirror; raw private state, credentials, tokens and provider payloads remain excluded.
