import matplotlib
matplotlib.use('GTK3Agg')

import matplotlib.pyplot as plt

from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure


class View:
    """
    Handles the plotting of the data contained in the application's model

    Args:
        model (Model): model to plot
    """
    def __init__(self, model):
        self.model = model
        self.fig, self.ax = plt.subplots(4,1,figsize=(6,6),sharex=False)
        self.canvas = FigureCanvas(self.fig)
        self.update_plot()

    def set_axes_limits(self):
        """Sets the y axes limits to the range (0,1)""" 
        for a in self.ax:
            a.set_ylim(-0.01,1.01)

    def set_labels(self):
        """Sets the axes labels"""
        self.ax[0].set_ylabel("$E_{rp}$")
        self.ax[1].set_ylabel("$E_{tp}$")
        self.ax[2].set_ylabel("$E_{rs}$")
        self.ax[3].set_ylabel("$E_{ts}$")
        self.ax[3].set_xlabel("Incident Angle $(^\circ$)")

    def plot_models(self):
        """Plots data from the model onto the axes"""
        self.ax[0].plot(self.model.angles, self.model.reflected_p_energies)
        self.ax[1].plot(self.model.angles, self.model.transmitted_p_energies)
        self.ax[2].plot(self.model.angles, self.model.reflected_s_energies)
        self.ax[3].plot(self.model.angles, self.model.transmitted_s_energies)

    def reset_plot(self):
        """Clears the plot"""
        for a in self.ax:
            a.cla()

    def update_plot(self):
        """Updates the plot
        
            Note: This is called by the controller to redraw the canvas when the model is updated
        """
        self.reset_plot()
        self.set_axes_limits()
        self.set_labels()
        self.plot_models()
        self.canvas.draw()



