from src.alert_manager import AlertManager
from src.schemas.event import AlertEvent, DetectionTrace
def test_log_sink(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    am = AlertManager(["log_event"], {"alert":{}})
    evt = AlertEvent(message="test", center_freq=0, sample_rate=0, device="file", traces=[])
    am.emit(evt)
    assert (tmp_path / "logs" / "events.jsonl").exists()
