import math

class Vector:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.magnitude = math.sqrt(x**2 + y**2)
        self.normalized = self if self.magnitude == 1 or self.magnitude == 0 else Vector(x/self.magnitude, y/self.magnitude)

    def toTuple(self):
        return (self.x,self.y)
    def toPoint(self,size=10):
        return (self.x - size, self.y - size, self.x + size, self.y + size) # (x1,y1,x2,y2)
    def toHeliocentric(self,scale):
        # need to make reverse function of Heliocentric.toVector
        return

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

class Heliocentric:
    def __init__(self,long,distance,scale):
        self.long = long
        self.distance = distance
        self.scale = scale

    def toVector(self):
        sin = math.sin(math.radians(self.long)) # Sine of hypotenuse
        cos = math.cos(math.radians(self.long)) # Cosine of hypotenuse
        distance = self.distance # Distance from the sun, measured in Astronomical Units, equal to about 150 million km
        positionRelativeToSun = Vector(distance * sin, distance * cos) # Position of planet relative to sun
        return Sun.position + positionRelativeToSun * self.scale # Position of planet in screen space