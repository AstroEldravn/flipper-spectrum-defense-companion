from pydantic import BaseModel, Field
from typing import List, Optional, Literal

DeviceType = Literal["rtlsdr", "hackrf", "rtl_tcp", "file"]

class GPIOConfig(BaseModel):
    pin: int = 17
    pulse_ms: int = 250
    pattern: str = "single"

class UARTConfig(BaseModel):
    enabled: bool = False
    port: str = "/dev/serial0"
    baudrate: int = 115200

class AlertConfig(BaseModel):
    sinks: List[str] = ["log_event"]
    gpio: GPIOConfig = GPIOConfig()
    uart: UARTConfig = UARTConfig()

class DeviceConfig(BaseModel):
    type: DeviceType = "rtlsdr"
    center_freq: int = 868_300_000
    sample_rate: int = 2_048_000
    gain: str = "auto"
    host: str = "127.0.0.1:1234"

class Thresholds(BaseModel):
    energy_db: float = 6.0
    hysteresis_db: float = 3.0
    burst_min_windows: int = 3
    burst_repeat_within_s: float = 3.0
    sk_threshold: float = 4.0
    cusum_threshold: float = 5.0

class Windowing(BaseModel):
    size: int = 4096
    hop: int = 2048

class Config(BaseModel):
    device: DeviceConfig = DeviceConfig()
    detectors: dict = {"enabled": ["energy", "burst"]}
    thresholds: Thresholds = Thresholds()
    window: Windowing = Windowing()
    alert: AlertConfig = AlertConfig()
    logging: dict = {"config": "config/logging.yaml"}
