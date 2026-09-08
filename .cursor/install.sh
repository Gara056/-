#!/usr/bin/env bash
# Idempotent Cloud Agent bootstrap for this repository.
#
# The repo is a set of PowerShell scripts (backup.ps1, Install-BackupTask.ps1)
# plus a document. The development toolchain is:
#   - PowerShell Core (pwsh) to run / syntax-check the scripts
#   - PSScriptAnalyzer to lint them
#
# Safe to run repeatedly: every step checks for existing state before acting.
set -euo pipefail

SUDO=""
if [ "$(id -u)" -ne 0 ]; then
  if command -v sudo >/dev/null 2>&1; then
    SUDO="sudo"
  fi
fi

install_powershell() {
  if command -v pwsh >/dev/null 2>&1; then
    echo "pwsh already installed: $(pwsh --version)"
    return
  fi

  echo "Installing PowerShell Core..."
  # shellcheck disable=SC1091
  . /etc/os-release
  local deb="/tmp/packages-microsoft-prod.deb"
  wget -q "https://packages.microsoft.com/config/ubuntu/${VERSION_ID}/packages-microsoft-prod.deb" -O "$deb"
  $SUDO dpkg -i "$deb"
  $SUDO apt-get update -qq
  $SUDO DEBIAN_FRONTEND=noninteractive apt-get install -y -qq powershell
  rm -f "$deb"
  echo "Installed: $(pwsh --version)"
}

install_ps_modules() {
  echo "Ensuring PSScriptAnalyzer is available..."
  pwsh -NoProfile -Command '
    Set-PSRepository -Name PSGallery -InstallationPolicy Trusted
    if (-not (Get-Module -ListAvailable -Name PSScriptAnalyzer)) {
      Install-Module -Name PSScriptAnalyzer -Scope CurrentUser -Force -AcceptLicense
    }
    Get-Module -ListAvailable PSScriptAnalyzer | Select-Object Name, Version
  '
}

install_powershell
install_ps_modules
echo "Environment ready."
