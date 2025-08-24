import json, os, logging, time
from pathlib import Path
log = logging.getLogger("spectrum.alerts.log_event")

def emit(event, cfg: dict):
    Path("logs").mkdir(exist_ok=True, parents=True)
    rec = event.model_dump()
    with open("logs/events.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    log.info("[LOG] %s", rec.get("message"))
