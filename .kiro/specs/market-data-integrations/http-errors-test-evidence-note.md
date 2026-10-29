# Task 4.3 test-evidence exception

The controller accepts one verification substitution for task 4.3 under the owner's prototype-first delivery workflow. This is a process exception, not a claim of owner approval for a new requirement or of historical behavioral RED.

The tests were authored before implementation, but initial collection failed because the existing environment lacks httpx. Implementation proceeded before the direct-ASGI tests ran. That chronology cannot be repaired retroactively. The implementation was not hidden or rolled back to manufacture a historical failure.

Acceptance still requires independent review, the full affected passing suite, native mounted-route and secret-canary checks, lint and size gates. In addition, an independent reviewer must observe an isolated post-implementation negative control: disabling the installer in memory must make the mounted failure regression fail; the unmodified implementation must pass. Record both actual child return codes and verify source hashes remain unchanged. Label this sensitivity evidence, not historical TDD.

This narrowly substitutes evidence for the missing RED receipt. Functional, security, compatibility and scope findings remain blocking. No runtime feature flag, dependency installation or production bypass is authorized. The approved requirements, design and task boundary remain unchanged.
