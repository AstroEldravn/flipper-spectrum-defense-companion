# Requires Administrator PowerShell
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "[+] Installing dependencies..."
if (Get-Command choco -ErrorAction SilentlyContinue) {
  choco install -y python git
} elseif (Get-Command scoop -ErrorAction SilentlyContinue) {
  scoop install python git
} else {
  Write-Host "Install Chocolatey (https://chocolatey.org) or Scoop (https://scoop.sh) first."
}

# Python venv + deps
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .[dev]

Write-Host "[!] For RTL-SDR on Windows, use Zadig to bind WinUSB to the dongle (RTL2832U)."
Write-Host "[+] Done."
