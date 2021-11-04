import gi
from zoeppritz import Zoeppritz

gi.require_version("Gtk","3.0")
from gi.repository import Gtk

from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure

class MainWindow(Gtk.Window):
    zoep = Zoeppritz()
    a1, a2 = 2000.,4000.
    b1, b2 = 1070.,2310.
    p1, p2 = 2000.,2500.
    fig = zoep.plot_energy_coeff(a1,a2,b1,b2,p1,p2)

    def __init__(self):
        #get gui from glade file
        self.builder = Gtk.Builder()
        self.builder.add_from_file("gui.glade")
        self.builder.connect_signals(self)

        #connect graph
        self.graph = self.builder.get_object("graph_box")
        canvas = FigureCanvas(self.fig)
        # canvas.set_size_request(800, 600)
        self.graph.add(canvas)

        #display main window
        self.main_window = self.builder.get_object("main_window")
        self.main_window.show_all()




    def on_main_window_destroy(self, widget, data=None):
        Gtk.main_quit()

    def main(self):
        Gtk.main()

if __name__ == "__main__":
    application = MainWindow()
    application.main()