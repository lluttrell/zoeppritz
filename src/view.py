import matplotlib
matplotlib.use('GTK3Agg')

import matplotlib.pyplot as plt

class View:
    def __init__(self, model):
        self.fig, self.ax = plt.subplots(4,1,sharex=False)
        self.initialize_plot(self.ax)
        self.model = model

    def initialize_plot(self, ax):
        ax[0].set_ylabel("$E_{rp}$")
        ax[0].set_ylim(-0.01,1.01)
        ax[1].set_ylabel("$E_{tp}$")
        ax[1].set_ylim(-0.01,1.01)
        ax[2].set_ylabel("$E_{rs}$")
        ax[2].set_ylim(-0.01,1.01)
        ax[3].set_ylabel("$E_{ts}$")
        ax[3].set_ylim(-0.01,1.01)
        ax[3].set_xlabel("Incident Angle $(^\circ$)")

    def update_plot(self):
        energy_coefficients = self.model.energy_coefficients()
        self.ax[0].plot(energy_coefficients[0],energy_coefficients[1])
        self.ax[1].plot(energy_coefficients[0],energy_coefficients[2])
        self.ax[2].plot(energy_coefficients[0],energy_coefficients[3])
        self.ax[3].plot(energy_coefficients[0],energy_coefficients[4])

