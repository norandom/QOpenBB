# Local image final review

APPROVED for task 2.91 on 2026-10-19: the identified unreleased Workspace and data images built, loaded and passed the bounded packaging/offline checks; the exact Workspace image exposed its authenticated application shell in an isolated browser. This supersedes the failed first checkpoint. No blocking findings remain within this scope.

## Source and image identity

Both final export records identify Workspace `027d7703bb1c5447c0d058256598fa7b52049d2e` and data API `49cc413e6ab67eaa0444e07485b0f9243c786f7b`, using pinned Dagger engine/SDK 0.21.8, engine digest `c9c1a0a6546380983d42e8d75adde070a2a0935c54b498d8bc9045d9cb2ee336`. Final loaded IDs equal the exported manifest digests:

| Service | Loaded image | Archive SHA-256 |
| --- | --- | --- |
| Workspace | `sha256:79eb31596c4cb89dc10b81ec2a190263a212446bb9f5307157de9fac24fe4b39` | `d1cec47a31d9a00fdf96aae5e9438c953464464a890c4323e6948e9500c1f5bf` |
| Data API | `sha256:bd9194307a51357c6730e310dd9c460150df98e7aa964b976f37038554755d79` | `aa27cba1cbc27c0840965c5b1b03fad40a66ad48714c45f8ac7176ac57828f71` |

## Verification reviewed

- Workspace packaging report completed against the final loaded ID: healthy, health/login 200, incorrect-password 401, Full same-origin configuration, disposable bind state, secret-free logs and owned cleanup. Data offline suite: **3 passed in 20.25s**.
- Independent running-container inspection confirmed the final Workspace ID, loopback port 55529 and exactly one writable disposable bind mount to `/data`, with no source overlay. Safe descriptor-field inspection confirmed image-only mode, matching frontend/runtime PUBLIC_URL, mode 0600 and `release_image_verified: false`; credentials were neither printed nor published.
- Existing isolated, headless Playwright/CDP harness: **2 passed, 0 skipped, 0 unexpected, 0 flaky**, one worker, no retries, 11.97 seconds. The packaged-page check performs real disposable login, verifies visible authenticated shell and same origin, rejects Vite/source assets and checks application/console/network diagnostics. The gallery continuity journey also passed against the built page.
- Independently viewed `packaged-workspace-shell.png`: the authenticated Apps page, navigation and local build identity are visible without credentials or private financial data. It is suitable as the single published screenshot. This is shell accessibility evidence; it does not certify renderer families or compare different left-hand series.

The first build exposed seven required AI source modules incorrectly removed by the global artifact filter; reviewed task 2.93 added exact-file exceptions. The first browser run then exposed a missing datafeed script served as SPA HTML; reviewed task 2.94 made missing `/assets/` files return 404. Final images use the ordinary pinned build with both repairs. The known unavailable datafeed bundle 404 remains explicitly allowed by the existing diagnostics contract; no diagnostic exception was broadened.

Publication approval covers this report, a sanitized identity summary matching the final reports, and the single packaged-shell PNG. Keep raw logs, private descriptors, account state, traces and image archives local. This checkpoint does not accept complete renderer parity, live providers, Anthropic, Excel, registry publication, release readiness or deployment.

Final publication check: `image-identities.json` was independently compared field by field with both final load reports; loaded IDs, archive/config/manifest digests, null registry digests and source labels match exactly. Its contents are public provenance only. The test-only verification commit `11c3424` follows the built application revision `027d770`; it does not change the image source identity. The scoped documentation addition accurately links this local checkpoint and retains its release/deployment limits. Approved publication set: this report, `image-identities.json` and the single packaged-shell PNG.
