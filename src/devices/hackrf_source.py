import numpy as np
from typing import Iterator

try:
    import SoapySDR  # type: ignore
    from SoapySDR import SOAPY_SDR_RX, SOAPY_SDR_CF32  # type: ignore
except Exception:  # pragma: no cover
    SoapySDR = None

class HackRFSource:
    def __init__(self, center_freq: int, sample_rate: int, gain: str = "auto"):
        if SoapySDR is None:
            raise RuntimeError("SoapySDR not available. Install soapysdr bindings.")
        args = dict(driver="hackrf")
        self.sdr = SoapySDR.Device(args)
        self.sdr.setSampleRate(SOAPY_SDR_RX, 0, sample_rate)
        self.sdr.setFrequency(SOAPY_SDR_RX, 0, center_freq)
        if gain != "auto":
            self.sdr.setGain(SOAPY_SDR_RX, 0, float(gain))
        self.stream = self.sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
        self.sdr.activateStream(self.stream)

    def read_blocks(self, read_size: int) -> Iterator[np.ndarray]:
        import numpy as np
        buff = np.empty(read_size, dtype=np.complex64)
        while True:
            sr = self.sdr.readStream(self.stream, [buff], read_size)
            if sr.ret > 0:
                yield buff.copy()

    def close(self):
        try:
            self.sdr.deactivateStream(self.stream)
            self.sdr.closeStream(self.stream)
        except Exception:
            pass
