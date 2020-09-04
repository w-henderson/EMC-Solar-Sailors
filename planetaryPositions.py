import solarsystem
import datetime
import argparse
import math
from PIL import Image

from vector import Vector

parser = argparse.ArgumentParser(description="Solar Sailors EMC Project")
parser.add_argument("date", type=str, help="The date to launch.") # format dd/mm/yyyy
parser.add_argument("mass", type=float, help="Mass of the spacecraft.")
args = parser.parse_args()

dateParts = args.date.split("/")
date = datetime.datetime(int(dateParts[2]),int(dateParts[1]),int(dateParts[0]),12)

def datetimeToPositions(dt):
    return solarsystem.heliocentric.Heliocentric(year=dt.year, month=dt.month, day=dt.day, hour=dt.hour, minute=dt.minute)

def heliocentricToXY(heliocentric,scale):
    sin = math.sin(math.radians(heliocentric[0]))
    cos = math.cos(math.radians(heliocentric[1]))
    distance = heliocentric[1] # Measured in Astronomical Units, equal to about 150 million km
    sunPosition = Vector(960,540)
    positionRelativeToSun = Vector(distance * sin, distance * cos)
    screenPosition = sunPosition + positionRelativeToSun * scale

def render():
    image = Image.new("RGB", Vector(1920,1080).toTuple())
    for planet in planets.keys():
        planets[planet]

planetPositionsObject = datetimeToPositions(date)
planets = planetPositionsObject.planets()

print(planets)