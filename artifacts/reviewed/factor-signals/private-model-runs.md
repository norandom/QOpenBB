# Owner-scoped model runs

Foundation task 6 persists the complete ModelRun, including source snapshot, assumptions, versioned descriptor, checks, exceptions, traces and independent verification. The generated run ID is independent of its content hashes. A fresh evaluation of the same inputs gets its own record.

The file store writes a private same-directory staging file and publishes it with an atomic, no-replace hard link. Readers reopen completed runs by opaque ID and exact authenticated subject. The implementation revalidates the saved contents and compares fingerprints on read. The test suite used temporary local directories and synthetic principals.

The controller saved three verified FCF yield evaluations and reopened them from a fresh store instance. The saved outputs retained −10%, zero and 5% with their original inputs, traces and matching reference evidence. A different principal could not retrieve any of the runs. Base revision e9d5ec8.

Independent review approved the storage component after reproducing failures on both sides of publication. A file-sync failure before publication left no visible record. After a successful link, simulated staging-cleanup and directory-sync failures returned a recoverable exception containing the published ID. A fresh store recovered the original evaluation by ID under the same principal. All 29 focused store and audit-evidence tests passed. Scoped Ruff passed. Both production modules fit the 400/300/50 complexity limits.
