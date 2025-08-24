import socket, struct, numpy as np
from typing import Iterator

class RTLTCPSocketSource:
    def __init__(self, host: str, center_freq: int, sample_rate: int, gain: str = "auto"):
        # host format: 'host:port'
        h, p = host.split(":")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((h, int(p)))
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        # Basic rtl_tcp tuning protocol
        self._set_freq(center_freq)
        self._set_sample_rate(sample_rate)
        if gain != "auto":
            self._set_gain(int(float(gain)*10))

    def _cmd(self, cmd: int, param: int):
        self.sock.sendall(struct.pack('>BI', cmd, param))

    def _set_freq(self, f): self._cmd(0x01, int(f))
    def _set_sample_rate(self, sr): self._cmd(0x02, int(sr))
    def _set_gain(self, g): self._cmd(0x03, int(g))

    def read_blocks(self, read_size: int) -> Iterator[np.ndarray]:
        # rtl_tcp returns unsigned IQ interleaved bytes centered at 127
        bsz = read_size * 2
        while True:
            buf = bytearray(bsz)
            view = memoryview(buf)
            n = 0
            while n < bsz:
                r = self.sock.recv_into(view[n:], bsz - n)
                if r == 0:
                    return
                n += r
            iq = np.frombuffer(buf, dtype=np.uint8).astype(np.float32)
            iq = (iq - 127.5) / 127.5
            iqc = iq[0::2] + 1j * iq[1::2]
            yield iqc.astype(np.complex64)

    def close(self):
        try:
            self.sock.close()
        except Exception:
            pass
