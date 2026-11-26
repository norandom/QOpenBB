# Financial model change verification

Foundation task 9.3 links changed contract identities to financial-modeling criteria and executable checks in the [impact map](../../../.kiro/modeling-impact.toml). The source check runs on the committed candidate and retains both ends of the Git comparison. The report distinguishes an unaffected range, a verified affected range and a blocked range.

A change to a model, rule, provider operation or saved widget selects checks through its mappings. A missing obligation triggers broader source verification and keeps the gap visible. Each pytest selector records the collected nodes and their setup, call and teardown outcomes. Unexecuted, skipped and missing checks leave the capability unverified.

For an affected range the gate exports the candidate and records the results of authenticated evaluations and saved-output reads. The report preserves the adopted contract and candidate identities, consumer and response hashes, source lock digest and exact fork pins. Verification used synthetic financial inputs. The source check exercised no deployed images or live providers.

## Observed candidate

The source change from `3f5cd2d2b96eb4e459a5da2de69ea9890fd749d8` to `2c7bdf9e5953b6db45b73c71d0195464b3752f0b` selected 72 checks. All 138 distinct pytest nodes passed and the report recorded zero mapping gaps. The candidate provider manifest was `91aa1f645c86aab39bccca430ff09945367d7344942a1ee49be63eb884cfc196` and the exercised saved-output evidence was `55b0447ee2c5f7797a261b601c1866f4089a199fff068724d20b9c0138db3fd3`. Both acquired forks matched their locked origins and revisions before and after execution.

The [integration report](modeling-impact-report.json) contains the exact selector outcomes, source pins and compatibility decision. Its SHA-256 was `ba74b4fdd82f9f5830f1a134f3db586350a8d5d25684e6da62696994114966c4`. Independent review approved the shared-input numerical coverage and regressions for collection filters that could omit a failing test file.

The full Ubuntu verification suite reported 1666 passed, 12 skipped, 1 deselected in 195.56s (0:03:15). The complexity inventory covered 862 files with zero errors or violations.
