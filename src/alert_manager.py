import importlib, json, os, logging
from typing import Dict, Any, List
from .schemas.event import AlertEvent, DetectionTrace

log = logging.getLogger("spectrum.alerts")

class AlertManager:
    def __init__(self, sinks: List[str], cfg: Dict[str, Any]):
        self.sinks = sinks
        self.cfg = cfg
        self.handlers = []
        for s in sinks:
            try:
                mod = importlib.import_module(f"alerts.{s}")
                self.handlers.append(mod)
            except Exception as e:
                log.error("Failed to load alert sink %s: %s", s, e)

    def emit(self, event: AlertEvent):
        for h in self.handlers:
            try:
                if hasattr(h, "emit"):
                    h.emit(event, self.cfg)
            except Exception as e:
                log.error("Alert sink error (%s): %s", h.__name__, e)
