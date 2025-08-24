import logging, numpy as np, time
from typing import Iterator, Optional
from .devices.file_source import FileIQSource
from .devices.rtlsdr_source import RTLSDRSource
from .devices.hackrf_source import HackRFSource
from .devices.rtl_tcp_source import RTLTCPSocketSource

log = logging.getLogger("spectrum.monitor")

class SpectrumMonitor:
    def __init__(self, device_type: str, center_freq: int, sample_rate: int, gain: str, host: str, iq_path: Optional[str]=None):
        self.device_type = device_type
        self.center_freq = center_freq
        self.sample_rate = sample_rate
        self.gain = gain
        self.host = host
        self.iq_path = iq_path
        self.dev = None

    def open(self):
        if self.device_type == "file":
            if not self.iq_path:
                raise ValueError("File device requires --iq path (numpy .npy of complex64 IQ)")
            self.dev = FileIQSource(self.iq_path)
        elif self.device_type == "rtlsdr":
            self.dev = RTLSDRSource(self.center_freq, self.sample_rate, self.gain)
        elif self.device_type == "hackrf":
            self.dev = HackRFSource(self.center_freq, self.sample_rate, self.gain)
        elif self.device_type == "rtl_tcp":
            self.dev = RTLTCPSocketSource(self.host, self.center_freq, self.sample_rate, self.gain)
        else:
            raise ValueError(f"Unknown device {self.device_type}")
        log.info("Opened device: %s", self.device_type)

    def blocks(self, block_size: int) -> Iterator[np.ndarray]:
        # prefer blocking read_blocks method
        rb = getattr(self.dev, "read_blocks")
        return rb(block_size)

    def close(self):
        if self.dev and hasattr(self.dev, "close"): self.dev.close()
