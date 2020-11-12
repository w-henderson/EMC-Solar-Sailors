# Import the required modules
from pyrl import learner, variables # PyRL to perform the learning
import datetime # To parse the start date
import math # To floor stuff
import main # Import main simulation information

# Initialise the learner
pyrlLearner = learner.Learner()

# Set the three variables it's using to floats
variables = {
    "sailRotation": variables.Float(135, 0.01, _min=0, _max=360),
    "mass": variables.Float(1100, 0.5, _min=1000),
    "sailSize": variables.Float(800, 0.5, _min=100, _max=800)
}

# Create a callback function to return the "reward" for an agent with certain properties
def callback(_agent):
    args = {
        "date": datetime.datetime(2020, 12, 17, 12),
        "mass": _agent.variables["mass"].value,
        "materialMass": 2.6,
        "sailSize": _agent.variables["sailSize"].value,
        "sailRotation": _agent.variables["sailRotation"].value,
        "calculationsPerDay": 24,
        "simulationLength": 500,
        "accountForPlanets": False,
        "lossless": False,
        "exportAsJSON": False
    }
    distanceFromMars = main.simulate(args["date"], args, getClosest=True)
    return -distanceFromMars

# Initialise the PyRL agent with the variables, callback, and exploration value
agent = learner.Agent(
    variableDict = variables,
    rewardCallback = callback,
    exploration = 0.5, # This indicates how likely the agent is each iteration to "explore" rather than "exploit", meaning how likely it is to randomly change values instead of trying to change values to improve
    mutabilityMultiplierPerIteration = 0.995
)

# Add 64 agents to the learner object
pyrlLearner.add(agent, count = 32)

def _callback(_learner, progress):
    print("Iteration {} - [{}{}] {}% - Best distance {}m".format(
        str(_learner.iterations+1).zfill(4),
        "#" * math.floor(progress * 25),
        " " * math.ceil((1 - progress) * 25),
        str(round(progress * 100)).zfill(3),
        round(-_learner.agents[0].currentScore)
    ), end="                \r")

# Perform 256 iterations on the learner object, calling the information callback each time
# THIS WILL TAKE > 12 HOURS, DON'T EXPECT IT TO BE QUICK
try:
    pyrlLearner.iterate(256, subCallback=_callback)
except KeyboardInterrupt:
    pass

print("""After {} iterations, the most beneficial attributes have been calculated to be:
sailRotation = {} degrees
mass = {} kilograms
sailSize = {} metres (side length)""".format(
    pyrlLearner.iterations,
    pyrlLearner.agents[0].variables["sailRotation"].value,
    pyrlLearner.agents[0].variables["mass"].value,
    pyrlLearner.agents[0].variables["sailSize"].value
))