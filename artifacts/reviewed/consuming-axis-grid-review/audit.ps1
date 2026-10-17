$ErrorActionPreference = 'Stop'
$capture = 'artifacts/consuming-axis-grid-capture'
$review = 'artifacts/consuming-axis-grid-review'
$checks = [System.Collections.Generic.List[string]]::new()
function Check([string]$name, [bool]$passed) {
  if (-not $passed) { throw "Independent audit failed: $name" }
  $checks.Add($name)
}
function ReadCapture([string]$name) {
  Get-Content -LiteralPath "$capture/$name.json" -Raw | ConvertFrom-Json
}
function SameJson($left, $right) {
  (ConvertTo-Json -InputObject $left -Depth 60 -Compress) -ceq
    (ConvertTo-Json -InputObject $right -Depth 60 -Compress)
}
$manifest = ReadCapture 'publication-allowlist'
Check '51 explicitly selected capture files' ($manifest.files.Count -eq 51)
foreach ($entry in $manifest.files) {
  Check "safe path $($entry.path)" (
    $entry.sourcePath -ceq "$capture/$($entry.path)" -and
    $entry.path -notmatch '(^/|\.\.|credential|runtime-private|state-|\.log$|(^|/)diagnostics\.json$)')
  $hash = (Get-FileHash -LiteralPath $entry.sourcePath -Algorithm SHA256).Hash.ToLowerInvariant()
  Check "publication hash $($entry.path)" ($hash -ceq $entry.sha256)
  if ($entry.path -notlike '*.png') {
    $content = Get-Content -LiteralPath $entry.sourcePath -Raw
    Check "no generated credential/token value $($entry.path)" (
      $content -notmatch 'Aa1![0-9a-f]{48}' -and
      $content -notmatch '"(?:access_token|refresh_token|id_token)"\s*:')
  }
}
$names = @('baseline','ui-axis-thickness-3','ui-grid-thickness-4','ui-grid-dash-5',
  'synthetic-width-3-style-1','synthetic-width-1-style-4','synthetic-opacity-quarter','synthetic-opacity-one')
$cases = @{}
foreach ($name in $names) {
  $value = ReadCapture $name
  $cases[$name] = $value
  $live = $value.state.live | Where-Object position -EQ left
  Check "$name animation inactive" ($value.state.settled.animationActive -eq $false)
  Check "$name five measured grid lines" ($live.gridNodes.Count -eq 5)
}
$baseline = $cases['baseline']
foreach ($axis in $baseline.state.effective.axes) {
  Check "$($axis.position) stroke rather than color" (
    $axis.line.stroke -ceq '#c1c1c2' -and $axis.line.presence.color.kind -ceq 'absent')
}
$baselineLeft = $baseline.state.live | Where-Object position -EQ left
Check 'disabled baseline line has zero scene width despite visible flag' (
  $baselineLeft.lineNode.visible -eq $true -and $baselineLeft.lineNode.strokeWidth -eq 0)
$ledger = ReadCapture 'action-ledger'
Check 'seven action records' ($ledger.Count -eq 7)
foreach ($entry in $ledger) {
  Check "ledger matches captured state $($entry.name)" (SameJson $entry.after $cases[$entry.name].state)
}
foreach ($position in @('left','right')) {
  $line = $cases['ui-axis-thickness-3'].state.model.chartOptions.bar.axes.number.$position.line
  Check "$position UI axis patch" ($line.enabled -eq $true -and $line.width -eq 3)
  $grid = $cases['ui-grid-thickness-4'].state.model.chartOptions.bar.axes.number.$position.gridLine
  Check "$position UI grid width patch" ($grid.width -eq 4)
  $dash = $cases['ui-grid-dash-5'].state.model.chartOptions.bar.axes.number.$position.gridLine.style[0]
  Check "$position UI dash patch" ($dash.stroke -ceq '#515153' -and (SameJson $dash.lineDash @(5)))
}
$expectedWidths = @(1,1,4,4,1,4,4,4)
for ($i=0; $i -lt $names.Count; $i++) {
  $name=$names[$i]; $value=$cases[$name]
  $live = $value.state.live | Where-Object position -EQ left
  Check "$name all scene widths" (@($live.gridNodes | Where-Object {$_.node.strokeWidth -ne $expectedWidths[$i]}).Count -eq 0)
  if ($i -gt 3) {
    Check "$name explicitly synthetic" ($value.kind -ceq 'synthetic-reference-public-update-no-ui-proof')
    Check "$name preserves UI event history" (
      SameJson $value.state.events $cases['ui-grid-dash-5'].state.events)
    $modelGrid = $value.state.model.chartOptions.bar.axes.number.left.gridLine
    Check "$name model projection reflects synthetic override" (
      $modelGrid.width -eq $value.input.width -and
      $modelGrid.style[0].strokeWidth -eq $value.input.strokeWidth -and
      (SameJson $modelGrid.style[0].lineDash $value.input.lineDash))
    Check "$name all synthetic scene colors/dashes" (@($live.gridNodes | Where-Object {
      $_.node.stroke -cne '#123abc' -or -not (SameJson $_.node.lineDash @(2,7))}).Count -eq 0)
  }
}
foreach ($name in @('synthetic-opacity-quarter','synthetic-opacity-one')) {
  $axis = $cases[$name].state.effective.axes | Where-Object position -EQ left
  $live = $cases[$name].state.live | Where-Object position -EQ left
  Check "$name unsupported processed opacity" ($axis.gridLine.style[0].presence.strokeOpacity.kind -ceq 'absent')
  Check "$name scene opacity stays one" (@($live.gridNodes | Where-Object {
    $_.node.strokeOpacity -ne 1 -or $_.node.opacity -ne 1}).Count -eq 0)
}
Check 'opacity PNG byte hashes identical' (
  (Get-FileHash "$capture/synthetic-opacity-quarter.png").Hash -ceq
  (Get-FileHash "$capture/synthetic-opacity-one.png").Hash)
$diagnostic = ReadCapture 'diagnostic-summary'
Check 'unsupported opacity diagnostic retained' (@($diagnostic.chartWarnings | Where-Object {
  $_.text -match 'Unknown option.*gridLine.style\[0\].strokeOpacity'}).Count -eq 1)
Check 'diagnostics retain original errors' ($diagnostic.pageErrors.Count -eq 2 -and $diagnostic.cdpExceptions.Count -eq 2)
foreach ($attempt in @('','attempt1/')) {
  $cleanup = ReadCapture ($attempt+'cleanup-report')
  Check "$attempt cleanup receipt complete" ($cleanup.containerAbsent -eq $true -and
    $cleanup.stateAbsent -eq $true -and $cleanup.credentialAbsent -eq $true -and $cleanup.remainingOwnedState.Count -eq 0)
  Check "$attempt browser closed" ((ReadCapture ($attempt+'browser-cleanup')).closed -eq $true)
}
Check 'final run exited zero' ((ReadCapture 'run-status').exitCode -eq 0)
Check 'failed first run retained' ((ReadCapture 'attempt1/run-status').exitCode -eq 1)
$research = Get-Content artifacts/widget-transaction-design/safe-hash-allowlist.json -Raw | ConvertFrom-Json
foreach ($entry in $research.files) {
  Check "research input/output hash $($entry.path)" (
    (Get-FileHash -LiteralPath $entry.path -Algorithm SHA256).Hash.ToLowerInvariant() -ceq $entry.sha256)
}
[ordered]@{
  status='PASS';scope='Independent offline artifact audit; no runtime replay or implementation approval'
  checks=$checks.Count;passed=$checks;captureFiles=$manifest.files.Count
  researchFiles=$research.files.Count
  reviewerAuditCorrection='Initial check incorrectly expected synthetic model equality. Direct proxy updates change getChartModels projection while UI event history stays unchanged; corrected check asserts the recorded synthetic model values. This was an audit assumption failure, not a runtime retry.'
  captureManifestSha256=(Get-FileHash "$capture/publication-allowlist.json").Hash.ToLowerInvariant()
} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath "$review/verification.json" -Encoding utf8
"Independent offline checks passed: $($checks.Count)"
