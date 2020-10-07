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
        self.momentum = Constants.h / wavelengthInM # in kg.m/s
    
    def collisionsAtPosition(self,area,distance):
        perSqM = self.perSecond / (4 * pi * distance**2)
        return perSqM * area

class GeneralSunPhoton:
    def __init__(self):
        photonOfEachWavelength = [Photon(wavelength) for wavelength in range(1,2500)]

        # Trapezium rule to calculate area
        totalArea = 0
        for i in range(2498):
            sideL = photonOfEachWavelength[i].perSecond
            sideR = photonOfEachWavelength[i + 1].perSecond
            width = 1
            area = ((sideL + sideR) / 2) * width
            totalArea += area
        
        self.perSecond = totalArea
        self.momentum = Constants.h / (700 * 1e-9)
        
    def collisionsAtPosition(self,area,distance):
        perSqM = (area * self.perSecond) / (4 * pi * distance**2)
        return perSqM