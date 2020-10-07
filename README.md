![Banner](images/banner.png)

# EMC Solar Sailors
EMC Solar Sailors is a project from Exeter Mathematics School in which we are designing a spacecraft to harness the power of photons to get to Mars. This repo contains the code for our simulations and calculations.

See the latest simulation demo on Streamable: [https://streamable.com/j7htrl](https://streamable.com/j7htrl).

## Usage
Run `python main.py <launchDate>` for a quick simulation without changing any parameters. Launch date is required and should be provided in the format `dd/mm/yyyy`. The optional parameters are as follows:
- `--mass` (float): mass of the spacecraft in kg, defaults to 1000
- `--sailSize` (float): side length of the sail in metres, defaults to 10
- `--calculationsPerDay` (int): number of calculations to simulate per day, defaults to 24. The more calculations, the higher the accuracy. Don't go below 24.
- `--simulationLength` (int): number of days to simulate for, defaults to 365.
- `--accountForPlanets` (switch/bool): whether to account for gravitational fields other than the sun's, False if not specified. This greatly increases the simulation time but may increase accuracy by about 0.015%.
- `--lossless` (switch/bool): whether to use lossless compression, False if not specified. Lossless compression (png rather than jpeg) takes twice as long to render but may improve image quality.
- `--exportAsJSON` (switch/bool): whether to export the simulation as JSON instead of a video, False if not specified. This is useful if you want to use Blender for rendering (see the "Using Blender for rendering" section) or to do more processing on the data afterwards.

### Example Code
This is what I've been using to test the latest commit with a calculation every second for a year.
```py
python main.py 06/10/2020 --mass 10 --sailSize 1000 --calculationsPerDay 1440
```

### Using Blender for rendering
A [Blender import script](https://github.com/w-henderson/EMC-Solar-Sailors/blob/master/modules/blenderImportScript.py) is included with this repo to make it easy to use Blender to improve the graphics of your simulation render. Here's how you'd go about generating a simulation and rendering it in Blender:
1. Generate your simulation the normal way, but make sure to pass the `--exportAsJSON` parameter. For example, you could run `python main.py 13/09/2020 --exportAsJSON` to use default parameters.
2. Open up Blender and go to the Scripting tab.
3. Copy and paste the contents of the [Blender import script](https://github.com/w-henderson/EMC-Solar-Sailors/blob/master/modules/blenderImportScript.py) into the code area.
4. Change the `filepath` variable to point to your simulated JSON file. Don't forget to use double backslashes between directories.
5. Press the triangular run button in the top right of the code area and your simulation will be imported into Blender for you to customise!

## Simulation Demo History
- [**11/09/2020**](https://streamable.com/l6im9k): implemented gravity so the sail orbits the Sun with the Earth
- [**25/09/2020**](https://streamable.com/7dkyk2): implemented first photon force so the sail is pushed by photons but the photons do not bounce off so the direction and magnitude are both inaccurate
- [**06/10/2020**](https://streamable.com/dx7v8b): implemented photon rebounding, simulation code is nearing completion
- [**07/10/2020**](https://streamable.com/j7htrl): fixed major bug with photon rebounding and added more information in the top left

# Credits

## Programming
- [William Henderson](https://github.com/w-henderson)
- [Elliot Whybrow](https://github.com/flauntingspade4)

## Physics and Maths
- [Frankie Lambert](https://github.com/Chrome599)
- Ella Ireland-Carson
- [Ollie Temple](https://github.com/olivertemple) (who also worked on `photons.py`)