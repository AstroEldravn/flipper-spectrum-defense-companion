import logging, time
from typing import Any
log = logging.getLogger("spectrum.alerts.flipper_uart")

try:
    import serial  # pyserial
except Exception:  # pragma: no cover
    serial = None

def emit(event, cfg: dict):
    uart_cfg = cfg.get("alert", {}).get("uart", {})
    if not uart_cfg.get("enabled", False):
        return
    if serial is None:
        log.warning("pyserial not available; cannot send UART alert.")
        return
    port = uart_cfg.get("port", "/dev/serial0")
    baud = int(uart_cfg.get("baudrate", 115200))
    msg = f"ALERT {event.severity} {event.message}\n"
    try:
        with serial.Serial(port, baud, timeout=0.5) as ser:
            ser.write(msg.encode("ascii"))
    except Exception as e:
        log.error("UART alert failed: %s", e)
