# Sankey editor integration source acceptance

SK3 is independently source-reviewed on 2026-10-27 at Workspace `138d0412b3b0f39b2ae5c2cc7de0826ee512ff1e`. Sankey is connected to the ordinary Table/File chart gallery and existing editor, with explicit source/target/value mapping and financial metadata. Browser, appearance and release acceptance remain open.

The reviewed implementation preserves editable invalid/empty states, rejects stale edits, clears invalid geometry and export registration, and retains mappings through session refresh and family changes. Existing title, subtitle, padding, background and tooltip controls are reused. The focused source tests exercise these behaviors; they do not establish packaged application acceptance.

The independent review records the exact checks and limitations. The combined complexity gate accepts all 34 production paths, including the separately reviewed, unchanged-size schema and declaration exceptions. These exceptions permit only Sankey chart vocabulary alignment. Existing TypeScript baseline diagnostics remain; this is not a clean whole-project type-check claim.

Next: build an identified image and run the retained AAPL FY2025 income-allocation journey, including correction, filtering, refresh, save/reopen and PNG export. The USD annual root is a sum of quarterly reported revenue; the graph is a derived allocation, not cash flows or provider-supplied links.

Evidence identities (SHA256):

- Independent review: `64835907e7744da564ea88fcea5e156b13fc1ee77ec1906836219cd15778295d`.
- Frozen source: `66db547eca4932ec8f1c91bb765759134498402aa829f664e72616e935c2031e`.
- Combined complexity: `10e317df4816d4a23270f60b368049d116d339cc9dd654c009cce8197451fa60`.
