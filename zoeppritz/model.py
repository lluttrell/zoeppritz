"""
Models a p wave incident at a boundary of two semi infinite rocks. 
Classes:

    Model
    ZoeppritzSystem
    Rock
"""

import numpy as np
import cmath as cmath


class Model:
    """
    Main model class for the application. Models the energy partitioning of the system for p-waves at multiple
    incidence angles.

    Args:
        num_datapoints (int): number of angles (evenly spread between 0 and 90 degrees) to model
    """

    def __init__(self, num_datapoints):
        self.rock1 = Rock(2000, 1070, 2000)
        self.rock2 = Rock(4000, 2310, 2500)
        self.angles = np.linspace(0, 90, num_datapoints)
        self._update_boundary_model_list()

    def _update_boundary_model_list(self):
        self.boundary_model = [ZoeppritzSystem(
            self.rock1, self.rock2, theta) for theta in self.angles]

    @property
    def vp1(self):
        return self.rock1.p_velocity

    @vp1.setter
    def vp1(self, velocity):
        self.rock1.p_velocity = velocity
        self._update_boundary_model_list()

    @property
    def vp2(self):
        return self.rock2.p_velocity

    @vp2.setter
    def vp2(self, velocity):
        self.rock2.p_velocity = velocity
        self._update_boundary_model_list()

    @property
    def vs1(self):
        return self.rock1.s_velocity

    @vs1.setter
    def vs1(self, velocity):
        self.rock1.s_velocity = velocity
        self._update_boundary_model_list()

    @property
    def vs2(self):
        return self.rock2.s_velocity

    @vs2.setter
    def vs2(self, velocity):
        self.rock2.s_velocity = velocity
        self._update_boundary_model_list()

    @property
    def rho1(self):
        return self.rock1.density

    @vp1.setter
    def rho1(self, density):
        self.rock1.density = density
        self._update_boundary_model_list()

    @property
    def rho2(self):
        return self.rock2.density

    @rho2.setter
    def rho2(self, density):
        self.rock2.density = density
        self._update_boundary_model_list()

    @property
    def transmitted_p_energies(self):
        return [bm.transmitted_p_energy for bm in self.boundary_model]

    @property
    def transmitted_s_energies(self):
        return [bm.transmitted_s_energy for bm in self.boundary_model]

    @property
    def reflected_p_energies(self):
        return [bm.reflected_p_energy for bm in self.boundary_model]

    @property
    def reflected_s_energies(self):
        return [bm.reflected_s_energy for bm in self.boundary_model]


class ZoeppritzSystem:
    """Solves the zoeppritz equations at a boundary between two rocks for an incident p wave

    Attributes:
        rock1 (Rock): rock that incident/reflected waves travel in
        rock2 (Rock): rock that refracted waves travel in
        theta1 (num): incident angle of p-wave (degrees from line normal to plane)
    """

    def __init__(self, rock1, rock2, theta1):
        self.rock1 = rock1
        self.rock2 = rock2
        self.theta1 = theta1
        self._set_normalized_energy_coefficients()

    @property
    def theta1(self):
        """num: Incident angle in radians

            Note: Setter expects angle input in degrees
        """
        return np.radians(self._theta1_degrees)

    @theta1.setter
    def theta1(self, value):
        if value < 0 or value > 90:
            raise ValueError("Incidence angle not in valid range (0,90)")
        self._theta1_degrees = value
        self._set_normalized_energy_coefficients()

    @property
    def phi1(self):
        return np.arcsin(self.rock1.s_velocity / self.rock1.p_velocity * np.sin(self.theta1))

    @property
    def sin_theta2(self):
        return self.rock2.p_velocity / self.rock1.p_velocity * np.sin(self.theta1)

    @property
    def cos_theta2(self):
        return cmath.sqrt(1. - self.sin_theta2**2)

    @property
    def sin_phi2(self):
        return self.rock2.s_velocity / self.rock1.p_velocity * np.sin(self.theta1)

    @property
    def cos_phi2(self):
        return cmath.sqrt(1. - self.sin_phi2**2)

    def _amplitude_matrix(self):
        """Computes the amplitude coefficients for the system"""
        vp1 = self.rock1.p_velocity
        vs1 = self.rock1.s_velocity
        zp1 = self.rock1.p_impedance
        zs1 = self.rock1.s_impedance

        vp2 = self.rock2.p_velocity
        vs2 = self.rock2.s_velocity
        zs2 = self.rock2.s_impedance
        zp2 = self.rock2.p_impedance

        # double angles
        s2t2 = 2 * self.sin_theta2 * self.cos_theta2
        s2d2 = 2 * self.sin_phi2 * self.cos_phi2
        c2d2 = 1. - 2 * self.sin_phi2**2

        # Zoepritz equations
        A = np.array([[np.cos(self.theta1), -np.sin(self.phi1), self.cos_theta2, self.sin_phi2],
                      [np.sin(self.theta1), np.cos(self.phi1), -
                       self.sin_theta2, self.cos_phi2],
                      [zp1 * np.cos(2 * self.phi1), -zs1 *
                       np.sin(2 * self.phi1), -zp2*c2d2, -zs2*s2d2],
                      [vs1 / vp1 * np.sin(2 * self.theta1), zs1 * np.cos(2*self.phi1), vs2 / vp2 * zs2 * s2t2, -zs2 * c2d2]])

        B = np.array([[np.cos(self.theta1)],
                      [-np.sin(self.theta1)],
                      [-zp1 * np.cos(2 * self.phi1)],
                      [vs1 / vp1 * zs1 * np.sin(2*self.theta1)]])

        # Solve the matrix equations
        return np.linalg.solve(A, B).flatten()

    def _set_normalized_energy_coefficients(self):
        """Sets the normalized energy coefficients for the system"""
        amp = self._amplitude_matrix()
        self.reflected_p_energy = np.absolute(amp[0])**2
        self.reflected_s_energy = (self.rock1.s_velocity * np.cos(self.phi1)) / (
            self.rock1.p_velocity * np.cos(self.theta1)) * np.absolute(amp[1])**2
        self.transmitted_p_energy = (self.rock1.density * self.rock2.p_velocity * np.real(self.cos_theta2)) / (
            self.rock1.density * self.rock1.p_velocity * np.cos(self.theta1)) * np.absolute(amp[2])**2
        self.transmitted_s_energy = (self.rock2.density * self.rock2.s_velocity * np.real(self.cos_phi2)) / (
            self.rock1.density * self.rock1.p_velocity * np.cos(self.phi1)) * np.absolute(amp[3])**2


class Rock:
    """
    Represents solid rock

    Args:
        p_velocity (int): p-wave velocity
        s_velocity (int): s-wave velocity
        density (int): density of rock
    """

    def __init__(self, p_velocity, s_velocity, density):
        self.p_velocity = p_velocity
        self.s_velocity = s_velocity
        self.density = density
        self.p_impedance = self.p_velocity * self.density
        self.s_impedance = self.s_velocity * self.density
