from coordinateSystems import Vector

class SolarSail:
    def __init__(self,mass,sailSize,sailRotation,position): # mass=float>0, sailSize=float>0, sailRotation=float(0-360)
        self.mass = mass
        self.sailSize = sailSize
        self.sailRotation = sailRotation
        self.force = Vector(0,0)
        self.velocity = Vector(0,0)
        self.position = position
    
    def addForce(self,force): # force=Vector
        self.force += force

    def updatePosition(self,acceleration,simulatedSecondsSinceLastUpdate):
        self.position += self.velocity*simulatedSecondsSinceLastUpdate + acceleration*0.5*(simulatedSecondsSinceLastUpdate**2) # s = vt + 0.5at^2
        self.velocity += acceleration * simulatedSecondsSinceLastUpdate # v = u + at
        self.force = Vector(0,0)