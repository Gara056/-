<#
.SYNOPSIS
  Streams a remote tar.gz of /home/openclaw over SSH to D:\Backups.

.DESCRIPTION
  Connects to 194.156.117.210 via OpenSSH and writes:
    D:\Backups\server_<yyyy-MM-dd>.tar.gz

  Intended path on the PC: D:\backup.ps1
  Requires OpenSSH Client and key-based (non-interactive) SSH auth for scheduled runs.

.PARAMETER SshUser
  Remote SSH username (default: root).

.PARAMETER SshHost
  Remote host (default: 194.156.117.210).

.PARAMETER RemotePath
  Directory to archive on the server (default: /home/openclaw).

.PARAMETER BackupRoot
  Local folder for archives (default: D:\Backups).
#>
[CmdletBinding()]
param(
    [string]$SshUser = "root",
    [string]$SshHost = "194.156.117.210",
    [string]$RemotePath = "/home/openclaw",
    [string]$BackupRoot = "D:\Backups"
)

$ErrorActionPreference = "Stop"

$date = Get-Date -Format "yyyy-MM-dd"
$dest = Join-Path $BackupRoot "server_$date.tar.gz"
$logDir = Join-Path $BackupRoot "logs"
$logFile = Join-Path $logDir "backup_$date.log"

function Write-BackupLog {
    param([string]$Message)
    $line = "[{0}] {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Message
    Add-Content -Path $logFile -Value $line -Encoding UTF8
    Write-Host $line
}

New-Item -ItemType Directory -Force -Path $BackupRoot | Out-Null
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

$ssh = Get-Command ssh -ErrorAction SilentlyContinue
if (-not $ssh) {
    throw "OpenSSH Client (ssh) not found. Install it via: Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0"
}

# Parse Unix paths with string ops — Split-Path is Windows-oriented.
$normalized = $RemotePath.Trim().Replace('\', '/').TrimEnd('/')
if ([string]::IsNullOrWhiteSpace($normalized) -or $normalized -eq '/') {
    throw "RemotePath must be a directory under / (got: $RemotePath)"
}
$slash = $normalized.LastIndexOf('/')
$remoteParent = if ($slash -le 0) { "/" } else { $normalized.Substring(0, $slash) }
$remoteName = $normalized.Substring($slash + 1)

# Archive relative to parent so the tarball contains a single top-level folder (e.g. openclaw/).
$remoteCmd = "tar -czf - -C '$remoteParent' '$remoteName'"
$sshTarget = "{0}@{1}" -f $SshUser, $SshHost
$sshArgs = @(
    "-o", "BatchMode=yes",
    "-o", "StrictHostKeyChecking=accept-new",
    "-o", "ConnectTimeout=30",
    $sshTarget,
    $remoteCmd
)

Write-BackupLog "Starting backup: $sshTarget : $RemotePath -> $dest"

if (Test-Path -LiteralPath $dest) {
    Write-BackupLog "Existing archive will be overwritten: $dest"
    Remove-Item -LiteralPath $dest -Force
}

# Stream stdout as raw bytes (PowerShell redirection can corrupt binary archives).
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $ssh.Source
$psi.Arguments = ($sshArgs | ForEach-Object {
        if ($_ -match '\s') { '"{0}"' -f ($_ -replace '"', '\"') } else { $_ }
    }) -join ' '
$psi.UseShellExecute = $false
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.CreateNoWindow = $true

$proc = New-Object System.Diagnostics.Process
$proc.StartInfo = $psi

try {
    [void]$proc.Start()
    # Read stderr concurrently to avoid pipe deadlock while streaming stdout.
    $stderrTask = $proc.StandardError.ReadToEndAsync()
    $outStream = [System.IO.File]::Create($dest)
    try {
        $proc.StandardOutput.BaseStream.CopyTo($outStream)
    }
    finally {
        $outStream.Dispose()
    }
    $stderr = $stderrTask.Result
    $proc.WaitForExit()

    if (-not [string]::IsNullOrWhiteSpace($stderr)) {
        $stderrPath = Join-Path $logDir "ssh_stderr_$date.txt"
        Set-Content -Path $stderrPath -Value $stderr -Encoding UTF8
    }

    if ($proc.ExitCode -ne 0) {
        Write-BackupLog "FAILED (exit $($proc.ExitCode)). $stderr"
        if (Test-Path -LiteralPath $dest) {
            Remove-Item -LiteralPath $dest -Force -ErrorAction SilentlyContinue
        }
        exit $proc.ExitCode
    }
}
finally {
    if (-not $proc.HasExited) {
        try { $proc.Kill() } catch { }
    }
    $proc.Dispose()
}

$size = (Get-Item -LiteralPath $dest).Length
if ($size -lt 1) {
    Write-BackupLog "FAILED: archive is empty: $dest"
    Remove-Item -LiteralPath $dest -Force -ErrorAction SilentlyContinue
    exit 1
}

Write-BackupLog ("OK: {0} ({1:N0} bytes)" -f $dest, $size)
exit 0
