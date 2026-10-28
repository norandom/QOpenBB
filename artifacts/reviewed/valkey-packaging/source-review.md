# Embedded Valkey source review

## Final combined audit

APPROVED at Workspace `dfda735c527663dd7ecc2f80af18e25843f575af`. Independent read-only audit confirms both production hashes below, unchanged accepted Python metadata/lock, and complete six-path combined scope. Retained final complexity evidence measures 76 files with zero errors/violations, including Dockerfile 188, Supervisor 40, metadata 138 and inventory 399 physical lines. The approved final inventory proposal SHA256 is `28b2f1aad8a60476aea15482b5efcf6049f937f9ca118f2e4219247f2460de98`. Controller adoption and candidate build may proceed; no repeated checks or runtime acceptance are implied.

VERDICT: APPROVED for the bounded source change relative to Workspace `dbd3d5c6a66cbc9bbf4faf7f635b0fadd8361cc3`. Combined scope checks, image build and runtime acceptance remain separate gates.

The independent reviewer read the VK1-VK4 contract, exact two-file fork diff, focused regression, retained RED/GREEN evidence, archive evidence, dynamic-library records and Dagger remote-asset translator. No network, installation, build, runtime or repeated test suite was used.

## Findings

No blocking findings. The recipe replaces the installed Redis server package with checksum-pinned Valkey 9.0.7 Jammy x86_64 binaries and adds `libssl3` and `libsystemd0`. The retained ELF requirements identify libc/libm, OpenSSL 3 and systemd; actual library resolution still needs image verification. The Debian base is unchanged and the current supported target remains Linux/amd64.

The downloaded archive independently hashes to `bf0f19982dd464ea111617608a90f1a6eaad2c9c59b2e289cbc1591129f6d2e4`, matching the contract and Dockerfile. Exact server, CLI and license archive paths are present in retained member evidence. The full license is installed at `/usr/local/share/licenses/valkey/LICENSE` after the earlier documentation cleanup, so that cleanup does not remove it. Extraction cleanup names only the fixed temporary archive and extracted directory.

The pinned ADD line matches the existing Dagger translator's supported checksum/HTTPS/absolute-target grammar. Dagger translates it to a checksum-verified fetched asset and local COPY; no additional build helper is required.

Supervisor changes only the command executable to `/usr/local/bin/valkey-server`. The process identifier, application user, priority, restart behavior, localhost binding, port 6379, `/data/redis` path and `--save 60 1` remain intact. Redis client dependencies, REDIS settings, entrypoint and the two-service Compose topology are unchanged. No extra public port is introduced. The previously accepted uv/Python-source changes remain present.

## Verification evidence

- `implementation/red.log`: the new regression fails on the previous recipe's missing pinned Valkey ADD.
- `implementation/green.log`: all four focused packaging checks pass in 0.80 seconds.
- `implementation/source.json`: archive/license checks and unchanged Supervisor options pass. Dockerfile is 188 physical lines and Supervisor configuration 40, both below the 400-line cap; logical/function caps do not apply to these formats.
- Independent source/archive hashes agree with the retained record. No new placeholders or credentials are introduced by the bounded diff.

Reviewed production SHA256:

- `lite/Dockerfile`: `558939da401085cfd6802f4f2fc81d5477fb24a90bdcff0087bc73a3125a31dc`
- `lite/supervisord.conf`: `3f547c1e749221b09622549a965d00ed9e37eeca647d699077a70dfbecce348f`

## Acceptance boundary

Commit and combined-source checking may proceed. Before image acceptance, verify actual Valkey version and dynamic libraries, absence of the Redis server package, retained Python source module origins, representative redis-py and queue operations, application login, data after recreation, and loading a synthetic snapshot produced by the deployed Redis version. Source evidence does not establish RDB compatibility or application behavior; no claim extends to arbitrary Redis modules or Redis CE 7.4+ persistence.
