import yaml, os, logging
from typing import Dict, Any
from .schemas.config import Config

log = logging.getLogger("spectrum.config")

def load_config(base_path: str = "config/config.yaml", profile: str = None) -> Dict[str, Any]:
    with open(base_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    if profile:
        prof_path = f"config/profiles/{profile}.yaml"
        if os.path.exists(prof_path):
            with open(prof_path, "r", encoding="utf-8") as p:
                prof = yaml.safe_load(p) or {}
            cfg = _deep_merge(cfg, prof)
        else:
            log.warning("Profile %s not found at %s", profile, prof_path)
    return cfg

def _deep_merge(a: dict, b: dict) -> dict:
    out = dict(a)
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out
