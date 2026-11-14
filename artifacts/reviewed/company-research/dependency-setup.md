# Company Research dependency setup

2026-11-14. The isolated Workspace dependencies are installed through pinned Safe Chain1.5.25 and Bun1.4.3 using the existing frozen lock. The existing company-selection suite passed all89 tests in one file with one worker. No feature source, package.json, bun.lock, task1 inventory or task1 evidence changed.

## Reuse

Working directory: D:/BuildArtifacts/QOpenBB/company-research/workspace/terminalpro.

Exact focused command, executed with Node24.22.1 and exit0:

```powershell
Set-Location D:/BuildArtifacts/QOpenBB/company-research/workspace/terminalpro
& 'C:/Program Files/nodejs/node.exe' node_modules/vitest/vitest.mjs run tests/unit/company-selection.test.ts --maxWorkers=1
```

External TEMP/TMP/TMPDIR remain D:/BuildArtifacts/Temp. BUN_INSTALL_CACHE_DIR remains D:/BuildArtifacts/bun; npm_config_cache remains D:/BuildArtifacts/npm. No new harness or browser was started. run-selector-tests.py captures output through a hidden child with180-second bound. company-selection-tests.log and company-selection-tests.json retain actual output and invocation. An initial invocation rejected --minWorkers (unsupported by installed Vitest4.1.11) before tests; company-selection-tests-invocation-error.log preserves it. The command above corrects that argument and passed89/89 in7.48s.

Installed actual versions: zod4.4.3, dayjs1.11.13, react-hook-form7.75.0, Vitest4.1.11. dependency-install.json records those versions and equal before/after SHA256 hashes for package.json and bun.lock. The dependency tree belongs exclusively to this isolated accepted Workspace snapshot.

## Acquisition and protection

The shell bun function calls Invoke-WrappedCommand, whose global Safe Chain selection is version1.5.15. Native PATH had no bun.exe; C:/Users/mariu/.bun/bin/bun.exe reports1.4.4. Those global tools were not used for installation. The required native Bun1.4.3 was provisioned under tools/bun/bun-windows-x64/bun.exe.

Official acquisition source: https://github.com/oven-sh/bun/releases/tag/bun-v1.4.3. The release API asset digest and official SHASUMS256.txt both identify bun-windows-x64.zip SHA2560bf84e808552beea67bf1202a287a35c6c825d837b287b3f8e9dd513dba35d3d; downloaded bytes matched both. The SHASUMS file itself matched release API SHA256861ce0f19aa4f8a94bef81045c7fcad38dbb2343f2c6e2d6bdc8561be5dba637. Retained archive, checksum text and extracted executable are beneath tools/. dependency-tool-hashes.json records their hashes and the pinned protection executable hash. Native Bun reports1.4.3.

Install command, executed hidden from the relevant frontend repository with600-second bound:

```powershell
$env:PATH = 'D:/BuildArtifacts/QOpenBB/company-research/tools/bun/bun-windows-x64;' + $env:PATH
& D:/BuildArtifacts/QOpenBB/native-foundation/protection/bin/safe-chain.exe bun install --frozen-lockfile
```

The explicit protection executable reports1.5.25 and matches accepted native tool SHA256158a126fe2920b066e000820f614462838914f5cc314508e4ae736ae4a0abfd7. The shell's ambiguous wrapper was bypassed by invoking the accepted protector explicitly, with pinned Bun first on child PATH. install-dependencies.py preserves the child command, external environment, timeout, before/after source hashes and package versions. dependency-install.log reports2048 packages installed in196.46s; exit0. Existing native foundation protection-js.log retains the accepted malicious-package blocking probe; no malware download probe was repeated in this setup.

No matched installed application dependency tree was available for reuse at accepted native-join/workspace or native-foundation/workspace, so protected frozen installation was necessary. No lock or dependency-pin migration occurred. git status remains clean for the isolated Workspace fork. Root verification dependencies remain separate. Task2 can now use the installed application libraries and focused existing test entry point directly.
