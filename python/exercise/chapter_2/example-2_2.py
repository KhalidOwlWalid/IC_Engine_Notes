import matplotlib.pyplot as plt
import numpy as np

from engine_lib.burn_fraction import BurnFraction

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

    engine_1 = BurnFraction(a=5, n=4, theta_s=-20, theta_d=60)

    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.plot(engine_1.theta, engine_1.xb, label="xb")
    ax1.set_ylabel("xb")
    ax2.plot(engine_1.theta, engine_1.dxb_dtheta, label="dxb_dtheta")
    ax2.set_ylabel("dxb_dtheta")
    plt.legend()
    plt.show()

    # x = wiebe_fcn(a, theta, theta_s, theta_d, n)

    # fig, (ax1, ax2) = plt.subplots(1, 2)
    # ax1.plot(theta, x, label="Energy release")
    # ax1.set_title("Burn fraction curve")
    # ax1.set_xlabel("Crank angle, theta")
    # ax1.set_ylabel("Cumulative burn fraction (0 - 1)")

    # burn_rate = np.gradient(x, theta)
    # ax2.plot(theta, burn_rate, label="Burn rate")
    # ax2.set_title("")

    # plt.legend()
    # plt.show()

if __name__ == "__main__":
    main()
