from pydantic import BaseModel
from typing import Optional, List, Literal
import time

Severity = Literal["low", "medium", "high"]

class DetectionTrace(BaseModel):
    detector: str
    score: float
    threshold: float
    window_ts: float

class AlertEvent(BaseModel):
    ts: float = time.time()
    severity: Severity = "low"
    message: str
    center_freq: int
    sample_rate: int
    device: str
    traces: List[DetectionTrace] = []
