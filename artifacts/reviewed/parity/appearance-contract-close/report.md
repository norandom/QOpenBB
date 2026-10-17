# Close derived colors; keep saved-state composition open

The bounded reference experiment establishes source-backed opaque-hex grid/subtitle derivation and bar/common/position conflict outcomes. It does not close the complete B2 application resolver: no saved model was injected, no line conflict was captured, and public proxy updates bypass the owned hook that replaces saved common. Do not promote these results to application activation or renderer acceptance.

Evidence dated 2026-10-17 uses original Workspace `38dffc33389aca0e4a87e0e88d42f7067aa220df`, image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`; candidate `76edf85a46298f7bc5212ff9944e4b66e9baa4af` was not run or modified. The synthetic observations are revenue/operating income in USD millions; null Q2 values remain missing. These are eight new discriminating cases, not the old eight stock/custom fixtures.

## What can be implemented after review

A small pure opaque-six-digit-hex color helper can derive the two missing tokens without renderer dependencies. Use supplied foreground/background and explicit text/chart-background tokens when present. For each 8-bit channel, preserve source operation order: `Math.round(clamp((fg/255)*(1-t)+(bg/255)*t,0,1)*255)`. Clamp occurs after interpolation. Do not use an algebraically equivalent byte-domain shortcut: floating-point rounding can differ. This is interpolation of encoded sRGB channels, without linear-light conversion. Grid t is computed literally as `1-.257` for ag-default-dark and `1-.1` for ag-default; subtitle t is .57/.38. Defaults are foreground #ffffff/#181d1f. Subtitle uses textColor/chartBackgroundColor aliases, which can differ from foregroundColor/backgroundColor. The helper must accept already resolved tokens, not guess arbitrary AG parameter graphs, alpha compositing, named/CSS colors, invalid colors or alternate bases.

[Normalized edge evidence](normalized-color-evidence.json) compares the installed MIT Color utility with the formula for all 65,536 red-channel pairs at each of four ratios (262,144 comparisons), with zero normalized mismatches. Foreground #000000/background #9b0000 at t=`1-.1` yields #8b0000; the rejected byte shortcut yields #8c0000. Byte shortcut mismatch counts are recorded, so these cases disprove that shortcut even though all eight captured colors happen to match it. Captured runtime cases are unchanged.

Matching installed `ag-charts-community` 12.1.1 is MIT licensed; original package.json also pins 12.1.1. [Source hashes](source-manifest.json) fix the installed bundle/license and original Git blobs. Bundle locations: default parameters 26227-26242; subtitle reference 26446-26453; dark parameters 26892-26903; foreground/background operation 33083-33094; mix operation 33142-33155; channel interpolation 1198 and 1558-1559; clamp constructor 1229 onward; output rounding 1376-1381. No dependency source was copied into production, and the application design still forbids copying AG's general resolver.

[44 independent offline assertions](assertions.json) check the above arithmetic against settled runtime leaves, conflict winners, case count and cleanup. Background-only dark gives grid #5e6c79/subtitle #838e98. Palette-only retains #515153/#7a7a7b. Light base plus background #edf3d7 gives #d8dec5/#696e65. Explicit foreground #123456 gives #21384d/#1d374f. The last case also supplies foregroundColorMuted and borderColor; their independent causal influence was not isolated. Supported public params are gridLineColor/subtleTextColor, not an invented foregroundColorMuted alias.

## Exact bounded collision observations

| Synthetic proxy input | Settled result |
| --- | --- |
| common and bar title/legend conflict | bar title FAMILY/#654321, legend right |
| common only title/legend | COMMON/#123456, bottom |
| number label and number.left label conflict | left #abcdef |
| common.series.fill #123456 | generated bar fill remains #5090dc |
| bar.series.fill #abcdef | bar fill #abcdef |
| palette-only first fill #d12378 | first series #d12378 |

The common-only series result disproves a universal common-over-palette assignment rule. These cases establish behavior for the original grouped bar options only. They do not prove line, stacked, palette exhaustion/reorder or all nested fields.

Owned `useChartOptions.tsx:406-434` separately replaces `chartOptions.common` with generated common, then lodash-merges generated options and saved branches. Therefore the public-proxy common-only case is not evidence that a stored common title survives that hook. The next saved-state capture must provide finite nonempty model options and record model/generated/effective under one action; then test generated common versus saved common and saved bar/line namespaces. Direct public updates are explicitly synthetic resolution, with no UI reachability, save/reopen or backend persistence claim.

## Reproduction and limits

From the repository root:

```text
wsl -d Debian -u mc -- bash /mnt/d/Source/QOpenBB/artifacts/parity/appearance-contract-close/run.sh
wsl -d Debian -u mc -- bash /mnt/d/Source/QOpenBB/artifacts/parity/appearance-contract-close/source-evidence.sh
wsl -d Debian -u mc -- /mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node /mnt/d/Source/QOpenBB/artifacts/parity/appearance-contract-close/cleanup.mjs
wsl -d Debian -u mc -- bash -c 'cd /mnt/d/Source/QOpenBB && pipeline/.venv/bin/python artifacts/parity/appearance-contract-close/assert.py'
```

Successful startup, journey, source manifest, cleanup, normalized-color evidence and offline assertion commands exited 0. Run normalized-colors.mjs with the same pinned Node before assert.py; it uses the existing installed MIT utility without installation or a browser. The first journey failed with DataCloneError because trusted owned callbacks cannot be structured-cloned; [failure](initial-failure/failure.json) is retained. The corrected run shallow-copies the trusted original theme in memory and adds finite data-only overrides; it does not deserialize callbacks. The launcher uses a fresh container/state/account, pinned Node, existing Playwright only, owned headless browser and CDP Runtime/Network diagnostics. No install/build or desktop interaction ran. Cleanup checks the exact container name and removes only owned state/credential paths. Both attempts' state directories were removed.

Screenshots are postlogin synthetic reference-only observations. The light-base synthetic case deliberately leaves the dashboard dark; it is not integrated light-theme parity. Projection waits for waitForUpdate; screenshots are supporting context, not pixel equivalence. The preexisting HTML-as-JavaScript datafeed error and 404 remain in [sanitized diagnostics](diagnostics-public.json). No candidate browser, general editor, export, persistence or full renderer acceptance is claimed.

[Cases](cases.json) are a sanitized derivative of raw-cases.json: only finite inherited appearance leaves and finite theme parameters/palette/overrides remain; nested inherited theme objects/callback markers were removed. Runtime metadata, raw diagnostics, raw cases, credentials and database state are not publication candidates. The replay script now writes finite case inputs directly, so a new run can have a different JSON layout without changing the assertions.

The [frozen publication allowlist](publication-allowlist.json) names exact files and SHA-256 bytes. It excludes raw output, runtime/start logs, dependency caches, private state and account metadata. Controller review and publication remain required. Research files are excluded from production caps; any future helper/typed mapper task must retain inventory ownership and 400 physical/300 logical units per file, 50/function gates.
