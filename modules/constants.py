##### EMC SOLAR SAILORS - CONSTANTS #####
# Programming by William Henderson and Elliot Whybrow
# Physics and maths by Frankie Lambert, Ella Ireland-Carson and Ollie Temple
# https://www.exetermathematicsschool.ac.uk/exeter-mathematics-certificate/

class Constants:
    planetMasses = {
        "Sun": 1.989e30,
        "Mercury": 3.285e23,
        "Venus": 4.867e24,
        "Earth": 5.972e24,
        "Mars": 6.39e23,
        "Jupiter": 1.898e27,
        "Saturn": 5.683e26,
        "Uranus": 8.681e25,
        "Neptune": 1.024e26,
        "Pluto": 1.309e22,
        "Ceres": 8.958e20,
        "Chiron": 4e15,
        "Eris": 1.66e22
    }

    cameraScale = 250

    G = 6.67408e-11 # Gravitational constant
    h = 6.62607004e-34 # Planck's constant
    c = 299792458 # Speed of light

    sunPower = 3.846e26 # Power of the sun in watts
    metresInAU = 1.496e11 # Number of metres in 1 AU
    moonHeight = 384402000 # Moon distance in metres
    moonHeightScreenSpace = (moonHeight / metresInAU) * cameraScale
    earthSpeed = 29780 # Earth's speed relative to the Sun in m/s
    earthSpeedScreenSpace = (earthSpeed / metresInAU) * cameraScale