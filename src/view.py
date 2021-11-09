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
        self.ax[0].clear()
        self.ax[1].clear()
        self.ax[2].clear()
        self.ax[3].clear()
        
        self.ax[0].plot(self.model.angles, self.model.reflected_p_energies)
        self.ax[1].plot(self.model.angles, self.model.transmitted_p_energies)
        self.ax[2].plot(self.model.angles, self.model.reflected_s_energies)
        self.ax[3].plot(self.model.angles, self.model.transmitted_s_energies)


