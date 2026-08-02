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

    # Normalized cylinder volume at a given crank angle
    # Note that in Engineering Fundamentals of the Internal Combustion Engine by Willard W. Pulkrabek, he used a different formula
    # See equation 2-13 and 2-14
    # Note: The equation taken from 2.38 from the textbook is wrong it should have been 1/r + ... instead of 1 + ...
    @staticmethod
    def V_tilda(r, theta):
        return 1/r + ((r - 1)/(2 * r)) * (1 - np.cos(theta))

    # Normalized dv_dtheta at a given crank angle
    @staticmethod
    def dVtilda_dtheta(r: float, theta: float | np.ndarray) -> float | np.ndarray:
        return (r - 1) * np.sin(theta) / (2 * r)
