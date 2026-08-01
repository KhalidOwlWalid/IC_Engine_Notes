import numpy as np


class BurnFraction:

    def __init__(self, a, n, theta_s, theta_d, theta_step_size=100):
        self.a = a
        self.n = n
        self.theta_s = theta_s
        self.theta_d = theta_d
        self.theta = np.linspace(theta_s, theta_s + theta_d, theta_step_size)

    def wiebe_fcn(self):
        return 1 - np.exp(-self.a * np.pow((self.theta - self.theta_s)/self.theta_d, self.n))

    @property
    def xb(self):
        return self.wiebe_fcn()

    @property
    def dxb_dtheta(self):
        X = (self.theta - self.theta_s) / self.theta_d
        dx_dtheta = (self.a * self.n / self.theta_d) * np.power(X, self.n - 1) * np.exp(-self.a * np.power(X, self.n))
        return dx_dtheta

    def simulate_burn_fraction(self, theta):
        pass

    def plot_cumulative_burn_fraction():
        pass


