import time, logging
from typing import Any
log = logging.getLogger("spectrum.alerts.flipper_gpio")

try:
    from gpiozero import OutputDevice
except Exception:  # pragma: no cover
    OutputDevice = None

def _pattern_to_blinks(pattern: str):
    if pattern == "triple":
        return [0.1,0.1,0.1]
    if pattern == "double":
        return [0.15,0.15]
    return [0.2]

def emit(event, cfg: dict):
    gpio_cfg = cfg.get("alert", {}).get("gpio", {})
    pin = int(gpio_cfg.get("pin", 17))
    pattern = gpio_cfg.get("pattern", "single")
    pulse_ms = int(gpio_cfg.get("pulse_ms", 250))
    if OutputDevice is None:
        log.warning("gpiozero not available; would pulse pin %s (%s)", pin, pattern)
        return
    dev = OutputDevice(pin, active_high=True, initial_value=False)
    try:
        for d in _pattern_to_blinks(pattern):
            dev.on()
            time.sleep(d)
            dev.off()
            time.sleep(0.08)
        # Ensure a final pulse for external latch devices
        dev.on(); time.sleep(pulse_ms/1000.0); dev.off()
    finally:
        dev.close()
