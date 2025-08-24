import logging
log = logging.getLogger("spectrum.alerts.sound_local")
def emit(event, cfg: dict):
    log.info("[SOUND] Beep for severity=%s", event.severity)
