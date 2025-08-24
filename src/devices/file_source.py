import numpy as np
from typing import Iterator

class FileIQSource:
    def __init__(self, npy_path: str):
        self.data = np.load(npy_path).astype(np.complex64)

    def read_blocks(self, read_size: int) -> Iterator[np.ndarray]:
        n = len(self.data)
        i = 0
        while i + read_size <= n:
            yield self.data[i:i+read_size]
            i += read_size
