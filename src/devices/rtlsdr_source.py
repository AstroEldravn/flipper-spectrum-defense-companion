import numpy as np
from typing import Iterator
try:
    from rtlsdr import RtlSdr
except Exception:  # pragma: no cover
    RtlSdr = None

class RTLSDRSource:
    def __init__(self, center_freq: int, sample_rate: int, gain: str = "auto"):
        if RtlSdr is None:
            raise RuntimeError("pyrtlsdr not available. Install or choose another device.")
        self.sdr = RtlSdr()
        self.sdr.sample_rate = sample_rate
        self.sdr.center_freq = center_freq
        if gain == "auto":
            self.sdr.gain = 'auto'
        else:
            self.sdr.gain = float(gain)

    def stream(self, read_size: int) -> Iterator[np.ndarray]:
        for iq in self.sdr.read_samples_async(num_samples=read_size):
            yield iq.astype(np.complex64)

    def read_blocks(self, read_size: int) -> Iterator[np.ndarray]:
        while True:
            data = self.sdr.read_samples(read_size)
            yield data.astype(np.complex64)

    def close(self):
        try:
            self.sdr.close()
        except Exception:
            pass
