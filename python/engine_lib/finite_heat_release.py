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
class FiniteHeatReleaseResults:
    theta: np.ndarray
    
    # Energy release results
    xb: np.ndarray
    dxb_dtheta: np.ndarray # [J/deg]

    # Cylinder volume [m3]
    dvtilda_dtheta: np.ndarray
    dv_dtheta: np.ndarray
    v: np.ndarray
    
    # Pressure [Pa]
    dptilda_dtheta: np.ndarray
    dp_dtheta: np.ndarray
    p: np.ndarray

    # Work [J]
    dqtilda_dtheta: np.ndarray
    q: np.ddarray

class FiniteHeatRelease:

    """
    The implementation of the finite heat release is based on the book:
    
    Internal Combustion Engines: Applied Thermosciences by Colin R. Ferguson/Allan T. Kirkpatrick

    Taken from page p.42 to p.47
    """

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

    # Equation 2.26, can also be re-written as Equation 2.25
    def dxb_dtheta(self, theta: float | np.ndarray) -> float | np.ndarray:
        X = (theta - self.theta_s) / self.theta_d
        dx_dtheta = (self.a * self.n / self.theta_d) * np.power(X, self.n - 1) * np.exp(-self.a * np.power(X, self.n))
        return dx_dtheta

    # TODO: Refactor this, this is a lot of just hardcoded implementation
    # TODO: Provide an option to solve with ODE solver (e.g. RK45) instead of forward-euler
    def solve_dptilda_dtheta(self, r: float | np.ndarray, theta: float | np.ndarry, V_bdc: float, gamma: float, P_0: float) -> FiniteHeatReleaseResults:
        """
        Solve the dP/dtheta problem using forward-euler, to yield higher accuracy, consider using RK45 (Runge Kutta method).

        Initial pressure, P_0 required to solve the equation as P in itself is a state with memory
        """

        results = FiniteHeatReleaseResults

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
            Vtilda = EngineGeometry.V_tilda(r, theta[i])
            V = Vtilda * V_bdc

            dVtilda_dtheta = EngineGeometry.dVtilda_dtheta(r, theta[i])
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

class FiniteHeatReleaseWithLoss:
    pass
