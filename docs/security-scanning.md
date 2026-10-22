# CodeQL security scanning

Use GitHub's Security tab to inspect CodeQL findings in the repository that owns the code. QOpenBB and its application forks have separate scans; scanning the root repository does not cover ignored vendor checkouts.

| Repository | Analyzed source | Languages | Triggers |
| --- | --- | --- | --- |
| [QOpenBB](https://github.com/norandom/QOpenBB/security/code-scanning) | `.dagger`, pipeline, services, tools, verification and tests | Python, JavaScript/TypeScript | Main pushes/PRs, weekly, manual |
| [Workspace fork](https://github.com/norandom/openbb-workspace/security/code-scanning) | Backend API, Lite and Terminal Pro | Python, JavaScript/TypeScript | Adaptation-branch pushes/PRs |
| [Data API fork](https://github.com/norandom/openbb-data-api/security/code-scanning) | `openbb_platform`, including providers | Python | Adaptation-branch pushes/PRs; manual against that branch |

The adaptation branch is `qopenbb/baseline`. The data API workflow is also available on its default branch to support manual dispatch; this does not merge application changes into that branch. Workspace manual dispatch requires its workflow to be available on the default branch first. Fork weekly schedules are not configured.

The workflows pin CodeQL v4.39.1 and checkout actions to exact commits. They use the standard security queries and no-build extraction, with two query threads and at most two language jobs per repository. Checkout has read permission; only analysis jobs receive permission to upload security events. They do not receive provider keys or registry credentials. Dependency caches and historical artifact copies are excluded from the declared source scope.

- [x] Independently review the workflow configuration and pass actionlint.
- [ ] Confirm successful extraction, analysis and result upload in all three repositories.

A successful scan records analysis coverage; it does not mean every finding is resolved or replace financial/browser acceptance. Review uploaded alerts separately. Image publication continues through the [prototype delivery workflow](prototype-delivery.md).
