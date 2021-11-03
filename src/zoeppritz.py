import numpy as np
import cmath as cmath
import matplotlib.pyplot as plt

class Zoeppritz:

    def solve(self, a1,a2,b1,b2,p1,p2,theta):
                
        # Compute the aucoustic Impedance
        z1s = p1*b1
        z2s = p2*b2
        z1p = p1*a1
        z2p = p2*a2

        t1 = np.radians(theta)
        
        # trig identities
        d1 = np.arcsin(b1/a1*np.sin(t1))
        st2 = a2/a1*np.sin(t1)
        ct2 = cmath.sqrt(1.-st2**2)
        sd2 = b2/a1*np.sin(t1)
        cd2 = cmath.sqrt(1.-sd2**2)

        #double angles
        s2t2 = 2*st2*ct2
        s2d2 = 2*sd2*cd2
        c2d2 = 1.-2*sd2**2

        #Zoepritz equations
        A = np.array([[np.cos(t1), -np.sin(d1), ct2, sd2],
                    [np.sin(t1), np.cos(d1), -st2, cd2],
                    [z1p*np.cos(2*d1), -z1s*np.sin(2*d1), -z2p*c2d2, -z2s*s2d2],
                    [b1/a1*np.sin(2*t1), z1s*np.cos(2*d1), b2/a2*z2s*s2t2, -z2s*c2d2]])

        B = np.array([[np.cos(t1)],
                    [-np.sin(t1)],
                    [-z1p*np.cos(2*d1)],
                    [b1/a1*z1s*np.sin(2*t1)]])

        #Solve the matrix equations
        c = np.linalg.solve(A,B)

        A1 = c[0]
        B1 = c[1]
        A2 = c[2]
        B2 = c[3]

        ERP = np.absolute(A1)**2
        ERS = (b1*np.cos(d1))/(a1*np.cos(t1))*np.absolute(B1)**2
        ETP = (p2*a2*np.real(ct2))/(p1*a1*np.cos(t1))*np.absolute(A2)**2
        ETS = (p2*b2*np.real(cd2))/(p1*a1*np.cos(d1))*np.absolute(B2)**2
        
        return (ERP,ERS,ETP,ETS)


    def plot_energy_coeff(self,a1,a2,b1,b2,p1,p2):
        # Takes the p-wave velocity, s-wave velocity and density for two layers and plots
        # the normalized energy coefficients of the reflected and transmitted p and s waves
        
        # Create array of incidence angles between 0 and 90 degrees
        N = 100
        thetas = np.linspace(0.,90.,N)

        #make zero arrays to be filled in later
        ERP = np.zeros(N)
        ERS = np.zeros(N)
        ETP = np.zeros(N)
        ETS = np.zeros(N)

        for i in range(0,N):
            results = self.solve(a1,a2,b1,b2,p1,p2,thetas[i])
            (ERP[i],ERS[i], ETP[i], ETS[i]) = results
        
        fig, ax = plt.subplots(4,1,figsize=(6,6),sharex=False)
        ax[0].plot(thetas,ERP)
        ax[0].set_ylabel("$E_{rp}$")
        ax[0].set_ylim(-0.01,1.01)

        ax[1].plot(thetas, ETP)
        ax[1].set_ylabel("$E_{tp}$")
        ax[1].set_ylim(-0.01,1.01)

        ax[2].plot(thetas, ERS)
        ax[2].set_ylabel("$E_{rs}$")
        ax[2].set_ylim(-0.01,1.01)

        ax[3].plot(thetas,ETS)
        ax[3].set_ylabel("$E_{ts}$")
        ax[3].set_ylim(-0.01,1.01)
        ax[3].set_xlabel("Incident Angle $(^\circ$)")

        return fig

if __name__ == '__main__':
    a1, a2 = 2000.,4000.
    b1, b2 = 1070.,2310.
    p1, p2 = 2000.,2500.
    zoep = Zoeppritz()
    fig = zoep.plot_energy_coeff(a1,a2,b1,b2,p1,p2)
    fig.savefig('test2.png')