# PowerShell accepts .ps1 as the file entry point.
$ErrorActionPreference = 'Stop'
$implementation = [IO.File]::ReadAllText((Join-Path $PSScriptRoot 'setup.psh'))
& ([scriptblock]::Create($implementation)) -RepositoryRoot $PSScriptRoot
