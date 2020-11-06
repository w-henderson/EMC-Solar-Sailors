##### EMC SOLAR SAILORS - COORDINATE SYSTEMS #####
# Programming by William Henderson and Elliot Whybrow
# Physics and maths by Frankie Lambert, Ella Ireland-Carson and Ollie Temple
# https://www.exetermathematicsschool.ac.uk/exeter-mathematics-certificate/

import math

from .constants import Constants

# Vector class, used for screen space coordinate system and for physics manipulation
class Vector:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.magnitude = math.sqrt(x**2 + y**2) # Pythagoras for the magnitude
        self.normalized = self if self.magnitude == 1 or self.magnitude == 0 else Vector(x/self.magnitude, y/self.magnitude)

    # Convert to different classes
    def toTuple(self):
        return (self.x,self.y) # Simple (x,y) tuple
    def toPoint(self,size=10):
        return (self.x - size, self.y - size, self.x + size, self.y + size) # Point tuple (x1,y1,x2,y2) for rendering
    def toHeliocentric(self):
        positionRelativeToSun = self - Sun.position
        distance = positionRelativeToSun.magnitude / Constants.cameraScale # AU
        long = math.atan(positionRelativeToSun.x / positionRelativeToSun.y) * (180 / math.pi)
        return Heliocentric(long,distance)
    def toPerpendicular(self):
        return Vector(self.y, -self.x)

    # Special methods to manipulate the vector
    def __add__(self,b):
        return Vector(self.x+b.x, self.y+b.y)
    def __sub__(self,b):
        return Vector(self.x-b.x, self.y-b.y)
    def __mul__(self,b):
        return Vector(self.x*b, self.y*b)
    def __truediv__(self,b):
        return Vector(self.x/b, self.y/b)
    def __eq__(self,b):
        return self.toTuple() == b.toTuple()
    def __repr__(self):
        return "Vector({},{})".format(self.x, self.y)

class Sun:
    position = Vector(960,540) # Position of sun in screen space

# Heliocentric class
class Heliocentric:
    def __init__(self,long,distance):
        self.long = long # In degrees
        self.distance = distance # In Astronomical Units

    # Pythagoras to convert to a screen space vector
    def toVector(self):
        sin = math.sin(math.radians(self.long)) # Sine of hypotenuse
        cos = math.cos(math.radians(self.long)) # Cosine of hypotenuse
        distance = self.distance # Distance from the sun, measured in Astronomical Units, equal to about 150 million km
        positionRelativeToSun = Vector(distance * sin, distance * cos) # Position of planet relative to sun
        return Sun.position + positionRelativeToSun * Constants.cameraScale # Position of planet in screen space

    def __eq__(self,b):
        return round(self.long,3) == round(b.long,3) and round(self.distance,3) == round(b.distance,3)
    def __repr__(self):
        return "Heliocentric(long={}, distance={})".format(self.long, self.distance)