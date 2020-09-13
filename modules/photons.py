##### EMC SOLAR SAILORS - Photons #####
# Programming by William Henderson and Elliot Whybrow
# Physics and maths by Frankie Lambert, Ella Ireland-Carson and Ollie Temple
# https://www.exetermathematicsschool.ac.uk/exeter-mathematics-certificate/

from .constants import Constants

class Photon:
    def __init__(self,wavelength):
        self.wavelength = wavelength
        wavelengthInM = wavelength * 1e-9
        self.energy = (Constants.h * Constants.c) / wavelengthInM
        self.perSecond = Constants.sunPower / self.energy
