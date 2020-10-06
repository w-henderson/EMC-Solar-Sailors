##### EMC SOLAR SAILORS - MAIN #####
# Programming by William Henderson and Elliot Whybrow
# Physics and maths by Frankie Lambert, Ella Ireland-Carson and Ollie Temple
# https://www.exetermathematicsschool.ac.uk/exeter-mathematics-certificate/

import solarsystem # To get planet position data for different dates
import datetime # To parse and manipulate dates
import argparse # To parse arguments
import shutil # To recursively remove output directory
import math # To do trigonometry
import time # To help improve efficiency
import os # To make output directory

from PIL import Image, ImageDraw, ImageFont # To render images
from modules.coordinateSystems import Vector, Heliocentric, Sun # Custom classes for coordinate systems
from modules.spacecraft import SolarSail # Custom class for solar sail
from modules.constants import Constants # Constants are stored in a separate file for readability
from modules.photons import Photon, GeneralSunPhoton # For calculations relating to photons

# Parse arguments
parser = argparse.ArgumentParser(description="Solar Sailors EMC Project")
parser.add_argument("date", type=str, help="Date to launch.") # format dd/mm/yyyy
parser.add_argument("--mass", type=float, default=1000.0, help="Mass of the spacecraft in km.")
parser.add_argument("--sailSize", type=float, default=10.0, help="Side length of the sail in metres.")
parser.add_argument("--sailRotation", type=float, default=0.0, help="Rotation of the sail in degrees.")
parser.add_argument("--calculationsPerDay", type=int, default=24, help="Calculations to perform per day. Higher number = higher accuracy of position.")
parser.add_argument("--simulationLength", type=int, default=365, help="Number of days to simulate.")
parser.add_argument("--accountForPlanets", action="store_true", help="Account for gravitational fields other than the sun.")
parser.add_argument("--lossless", action="store_true", help="Use lossless compression.")
parser.add_argument("--exportAsJSON", action="store_true", help="Export as JSON tracking data instead of a video.")
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
        solarSystemHeliocentric[planet] = Heliocentric(planetObject[0], planetObject[2])
    return solarSystemHeliocentric

# Render frame of the simulation
def render(planets, sail, date, frame, velocity, photonForce, forceDirection, colls):
    # Set up PIL image
    image = Image.new("RGB", Vector(1920,1080).toTuple())
    font = ImageFont.truetype("font_inter.otf",30)
    draw = ImageDraw.Draw(image)

    # Draw sun and info text
    draw.ellipse(Sun.position.toPoint(size=25), fill="yellow") # Render sun
    infoString = "\n".join([
        "Date: " + date.strftime("%d/%m/%y"),
        "Velocity: " + str(velocity.magnitude) + "m/s",
        "Photon force: " + str(photonForce.magnitude) + "N",
        "Area facing sun: " + str(sail.areaFacingSun()),
        "Collisions: " + str(colls)
    ])
    draw.text((0,0), infoString, fill="red", font=font) # Render info text
    
    # Draw sail and force arrow
    draw.line(sail.toPoint(8), fill="orange", width=4) # Draw line to represent sail
    draw.line((sail.position.x, sail.position.y, sail.position.x + forceDirection.x * photonForce.magnitude, sail.position.y + forceDirection.y * photonForce.magnitude), fill="red", width=4) # Draw line to represent force vector
    draw.text(sail.position.toTuple(), "SOLAR SAIL", fill="white", font=font) # Render sail text
    
    # Iterate through the planets and draw them
    for planet in planets.keys():
        draw.ellipse(planets[planet].toVector().toPoint(), fill="white") # Planet circle
        draw.text(planets[planet].toVector().toTuple(), planet, fill="red", font=font) # Planet name

    # Save the rendered image in appdata
    if args.lossless: image.save(os.getenv("APPDATA")+"\\EMCSS_simulationOutput\\frame"+str(frame).zfill(4)+".png", compress_level=1)
    else: image.save(os.getenv("APPDATA")+"\\EMCSS_simulationOutput\\frame"+str(frame).zfill(4)+".jpeg", quality=90)

tracks = []
def trackingExport(planets, sail):
    # Add tracks for sun and sail
    sailPosition = sail.position.toTuple()
    trackThisFrame = {
        "Sun": [0,0,0],
        "Sail": [sailPosition[0] - 960, sailPosition[1] - 540, 0] # Subtracts sun position because sun is central
    }

    # Iterate through planets and add their positions
    for planet in planets.keys():
        planetPosition = planets[planet].toVector().toTuple()
        trackThisFrame[planet] = [planetPosition[0] - 960, planetPosition[1] - 540, 0]

    # Add all the tracking data from this frame to the master track
    tracks.append(trackThisFrame)

# Run simulation
def simulate(startDate,cutoff=args.simulationLength): # Launch date is a datetime object and cutoff is the number of days to simulate
    # Set up output directory
    if "EMCSS_simulationOutput" in os.listdir(os.getenv("APPDATA")): shutil.rmtree(os.getenv("APPDATA")+"\\EMCSS_simulationOutput")
    os.mkdir(os.getenv("APPDATA")+"\\EMCSS_simulationOutput")
    currentFrame = 0
    totalRenderingTime = 0
    totalCalculatingTime = 0

    # Calculate earth's current direction to apply to sail
    earthPositionsBefore = [datetimeToPositions(startDate - datetime.timedelta(1/args.calculationsPerDay))["Earth"], datetimeToPositions(startDate)["Earth"]]
    earthVelocity = (earthPositionsBefore[1].toVector() - earthPositionsBefore[0].toVector()) / ((60 * 60 * 24) / args.calculationsPerDay)
    #sailRelativeToEarth = Vector(math.sin(math.radians(args.launchTrajectory)) * Constants.moonHeightScreenSpace, -math.cos(math.radians(args.launchTrajectory)) * Constants.moonHeightScreenSpace)
    launchPosition = earthPositionsBefore[1].toVector() # + sailRelativeToEarth

    # Set up solar sail with arguments
    solarSail = SolarSail(args.mass, args.sailSize, args.sailRotation, launchPosition)
    solarSail.velocity = earthVelocity

    photon = GeneralSunPhoton()

    # Loop through dates (one frame = one day for simplicity)
    for date in (startDate + datetime.timedelta(n) for n in range(cutoff)):
        timeBeforeCalculation = time.time()

        # Perform multiple calculations per day
        for calc in range(args.calculationsPerDay):
            date += datetime.timedelta(1 / args.calculationsPerDay)
            # Get planet positions at date
            planets = datetimeToPositions(date)

            # Iterate through planets and apply gravity from each one to the solar sail (disabled by default)
            if args.accountForPlanets:
                for planet in planets.keys():
                    r = (planets[planet].toVector() - solarSail.position).magnitude / Constants.cameraScale # measured in AU
                    r = r * Constants.metresInAU # Convert to metres
                    gravitationalForce = (Constants.G * args.mass * Constants.planetMasses[planet]) / r**2 # Gravitational force magnitude
                    solarSail.addForce((planets[planet].toVector() - solarSail.position).normalized * gravitationalForce)

            # Apply the sun's gravity
            sunDistance = (Sun.position - solarSail.position).magnitude / Constants.cameraScale # measured in AU
            sunDistance = sunDistance * Constants.metresInAU # Convert to metres
            sunGravitationalForce = (Constants.G * args.mass * Constants.planetMasses["Sun"]) / sunDistance**2
            solarSail.addForce((Sun.position - solarSail.position).normalized * sunGravitationalForce)

            # Calculate the force direction
            forceDirection1 = Vector(math.sin(math.radians(args.sailRotation)), math.cos(math.radians(args.sailRotation)))
            forceDirection2 = forceDirection1 * -1 # There are 2 possible directions (opposite directions along same line)
            further1 = solarSail.position + forceDirection1
            further2 = solarSail.position + forceDirection2
            distanceFromSun1 = (further1 - Sun.position).magnitude
            distanceFromSun2 = (further2 - Sun.position).magnitude

            # Choose which direction goes away from the sun
            forceDirection = forceDirection1 if distanceFromSun1 > distanceFromSun2 else forceDirection2

            # Apply force from photons
            location = ((solarSail.position - Sun.position) / Constants.cameraScale) * Constants.metresInAU
            colls = photon.collisionsAtPosition(solarSail.sailSize ** 2, location.magnitude)
            photonMomentumVector = forceDirection.normalized * 2 * photon.momentum * colls
            photonMomentumVector *= solarSail.areaFacingSun() / solarSail.sailSize ** 2 # Account for how much the sail is facing the sun
            solarSail.addForce(photonMomentumVector / ((60*60*24) / args.calculationsPerDay))

            # Calculate the acceleration and update the solar sail's position
            acceleration = solarSail.force / solarSail.mass
            solarSail.updatePosition(acceleration, (60*60*24) / args.calculationsPerDay)
            
        print("Calculated simulation up to "+date.strftime("%d/%m/%y")+", solar sail position was "+str(solarSail.position.toTuple())+"...", end="\r")
        totalCalculatingTime += time.time() - timeBeforeCalculation

        # Render or export the current frame
        currentFrame += 1
        timeBeforeRender = time.time()
        if not args.exportAsJSON: render(planets,solarSail,date,currentFrame,solarSail.velocity,photonMomentumVector,forceDirection,colls) # Standard render
        else: trackingExport(planets,solarSail) # Export JSON tracking data for Blender or more processing somewhere else
        totalRenderingTime += time.time() - timeBeforeRender
        
    if not args.exportAsJSON:
        # Use FFMPEG to convert the image sequence into a final mp4 video
        if args.lossless: os.system('ffmpeg -i "'+os.getenv("APPDATA")+'\\EMCSS_simulationOutput\\frame%04d.png" -framerate 30 -c:v libx264 -crf 22 simulation.mp4')
        else: os.system('ffmpeg -i "'+os.getenv("APPDATA")+'\\EMCSS_simulationOutput\\frame%04d.jpeg" -framerate 30 -c:v libx264 -crf 22 simulation.mp4')
    else:
        with open("simulation.json", "w") as f:
            f.write(repr(tracks).replace("'", '"')) # Quick and easy JSON export

    # Output metrics
    print("\nAverage render time: "+str(round(totalRenderingTime/currentFrame,2))+"s")
    print("Total time spent rendering: "+str(round(totalRenderingTime,2))+"s")
    print("Total time spent calculating: "+str(round(totalCalculatingTime,2))+"s")

# Start the simulation
if __name__ == "__main__":
    simulate(launchDate)