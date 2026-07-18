<#
.SYNOPSIS
  Installs C:\backup.ps1 and registers a weekly Sunday 03:00 Scheduled Task.

.DESCRIPTION
  Run once elevated (Administrator) on the Windows PC.

  Copies this folder's backup.ps1 to C:\backup.ps1 (or uses -SourceScript),
  ensures C:\Backups exists, and registers task "OpenClaw Server Backup".

.PARAMETER SourceScript
  Path to backup.ps1 to install (default: backup.ps1 next to this script).

.PARAMETER TaskName
  Scheduled Task name (default: OpenClaw Server Backup).

.PARAMETER SshUser
  Passed through to backup.ps1 via the task action (default: root).
#>
[CmdletBinding()]
param(
    [string]$SourceScript = (Join-Path $PSScriptRoot "backup.ps1"),
    [string]$TaskName = "OpenClaw Server Backup",
    [string]$SshUser = "root",
    [string]$InstallPath = "C:\backup.ps1",
    [string]$BackupRoot = "C:\Backups"
)

$ErrorActionPreference = "Stop"

$principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    throw "Run this script as Administrator (elevated PowerShell)."
}

if (-not (Test-Path -LiteralPath $SourceScript)) {
    throw "Source script not found: $SourceScript"
}

$drive = Split-Path -Qualifier $InstallPath
if (-not (Test-Path -LiteralPath $drive)) {
    throw "Drive $drive is not available on this machine."
}

New-Item -ItemType Directory -Force -Path $BackupRoot | Out-Null
Copy-Item -LiteralPath $SourceScript -Destination $InstallPath -Force
Write-Host "Installed: $InstallPath"

$ssh = Get-Command ssh -ErrorAction SilentlyContinue
if (-not $ssh) {
    Write-Warning "OpenSSH Client not found. Install before the first scheduled run:"
    Write-Warning "  Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0"
}

$psExe = Join-Path $env:SystemRoot "System32\WindowsPowerShell\v1.0\powershell.exe"
$arg = "-NoProfile -ExecutionPolicy Bypass -File `"$InstallPath`" -SshUser `"$SshUser`" -BackupRoot `"$BackupRoot`""

$action = New-ScheduledTaskAction -Execute $psExe -Argument $arg
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 3:00AM
$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Hours 6)

# Run whether user is logged on or not requires a stored password in interactive Register-ScheduledTask.
# InteractiveToken works when the installing user is logged on; StartWhenAvailable catches missed runs.
$taskPrincipal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType Interactive `
    -RunLevel Highest

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $taskPrincipal `
    -Description "Weekly SSH stream backup of /home/openclaw from 194.156.117.210 to C:\Backups" `
    -Force | Out-Null

Write-Host "Scheduled task registered: '$TaskName'"
Write-Host "  Trigger: every Sunday at 03:00"
Write-Host "  Action:  $psExe $arg"
Write-Host ""
Write-Host "Prerequisites for non-interactive SSH:"
Write-Host "  1. OpenSSH Client installed"
Write-Host "  2. Key-based auth for $SshUser@194.156.117.210 (BatchMode=yes)"
Write-Host "  3. Test once: powershell -File $InstallPath"
Write-Host ""
Get-ScheduledTask -TaskName $TaskName | Format-List TaskName, State, Description
Get-ScheduledTaskInfo -TaskName $TaskName | Format-List LastRunTime, NextRunTime, LastTaskResult
