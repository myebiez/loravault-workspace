from hx711 import HX711
from config import Pinout
import statistics

class WeightSensor:
    def __init__(self):
        self.hx = HX711(dout_pin=Pinout.SCALE_DT, pd_sck_pin=Pinout.SCALE_SCK)
        # Pragmatic: Fail fast if hardware isn't calibrated
        self.hx.set_reference_unit(1.0) # To be updated via Flask calibration
        self.hx.reset()
        self.hx.tare()

    def get_stable_weight(self, samples=5):
        # CLRS: \mathcal{O}(N \log N) due to sorting in median function to filter noise.
        # Robust against physical bumps (DOET: Error prevention).
        readings = []
        for _ in range(samples):
            val = self.hx.get_weight(5)
            readings.append(val)
        return statistics.median(readings)