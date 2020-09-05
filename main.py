##### EMC SOLAR SAILORS - MAIN #####
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
from spacecraft import SolarSail # Custom class for solar sail
from constants import Constants # Constants are stored in a separate file for readability

# Parse arguments
parser = argparse.ArgumentParser(description="Solar Sailors EMC Project")
parser.add_argument("date", type=str, help="Date to launch.") # format dd/mm/yyyy
parser.add_argument("mass", type=float, help="Mass of the spacecraft in km.")
parser.add_argument("sailSize", type=float, help="Area of the sail in m^2.")
parser.add_argument("sailRotation", type=float, help="Rotation of the sail in degrees.")
args = parser.parse_args()

# Parse date argument from dd/mm/yyyy to a datetime object
dateParts = args.date.split("/")
launchDate = datetime.datetime(int(dateParts[2]),int(dateParts[1]),int(dateParts[0]),12)

# Parse solar system object at given datetime into dictionary of Heliocentric coordinate system objects
def datetimeToPositions(dt):
    solarSystemObject = solarsystem.heliocentric.Heliocentric(year=dt.year, month=dt.month, day=dt.day, hour=dt.hour, minute=dt.minute)
    solarSystemObject = solarSystemObject.planets()
    solarSystemHeliocentric = {}
    for planet in solarSystemObject.keys():
        planetObject = solarSystemObject[planet] # tuple of (longitude, latitude, distance)
        solarSystemHeliocentric[planet] = Heliocentric(planetObject[0], planetObject[2], Constants.cameraScale)
    return solarSystemHeliocentric

# Render frame of the simulation
def render(planets,sail,date,frame,acceleration):
    # Set up PIL image
    image = Image.new("RGB", Vector(1920,1080).toTuple())
    font = ImageFont.truetype("font_inter.otf",30)
    draw = ImageDraw.Draw(image)

    # Draw simple objects (sun, sail and text)
    draw.ellipse(Sun.position.toPoint(size=25), fill="yellow") # Render sun
    draw.text((0,0), "Date: "+date.strftime("%d/%m/%y")+"\nAcceleration: "+str(acceleration.magnitude)+" m/s^2", fill="red", font=font) # Render info text
    draw.ellipse(sail.position.toPoint(size=5), fill="orange") # Render sail
    draw.text(sail.position.toTuple(), "SOLAR SAIL", fill="white", font=font) # Render sail text
    
    # Iterate through the planets and draw them
    for planet in planets.keys():
        draw.ellipse(planets[planet].toVector().toPoint(), fill="white") # Planet circle
        draw.text(planets[planet].toVector().toTuple(), planet, fill="red", font=font) # Planet name

    # Save the rendered image losslessly in appdata
    image.save(os.getenv("APPDATA")+"\\EMCSS_simulationOutput\\frame"+str(frame).zfill(4)+".png")

# Run simulation
def simulate(startDate,cutoff=365): # Launch date is a datetime object and cutoff is the number of days to simulate
    # Set up output directory
    if "EMCSS_simulationOutput" in os.listdir(os.getenv("APPDATA")): shutil.rmtree(os.getenv("APPDATA")+"\\EMCSS_simulationOutput")
    os.mkdir(os.getenv("APPDATA")+"\\EMCSS_simulationOutput")
    currentFrame = 0

    # Set up solar sail with arguments
    solarSail = SolarSail(args.mass, args.sailSize, args.sailRotation, Vector(600,500))
    solarSail.velocity = Vector(0,-2.5e-5) # THIS IS FOR TESTING, IN THE REAL SIMULATION WE WON'T SET AN INITIAL VELOCITY BECAUSE IT'S PHYSICALLY IMPOSSIBLE

    # Loop through dates (one frame = one day for simplicity)
    for date in (startDate + datetime.timedelta(n) for n in range(cutoff)):
        # Get planet positions at date
        planets = datetimeToPositions(date)

        # Iterate through planets and apply gravity from each one to the solar sail
        for planet in planets.keys():
            r = (planets[planet].toVector() - solarSail.position).magnitude / Constants.cameraScale # measured in AU
            r = r * Constants.metresInAU # Convert to metres
            gravitationalForce = (Constants.G * args.mass * Constants.planetMasses[planet]) / r**2 # Gravitational force magnitude
            solarSail.addForce((planets[planet].toVector() - solarSail.position).normalized * (gravitationalForce / Constants.metresInAU) * Constants.cameraScale)

        # Apply the sun's gravity
        sunDistance = (Sun.position - solarSail.position).magnitude / Constants.cameraScale # measured in AU
        sunDistance = sunDistance * Constants.metresInAU # Convert to metres
        sunGravitationalForce = (Constants.G * args.mass * Constants.planetMasses["Sun"]) / sunDistance**2
        solarSail.addForce((Sun.position - solarSail.position).normalized * (sunGravitationalForce / Constants.metresInAU) * Constants.cameraScale)

        # Calculate the acceleration and update the solar sail's position
        acceleration = solarSail.force / solarSail.mass
        solarSail.updatePosition(acceleration, 60*60*24)

        # Render the current frame
        currentFrame += 1
        render(planets,solarSail,date,currentFrame,acceleration)
        print("Rendered simulation for "+date.strftime("%d/%m/%y")+", solar sail position was "+str(solarSail.position.toTuple())+"...", end="\r")

    # Use FFMPEG to convert the image sequence into a final mp4 video
    os.system('ffmpeg -i "'+os.getenv("APPDATA")+'\\EMCSS_simulationOutput\\frame%04d.png" -framerate 30 -c:v libx264 -crf 22 simulation.mp4')

# Start the simulation
if __name__ == "__main__":
    simulate(launchDate)