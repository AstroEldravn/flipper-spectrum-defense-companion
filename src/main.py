import os, sys, time, logging, logging.config, json
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel

from .config_loader import load_config
from .spectrum_monitor import SpectrumMonitor
from .firewall_listener import ListenerOrchestrator
from .alert_manager import AlertManager
from .schemas.event import AlertEvent

app = typer.Typer(add_completion=False)
console = Console()

def setup_logging(cfg: dict):
    logcfg = cfg.get("logging", {}).get("config")
    if logcfg and os.path.exists(logcfg):
        import yaml
        with open(logcfg, "r", encoding="utf-8") as f:
            logging.config.dictConfig(yaml.safe_load(f))
    else:
        logging.basicConfig(level=logging.INFO)

@app.command()
def run(profile: str = typer.Option("demo_indoor", help="Profile name in config/profiles"),
        device: str = typer.Option("file", help="Device type: rtlsdr|hackrf|rtl_tcp|file"),
        freq: Optional[int] = typer.Option(None, "--freq", help="Center frequency Hz"),
        sample_rate: Optional[int] = typer.Option(None, "--sample-rate", help="Sample rate"),
        host: Optional[str] = typer.Option(None, "--host", help="rtl_tcp host:port"),
        iq: Optional[str] = typer.Option(None, "--iq", help=".npy complex64 IQ file for 'file' device")):
    """Run the spectrum watchdog daemon."""
    cfg = load_config(profile=profile)
    # override from CLI
    cfg.setdefault("device", {})
    if freq: cfg["device"]["center_freq"] = freq
    if sample_rate: cfg["device"]["sample_rate"] = sample_rate
    if host: cfg["device"]["host"] = host
    if device: cfg["device"]["type"] = device

    setup_logging(cfg)
    logging.getLogger("spectrum")
    console.print(Panel.fit(f"[bold cyan]Flipper Spectrum Defense Companion[/]\nProfile: [yellow]{profile}[/]  Device: [yellow]{cfg['device']['type']}[/]", title="Pocket Jam/Intrusion Alarm"))

    mon = SpectrumMonitor(
        device_type=cfg["device"]["type"],
        center_freq=int(cfg["device"].get("center_freq", 0)),
        sample_rate=int(cfg["device"].get("sample_rate", 2048000)),
        gain=str(cfg["device"].get("gain", "auto")),
        host=str(cfg["device"].get("host", "127.0.0.1:1234")),
        iq_path=iq,
    )
    orch = ListenerOrchestrator(cfg)
    alerts = AlertManager(cfg.get("alert", {}).get("sinks", ["log_event"]), cfg)

    # Open device and run
    mon.open()
    block = int(cfg.get("window", {}).get("size", 4096))
    hop = int(cfg.get("window", {}).get("hop", 2048))

    # Simple overlap handling: keep tail from previous block
    import numpy as np
    tail = np.zeros(0, dtype=np.complex64)
    for chunk in mon.blocks(hop):
        x = np.concatenate([tail, chunk])
        if len(x) >= block:
            win = x[:block]
            tail = x[hop:]
            traces = orch.process_window(win)
            if traces and orch.fuse(traces):
                sev = orch.severity(traces)
                msg = f"Anomaly detected: {', '.join(t.detector for t in traces)}"
                event = AlertEvent(
                    severity=sev,
                    message=msg,
                    center_freq=cfg["device"].get("center_freq", 0),
                    sample_rate=cfg["device"].get("sample_rate", 0),
                    device=cfg["device"].get("type", "unknown"),
                    traces=traces,
                )
                alerts.emit(event)

if __name__ == "__main__":
    app()
