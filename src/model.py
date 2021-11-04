from zoeppritz import Zoeppritz

class Model:
    vp1 = 2000
    vp2 = 4000
    vs1 = 1070
    vs2 =  2310
    density1 = 2000
    density2 = 2500

    def generate_energy_graph(self):
        zoep = Zoeppritz()
        return zoep.plot_energy_coeff(self.vp1, self.vp2, self.vs1, self.vs2, self.density1, self.density2)