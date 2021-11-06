import numpy as np

class Model:
    def __init__(self):
        self.rock1 = Rock(2000,1070,2000)
        self.rock2 = Rock(4000, 2310, 2500)

    def reflected_s_angle(theta):
        return np.arcsin(rock1.s_velocity / rock1.p_velocity * np.sin(theta))

    def transmitted_p_angle():
        return np.arcsin(rock2.p_velocity / rock1.p_velocity * np.sin(theta))

    def transmitted_s_angle():
        return np.arcsin(rock2.s_velocity / rock1.p_velocity * np.sin(theta))

    def generate_energy_graph(self):
        zoep = Zoeppritz()
        return zoep.plot_energy_coeff(self.vp1, self.vp2, self.vs1, self.vs2, self.density1, self.density2)

    def amplitude_matrix(self, theta_deg):
        theta1 = np.radians(theta_deg)

        z1s = rock1.s_impedance
        z1p = rock1.p_impedance
        z2s = rock2.s_impedance
        z2p = rock2.p_impedance

        theta2 = transmitted_p_angle(theta1)
        phi1 = reflected_s_angle(theta1)
        phi2 = transmitted_s_angle(theta1)


        B = np.array([[np.cos(t1)],
                    [-np.sin(t1)],
                    [-z1p*np.cos(2*d1)],
                    [b1/a1*z1s*np.sin(2*t1)]])

        #Solve the matrix equations
        c = np.linalg.solve(A,B)

class Rock:
    def __init__(self, p_velocity, s_velocity, density):
        self.p_velocity = p_velocity
        self.s_velocity = s_velocity
        self.density = density

    @property
    def p_impedance(self):
        return self.p_velocity * self.density

    @property
    def s_impedance(self):
        return self.s_velocity * self.density