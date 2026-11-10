# Native Compose endpoint correction

The shared native environment now gives Docker Compose the local Docker-compatible pipe belonging to the explicitly selected Podman machine. Podman's SSH endpoint remains unchanged for Podman commands. Selection is checked against registered machine identity, user/socket, port, key path and running/rootful facts; an unmapped or ambiguous connection fails closed.

Real task-5 startup exposed the mismatch: Docker Compose treated Podman's SSH endpoint as Docker SSH transport and attempted `docker system dial-stdio` inside the VM. No application resources were created by those failed attempts. The correction changes child-process configuration only; no VM or global configuration was modified.

On 2026-11-10, 28 focused native checks passed with one POSIX-only skip. Independent Astra review reproduced those checks and a real read-only Compose handshake. Doctor now verifies actual provider access rather than only its version. The combined size gate passed for 88 controller files with no errors or violations. Docker context behavior is preserved.

Raw RED/GREEN, doctor, combined-gate and review records remain under `D:/BuildArtifacts/QOpenBB/native-endpoint`, including `review.md`. This fixes the upstream connection contract so task 5 can resume; it does not establish application startup, bind mapping or browser acceptance.
