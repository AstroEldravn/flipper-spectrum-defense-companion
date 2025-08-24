import numpy as np
from typing import Tuple

def db10(x: np.ndarray, eps: float = 1e-12) -> float:
    p = float(np.mean(np.abs(x) ** 2))
    return 10.0 * np.log10(max(p, eps))

def window_signal(x: np.ndarray, size: int, hop: int):
    for i in range(0, len(x) - size + 1, hop):
        yield x[i:i+size]

class RingBuffer:
    def __init__(self, capacity: int):
        self.buf = np.zeros(capacity, dtype=float)
        self.capacity = capacity
        self.idx = 0
        self.full = False

    def append(self, value: float):
        self.buf[self.idx] = value
        self.idx = (self.idx + 1) % self.capacity
        if self.idx == 0:
            self.full = True

    def values(self) -> np.ndarray:
        if not self.full:
            return self.buf[:self.idx]
        return np.concatenate([self.buf[self.idx:], self.buf[:self.idx]])
