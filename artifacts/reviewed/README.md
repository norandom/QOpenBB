# Reviewed evidence mirror

Review this curated evidence before staging it. The manifest records exact source and published SHA-256 values for each copied file. Original ignored folders remain authoritative raw evidence; this mirror does not claim to publish all repository artifacts or establish new acceptance.

## Included evidence

- SQLite tasks 4.6 through 4.9: task/reviewer reports, serial verification scripts, actual logs/results, boundary diffs and quality inventories. Start at [the joined review](task-4.9/review/review.md).
- Chart application design: [design and source-range review](chart-application-design/review/design-review.md), [stock matrix review](chart-application-design/review/theme-matrix-review.md), source paths and capture handoff.
- Original chart editor, payload and line captures: synthetic fixture inputs, post-login screenshots, finite UI JSON, saved-item writes, patch deltas, sanitized diagnostics and reports. Redundant DOM HTML is omitted; equivalent JSON captures remain.
- Original theme finite projection and [six stock cases](parity/theme-matrix/report.md), including authoritative first-pass dark stacked/line JSON and screenshots. The report's case table defines which attempt owns each observation. First-pass scripts and duplicate intermediate images are omitted.

- [Custom grouped-column themes](parity/custom-theme-contract/report.md): actual dark/light UI saves and finite palette/background assertions, with the first oracle failure, final Node/assertion success and shell-wrapper failure retained.
- [Formatting source extracts](chart-format-contract/) and the [initial publication review](artifact-publication-review/review.md). Source inspection is not runtime formatter acceptance.

## Reproduction and link mapping

Paths below this directory preserve their source-relative layout beneath `artifacts/`. For example, `artifacts/parity/theme-matrix/report.md` maps to `artifacts/reviewed/parity/theme-matrix/report.md`. Relative links among included siblings retain their meaning. Existing report commands, absolute paths, source hashes and embedded artifact paths are historical evidence and have not been rewritten. Resolve repository spec/source links from the repository root. Links to excluded raw/private artifacts are provenance references, not public dependencies; consult the manifest exclusions and the finite derived outputs instead. Raw inspector references are intentionally unavailable.

Verification sources are exact historical copies, not relocated portable commands. To reproduce SQLite checks, use the original source-relative script location described in the reports, or restore the mirrored script to that location in a disposable checkout. Relative `__file__` root calculations would otherwise resolve incorrectly inside this mirror. The stock matrix `start.mjs`, `journey.mjs`, `run.sh` and fixture form the minimal runnable research starting point at their recorded original paths, with pinned local WSL Node/Playwright/browser/image prerequisites. They create new random disposable credentials; generated credential files must stay ignored. No script was executed during this synchronization. Legacy env-reading capture launchers, older raw-inspector projection scripts and private dumps are excluded; their finite observed outputs are retained. The custom-theme journey includes its bounded reference-only projection, which is not a production dependency. Reproduction still requires the pinned original image and stated dependencies.

## Publication boundary

No real environment files, accounts, databases, storage state, provider keys, credential-private files, login screenshots, raw private inspectors, dependency/cache directories, image archives, traces or authentication logs are included. The literal `Aa1!` in launchers is an explicitly synthetic password-policy prefix concatenated with fresh cryptographic random bytes, not a login credential. Package names such as SecretStorage and source identifiers containing password/token are not secret values. No known ephemeral login literal required redaction; every mirrored source is an exact byte copy. README and manifest are synchronization metadata, not historical source evidence.

Earlier task 1.x/2.x/3.x evidence and older parity builds/probes remain backlog outside this synchronization. Range findings are covered by the design review addendum and authoritative repository specification, not invented browser range evidence. Custom-theme behavior beyond the two grouped-column cases, expanded controls, exports, backend reopen, candidate parity and project release acceptance remain open as recorded in the original reports. The original bundle parse errors and first-pass nonzero exits remain visible. This synchronization performs no heavy build or browser verification and grants no implementation acceptance.

The [source/custom-theme review](formatter-contract-review/review.md) and [publication delta review](formatter-contract-review/publication-delta-review.md) cover the later additions. Earlier publication counts identify their reviewed snapshot, not the expanded manifest.

The [integration freeze review](chart-integration-freeze-review/review.md) permits bounded source-safe task planning after phase approvals. The [editor probe](parity/editor-contract-completion/report.md) and [retry](parity/editor-contract-retry/report.md) preserve failures and finite projection progress; neither establishes nested-control parity. Historical failed launchers must not be rerun with their old cleanup paths.
