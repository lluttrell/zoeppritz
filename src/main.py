import gi
from model import Model
from view import View

gi.require_version("Gtk","3.0")
from gi.repository import Gtk

from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure

class Handler:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def on_adjustment_p1_value_changed(self, adjustment):
        self.model.vp1 = adjustment.get_value()
        self.view.update_plot()
    
    def on_adjustment_p2_value_changed(self, adjustment):
        self.model.vp2 = adjustment.get_value()
        self.view.update_plot()
    
    def on_adjustment_s1_value_changed(self, adjustment):
        self.model.vs1 = adjustment.get_value()
        self.view.update_plot()
    
    def on_adjustment_s2_value_changed(self, adjustment):
        self.model.vs2 = adjustment.get_value()
        self.view.update_plot()
        
    def on_adjustment_rho1_value_changed(self, adjustment):
        self.model.rho1 = adjustment.get_value()
        self.view.update_plot()
    
    def on_adjustment_rho2_value_changed(self, adjustment):
        self.model.rho2 = adjustment.get_value()
        self.view.update_plot()

    def on_main_window_destroy(self, widget, data=None):
        Gtk.main_quit()

class MainWindow(Gtk.Window):


    def __init__(self):
        self.model = Model(100)
        self.view = View(self.model)
        
        #get gui from glade file
        self.builder = Gtk.Builder()
        self.builder.add_from_file("gui.glade")
        self.builder.connect_signals(Handler(self.model, self.view))

        #connect graph
        self.graph = self.builder.get_object("graph_box")
        canvas = FigureCanvas(self.view.fig)
        self.graph.add(canvas)

        #display main window
        self.main_window = self.builder.get_object("main_window")
        self.main_window.show_all()

    def main(self):
        Gtk.main()

if __name__ == "__main__":
    application = MainWindow()
    application.main()