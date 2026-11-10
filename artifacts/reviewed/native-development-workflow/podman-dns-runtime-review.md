# Corrected image and offline route review

APPROVED for the corrected Workspace image and bounded offline metadata qualification. The previous catalog-routing blocker is resolved on the qualified image pair. Financial/provider and browser acceptance remain unverified.

Identity reviewed:
- Root build input: 0f4a8c9af13be0829e3be34220e882f29a8ecdfc.
- Workspace source: e1a12c3a031a23598f41166a0f91b8fb24ac2387.
- Data API source: 2e60c0a7aff039eda5f14a9d494beaec822fb9c4.
- Workspace loaded image: sha256:05e16ad56e7275a71edb3aadd4449063f3df40073713588b1f0dedee55e60053.
- Workspace archive SHA256: ac559d1ae72bcd97e7b63d762d3cd546a38eb3483ee5af75589fba061ca72d01.
- Workspace manifest: sha256:418769c2d8dc67af8a465e0b657d135d9e760c38be2a26f0c9a26c0625776952.
- Unchanged Data API image: sha256:b3e56de1878d02f894d80111ba4ecff14b98292b9045ea6cc88e793f41a5f807.

Independently compared receipt.json, workspace.export.json and workspace.load.json: archive, configuration, manifest, labels, architecture and OS agree; loaded image equals the configuration digest. Export source hashes include the previously approved script and test bytes. Build source lock and contracts match the clean root commit. Stage and build receipts each report exit 0, using Dagger SDK 0.21.8 and engine digest c9c1a0a6546380983d42e8d75adde070a2a0935c54b498d8bc9045d9cb2ee336, consistent before and after build. These are local image identities; the load report has no registry digest or publication claim.

Reviewed the frozen check_runtime.py and its packaged-smoke helper. Checker SHA256: 742bb845d0213d1f6ef68f98b857194a9d451922d93b1a2b518a81d7bb35dde6. It requires immutable image identity and new outputs, starts owned disposable runtime, validates installed script bytes and resolver directives, exercises health/config/login/rejected-password/private-state checks, requests catalog and readiness through the actual host origin, captures sanitized logs and cleans up. Its requested application endpoints contain no financial provider endpoint or browser operation. The provider_endpoints_requested zero field is a scope declaration, not an independently instrumented network-send counter.

Final qualification.json SHA256: 4d21678544bb83d3b95fc96271cba62da478016eccea6f9bdc10e572704844e6. The parent reports process exit 0; the inspected final report has verified=true, exact matching image pair, health/login 200, rejected password 401, bind-state checks passed and logs_secret_free=true. Windows bind-mounted state is checked through Windows owner-only ACL authority; its reported POSIX 0777 representation is not used as the permission authority. Container-local private files are 0600 and nonroot-owned.

Actual resolver 10.89.13.1 matches the generated nginx directive. Installed configure-origin.sh SHA256 is d471101199c7c7ffefe9424a0527c6c6f6b23cf534ac9dd0c5513f964d736037. Through the actual origin, /data/widgets.json returned 200 with all eleven expected native financial definitions and table/data/provider metadata; Income endpoint, default annual period and annual/quarter options passed. /data/readyz returned 200 with no missing services/routes. This supports real container DNS and reverse-proxy catalog routing, beyond the earlier shell fixtures. Cleanup reports container_removed=true and state_preserved=true.

No blockers within this scope. Reviewer ran no build, suite, container, browser or provider rerun. This evidence supports presenting the exact corrected image pair for a separately authorized financial attempt. It neither accepts financial values or save/reopen behavior nor authorizes that attempt.
