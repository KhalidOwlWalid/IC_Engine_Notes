from dataclasses import dataclass
from engine_lib.engine_kinematics import EngineGeometry

import numpy as np

@dataclass
class WiebeParams:
    a: float
    n: float
    theta_s: float
    theta_d: float
    q_in: float

@dataclass
class BurnFractionResults:
    theta: np.ndarray
    xb: np.ndarray
    dxb_dtheta: np.ndarray
    dvtilda_dtheta: np.ndarray
    dv_dtheta: np.ndarray
    
    dptilda_dtheta: np.ndarray
    dp_dtheta: np.ndarray

class BurnFraction:

    def __init__(self, wiebe_params: WiebeParams):
        self.a = wiebe_params.a
        self.n = wiebe_params.n
        self.theta_s = wiebe_params.theta_s
        self.theta_d = wiebe_params.theta_d
        self.q_in = wiebe_params.q_in
        
        self._results = None

    def wiebe_fcn(self, theta):
        return 1 - np.exp(-self.a * np.pow((theta - self.theta_s)/self.theta_d, self.n))

    def xb(self, theta):
        return self.wiebe_fcn(theta)

    def dxb_dtheta(self, theta: float | np.ndarray) -> float | np.ndarray:
        X = (theta - self.theta_s) / self.theta_d
        dx_dtheta = (self.a * self.n / self.theta_d) * np.power(X, self.n - 1) * np.exp(-self.a * np.power(X, self.n))
        return dx_dtheta

    def V(self, V_bdc: float, r: float, theta: float | np.ndarray) -> float | np.ndarray:
        return BurnFraction.V_tilda(r, theta) * V_bdc

    def dV_dtheta(self, V_bdc: float, r: float, theta: float | np.ndarray) -> float | np.ndarray:
        return BurnFraction.dVtilda_dtheta(r, theta) * V_bdc

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

    def dPtilda_dtheta(self, theta: float | np.ndarray, gamma: float, Ptilda: float | np.ndarray, Vtilda: float | np.ndarray) -> float | np.ndarray:

        for i in range(len(theta)):
            Q_in = 0
            # If it is not during the combustion process, then there is no heat added into the system
            # At this point, dQ/dtheta = 0
            if (theta[i] < self.theta_s or theta[i] > (self.theta_s + self.theta_d)):
                Q_in = 0
            else:
                Q_in = self.q_in


    def simulate(self, r, theta, V_bdc, gamma):

        P_results = []
        burn_rate = []
        T_results = []

        # Initial conditions
        P_0 = 1e5
        P = P_0 # Pa
        P_results.append(P / 1000)
        Q_in = 0
        T_0 = 300 # K
        T_results.append(T_0)
        for i in range(len(theta)):
            
            # Calculate the burn rate
            dx_dtheta = self.dxb_dtheta(theta[i])
            burn_rate.append(dx_dtheta)

            # Calculate the cylinder volume
            Vtilda = BurnFraction.V_tilda(r, theta[i])
            V = Vtilda * V_bdc

            dVtilda_dtheta = BurnFraction.dVtilda_dtheta(r, theta[i])
            dV_dtheta = dVtilda_dtheta * V_bdc

            if (theta[i] < self.theta_s or theta[i] > (self.theta_s + self.theta_d)):
                Q_in = 0
            else:
                Q_in = self.q_in

            dP_dtheta = -gamma * (P / V) * dV_dtheta + (gamma - 1) * (Q_in / V) * dx_dtheta

            if (i < len(theta) - 1):
                P = P + dP_dtheta * (theta[i + 1] - theta[i])
                curr_T = T_0 * (P / P_0) * (V / V_bdc)
                T_results.append(curr_T)
                P_results.append(P / 1000) # Converted into kPa

        return P_results, burn_rate, T_results
