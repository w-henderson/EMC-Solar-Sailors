##### EMC SOLAR SAILORS - Photons #####
# Programming by William Henderson and Elliot Whybrow
# Physics and maths by Frankie Lambert, Ella Ireland-Carson and Ollie Temple
# https://www.exetermathematicsschool.ac.uk/exeter-mathematics-certificate/

from .constants import Constants
from math import pi

class Photon:
    def __init__(self,wavelength):
        self.wavelength = wavelength
        wavelengthInM = wavelength * 1e-9
        self.energy = (Constants.h * Constants.c) / wavelengthInM
        self.perSecond = Constants.sunPower / self.energy
        self.momentum = Constants.h / self.wavelength # in kg.m/s
    
    def collisionsAtPosition(self,area,distance):
        perSqM = self.perSecond / (4 * pi * distance**2)
        return perSqM * area