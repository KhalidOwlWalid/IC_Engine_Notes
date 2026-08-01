import numpy as np
import matplotlib.pyplot as plt
from engine_lib.heat_cycle import wiebe_fcn 

def main():

    a = 5
    n = 4
    theta_s = -20
    theta_d = 60
    theta = np.linspace(theta_s, theta_s + theta_d, theta_d + theta_s)

    x = wiebe_fcn(a, theta, theta_s, theta_d, n)

    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.plot(theta, x, label="Energy release")

    burn_rate = np.gradient(x, theta)
    ax2.plot(theta, burn_rate, label="Burn rate")

    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
