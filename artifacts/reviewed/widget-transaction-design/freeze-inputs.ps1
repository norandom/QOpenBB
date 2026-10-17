$ErrorActionPreference='Stop'
$out='artifacts/widget-transaction-design'
$inputs=@(
 'vendor/workspace/terminalpro/src/components/Widget.hooks.tsx',
 'vendor/workspace/terminalpro/src/components/Widget.context.tsx',
 'vendor/workspace/terminalpro/src/components/types.d.ts',
 'vendor/workspace/terminalpro/src/hooks/useRefHooks.tsx',
 'vendor/workspace/terminalpro/src/lib/utils/app.ts',
 'vendor/workspace/terminalpro/src/lib/utils/utils.ts',
 'vendor/workspace/terminalpro/src/lib/state/app.ts',
 'vendor/workspace/terminalpro/src/components/LayoutAuth/useSyncItems.tsx',
 '.kiro/steering/complexity.md','.kiro/steering/documentation.md','.kiro/steering/delegation.md'
)
$baselines=@(foreach($p in $inputs[0..2]){
 $text=[IO.File]::ReadAllText((Resolve-Path $p)) -replace '\r\n?',"`n"
 if($text.EndsWith("`n")){$text=$text.Substring(0,$text.Length-1)}
 [ordered]@{path=$p;physicalLines=$text.Split("`n").Length;logicalAndFunction='not measured'}
})
$setters=@(
 [ordered]@{id='preview';path=$inputs[0];line=110;scope='existing preview widget replacement'},
 [ordered]@{id='stale-time';path=$inputs[0];line=154;scope='existing defaulting'},
 [ordered]@{id='groups';path=$inputs[0];line=190;scope='group helper mutates input; query event in updater'},
 [ordered]@{id='inner-tab';path=$inputs[0];line=230;scope='subscription innerTab'},
 [ordered]@{id='public-updater';path=$inputs[0];line=259;scope='captured request mutation and enclosing store/context effects'},
 [ordered]@{id='refresh';path=$inputs[0];line=296;scope='timestamp and custom-event scheduling in updater'}
)
$audit=[ordered]@{status='source-only-design-research; not design approval or verified implementation';date='2026-10-17';candidate='ea02ec15956dee8d2c8a06825387a570757db12d';baselines=$baselines;setterPaths=$setters;preferredCandidate='Additive chart port and completion metadata in existing React widget owner; conditional on explicit fence/conflict/save joins';alternativeNotRequired='Whole-owner action reducer/outbox';unresolved=@('exact external data/theme/input fence publication ordering','same-field conflict classifier and interaction lifecycle','contextOverride batching semantics','saveWidgets/explicit save barrier and real backend readback');nonClaims=@('No arbitrary legacy callback purity or exactly-once execution guarantee','At-most-once invocation per mounted owner is not backend delivery','No completion API currently exists in the void updater','No frozen session artifacts changed','No production, runtime, suite, browser, build, install or network work')}
$audit|ConvertTo-Json -Depth 12|Set-Content -LiteralPath "$out/source-audit.json" -Encoding utf8
$draft=Get-Content -Raw "$out/draft.md"
$required=@('ChartWritePort','chart-only','same owner','six setter','at-most-once','not a freeze','explicit save','886','400 physical','300 logical','50/function')
$missing=@($required|Where-Object {-not $draft.Contains($_)})
$check=[ordered]@{status=$(if($missing.Count){'FAIL'}else{'PASS'});scope='Mechanical draft marker and source inventory check only; no runtime/TypeScript/behavior verification';setterPaths=$setters.Count;baselineCounts=$baselines;missingMarkers=$missing}
$check|ConvertTo-Json -Depth 10|Set-Content -LiteralPath "$out/mechanical-check.json" -Encoding utf8
$outputs=@("$out/draft.md","$out/source-audit.json","$out/mechanical-check.json","$out/freeze-inputs.ps1")
$files=@(foreach($p in ($inputs+$outputs)){
 [ordered]@{path=$p;sha256=(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant();bytes=(Get-Item -LiteralPath $p).Length;class=$(if($p.StartsWith($out)){'draft-output-pending-independent-review'}else{'read-only-source-input'})}
})
[ordered]@{status='explicit source and draft allowlist; controller/independent review pending';files=$files;excluded=@('Unlisted source/artifact trees','Environment/credential/private state/runtime files','Frozen session artifacts','Production/runtime/suite/browser/network outputs')}|ConvertTo-Json -Depth 10|Set-Content -LiteralPath "$out/safe-hash-allowlist.json" -Encoding utf8
$check|ConvertTo-Json -Compress -Depth 5
if($missing.Count){exit 1}
