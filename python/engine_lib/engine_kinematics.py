from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class EngineGeometry:
    conrod_length: float
    stroke: float
    bore: float
    compression_ratio: float
    N_c: float # Number of cylinders

    @property
    def V_d(self):
        return self.N_c * (np.pi / 4) * np.power(self.B, 2) * self.S 

    @property
    def B(self):
        return self.bore

    @property
    def S(self):
        return self.stroke

    @property
    def V_bdc(self):
        pass

    @property
    def r(self):
        return self.compression_ratio

    @property
    def V_c(self):
        return self.V_d / (self.r - 1)
