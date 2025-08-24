#!/usr/bin/env bash
set -euo pipefail

echo "[+] Installing system dependencies..."
if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y python3-venv python3-dev build-essential pkg-config \       rtl-sdr hackrf soapysdr-module-all libsoapysdr-dev
  # Udev rules for RTL-SDR
  sudo cp scripts/udev-rtl-sdr.rules /etc/udev/rules.d/20-rtl-sdr.rules || true
  sudo udevadm control --reload-rules || true
fi

python3 -m venv .venv
source .venv/bin/activate

echo "[+] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .[dev] || true

echo "[+] Done. Try: make run PROFILE=demo_indoor DEVICE=file IQ=tests/data/sample_burst.npy"
