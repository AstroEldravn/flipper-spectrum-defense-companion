import numpy as np
from typing import Dict, Any
from ..utils import db10

class CUSUMDetector:
    def __init__(self, threshold: float=5.0):
        self.threshold = threshold
        self.mu = None
        self.gp = 0.0

    def process(self, x: np.ndarray) -> Dict[str, Any]:
        p = db10(x)
        if self.mu is None:
            self.mu = p
        # Update mean slowly
        self.mu = 0.99*self.mu + 0.01*p
        s = p - self.mu - 0.1  # small drift
        self.gp = max(0.0, self.gp + s)
        trig = self.gp >= self.threshold
        if trig:
            self.gp = 0.0
        return {"triggered": trig, "score": float(self.gp), "power_db": float(p)}
