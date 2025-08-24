#!/usr/bin/env python3
"""Generate tiny placeholder IR/SubGHz assets for demo."""
import os, pathlib
root = pathlib.Path(__file__).resolve().parents[1] / "flipper" / "assets"
(root / "infrared").mkdir(parents=True, exist_ok=True)
(root / "subghz").mkdir(parents=True, exist_ok=True)
(root / "infrared" / "demo.ir").write_text("# IR demo payload (placeholder)\n")
(root / "subghz" / "demo.sub").write_text("# SubGHz demo payload (placeholder)\n")
print("[+] Wrote demo IR/SubGHz assets.")
