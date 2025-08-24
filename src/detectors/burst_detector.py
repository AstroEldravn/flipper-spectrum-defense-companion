import numpy as np, time
from typing import Dict, Any, List

class BurstDetector:
    def __init__(self, min_windows: int=3, repeat_within_s: float=3.0):
        self.min_windows = min_windows
        self.repeat_within_s = repeat_within_s
        self._times: List[float] = []

    def process(self, triggered_energy: bool) -> Dict[str, Any]:
        now = time.time()
        if triggered_energy:
            self._times.append(now)
            self._times = [t for t in self._times if now - t <= self.repeat_within_s]
        fired = len(self._times) >= self.min_windows
        return {"triggered": fired, "count": len(self._times)}
