##### EMC SOLAR SAILORS - COORDINATE SYSTEMS #####
# Programming by William Henderson and Elliot Whybrow
# Physics and maths by Frankie Lambert, Ella Ireland-Carson and Ollie Temple
# https://www.exetermathematicsschool.ac.uk/exeter-mathematics-certificate/

import math

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
    def toHeliocentric(self,scale):
        # In development, will return heliocentric equivalent of the screen space vector
        return

    # Special methods to manipulate the vector
    def __add__(self,b):
        return Vector(self.x+b.x, self.y+b.y)
    def __sub__(self,b):
        return Vector(self.x-b.x, self.y-b.y)
    def __mul__(self,b):
        return Vector(self.x*b, self.y*b)
    def __truediv__(self,b):
        return Vector(self.x/b, self.y/b)

class Sun:
    position = Vector(960,540) # Position of sun in screen space

# Heliocentric class
class Heliocentric:
    def __init__(self,long,distance,scale):
        self.long = long
        self.distance = distance
        self.scale = scale

    # Pythagoras to convert to a screen space vector
    def toVector(self):
        sin = math.sin(math.radians(self.long)) # Sine of hypotenuse
        cos = math.cos(math.radians(self.long)) # Cosine of hypotenuse
        distance = self.distance # Distance from the sun, measured in Astronomical Units, equal to about 150 million km
        positionRelativeToSun = Vector(distance * sin, distance * cos) # Position of planet relative to sun
        return Sun.position + positionRelativeToSun * self.scale # Position of planet in screen space