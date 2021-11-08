import numpy as np
import cmath as cmath

class Model:
    def __init__(self, num_datapoints):
        self.angles = np.linspace(0, 90, num_datapoints)
        self.rock1 = Rock(2000,1070,2000)
        self.rock2 = Rock(4000, 2310, 2500)

    @property
    def vp1(self):
        return self.rock1.p_velocity

    @vp1.setter
    def vp1(self, velocity):
        self.rock1.p_velocity = velocity

    def energy_coefficients(self):
        return [[theta, BoundaryModel(self.rock1, self.rock2, theta).normalized_energy_coefficients()] for theta in self.angles]

class BoundaryModel:
    def __init__(self,rock1, rock2, theta1):
        self.rock1 = rock1
        self.rock2 = rock2
        self.theta1 = theta1

    @property
    def theta1(self):
        return np.radians(self._theta1_degrees)

    @theta1.setter
    def theta1(self, value):
        if value < 0 or value > 90:
            raise ValueError("Incidence angle not in valid range (0,90)")
        self._theta1_degrees = value

    @property
    def phi1(self):
        return np.arcsin(self.rock1.s_velocity / self.rock1.p_velocity * np.sin(self.theta1))

    @property
    def sin_theta2(self):
        return  self.rock2.p_velocity / self.rock1.p_velocity * np.sin(self.theta1)

    @property
    def cos_theta2(self):
        return cmath.sqrt(1. - self.sin_theta2**2)

    @property
    def sin_phi2(self):
        return self.rock2.s_velocity / self.rock1.p_velocity * np.sin(self.theta1)

    @property
    def cos_phi2(self):
        return cmath.sqrt(1. - self.sin_phi2**2)

    def amplitude_matrix(self):
        vp1 = self.rock1.p_velocity
        vs1 = self.rock1.s_velocity
        zp1 = self.rock1.p_impedance
        zs1 = self.rock1.s_impedance
        
        vp2 = self.rock2.p_velocity
        vs2 = self.rock2.s_velocity
        zs2 = self.rock2.s_impedance
        zp2 = self.rock2.p_impedance

        #double angles
        s2t2 = 2 * self.sin_theta2 * self.cos_theta2
        s2d2 = 2 * self.sin_phi2 * self.cos_phi2
        c2d2 = 1. - 2 * self.sin_phi2**2

        #Zoepritz equations
        A = np.array([[np.cos(self.theta1), -np.sin(self.phi1), self.cos_theta2, self.sin_phi2],
                    [np.sin(self.theta1), np.cos(self.phi1), - self.sin_theta2, self.cos_phi2],
                    [zp1 * np.cos(2 * self.phi1), -zs1*np.sin(2 *self.phi1), -zp2*c2d2, -zs2*s2d2],
                    [vs1 / vp1 * np.sin(2 * self.theta1), zs1 * np.cos(2*self.phi1), vs2 / vp2 * zs2 * s2t2, -zs2 * c2d2]])

        B = np.array([[np.cos(self.theta1)],
                    [-np.sin(self.theta1)],
                    [-zp1 * np.cos(2 * self.phi1)],
                    [vp1 / vs1 * zs1 * np.sin(2*self.theta1)]])

        #Solve the matrix equations
        return np.linalg.solve(A,B)

    def normalized_energy_coefficients(self):
        amp = self.amplitude_matrix()

        list = np.array([
            np.absolute(amp[0])**2,
            (self.rock1.s_velocity * np.cos(self.phi1)) / (self.rock1.p_velocity * np.cos(self.theta1)) * np.absolute(amp[1])**2,
            (self.rock1.density * self.rock2.p_velocity * np.real(self.cos_theta2)) / (self.rock1.density * self.rock1.p_velocity * np.cos(self.theta1)) * np.absolute(amp[2])**2,
            (self.rock2.density * self.rock2.s_velocity * np.real(self.cos_phi2)) / (self.rock1.density * self.rock1.p_velocity * np.cos(self.phi1)) * np.absolute(amp[3])**2
        ])

        return list.T.flatten()
        
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
    model = Model(10)
    print(model.energy_coefficients())