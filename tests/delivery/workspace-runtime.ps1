<#
.SYNOPSIS
Controls a disposable, image-only Workspace runtime in WSL.
.DESCRIPTION
Delegates isolation, readiness, credential handling and cleanup to the existing
Python helper. PrivatePath must be on the Linux filesystem, which enforces 0600.
.EXAMPLE
./tests/delivery/workspace-runtime.ps1 -Action start -Image sha256:IMAGE_DIGEST `
    -PrivatePath /home/mc/qopenbb-work/box-candidate-ci-private.json -Port 55551
.EXAMPLE
./tests/delivery/workspace-runtime.ps1 -Action status `
    -PrivatePath /home/mc/qopenbb-work/box-candidate-ci-private.json
#>
[CmdletBinding()]
param(
    [ValidateSet('start', 'status', 'restart', 'stop')]
    [string] $Action = 'start',

    [Parameter(Mandatory)]
    [ValidatePattern('^/(?!mnt/)[^\r\n]+$')]
    [string] $PrivatePath,

    [string] $Image,

    [ValidateRange(1, 65535)]
    [int] $Port = 55551,

    [ValidateNotNullOrEmpty()]
    [string] $Distro = 'Debian',

    [ValidateNotNullOrEmpty()]
    [string] $LinuxUser = 'mc',

    [ValidatePattern('^/[^\r\n]+$')]
    [string] $Repository = '/mnt/d/Source/QOpenBB',

    [string] $Python
)

$ErrorActionPreference = 'Stop'
$Action = $Action.ToLowerInvariant()
if ($Action -eq 'start' -and [string]::IsNullOrWhiteSpace($Image)) {
    throw '-Image is required when -Action is start.'
}
if ([string]::IsNullOrWhiteSpace($Python)) {
    $Python = "$($Repository.TrimEnd('/'))/pipeline/.venv/bin/python"
}
$helper = "$($Repository.TrimEnd('/'))/tests/delivery/workspace_runtime.py"
$wslArguments = @(
    '-d', $Distro, '-u', $LinuxUser, '--', $Python, $helper,
    $Action, '--private', $PrivatePath
)
if ($Action -eq 'start') {
    $wslArguments += @(
        '--image', $Image, '--image-only',
        '--public-origin', "http://127.0.0.1:$Port"
    )
}

# Pass an argument array so paths remain literal; do not evaluate a shell string.
& wsl.exe @wslArguments
exit $LASTEXITCODE
