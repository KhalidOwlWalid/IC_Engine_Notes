from dataclasses import dataclass
from typing import Optional

import numpy as np

class EngineGeometryError(ValueError):
    """Raised when EngineGeometry parameters are missing or mutually inconsistent"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

@dataclass(frozen=True)
class EngineGeometry:
    conrod_length: float | None # NOT USED YET 
    stroke: float
    bore: float
    compression_ratio: float
    N_c: float # Number of cylinders
    V_bdc: float
    V_tdc: float

    @classmethod
    def from_bore_stroke(cls, stroke: float, bore: float, compression_ratio: float, N_c: float):
        V_d = N_c * (np.pi / 4) * np.power(bore, 2) * compression_ratio 
        V_tdc = V_d / (compression_ratio - 1)
        V_bdc = (V_d + V_tdc)
        return cls(conrod_length=None, stroke=stroke, bore=bore, compression_ratio=compression_ratio, N_c=N_c, V_tdc=V_tdc, V_bdc=V_bdc)

    @classmethod
    def from_volume(cls, V_bdc: float, V_tdc: float):
        if (V_bdc <= V_tdc):
            raise EngineGeometryError(f"V_bdc ({V_bdc}) is less than V_tdc ({V_tdc})")
        compression_raio = V_bdc / V_tdc
        return cls(conrod_length=None, stroke=None, bore=None, compression_ratio=compression_raio, N_c=None, V_tdc=V_tdc, V_bdc=V_bdc)

    @classmethod
    def from_all(cls, stroke: float, bore: float, N_c: float, V_bdc: float, V_tdc: float):
        if (V_bdc <= V_tdc):
            raise EngineGeometryError(f"V_bdc ({V_bdc}) is less than V_tdc ({V_tdc})")
        compression_ratio = V_bdc/V_tdc
        return cls(conrod_length=None, stroke=stroke, bore=bore, compression_ratio=compression_ratio, N_c=N_c, V_bdc=V_bdc, V_tdc=V_tdc)

    @property
    def V_d(self) -> float:
        return self.V_bdc - self.V_tdc

    @property
    def V_c(self) -> float:
        return self.V_tdc

    @property
    def B(self) -> float:
        if (self.bore is None):
            raise EngineGeometryError("Bore, B is not provided. Use of the bore parameter will result in bug")
        return self.bore

    @property
    def S(self) -> float:
        if (self.stroke is None):
            raise EngineGeometryError("Bore, B is not provided. Use of the bore parameter will result in bug")
        return self.stroke

    @property
    def r(self) -> float:
        return self.compression_ratio

    def V_tilda(self, theta: float | np.ndarray) -> float | np.ndarray:
        return 1/self.r + ((self.r - 1)/(2 * self.r)) * (1 - np.cos(theta))

    def dVtilda_dtheta(self, theta: float | np.ndarray) -> float | np.ndarray:
        return (self.r - 1) * np.sin(theta) / (2 * self.r)

    # Normalized cylinder volume at a given crank angle
    # Note that in Engineering Fundamentals of the Internal Combustion Engine by Willard W. Pulkrabek, he used a different formula
    # See equation 2-13 and 2-14
    # Note: The equation taken from 2.38 from the textbook is wrong it should have been 1/r + ... instead of 1 + ...
    @staticmethod
    def V_tilda_static(r, theta):
        return 1/r + ((r - 1)/(2 * r)) * (1 - np.cos(theta))

    # Normalized dv_dtheta at a given crank angle
    @staticmethod
    def dVtilda_dtheta_static(r: float, theta: float | np.ndarray) -> float | np.ndarray:
        return (r - 1) * np.sin(theta) / (2 * r)
