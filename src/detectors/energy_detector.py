import numpy as np
from typing import Dict, Any
from ..utils import db10

class EnergyDetector:
    def __init__(self, threshold_db: float=6.0, hysteresis_db: float=3.0):
        self.threshold_db = threshold_db
        self.hysteresis_db = hysteresis_db
        self.noise_db = None
        self.latched = False

    def process(self, x: np.ndarray) -> Dict[str, Any]:
        p_db = db10(x)
        if self.noise_db is None:
            self.noise_db = p_db
        # Update baseline when not latched and current power is near baseline
        if not self.latched and p_db <= self.noise_db + self.threshold_db/2:
            self.noise_db = 0.98*self.noise_db + 0.02*p_db
        delta = p_db - self.noise_db
        trigger_thr = self.threshold_db if not self.latched else self.hysteresis_db
        triggered = delta >= trigger_thr
        self.latched = triggered
        return {"triggered": triggered, "score": float(delta), "power_db": float(p_db), "baseline_db": float(self.noise_db)}
