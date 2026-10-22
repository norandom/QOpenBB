# Prerelease builds and CodeQL

The reviewed delivery change builds both images when a prerelease is published manually. Ordinary pushes remain checks-only. The tagged commit supplies the source pins; publication attaches the manifest and install assets to the existing release.

- [x] Independent source review: manual prerelease selection, tagged checkout, quoted release arguments, asset upload and serialized publication.
- [x] Portable `bash pipeline/ci.sh check`: exit 0, 145 tests passed, maintained-scope quality checks passed.
- [x] Actionlint passed all four changed workflows; shell syntax passed.
- [x] Independent CodeQL source review: root Python/JavaScript and both application forks, pinned actions, bounded analysis and security-event upload permissions.
- [x] Workspace hosted CodeQL passed both languages: [run 39836160955](https://github.com/norandom/openbb-workspace/actions/runs/39836160955).
- [ ] Confirm root and data API hosted scans finish successfully.
- [ ] Exercise a manually published prerelease through hosted image publication at the next accepted milestone.

No new release is claimed by these source checks. Range chart visual acceptance remains open; the published alpha is unchanged. CodeQL completion does not imply that all reported alerts are resolved.
