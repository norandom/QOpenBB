# Saved-output contract compatibility

Foundation task 9.2 checks the QOpenBB saved-output Workspace consumer. Its accepted baseline is the immutable adoption commit `e0ed60b95740c950e93080d113dde8693fd15c8d`. That commit pins the producer and consumer source revision `31c618559f347f973d07f2dd7b496629fe92e9d5`. The candidate cannot select its own baseline through its consumer or provider manifest.

The gate verifies the bundle's file set and hashes and binds the response evidence to the candidate manifest, consumer and acceptance-case digests. It compares the accepted and candidate consumer, both forms of the exported schemas, the OpenAPI binding, method and rule descriptors, and widget discovery. Unclassified changes block promotion. A compatible verdict requires replaying the candidate export from its local source commit. A blocked report identifies the saved widget and operation and instructs the maintainer to retain the supported version or explicitly review and adopt a versioned migration.

Signed HTTP tests use disposable registered methods and private saved runs. The cases exercise a negative value, zero, missing data, a partial run with independently verified and withheld outputs, stale/unverified selection, a validation error and wrong-owner reads. The observations cover both saved runs and the corresponding widget projections. The baseline declares the expected unit, scale, currency, period and verification evidence. The service registry used in normal operation stays at its adopted revision.

## Verification

The candidate manifest `2751c9e18eae301de2c6b8de4dc33c231cd821dc16e383e61e3196aef9d8fb4a` passed with exercised evidence `fd60993e6e497fa80722cdd5ef83f56e74faba1e00b7e508f649af0b60cc9c88` and pinned expectations `51726944f2ea4b5c90b9d81c32f899868bfea8db47e6b44615933b0e6d20634f`. Changing the negative result’s widget unit while retaining the saved run and candidate produced a blocked decision and exit status 1. The finding identified the negative widget response and the affected operation `readSavedWidgetOutput`.

Independent review approved the final implementation after checking provider source identity, later-row financial context and required OpenAPI metadata. All 80 focused structural cases passed. These are offline contract and authenticated service checks using synthetic observations.

The full Ubuntu pipeline reported 1616 passed, 12 skipped, 1 deselected in 166.37s (0:02:46).
