# Bounded model execution

Foundation task 4.2 runs an installed method in a fresh Python interpreter with a child-specific Polars thread budget. The frozen model descriptor stays wire-compatible. The executor binds trusted size measurement and execution limits to the exact model ID and version. The service defaults to one active evaluation, one Polars thread and a 60-second timeout; method-specific timeouts can shorten the deadline.

The worker checks the supplied snapshot and assumptions, measures actual rows, horizon and scenario count, and returns a validated candidate. The test method explicitly collects a Polars lazy frame and checks that its declared decimal type can represent each supplied amount without rounding. Clean, null, unsupported numeric, wrong-schema, over-limit and unknown-version cases have focused coverage.

On Ubuntu, an evaluation has a dedicated process group. Timeout and cancellation end the worker and its ordinary subprocesses before releasing the slot. The controller also exercised the staged runtime package using temporary test registrations. Three issuer evaluations returned −10%, zero and 5%, with the original traces, after a cancelled request. The Polars and native runtime entries in the portable test lock match the service lock, including version 1.44.2 and wheel hashes.

Independent review approved the deadline and admission behavior at the public entry point. The 350 ms timeout probe returned in 354 ms. Cancellation at 80 ms returned in 104 ms. The same executor then returned the exact decimal 12345678901234.0025. Model serialization occurred only at executor construction. Transfer checkpoints and private IPC caps of 64 MiB for input and 16 MiB for output bound the request path. The worker and parent each enforce the result limit.

All 34 focused executor and registry tests passed. The final portable gate passed 1,236 tests with 12 skipped and one deselected. It checked 826 maintained files with zero complexity violations. Verification ran on Ubuntu with Python 3.13.15 and pinned Node 24.22.1. Base revision d89da59.
