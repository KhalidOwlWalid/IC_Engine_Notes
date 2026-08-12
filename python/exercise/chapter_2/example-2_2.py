import matplotlib.pyplot as plt
import numpy as np

from dataclasses import asdict

from engine_lib.engine_kinematics import EngineGeometry
from engine_lib.finite_heat_release import (
    AirProperties,
    FiniteHeatRelease,
    FiniteHeatReleaseIV,
    WiebeParams,
)

"""
Example 2.2

A single-cylinder spark ignition cycle engine is operated at full throttle, and its performance is to be predicted using a Wiebe
energy release analysis. The engine has a compression ratio of 10. The initial cylinder pressure, P1, at bottom dead center is 1 bar,
with a temperature T1 at bottom dead center of 300 K. The bore and stroke of the engine are b = 100 mm and s = 100 mm. The total heat
addition Qin = 1764 J and the combustion duration θd is  constant at 40◦. Assume that the ideal gas specific heat ratio γ is 1.4, the
molecular mass of the gas mixture is 29 kg/kmol, and the Wiebe energy release parameters are a = 5 and n = 3.

(a) Compute the displacement volume Vd, the volume at bottom dead center V1, the dimensionless heat addition ̃Q,
and the mass of gas in the cylinder m.

(b) Plot the pressure and temperature profiles versus crank angle for θs1 = −20◦(engine 1)  and θs2 = 0◦(engine 2).

(c) Determine the effect of changing the start of energy release from θs = −50◦ to θs =  +20◦ atdc on the thermal efficiency,
and imep of the engine.

"""
def main():

    theta = np.linspace(-np.pi, np.pi, 1000)

    fhr_iv = FiniteHeatReleaseIV(P_0=100e3, T_0=300)
    air_properties = AirProperties(gamma=1.4)
    engine_geometry = EngineGeometry.from_bore_stroke(bore=100e-3, stroke=100e-3, compression_ratio=10, N_c=1) 

    theta_s = [
        -40,
        -20,
        0,
        10,
        20
    ]
    num_eng = len(theta_s)

    fig, (P_ax, T_ax) = plt.subplots(2, 1)

    engine_results: dict = {}

    # Question (b)
    for i in range(num_eng):
        engine_wb_params = WiebeParams(
            a=5, n=3, theta_s=np.deg2rad(theta_s[i]), theta_d=np.deg2rad(40), q_in=1764
        )
        engine = FiniteHeatRelease(engine_geometry, engine_wb_params, air_properties, fhr_iv)
        engine.full_solve(theta)
        engine_results[i] = engine

        label = f"Engine {i} with theta_s={np.rad2deg(engine._wb_parm.theta_s)} deg"
        engine.plot_data_with_theta(P_ax, "W_net", label)
        engine.plot_data_with_theta(T_ax, "dWtilda_dtheta", label)

    P_ax.set_ylabel("dQtilda_dtheta")
    P_ax.set_xlabel("Theta (deg)")
    P_ax.set_title("Comparison of different theta_s configuration")

    T_ax.set_ylabel("Temperature (K)")
    T_ax.set_xlabel("Theta (deg)")

    axes = [P_ax, T_ax]

    for i, ax in enumerate(axes):
        ax.grid()
        ax.legend()

    plt.show()

    # My own analysis
    fig, ax = plt.subplots(1, 1)
    for key in engine_results.keys():
        engine = engine_results[key]
        label = f"Engine {key} with theta_s={np.rad2deg(engine._wb_parm.theta_s)} deg"
        engine.plot_data_with_theta(ax, "W_net", label)

    ax.set_xlabel("Theta (deg)")
    ax.set_ylabel("W_net (J)")
    plt.legend()
    plt.grid()
    plt.show()

    # Question (c)
    theta_s_array = np.linspace(-50, 20, 70)
    imep_result: np.ndarray = np.empty(len(theta_s_array))
    eta_t_result: np.ndarray = np.empty(len(theta_s_array))

    for i, theta_s in enumerate(theta_s_array):
        engine_wb_params = WiebeParams(
            a=5, n=3, theta_s=np.deg2rad(theta_s), theta_d=np.deg2rad(40), q_in=1764
        )
        engine = FiniteHeatRelease(engine_geometry, engine_wb_params, air_properties, fhr_iv)
        engine.full_solve(theta)
        imep_result[i] = engine._results.imep
        eta_t_result[i] = engine._results.eta_t

    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.plot(theta_s_array, imep_result, label="imep")
    ax1.set_xlabel("theta_s")
    ax1.set_ylabel("imep")
    ax1.grid()
    ax1.legend()
    ax1.set_title("Comparison of the effect of θs to engine's efficiency")

    ax2.plot(theta_s_array, eta_t_result, label="eta_t")
    ax2.set_xlabel("theta_s")
    ax2.set_ylabel("eta_t")
    ax2.legend()
    ax2.grid()

    plt.show()

if __name__ == "__main__":
    main()
