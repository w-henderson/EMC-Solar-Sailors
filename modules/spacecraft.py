##### EMC SOLAR SAILORS - SOLAR SAIL #####
# Programming by William Henderson and Elliot Whybrow
# Physics and maths by Frankie Lambert, Ella Ireland-Carson and Ollie Temple
# https://www.exetermathematicsschool.ac.uk/exeter-mathematics-certificate/

from .coordinateSystems import Vector
from .constants import Constants
from .photons import Photon

import math

class SolarSail:
    def __init__(self,mass,sailSize,sailRotation,position): # mass=float>0, sailSize=float>0, sailRotation=float(0-360)
        self.mass = mass # In KG
        self.sailSize = sailSize # In metres
        self.sailRotation = sailRotation # In degrees from north
        self.force = Vector(0,0)
        self.velocity = Vector(0,0) # In AU/s
        self.position = position
    
    def addForce(self,force): # force=Vector, should be in Newtons I think...
        self.force += (force / Constants.metresInAU) * Constants.cameraScale

    def updatePosition(self,acceleration,simulatedSecondsSinceLastUpdate):
        self.position += self.velocity*simulatedSecondsSinceLastUpdate + acceleration*0.5*(simulatedSecondsSinceLastUpdate**2) # s = vt + 0.5at^2
        self.velocity += acceleration * simulatedSecondsSinceLastUpdate # v = u + at
        self.force = Vector(0,0) # reset force

    def areaFacingSun(self):
        positionHeliographic = self.position.toHeliocentric()
        rot = self.sailRotation if self.sailRotation < 180 else self.sailRotation - 180
        return (self.sailSize * math.sin((positionHeliographic.long - rot) * (math.pi / 180))) ** 2

    def toPoint(self, renderSize):
        cornerPosition = Vector(math.sin(self.sailRotation * (math.pi / 180)) * -5, math.cos(self.sailRotation * (math.pi / 180)) * 5)
        topRight = self.position + cornerPosition * renderSize
        bottomLeft = self.position - cornerPosition * renderSize
        point = (topRight.x, topRight.y, bottomLeft.x, bottomLeft.y)
        return point