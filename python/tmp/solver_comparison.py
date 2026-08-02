"""
Playground: comparing numerical ODE solver choices for the finite heat release
pressure equation dP/dtheta = f(theta, P), using the Example 2.2 engine as the
test case (a = 5, n = 3, r = 10, theta_s = -20 deg, theta_d = 40 deg).

Questions this script answers:
  1. How does hand-rolled forward Euler converge as you add more fixed steps?
  2. How does scipy's solve_ivp (adaptive step size) compare -- how many
     function evaluations does it need to reach similar accuracy?
  3. How do different solve_ivp methods (RK45, RK23, DOP853, Radau, BDF,
     LSODA) compare to each other at the same tolerance?
  4. What happens to accuracy / cost as you loosen or tighten rtol?
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# --- Physics: Wiebe combustion + finite heat release pressure model ---
# (Same equations as engine_lib/finite_heat_release.py, kept standalone here
# so this script has nothing to do with solver choice except the ODE itself.)

A, N_WIEBE = 5, 3
THETA_S = np.deg2rad(-20)
THETA_D = np.deg2rad(40)
Q_IN = 1764       # J, total heat release
R = 10            # compression ratio
GAMMA = 1.4
V_BDC = 8.73e-4   # m^3
P0 = 1e5          # Pa, initial pressure at BDC


def dxb_dtheta(theta):
    X = (theta - THETA_S) / THETA_D
    return (A * N_WIEBE / THETA_D) * X ** (N_WIEBE - 1) * np.exp(-A * X ** N_WIEBE)


def V_tilda(theta):
    return 1 / R + ((R - 1) / (2 * R)) * (1 - np.cos(theta))


def dVtilda_dtheta(theta):
    return (R - 1) * np.sin(theta) / (2 * R)


def dP_dtheta(theta, P):
    """The ODE itself: dP/dtheta = f(theta, P). P is a length-1 array (scipy's convention)."""
    P = P[0]
    V = V_tilda(theta) * V_BDC
    dV_dtheta = dVtilda_dtheta(theta) * V_BDC
    Q_in = Q_IN if THETA_S <= theta <= THETA_S + THETA_D else 0.0
    return [-GAMMA * (P / V) * dV_dtheta + (GAMMA - 1) * (Q_in / V) * dxb_dtheta(theta)]


# --- Method 1: hand-rolled forward Euler, at varying fixed resolutions ---

def euler_solve(n_points):
    theta = np.linspace(-np.pi, np.pi, n_points)
    P = np.empty(n_points)
    P[0] = P0
    for i in range(n_points - 1):
        P[i + 1] = P[i] + dP_dtheta(theta[i], [P[i]])[0] * (theta[i + 1] - theta[i])
    return theta, P


# --- Method 2: scipy.integrate.solve_ivp, adaptive step size ---

def scipy_solve(method="RK45", rtol=1e-6, atol=1e-9, n_eval=200):
    theta_eval = np.linspace(-np.pi, np.pi, n_eval)
    return solve_ivp(
        dP_dtheta, (-np.pi, np.pi), y0=[P0],
        t_eval=theta_eval, method=method, rtol=rtol, atol=atol,
    )


if __name__ == "__main__":

    # 0) Reference "ground truth": a very tight-tolerance, high-order solve.
    ref = scipy_solve(method="DOP853", rtol=1e-12, atol=1e-6, n_eval=2000)
    ref_peak = ref.y[0].max()
    print(f"Reference (DOP853, rtol=1e-12): peak P = {ref_peak:9.1f} Pa, nfev = {ref.nfev}\n")

    # 1) Forward Euler convergence -- error should roughly halve each time n doubles
    #    (that's what "first-order accurate" means in practice).
    print("Forward Euler convergence (fixed step count = fixed # of f evaluations):")
    for n in [50, 100, 500, 2000, 10000, 50000]:
        _, P = euler_solve(n)
        err = abs(P.max() - ref_peak) / ref_peak * 100
        print(f"  n={n:>6}: peak = {P.max():>10.1f} Pa   error = {err:7.4f}%   fn evals = {n:>6}")

    # 2) scipy methods at a shared loose-ish tolerance, few output points --
    #    note nfev is decided by the solver's internal adaptive stepping,
    #    NOT by n_eval (t_eval only controls where results are *reported*).
    print("\nscipy solve_ivp methods (rtol=1e-6, atol=1e-6, 200 reported points):")
    for method in ["RK45", "RK23", "DOP853", "Radau", "BDF", "LSODA"]:
        sol = scipy_solve(method=method, rtol=1e-6, atol=1e-6, n_eval=200)
        peak = sol.y[0].max()
        err = abs(peak - ref_peak) / ref_peak * 100
        print(f"  {method:>8}: peak = {peak:>10.1f} Pa   error = {err:7.4f}%   fn evals = {sol.nfev:>5}")

    # 3) Effect of tightening/loosening tolerance on RK45 specifically
    print("\nEffect of rtol on RK45 cost vs accuracy:")
    for rtol in [1e-2, 1e-4, 1e-6, 1e-8, 1e-10]:
        sol = scipy_solve(method="RK45", rtol=rtol, atol=rtol * 1e-3, n_eval=200)
        peak = sol.y[0].max()
        err = abs(peak - ref_peak) / ref_peak * 100
        print(f"  rtol={rtol:.0e}: peak = {peak:>10.1f} Pa   error = {err:7.4f}%   fn evals = {sol.nfev:>5}")

    # --- Plot: cheap Euler vs converged Euler vs a cheap adaptive RK45 ---
    theta_e50, P_e50 = euler_solve(50)
    theta_e2000, P_e2000 = euler_solve(2000)
    sol_rk45 = scipy_solve(method="RK45", rtol=1e-6, atol=1e-6, n_eval=50)

    plt.figure(figsize=(8, 5))
    plt.plot(np.degrees(ref.t), ref.y[0] / 1000, "k-", linewidth=2,
             label="Reference (DOP853, tight tol)")
    plt.plot(np.degrees(theta_e50), P_e50 / 1000, "r--",
              label="Forward Euler, n=50 (50 fn evals)")
    plt.plot(np.degrees(theta_e2000), P_e2000 / 1000, "orange", linestyle="--",
              label="Forward Euler, n=2000 (2000 fn evals)")
    plt.plot(np.degrees(sol_rk45.t), sol_rk45.y[0] / 1000, "bo", markersize=4,
             label=f"RK45, 50 reported points ({sol_rk45.nfev} fn evals)")
    plt.xlabel("Crank angle (deg)")
    plt.ylabel("Pressure (kPa)")
    plt.title("Same accuracy target, very different cost: Euler vs adaptive RK45")
    plt.legend()
    plt.tight_layout()
    plt.show()
