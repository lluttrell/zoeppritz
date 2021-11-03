import gi
import zoeppritz

gi.require_version("Gtk","3.0")
from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Zoeppritz Explorer")
        self.button = Gtk.Button(label="click here")
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)

    def on_button_clicked(self, widget):
        a1, a2 = 2000.,4000.
        b1, b2 = 1070.,2310.
        p1, p2 = 2000.,2500.
        zoep = Zoeppritz()
        fig = zoep.plot_energy_coeff(a1,a2,b1,b2,p1,p2)
        fig.savefig('test3.png')

win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()