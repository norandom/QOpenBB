[CmdletBinding()]
param(
    [ValidateSet('start','status','restart','recreate','stop')][string]$Action = 'start',
    [Parameter(Mandatory)][string]$PrivatePath,
    [string]$Image,
    [string]$DataImage,
    [ValidateRange(1,65535)][int]$Port = 55551,
    [string]$Python = 'D:/BuildArtifacts/QOpenBB/native-foundation/pipeline-venv/Scripts/python.exe',
    [switch]$RemoveState
)
$ErrorActionPreference = 'Stop'
$repository = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$arguments = @('-B',(Join-Path $PSScriptRoot 'workspace_runtime.py'),$Action,'--private',$PrivatePath)
if ($Action -eq 'start') {
    $arguments += @('--image',$Image,'--data-image',$DataImage,'--image-only','--public-origin',"http://127.0.0.1:$Port")
}
if ($RemoveState) { $arguments += '--remove-state' }
$previousPath = $env:PYTHONPATH
$env:PYTHONPATH = Join-Path $repository 'pipeline'
Push-Location -LiteralPath $repository
try { & $Python @arguments; $code = $LASTEXITCODE }
finally { Pop-Location; $env:PYTHONPATH = $previousPath }
exit $code
