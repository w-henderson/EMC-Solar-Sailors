![Banner](images/banner.png)

# EMC Solar Sailors
EMC Solar Sailors is a project from Exeter Mathematics School in which we are designing a spacecraft to harness the power of photons to get to Mars. This repo contains the code for our simulations and calculations.

See the latest simulation demo on Streamable: [https://streamable.com/l6im9k](https://streamable.com/l6im9k).

## Usage
Run `python main.py <launchDate>` for a quick simulation without changing any parameters. Launch date is required and should be provided in the format `dd/mm/yyyy`. The optional parameters are as follows:
- `--mass` (float): mass of the spacecraft in kg, defaults to 1000
- `--sailSize` (float): size of the sail in m^2, defaults to 32
- `--calculationsPerDay` (int): number of calculations to simulate per day, defaults to 24. The more calculations, the higher the accuracy. Don't go below 24.
- `--simulationLength` (int): number of days to simulate for, defaults to 365.
- `--accountForPlanets` (switch/bool): whether to account for gravitational fields other than the sun's, False if not specified. This greatly increases the simulation time but may increase accuracy by about 0.015%.
- `--lossless` (switch/bool): whether to use lossless compression, False if not specified. Lossless compression (png rather than jpeg) takes twice as long to render but may improve image quality.

### Example Code
This is what I've been using to test the latest commit with a calculation every second.
```py
python main.py 11/09/2020 --calculationsPerDay 1440
```

# Credits

## Programming
- [William Henderson](https://github.com/w-henderson)
- [Elliot Whybrow](https://github.com/flauntingspade4)

## Physics and Maths
- Frankie Lambert
- Ella Ireland-Carson
- [Ollie Temple](https://github.com/olivertemple) (who also worked on `photons.py`)