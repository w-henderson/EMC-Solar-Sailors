##### EMC SOLAR SAILORS #####
# Programming by William Henderson and Elliot Whybrow
# Physics and maths by Frankie Lambert, Ella Ireland-Carson and Ollie Temple
# https://www.exetermathematicsschool.ac.uk/exeter-mathematics-certificate/

import solarsystem # To get planet position data for different dates
import datetime # To parse and manipulate dates
import argparse # To parse arguments
import shutil # To recursively remove output directory
import math # To do trigonometry
import os # To make output directory

from PIL import Image, ImageDraw, ImageFont # To render images
from coordinateSystems import Vector, Heliocentric, Sun # Custom classes for coordinate systems

simulationScale = 250

parser = argparse.ArgumentParser(description="Solar Sailors EMC Project")
parser.add_argument("date", type=str, help="The date to launch.") # format dd/mm/yyyy
parser.add_argument("mass", type=float, help="Mass of the spacecraft.")
args = parser.parse_args()

dateParts = args.date.split("/")
launchDate = datetime.datetime(int(dateParts[2]),int(dateParts[1]),int(dateParts[0]),12)

# Parse solar system object with given datetime into dictionary of Heliocentric coordinate system objects
def datetimeToPositions(dt):
    solarSystemObject = solarsystem.heliocentric.Heliocentric(year=dt.year, month=dt.month, day=dt.day, hour=dt.hour, minute=dt.minute)
    solarSystemObject = solarSystemObject.planets()
    solarSystemHeliocentric = {}
    for planet in solarSystemObject.keys():
        planetObject = solarSystemObject[planet] # tuple of (longitude, latitude, distance)
        solarSystemHeliocentric[planet] = Heliocentric(planetObject[0], planetObject[2], simulationScale)
    return solarSystemHeliocentric

# Render frame of the simulation
def render():
    image = Image.new("RGB", Vector(1920,1080).toTuple())
    font = ImageFont.truetype("font_inter.otf",20)
    draw = ImageDraw.Draw(image)

    draw.ellipse(Sun.position.toPoint(size=25), fill="yellow") # Render sun
    draw.text((0,0), "Date: "+currentSimulatedDate.strftime("%d/%m/%y"), fill="red", font=font) # Render info text
    
    for planet in planets.keys():
        draw.ellipse(planets[planet].toVector().toPoint(), fill="white")
        draw.text(planets[planet].toVector().toTuple(), planet, fill="red", font=font)
    image.save("simulationOutput/frame"+str(currentFrame).zfill(4)+".png")

planets = {}
currentSimulatedDate = 0
currentFrame = 0

def simulate(startDate,cutoff=365): # Launch date is a datetime object and cutoff is the number of days to simulate
    global planets
    global currentSimulatedDate
    global currentFrame

    if "simulationOutput" in os.listdir(): shutil.rmtree("simulationOutput")
    os.mkdir("simulationOutput")

    for date in (startDate + datetime.timedelta(n) for n in range(cutoff)):
        planets = datetimeToPositions(date)
        currentSimulatedDate = date
        currentFrame += 1
        render()
        print("Rendered simulation for "+date.strftime("%d/%m/%y")+"...", end="\r")

    os.system('ffmpeg -i "simulationOutput/frame%04d.png" -r 30 simulation.avi')

simulate(launchDate)