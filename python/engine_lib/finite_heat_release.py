from dataclasses import dataclass, field

import numpy as np
from scipy.integrate import solve_ivp

from engine_lib.engine_kinematics import EngineGeometry


@dataclass
class WiebeParams:
    a: float
    n: float
    theta_s: float
    theta_d: float
    q_in: float

@dataclass
class FiniteHeatReleaseResults:
    theta: np.ndarray = field(default_factory=list)

    # Energy release results
    xb: np.ndarray = field(default_factory=list)
    dxb_dtheta: np.ndarray = field(default_factory=list) # [J/deg]

    # Cylinder volume [m3]
    dvtilda_dtheta: np.ndarray = field(default_factory=list)
    dv_dtheta: np.ndarray = field(default_factory=list)
    v: np.ndarray = field(default_factory=list)

    # Pressure [Pa]
    dptilda_dtheta: np.ndarray = field(default_factory=list)
    dp_dtheta: np.ndarray = field(default_factory=list)
    p: np.ndarray = field(default_factory=list)

    # Work [J]
    dqtilda_dtheta: np.ndarray = field(default_factory=list)
    q: np.ndarray = field(default_factory=list)

    # Temperature
    T: np.ndarray = field(default_factory=list)

class FiniteHeatRelease:

    """
    The implementation of the finite heat release is based on the book:
    
    Internal Combustion Engines: Applied Thermosciences by Colin R. Ferguson/Allan T. Kirkpatrick

    Taken from page p.42 to p.47
    """

    def __init__(self, eng_geometry: EngineGeometry, wiebe_params: WiebeParams):
        self._wb_parm = wiebe_params
        self._eng_geom = eng_geometry

    def wiebe_fcn(self, theta):
        return 1 - np.exp(-self._wb_parm.a * np.pow((theta - self._wb_parm.theta_s)/self._wb_parm.theta_d, self._wb_parm.n))

    def xb(self, theta):
        return self.wiebe_fcn(theta)

    # Equation 2.26, can also be re-written as Equation 2.25
    def dxb_dtheta(self, theta: float | np.ndarray) -> float | np.ndarray:
        X = (theta - self._wb_parm.theta_s) / self._wb_parm.theta_d
        dx_dtheta = (self._wb_parm.a * self._wb_parm.n / self._wb_parm.theta_d) * np.power(X, self._wb_parm.n - 1) * np.exp(-self._wb_parm.a * np.power(X, self._wb_parm.n))
        return dx_dtheta

    def _dp_dtheta_ode(self, theta, y, gamma):

        P = y[0]

        # Calculate the cylinder volume
        Vtilda = EngineGeometry.V_tilda(self._eng_geom.r, theta)
        V = Vtilda * self._eng_geom.V_bdc

        dVtilda_dtheta = EngineGeometry.dVtilda_dtheta(self._eng_geom.r, theta)
        dV_dtheta = dVtilda_dtheta * self._eng_geom.V_bdc

        if (theta < self._wb_parm.theta_s or theta > (self._wb_parm.theta_s + self._wb_parm.theta_d)):
            Q_in = 0
            dx_dtheta = 0
        else:
            Q_in = self._wb_parm.q_in
            dx_dtheta = self.dxb_dtheta(theta)

        dp_dtheta = -gamma * (P / V) * dV_dtheta + (gamma - 1) * (Q_in / V) * dx_dtheta

        return [dp_dtheta]

    def solve_pressure_ivp(self, theta, gamma, iv_P):
        """Solves the pressure equation (dP/dtheta) via initial value solver

        Args:
            theta (_type_): _description_
            gamma (_type_): _description_
            iv_P (_type_): _description_

        Raises:
            RuntimeError: _description_

        Returns:
            _type_: _description_
        """
        sol = solve_ivp(
            fun=self._dp_dtheta_ode,
            t_span=(theta[0], theta[-1]),
            y0=[iv_P],
            t_eval=theta,
            args=[gamma]
        )

        if not sol.success:
            raise RuntimeError(f"Solve IVP failed: {sol.message}")
        return sol

    # Forward-Euler solver, leaving this here but user should be using the solve_pressure_ivp function instead
    def solve(self, r: float | np.ndarray, theta: float | np.ndarray, V_bdc: float, gamma: float, P_0: float) -> FiniteHeatReleaseResults:
        """
        Solve the dP/dtheta problem using forward-euler, to yield higher accuracy, consider using RK45 (Runge Kutta method).

        Initial pressure, P_0 required to solve the equation as P in itself is a state with memory
        """

        results = FiniteHeatReleaseResults()

        # Initial conditions
        P = P_0 # Pa
        Q_in = 0

        results.p.append(P)
        for i in range(len(theta)):
            
            # Calculate the burn rate
            dx_dtheta = self.dxb_dtheta(theta[i])
            results.dxb_dtheta.append(dx_dtheta)

            # Calculate the cylinder volume
            Vtilda = EngineGeometry.V_tilda(r, theta[i])
            V = Vtilda * V_bdc
            results.v.append(V)

            dVtilda_dtheta = EngineGeometry.dVtilda_dtheta(r, theta[i])
            dV_dtheta = dVtilda_dtheta * V_bdc
            results.dv_dtheta.append(dV_dtheta)

            if (theta[i] < self.theta_s or theta[i] > (self.theta_s + self.theta_d)):
                Q_in = 0
            else:
                Q_in = self.q_in
            results.q.append(Q_in)

            dP_dtheta = -gamma * (P / V) * dV_dtheta + (gamma - 1) * (Q_in / V) * dx_dtheta
            results.dp_dtheta.append(dP_dtheta)

            if (i < len(theta) - 1):
                P = P + dP_dtheta * (theta[i + 1] - theta[i])
                results.p.append(P)

        return results 

class FiniteHeatReleaseWithLoss:
    pass
