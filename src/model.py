import numpy as np

class Model:
    def __init__(self):
        self.rock1 = Rock(2000,1070,2000)
        self.rock2 = Rock(4000, 2310, 2500)

    def reflected_s_angle(self, theta):
        return np.arcsin(self.rock1.s_velocity / self.rock1.p_velocity * np.sin(theta))

    def transmitted_p_angle(self, theta):
        return np.arcsin(self.rock2.p_velocity / self.rock1.p_velocity * np.sin(theta))

    def transmitted_s_angle(self, theta):
        return np.arcsin(self.rock2.s_velocity / self.rock1.p_velocity * np.sin(theta))

    def generate_energy_graph(self, theta):
        zoep = Zoeppritz()
        return zoep.plot_energy_coeff(self.vp1, self.vp2, self.vs1, self.vs2, self.density1, self.density2)

    def amplitude_matrix(self, theta_deg):
        theta1 = np.radians(theta_deg)

        vp1 = self.rock1.p_velocity
        vp2 = self.rock2.p_velocity
        vs1 = self.rock2.s_velocity
        vs2 = self.rock2.s_velocity
        rho1 = self.rock1.density
        rho2 = self.rock2.density

        theta2 = self.transmitted_p_angle(theta1)
        phi1 = self.reflected_s_angle(theta1)
        phi2 = self.transmitted_s_angle(theta1)

        A = np.array([
            [-np.sin(theta1), -np.cos(phi1), np.sin(theta2), np.cos(phi2)],
            [np.cos(theta1), -np.sin(phi1), np.cos(theta2), -np.sin(theta2)],
            [np.sin(2*theta1), vp1 / vp2 * np.cos(2 * phi1), (rho2 * vs2**2 * vp1) / (rho1 * vs1**2 * vp2) * np.sin(2*theta2), (rho2 * vs2 * vp1) / (rho1 * vs1**2) * np.cos(2*phi2)],
            [-np.cos(2 * phi1), vs1 / vp1 * np.sin(2*phi1), (rho2 * vp2) / (rho1 * vp1) * np.cos(2*phi2), (-rho2 * vs2) / (rho1 * vp1) * np.sin(2*phi2)]
        ])

        B = np.array([
            [np.sin(theta1)],
            [np.cos(theta1)],
            [np.sin(2*theta1)],
            [np.cos(2*phi1)]
        ])

        #Solve the matrix equations
        return np.linalg.solve(A,B)

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

if __name__ == "__main__":
    model = Model()
    print(model.amplitude_matrix(45))