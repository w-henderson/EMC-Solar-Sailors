##### EMC SOLAR SAILORS - SOLAR SAIL #####
# Programming by William Henderson and Elliot Whybrow
# Physics and maths by Frankie Lambert, Ella Ireland-Carson and Ollie Temple
# https://www.exetermathematicsschool.ac.uk/exeter-mathematics-certificate/

from coordinateSystems import Vector
from constants import Constants

class SolarSail:
    def __init__(self,mass,sailSize,sailRotation,position): # mass=float>0, sailSize=float>0, sailRotation=float(0-360)
        self.mass = mass # In KG
        self.sailSize = sailSize
        self.sailRotation = sailRotation
        self.force = Vector(0,0)
        self.velocity = Vector(0,0) # In AU/s
        self.position = position
    
    def addForce(self,force): # force=Vector, should be in Newtons I think...
        self.force += (force / Constants.metresInAU) * Constants.cameraScale

    def updatePosition(self,acceleration,simulatedSecondsSinceLastUpdate):
        self.position += self.velocity*simulatedSecondsSinceLastUpdate + acceleration*0.5*(simulatedSecondsSinceLastUpdate**2) # s = vt + 0.5at^2
        self.velocity += acceleration * simulatedSecondsSinceLastUpdate # v = u + at
        self.force = Vector(0,0) # reset force