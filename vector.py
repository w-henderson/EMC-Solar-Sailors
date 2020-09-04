import math

class Vector:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.magnitude = math.sqrt(x^2 + y^2)
        self.normalized = Vector(x/self.magnitude, y/self.magnitude)
    def toTuple(self):
        return (self.x,self.y)
    def __add__(self,b):
        return Vector(self.x+b.x, self.y+b.y)
    def __sub__(self,b):
        return Vector(self.x-b.x, self.y-b.y)
    def __mul__(self,b):
        return Vector(self.x*b, self.y*b)
    def __div__(self,b):
        return Vector(self.x/b, self.y/b)