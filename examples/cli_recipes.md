# CLI Recipes

- rtl_tcp from SDR++:
  ```bash
  rtl_tcp -a 0.0.0.0 -p 1234
  make run PROFILE=field_patrol DEVICE=rtl_tcp HOST=127.0.0.1:1234 FREQ=433920000 SR=1024000
  ```

- File playback:
  ```bash
  make run PROFILE=demo_indoor DEVICE=file IQ=tests/data/sample_burst.npy
  ```
