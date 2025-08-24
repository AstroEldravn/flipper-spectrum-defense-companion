import requests, logging
log = logging.getLogger("spectrum.alerts.webhook")
def emit(event, cfg: dict):
    url = cfg.get("alert", {}).get("webhook_url")
    if not url:
        return
    try:
        requests.post(url, json=event.model_dump(), timeout=2.0)
    except Exception as e:
        log.error("webhook failed: %s", e)
