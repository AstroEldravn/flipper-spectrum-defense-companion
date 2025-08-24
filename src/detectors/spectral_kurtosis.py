import numpy as np
from typing import Dict, Any

def kurtosis(x: np.ndarray, eps: float=1e-12) -> float:
    x = x - np.mean(x)
    m2 = np.mean(np.abs(x)**2) + eps
    m4 = np.mean(np.abs(x)**4)
    return float(m4 / (m2*m2 + eps))

class SpectralKurtosisDetector:
    def __init__(self, threshold: float=4.0):
        self.threshold = threshold

    def process(self, x: np.ndarray) -> Dict[str, Any]:
        k = kurtosis(x)
        return {"triggered": k >= self.threshold, "score": k}
