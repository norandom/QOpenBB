[CmdletBinding()]
param(
    [Parameter(Mandatory)][ValidateSet('doctor','build','start','verify','recreate','stop')][string]$Action,
    [string]$Python,
    [string]$Artifacts = 'D:/BuildArtifacts/QOpenBB',
    [string]$ToolsFile = 'D:/BuildArtifacts/QOpenBB/native-foundation/resolved-tools.json',
    [string]$SessionPath,
    [string]$WorkspaceImage,
    [string]$DataImage,
    [ValidateSet('foundation','workspace','data-api')][string]$BuildSelection
)
$ErrorActionPreference = 'Stop'
$repository = Split-Path -Parent $PSScriptRoot
try {
    if (-not $Python) {
        $Python = (Get-Content -LiteralPath $ToolsFile -Raw | ConvertFrom-Json).python.path
    }
    $resolved = Get-Item -LiteralPath $Python
    if ($resolved.Extension -ne '.exe') { throw 'Python must be a real .exe' }
    $arguments = @('-B','-m','qopenbb_ci.native_environment','--action',$Action,'--repository',$repository,
                   '--artifacts',$Artifacts,'--tools-file',$ToolsFile)
    foreach ($pair in @(@('session-path',$SessionPath),@('workspace-image',$WorkspaceImage),
                       @('data-image',$DataImage),@('build-selection',$BuildSelection))) {
        if ($pair[1]) { $arguments += @('--' + $pair[0],$pair[1]) }
    }
    $previousPath = $env:PYTHONPATH
    $env:PYTHONPATH = Join-Path $repository 'pipeline'
    Push-Location -LiteralPath $repository
    try { & $resolved.FullName @arguments; $code = $LASTEXITCODE }
    finally { Pop-Location; $env:PYTHONPATH = $previousPath }
    exit $code
} catch {
    Write-Error ('Native entry failed: ' + $_.Exception.Message)
    exit 2
}
