from src.config_loader import load_config

def test_profile_merge():
    cfg = load_config(profile="demo_indoor")
    assert cfg["detectors"]["enabled"][0] == "energy"
