$ErrorActionPreference='Stop'
$out='artifacts/consuming-contract-freeze/session'
$ledger=Get-Content -Raw "$out/editor-field-ledger.json"|ConvertFrom-Json
$paths=@($ledger.rows.references.path)+@(
 '.kiro/steering/complexity.md','.kiro/steering/documentation.md','.kiro/steering/delegation.md',
 '.kiro/steering/testing.md','.kiro/steering/ci.md',
 '.agents/skills/kiro-spec-design/rules/design-principles.md',
 '.kiro/specs/openbb-self-service/chart-consuming-integration-readiness.md',
 '.kiro/specs/openbb-self-service/chart-application-integration-design.md',
 '.kiro/specs/openbb-self-service/chart-appearance-editor-integration-design.md',
 '.kiro/specs/openbb-self-service/chart-editor-contract-close.md',
 'vendor/workspace/terminalpro/src/components/General/Table/Chart/application/types.ts',
 'vendor/workspace/terminalpro/src/components/General/Table/Chart/application/sessionState.ts',
 'vendor/workspace/terminalpro/src/components/General/Table/Chart/application/financialFormatting.ts',
 'vendor/workspace/terminalpro/src/components/General/Table/Chart/application/gridCapture.ts',
 'vendor/workspace/terminalpro/src/components/General/Table/Chart/compatibility/snapshotTypes.ts',
 'vendor/workspace/terminalpro/src/components/General/Table/Chart/echarts/cartesian.ts',
 'vendor/workspace/terminalpro/src/components/General/Table/Chart/themes.tsx',
 'vendor/workspace/terminalpro/src/components/General/Table/Chart/echarts/lifecycle.ts',
 'vendor/workspace/terminalpro/src/components/General/Table/Chart/echarts/EChartsHost.tsx',
 'vendor/workspace/terminalpro/src/components/Widget.hooks.tsx',
 "$out/draft.md","$out/editor-field-ledger.json","$out/generate-ledger.ps1","$out/freeze-inputs.ps1","$out/mechanical-check.json"
)|Sort-Object -Unique
$files=@(foreach($p in $paths){[ordered]@{path=$p;sha256=(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant();bytes=(Get-Item -LiteralPath $p).Length;class=$(if($p.StartsWith($out)){'draft-output-pending-controller-review'}elseif($p.StartsWith('artifacts/reviewed/')){'existing-selected-reviewed-evidence'}else{'source-contract-input'})}})
$original='38dffc33389aca0e4a87e0e88d42f7067aa220df'
$originalPaths=@('terminalpro/src/components/General/Table/Chart/hooks/useChartOptions.tsx','terminalpro/src/components/General/Table/Chart/AgChartView.tsx','terminalpro/src/components/General/Table/hooks/useTableContext.tsx','terminalpro/src/components/General/Table/hooks/useUpdateColumnState.ts')
$gitInputs=@(foreach($p in $originalPaths){
 $start=[Diagnostics.ProcessStartInfo]::new();$start.FileName='git';$start.WorkingDirectory=(Resolve-Path vendor/workspace).Path;$start.UseShellExecute=$false;$start.CreateNoWindow=$true;$start.RedirectStandardOutput=$true;$start.StandardOutputEncoding=[Text.UTF8Encoding]::new($false)
 $start.ArgumentList.Add('show');$start.ArgumentList.Add($original+':'+$p)
 $process=[Diagnostics.Process]::Start($start);$content=$process.StandardOutput.ReadToEnd();$process.WaitForExit();if($process.ExitCode -ne 0){throw 'Original source read failed'}
 $sha=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData([Text.UTF8Encoding]::new($false).GetBytes($content))).ToLowerInvariant()
 $blob=git -C vendor/workspace rev-parse ($original+':'+$p)
 [ordered]@{repository='vendor/workspace';revision=$original;path=$p;gitBlob=$blob;sha256=$sha;method='git show UTF-8 text retaining original line endings'}
})
$manifest=[ordered]@{status='explicit-safe-input-and-draft-output-allowlist; controller review required before publication';scope=$out;files=$files;originalGitInputs=$gitInputs;excluded=@('Environment/credential/private account/database/runtime files','Unlisted artifact trees, raw diagnostics/request bodies and authentication traces','Production edits, root/spec edits, browser/network/build/install/suite output')}
$errors=[System.Collections.Generic.List[string]]::new()
foreach($r in $ledger.rows){foreach($ref in $r.references){if(-not(Test-Path -LiteralPath $ref.path)){$errors.Add('missing '+$ref.path)}elseif((Get-FileHash -LiteralPath $ref.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $ref.sha256){$errors.Add('hash mismatch '+$ref.path)}}}
$supported=@($ledger.rows|Where-Object {$_.id -like 'supported-*'})
if($supported.Count -ne 5){$errors.Add('Expected five supported commands')}
foreach($kind in @('title-text','title-enabled','legend-position','stroke-width','tooltip-mode')){if('supported-'+$kind -notin $supported.id){$errors.Add('Missing '+$kind)}}
$runtimeRows=@($ledger.rows|Where-Object {$_.id -like 'runtime-*'}).Count
$inventoryRows=@($ledger.rows|Where-Object {$_.id -like 'inventory-*'}).Count
if($runtimeRows -ne 202 -or $inventoryRows -ne 88 -or $ledger.rows.Count -ne 295){$errors.Add('Row composition must be 202 runtime + 88 inventory + 5 supported = 295 total')}
$draft=Get-Content -Raw "$out/draft.md"
$explicitFill=$draft.Contains('readonly chartBarFillEnabled: boolean;')
$explicitSourceKey=$draft.Contains('sourceKey = column.id')
if(-not $explicitFill -or -not $explicitSourceKey){$errors.Add('Missing explicit bar-fill input or ordinary source-key binding rule')}
$check=[ordered]@{status=$(if($errors.Count){'FAIL'}else{'PASS'});scope='Mechanical JSON/reference/hash and five-command inventory only; no compilation/runtime/visual/persistence claim';totalRows=$ledger.rows.Count;runtimeCaptureRows=$runtimeRows;inventoryCaptureRows=$inventoryRows;finiteCaptureRows=($runtimeRows+$inventoryRows);unknownQueries=$ledger.unresolved.Count;supportedCommands=$supported.Count;explicitBarFillInput=$explicitFill;explicitOrdinarySourceKeyRule=$explicitSourceKey;hashedFiles=$files.Count;originalGitInputs=$gitInputs.Count;errors=$errors}
$check|ConvertTo-Json -Depth 8|Set-Content -LiteralPath "$out/mechanical-check.json" -Encoding utf8
$checkEntry=$manifest.files|Where-Object path -EQ "$out/mechanical-check.json"
$checkEntry.sha256=(Get-FileHash -LiteralPath "$out/mechanical-check.json" -Algorithm SHA256).Hash.ToLowerInvariant()
$checkEntry.bytes=(Get-Item -LiteralPath "$out/mechanical-check.json").Length
$manifest|ConvertTo-Json -Depth 10|Set-Content -LiteralPath "$out/safe-hash-allowlist.json" -Encoding utf8
$check|ConvertTo-Json -Compress -Depth 4
if($errors.Count){exit 1}
