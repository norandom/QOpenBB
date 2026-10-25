# Protected dependency promotion review

**APPROVED to promote the reviewed package.json and bun.lock only.** Reviewed 2026-10-25. No installation, source mutation or broad check was performed by this reviewer.

Read the dependency plan, install report, exact install script/command, protected-install summary, post-install semantic comparator/report and typed/converter evidence. Actual install, typed import and converter smoke each record exit0. Safe Chain records both requested tarball paths and2058 scanned packages with no malware found; this is protected installation evidence, not merely a wrapper availability check. The script uses the direct pinned wrapper, frozen lock, ignored scripts,48-hour age protection and an initially absent owned cache. No integrity bypass is present.

The post-install comparator checks exact direct pins `culori@4.0.2` and `@types/culori@4.0.1`, exact approved SHA512 entries, all2539 existing package records and all remaining package/lock metadata unchanged. Its assertions compare parsed structures, not only record counts. Independently reread hashes match:

| File | SHA256 |
| --- | --- |
| Stage package.json | ffa573fad8456552d4caa372715e1c8e615314669a048c8d718fa6610b3b576a |
| Stage bun.lock | 4b2754f9f91b9fe22a501f44b496e8339e1a46a977e08a3bfd6ff555ae8892e7 |
| Current production package.json | 22b8936be4a077f40ced2b3ab6a1dd7f0731c5b90f7ba59267fabf07624dafe0 |
| Current production bun.lock | 747dd1514aac6aaa3bb63e33e4146b9f0a9bd4f02da2a1e595f15102f4d290f5 |

Stage is `/home/mc/qopenbb-work/h2-culori.3abcwa`. Promotion must preserve these exact staged bytes and recheck unchanged destination baselines if another dependency operation intervenes. The earlier `semantic-review.json` is explicitly pre-install evidence; `post-install-semantic-review.json` supersedes its installation status.

Strict typed-import evidence covers normal ESM conversion/formatter types and negative sentinels; converter smoke covers installed versions, MIT files, independent red OKLCH reference tolerances, red/white/black roundtrips and undefined invalid input. It does not establish original interpolation or renderer parity. No application-wide clean compilation or separate retained-tarball digest check is claimed; Bun's normal integrity verification remains the archive check.

Parent's proposed local test access through two new package symlinks is acceptable as a serialized development-only step: verify each destination is absent, including dangling links, target the exact protected stage packages and retain that stage while consumers run. Do not replace existing dependency entries or the terminalpro node_modules root symlink. Record the new links; they are not clean-install evidence. Reviewed package/lock and protected frozen CI installation remain the delivery mechanism.

No blocker remains to this exact promotion. Keep the upstream Bun compatibility exception, one lockfile and unchanged overrides; no dependency migration or unrelated update is authorized.
