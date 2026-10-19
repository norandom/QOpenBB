# Published development alpha

2026-10-19. Root source: `2d7b0bb7224f45cf5c41b741f7a6ebfc29811e1d`.

- GitHub workflow [39237590906](https://github.com/norandom/QOpenBB/actions/runs/39237590906) succeeded: 134 focused checks, maintained-scope quality check, both Dagger builds and alpha publication.
- The hosted engine report confirms the classic Docker configuration ID differs from the pinned registry manifest digest. The corrected check verifies the pinned repository digest and resolved local identity separately.
- [alpha-39237590906-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-39237590906-1) is a tagged prerelease with Compose, environment template and manifest assets. GitHub names the environment asset `default.env.sample`; installation saves it as `.env.sample`.
- Both public `latest` images were pulled in WSL using a temporary empty Docker credential directory. Their registry digests match the attached release manifest.
- Independent Sol review found no blocking pipeline issues; focused local delivery checks passed 98 tests. The alpha publisher separately passed 34 tests including immutable/latest identity failure cases.
- The README delivery plan is a standalone SVG, rendered and visually checked in isolated Chromium.

This verifies image build, publication and anonymous pull, not a new application runtime. Browser, live-data and assembled Compose acceptance remain open. No service was started for this check. Updating the pair of latest tags is not atomic; exact alpha image pairs remain recorded in the release manifest.
