import gi
from model import Model

gi.require_version("Gtk","3.0")
from gi.repository import Gtk

from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure

class Handler():
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def on_adjustment_p1_changed(self, adjustment):
        self.model.vp1 = adjustment.get_value()
        print(self.model.vp1)
        self.view.update_graph()


    def on_main_window_destroy(self, widget, data=None):
        Gtk.main_quit()

class MainWindow(Gtk.Window):
    model = Model()

    def __init__(self):
        #get gui from glade file
        self.builder = Gtk.Builder()
        self.builder.add_from_file("gui.glade")
        self.builder.connect_signals(Handler(self.model, self))

        #display main window
        self.main_window = self.builder.get_object("main_window")
        self.main_window.show_all()

    def main(self):
        Gtk.main()

if __name__ == "__main__":
    application = MainWindow()
    application.main()