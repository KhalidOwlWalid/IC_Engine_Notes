import matplotlib.pyplot as plt
import numpy as np

from engine_lib.finite_heat_release import FiniteHeatRelease, WiebeParams

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

    theta = np.linspace(-np.pi, np.pi, 100)
    theta_deg = theta * 180 / np.pi

    engine1_wb_params = WiebeParams(
        a=5, n=3, theta_s=np.deg2rad(0), theta_d=np.deg2rad(40), q_in=1764
    )

    engine2_wb_params = WiebeParams(
        a=5, n=3, theta_s=np.deg2rad(-20), theta_d=np.deg2rad(40), q_in=1764
    )

    engine1 = FiniteHeatRelease(engine1_wb_params)
    engine2 = FiniteHeatRelease(engine2_wb_params)
    engine1_P, engine1_burn_rate, engine1_temp = engine1.solve_dptilda_dtheta(10, theta, 8.73e-4, 1.4, 100e3)
    engine2_P, engine2_burn_rate, engine2_temp = engine2.solve_dptilda_dtheta(10, theta, 8.73e-4, 1.4, 100e3)

    plt.plot(theta_deg, engine1_temp, label="Engine 1")
    plt.plot(theta_deg, engine2_temp, label="Engine 2")
    # plt.plot(theta_deg, engine1_P, label="Engine 1")
    # plt.plot(theta_deg, engine2_P, label="Engine 2")
    plt.title("Different crank angle start comparison")
    plt.ylabel("Pressure (kPa)")
    plt.xlabel("Theta (degree)")
    plt.grid()
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
