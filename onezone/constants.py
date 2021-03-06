__author__ = "aemerick <emerick@astro.columbia.edu>"

import numpy as np

from collections import OrderedDict

def _make_conversion_dictionaries():

    x = OrderedDict()

    elements = ['H','He', 'Li', 'Be', 'B','C','N','O','F',
                'Ne','Na','Mg','Al','Si','P','S',
                'Cl', 'Ar', 'K', 'Ca','Sc','Ti',
                'V','Cr','Mn','Fe','Co','Ni','Cu',
                'Zn','Ga','Ge','As','Se','Br','Kr',
                'Rb','Sr','Y','Zr','Nb','Mo', 'Tc',
                'Ru','Rh','Pd','Ag','Cd','In','Sn',
                'Sb','Te','I','Xe','Cs','Ba','La',
                'Ce','Pr','Nd','Pm','Sm','Eu','Gd',
                'Tb','Dy','Ho','Er','Tm','Yb','Lu',
                'Hf','Ta','W','Re','Os','Ir','Pt',
                'Au','Hg','Tl','Pb','Bi']

    for i in np.arange(1, len(elements)+1, 1):
        x[elements[i-1]] = i

    y = {v: k for k, v in x.items()}

    return x, y

asym_to_anum, anum_to_asym = _make_conversion_dictionaries()


def _set_abundance_dictionary():
#
# Solar abundances from Asplund et. al. 2009
# Meteorite abundances used for elements with
# no given solar measurements
#
    x = { 1 : 12.00,  2 : 10.93,  3 : 1.05,
          4 :  1.38,  5 :  2.70,  6 : 8.43,
          7 :  7.83,  8 :  8.69,  9 : 4.56,
         10 :  7.93, 11 :  6.24, 12 : 7.60,
         13 :  6.45, 14 :  7.51, 15 : 5.41,
         16 :  5.41, 17 :  5.50, 18 : 6.40,
         19 :  5.03, 20 :  6.34, 21 : 3.15,
         22 :  4.95, 23 :  3.93, 24 : 5.64,
         25 :  5.43, 26 :  7.50, 27 : 4.99,
         28 :  6.22, 29 :  4.19, 30 : 4.56,
         31 :  3.04, 32 :  3.65, 33 : 2.30,
         34 :  3.34, 35 :  2.54, 36 : 3.25,
         37 :  2.52, 38 :  2.87, 39 : 2.21,
         40 :  2.58, 41 :  1.46, 42 : 1.88,
         43 :  0.00, 44 :  1.75, 45 : 0.91,
         46 :  1.57, 47 :  0.94, 48 : 1.71,
         49 :  0.80, 50 :  2.04, 51 : 1.01,
         52 :  2.18, 53 :  1.55, 54 : 2.24,
         55 :  1.08, 56 :  2.18, 57 : 1.10,
         58 :  1.58, 59 :  0.72, 60 : 1.42,
         61 :  0.00, 62 :  0.96, 63 : 0.52,
         64 :  1.07, 65 :  0.30, 66 : 1.10,
         67 :  0.48, 68 :  0.92, 69 : 0.10,
         70 :  0.84, 71 :  0.10, 72 : 0.85,
         73 : -0.12, 74 :  0.85, 75 : 0.26,
         76 :  1.40, 77 :  1.38, 78 : 1.62,
         79 :  0.92, 80 :  1.17, 81 : 0.90,
         82 :  1.75, 83 :  0.65}

    for anum in list(x.keys()):
        x[anum_to_asym[anum]] = x[anum]

    return x


def _set_molecular_weight_dictionary():

    x = { 1 : 1.0079, 2 : 4.0026, 3: 6.941, 4: 9.0122,
          5 : 10.811, 6 : 12.0107, 7 : 14.0067, 8 : 15.9994,
          9 : 18.9984, 10 : 20.1797, 11 : 22.9897, 12 : 24.305,
         13 : 26.9815, 14 : 28.0855, 15 : 30.9738, 16 : 32.065,
         17 : 35.453,  18 : 39.948, 19 : 39.098, 20 : 40.078,
         21 : 44.955912, 22 : 47.867, 23 : 50.9415, 24 : 51.9961,
         25 : 54.938045, 26 : 55.845, 27 : 58.933195, 28 : 58.6934,
         29 : 63.546, 30 : 65.38, 31 : 69.723, 32 : 72.64, 33 : 74.9216,
         34 : 78.96, 35 : 79.904, 36 : 83.798, 37 : 85.4678, 38 : 87.62,
         39 : 88.90585, 40 : 91.224, 41 : 92.90638, 42 : 95.96, 43 : 97.9072,
         44 : 101.07, 45 : 102.90550, 46 : 106.42, 47 : 107.8682,
         48 : 112.411, 49 : 114.818, 50 : 118.710, 51 : 121.760,
         52 : 127.60, 53 : 126.90447, 54 : 131.293, 55 : 132.9054519,
         56 : 137.327, 57 : 138.90547, 58 : 140.116, 59 : 140.90765,
         60 : 144.242, 61 : 145.0, 62 : 150.36, 63 : 151.964, 64 : 157.25,
         65 : 158.92535, 66 : 162.500, 67 : 164.93032, 68 : 167.259,
         69 : 168.93421, 70 : 173.054, 71 : 174.9668, 72 : 178.49,
         73 : 180.94788, 74 : 183.84, 75 : 186.207, 76 : 190.23, 77 : 192.217,
         78 : 195.084, 79 : 196.966569, 80 : 200.59, 81 : 204.3833,
         82 : 207.2, 83 : 208.98040}

    # double up with element names
    for anum in list(x.keys()):
        x[anum_to_asym[anum]] = x[anum]

    return x


class constants:
    """ 
    Helpful contants. In cgs or cgs conversions 
    except ionization energies (eV)
    """

    def __init__(self):
        self.eV_erg  = 6.24150934326E11
        self.k_boltz = 1.380658E-16
        self.c       = 2.99792458E10
        self.h       = 6.6260755E-27
        self.G       = 6.6743E-8
        self.Msun = 1.998E33 # solar masses in cgs
        self.Rsun = 69.63E9  # solar radius in cgs
        self.Lsun = 3.9E33   # solar luminosity in cgs
        self.Tsun = 5777.0   # solar temperature in cgs
        self.tau_sun = 10.0E9 * 3.1536E7 # solar lifetime in cgs
        self.E_HI    = 13.6 # eV
        self.E_HeI   = 24.587
        self.m_p     = 1.6726219E-24

        self.Zsolar_ostar  = 0.01700 # Grevesse & Sauval 1998 - used in OSTAR2002
        self.Zsolar_parsec = 0.01524     # Caffau et. al. 2009 / 2011 - used in PARSEC SE code

        self.Zsolar_s99    = 0.02 # starburst 99 

        self.black_body_q0  = [0.1,  3.2]
        self.black_body_q1  = [0.001, 4.0]
        self.black_body_fuv = [1.,1.] #[1.0E-4, 2.3E-5]
        self.black_body_LW  = [1.,1.] #[5.0E-5, 5.0E-6]
      
        self.yr_to_s = 3.16224E7
        self.Myr     = self.yr_to_s * 1.0E6

        self.km      = 1.0E5
        self.pc      = 3.0865677E18
        self.kpc     = 1.0E3 * self.pc
        self.Mpc     = 1.0E3 * self.kpc

        self.solar_abundance = _set_abundance_dictionary()
        self.molecular_weight = _set_molecular_weight_dictionary()
        self.amu = 1.66054E-24 # amu to g

        return None

    @property
    def hubble_time(self, H_o = 70.0, z = 0.0):

        tau = 1.0 / H_o

        return tau * self.Mpc / self.km

CONST = constants()

