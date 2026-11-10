# Native Compose lifecycle accepted

Task 6 is accepted on 2026-11-10. An owned Compose session can be recreated with its existing account, state, origin and image pair; cleanup removes only verified session resources and preserves state by default.

Actual Podman evidence records Workspace container d3690e68 changing to d4464e98, successful existing-account login and retained host/container markers. Wrong-daemon and replacement-resource probes refused mutation. Repeated stop preserved state and left an unrelated fixture untouched. The serialized test restored exact historical template bytes temporarily and restored the current reviewed bytes afterward; no ownership checks were bypassed.

Independent Astra review identified two defects and accepted their repairs: interrupted recreation now requires an exclusive protected intent journal before adopting checked replacement IDs; POSIX explicit directory deletion fails closed before deleting entries. Windows private-only empty directory removal remains supported. Nested or nonprivate container state is retained for owner cleanup.

Verification: the five focused lifecycle/runtime/storage suites passed 59 tests with two POSIX-only skips. Two remediation tests failed before the fixes. Initial implementation RED evidence was not retained. Journal recovery has native regression evidence, not a new real process-kill recovery run. The combined gate passed 97 maintained controller files; all modified production code satisfies 400/300/50 caps. Runtime logic now lives in maintained pipeline modules, with thin compatibility entry points under tests.

Raw commands, image IDs, template hashes, cleanup evidence and independent review remain under D:/BuildArtifacts/QOpenBB/compose-lifecycle. No provider calls, financial browser acceptance or Linux execution are claimed. Task 12 owns Linux compatibility; the runtime session is stopped and its state retained.
