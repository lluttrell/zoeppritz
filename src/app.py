import gi
from zoeppritz import Zoeppritz

gi.require_version("Gtk","3.0")
from gi.repository import Gtk

from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Zoeppritz Explorer")
        a1, a2 = 2000.,4000.
        b1, b2 = 1070.,2310.
        p1, p2 = 2000.,2500.
        zoep = Zoeppritz()
        fig = zoep.plot_energy_coeff(a1,a2,b1,b2,p1,p2)
        self.sw = Gtk.ScrolledWindow()
        self.add(self.sw)
        canvas = FigureCanvas(fig)
        canvas.set_size_request(800, 600)
        self.sw.add(canvas)

    def on_button_clicked(self, widget):
        a1, a2 = 2000.,4000.
        b1, b2 = 1070.,2310.
        p1, p2 = 2000.,2500.
        zoep = Zoeppritz()
        fig = zoep.plot_energy_coeff(a1,a2,b1,b2,p1,p2)
        self.sw = Gtk.ScrolledWindow()
        self.add(self.sw)
        canvas = FigureCanvas(fig)
        canvas.set_size_request(800, 600)
        self.sw.add(canvas)


win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()