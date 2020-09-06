##### EMC SOLAR SAILORS - Photons #####
# Programming by William Henderson and Elliot Whybrow
# Physics and maths by Frankie Lambert, Ella Ireland-Carson and Ollie Temple
# https://www.exetermathematicsschool.ac.uk/exeter-mathematics-certificate/

import argparse
h = float(6.62607004e-34) #Plank's Constant
c = float(299792458) #Speed of light
PowerSun = float(3.846e26) #Power output of the sun in watts

parser = argparse.ArgumentParser(description="Energy of a single photons for a given wavelength and how many photons are emmitted by the sun per second")
parser.add_argument("wavelength", type=float, help="wavelength of light in nm")
args = parser.parse_args()

wavelength = args.wavelength * 1e-9
E1=float(h*c/wavelength)
print("Energy of one photon = " + str(E1) + " J")
PhotonsPerSec = float(PowerSun/E1)
print("Photons emmited by the sun per second = "+ str(PhotonsPerSec))