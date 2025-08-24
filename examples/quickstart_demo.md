# Quickstart Demo

This 5‑minute walkthrough runs the watchdog against a sample IQ file (no hardware), then with RTL‑SDR.

```bash
make install
make run PROFILE=demo_indoor DEVICE=file IQ=tests/data/sample_burst.npy

# With RTL‑SDR @ 868.3 MHz
make run PROFILE=field_patrol DEVICE=rtlsdr FREQ=868300000 SR=2048000
```
