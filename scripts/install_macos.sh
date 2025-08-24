#!/usr/bin/env bash
set -euo pipefail

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew required. Install from https://brew.sh"
  exit 1
fi

brew update
brew install python@3 rtl-sdr hackrf soapysdr

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .[dev] || true

echo "[+] Done. If HackRF/Soapy issues appear, re-plug device and check 'SoapySDRUtil --find'."
