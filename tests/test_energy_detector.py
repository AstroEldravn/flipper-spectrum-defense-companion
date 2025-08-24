import numpy as np
from src.detectors.energy_detector import EnergyDetector

def test_energy_detector_triggers_on_spike():
    ed = EnergyDetector(threshold_db=3.0, hysteresis_db=1.5)
    noise = (np.random.randn(4096)+1j*np.random.randn(4096))/10
    ed.process(noise)
    spike = noise + (np.ones(4096)+1j*np.ones(4096))*0.4
    out = ed.process(spike)
    assert out["triggered"] is True
