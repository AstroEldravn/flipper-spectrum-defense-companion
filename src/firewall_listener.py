import logging, time
from typing import Dict, Any, List
import numpy as np

from .detectors.energy_detector import EnergyDetector
from .detectors.burst_detector import BurstDetector
from .detectors.spectral_kurtosis import SpectralKurtosisDetector
from .detectors.changepoint import CUSUMDetector
from .schemas.event import AlertEvent, DetectionTrace

log = logging.getLogger("spectrum.listener")

class ListenerOrchestrator:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        thr = cfg.get("thresholds", {})
        self.energy = EnergyDetector(threshold_db=float(thr.get("energy_db", 6.0)),
                                     hysteresis_db=float(thr.get("hysteresis_db", 3.0)))
        self.burst = BurstDetector(min_windows=int(thr.get("burst_min_windows",3)),
                                   repeat_within_s=float(thr.get("burst_repeat_within_s",3.0)))
        self.sk = SpectralKurtosisDetector(threshold=float(thr.get("sk_threshold",4.0)))
        self.cusum = CUSUMDetector(threshold=float(thr.get("cusum_threshold",5.0)))

    def process_window(self, x: np.ndarray) -> List[DetectionTrace]:
        traces: List[DetectionTrace] = []
        e = self.energy.process(x)
        traces.append(DetectionTrace(detector="energy", score=e["score"], threshold=float(self.cfg.get("thresholds",{}).get("energy_db",6.0)), window_ts=time.time()))
        b = self.burst.process(e["triggered"])  # depends on energy
        if b["triggered"]:
            traces.append(DetectionTrace(detector="burst", score=b["count"], threshold=float(self.cfg.get("thresholds",{}).get("burst_min_windows",3)), window_ts=time.time()))
        s = self.sk.process(x)
        if s["triggered"]:
            traces.append(DetectionTrace(detector="spectral_kurtosis", score=s["score"], threshold=float(self.cfg.get("thresholds",{}).get("sk_threshold",4.0)), window_ts=time.time()))
        c = self.cusum.process(x)
        if c["triggered"]:
            traces.append(DetectionTrace(detector="cusum", score=c["score"], threshold=float(self.cfg.get("thresholds",{}).get("cusum_threshold",5.0)), window_ts=time.time()))
        return traces

    def fuse(self, traces: List[DetectionTrace]) -> bool:
        # Simple OR over detectors, but require at least energy or burst
        names = {t.detector for t in traces}
        return ("burst" in names) or ("energy" in names and ("spectral_kurtosis" in names or "cusum" in names))

    def severity(self, traces: List[DetectionTrace]) -> str:
        names = {t.detector for t in traces}
        if "burst" in names and ("spectral_kurtosis" in names or "cusum" in names):
            return "high"
        if "burst" in names or "spectral_kurtosis" in names:
            return "medium"
        return "low"
