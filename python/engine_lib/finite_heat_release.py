from dataclasses import dataclass, field

import numpy as np
from scipy.integrate import solve_ivp, cumulative_trapezoid

from engine_lib.engine_kinematics import EngineGeometry


@dataclass(frozen=True)
class WiebeParams:
    a: float
    n: float
    theta_s: float
    theta_d: float
    q_in: float

# Should not be mutable once initialized
@dataclass(frozen=True)
class FiniteHeatReleaseIV:
    """ Finite Heat Release initial values """
    P_0: float
    T_0: float

@dataclass
class AirProperties:
    """ Struct to hold properties of gas """
    # Specific heat ratio
    gamma: float

@dataclass
class FiniteHeatReleaseResults:
    theta: np.ndarray = field(default_factory=list)

    # Energy release results
    xb: np.ndarray = field(default_factory=list)
    dxb_dtheta: np.ndarray = field(default_factory=list) # [J/deg]

    # Cylinder volume [m3]
    dVtilda_dtheta: np.ndarray = field(default_factory=list)
    dV_dtheta: np.ndarray = field(default_factory=list)
    V: np.ndarray = field(default_factory=list)
    V_tilda: np.ndarray = field(default_factory=list)

    # Pressure [Pa]
    dPtilda_dtheta: np.ndarray = field(default_factory=list)
    dP_dtheta: np.ndarray = field(default_factory=list)
    P: np.ndarray = field(default_factory=list)

    # Work [J]
    dQtilda_dtheta: np.ndarray = field(default_factory=list)
    dQ_dtheta: np.ndarray = field(default_factory=list)
    Q: np.ndarray = field(default_factory=list)

    # Temperature
    T: np.ndarray = field(default_factory=list)

    # Indicated mean effective pressure
    imep: float | None = None
    # Thermal efficiency
    eta_t: float | None = None
    # Work
    W_net: np.ndarray = field(default_factory=list)

class FiniteHeatRelease:

    """
    The implementation of the finite heat release is based on the book:
    
    Internal Combustion Engines: Applied Thermosciences by Colin R. Ferguson/Allan T. Kirkpatrick

    Taken from page p.42 to p.47
    """

    def __init__(self, eng_geometry: EngineGeometry, wiebe_params: WiebeParams, air_prop: AirProperties, iv: FiniteHeatReleaseIV):
        self._eng_geom: EngineGeometry = eng_geometry
        self._wb_parm: WiebeParams = wiebe_params
        # Initial Values
        self._iv: FiniteHeatReleaseIV = iv
        self._air_prop: AirProperties = air_prop

        self._results: FiniteHeatReleaseResults | None = None

    def wiebe_fcn(self, theta):
        return 1 - np.exp(-self._wb_parm.a * np.pow((theta - self._wb_parm.theta_s)/self._wb_parm.theta_d, self._wb_parm.n))

    def xb(self, theta):
        return self.wiebe_fcn(theta)

    # Equation 2.26, can also be re-written as Equation 2.25
    def dxb_dtheta(self, theta: float | np.ndarray) -> float | np.ndarray:
        X = (theta - self._wb_parm.theta_s) / self._wb_parm.theta_d
        dx_dtheta = (self._wb_parm.a * self._wb_parm.n / self._wb_parm.theta_d) * np.power(X, self._wb_parm.n - 1) * np.exp(-self._wb_parm.a * np.power(X, self._wb_parm.n))
        return dx_dtheta

    def full_solve(self, theta: np.ndarray) -> FiniteHeatReleaseResults:

        # Solve for pressure
        sol = self.solve_pressure_ivp(theta)
        P = sol.y[0]

        # Theta evaluated by the numerical solver
        theta_eval = sol.t

        # Solve for the energy release
        # FIXBUG: This is wrong, as Q will be 0, when theta_eval is not during combustion region
        Q: np.ndarray = self._wb_parm.q_in * self.xb(theta_eval)
        dQ_dtheta: np.ndarray = self._wb_parm.q_in * self.dxb_dtheta(theta_eval)

        # Solve for volume
        V_tilda = self._eng_geom.V_tilda(theta_eval)
        V = V_tilda * self._eng_geom.V_bdc

        # Solve for temperature
        T_n = self._iv.T_0 * (P * V) / (self._iv.P_0 * self._eng_geom.V_bdc)

        # Solve for work (work is the area under P-v diagram), it is given by W = P dV
        W_net = cumulative_trapezoid(P, V, initial=0)

        # Solve for thermal efficiency
        eta_t = W_net / self._wb_parm.q_in

        # Solve imep (scalar)
        Q_tilda = self._wb_parm.q_in / (self._iv.P_0 * self._eng_geom.V_bdc)
        imep = eta_t * Q_tilda * self._iv.P_0 * (self._eng_geom.r / (self._eng_geom.r - 1))

        self._results = FiniteHeatReleaseResults(
            theta=theta_eval,
            xb=self.xb(theta_eval),
            dxb_dtheta=self.dxb_dtheta(theta_eval),
            V=V,
            V_tilda=V_tilda,
            P=P,
            Q=Q,
            dQ_dtheta=dQ_dtheta,
            T=T_n,
            W_net=W_net,
            imep=imep[-1],
            eta_t=eta_t[-1]
        )

    # See equation 2.36 from the book
    def _dp_dtheta_ode(self, theta, y):

        P = y[0]

        # Calculate the cylinder volume
        Vtilda = self._eng_geom.V_tilda(theta)
        V = Vtilda * self._eng_geom.V_bdc

        dVtilda_dtheta = self._eng_geom.dVtilda_dtheta(theta)
        dV_dtheta = dVtilda_dtheta * self._eng_geom.V_bdc

        if (theta < self._wb_parm.theta_s or theta > (self._wb_parm.theta_s + self._wb_parm.theta_d)):
            Q_in = 0
            dx_dtheta = 0
        else:
            Q_in = self._wb_parm.q_in
            dx_dtheta = self.dxb_dtheta(theta)

        dp_dtheta = -self._air_prop.gamma * (P / V) * dV_dtheta + (self._air_prop.gamma - 1) * (Q_in / V) * dx_dtheta

        return [dp_dtheta]

    def solve_pressure_ivp(self, theta):
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
            y0=[self._iv.P_0],
            t_eval=theta,
            rtol=1e-8,
            atol=1e-10,
        )

        if not sol.success:
            raise RuntimeError(f"Solve IVP failed: {sol.message}")
        return sol

    # Forward-Euler solver, leaving this here but user should be using the solve_pressure_ivp function instead
    def fe_solver(self, r: float | np.ndarray, theta: float | np.ndarray, V_bdc: float, gamma: float, P_0: float) -> FiniteHeatReleaseResults:
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
            Vtilda = EngineGeometry.V_tilda_static(r, theta[i])
            V = Vtilda * V_bdc
            results.v.append(V)

            dVtilda_dtheta = EngineGeometry.dVtilda_dtheta_static(r, theta[i])
            dV_dtheta = dVtilda_dtheta * V_bdc
            results.dv_dtheta.append(dV_dtheta)

            if (theta[i] < self._wb_parm.theta_s or theta[i] > (self._wb_parm.theta_s + self._wb_parm.theta_d)):
                Q_in = 0
            else:
                Q_in = self._wb_parm.q_in
            results.q.append(Q_in)

            dP_dtheta = -gamma * (P / V) * dV_dtheta + (gamma - 1) * (Q_in / V) * dx_dtheta
            results.dp_dtheta.append(dP_dtheta)

            if (i < len(theta) - 1):
                P = P + dP_dtheta * (theta[i + 1] - theta[i])
                results.p.append(P)

        return results 

class FiniteHeatReleaseWithLoss:
    pass
