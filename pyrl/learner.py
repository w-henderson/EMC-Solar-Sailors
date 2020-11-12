import random

class Learner:
    def __init__(self):
        self.agents = []
        self.iterations = 0
    def add(self, agent, count=1):
        for _ in range(count):
            self.agents.append(agent.clone())
    def tick(self, subCallback):
        self.agents.sort(key=lambda x: x.score(), reverse=True)
        self.agents = self.agents[0:len(self.agents)//2]
        for i in range(len(self.agents)):
            self.agents.append(self.agents[i].clone())
        for i in range(len(self.agents)):
            if subCallback != None: subCallback(self, (i+1)/len(self.agents))
            self.agents[i].mutate()
        self.iterations += 1
    def iterate(self, iterations, callback=None, subCallback=None):
        for _ in range(iterations):
            self.tick(subCallback=subCallback)
            if callback != None: callback(self)

class Agent:
    def __init__(self, variableDict, rewardCallback, exploration, masterMutability=1, mutabilityMultiplierPerIteration=1):
        self.variables = {}
        for var in variableDict.keys():
            self.variables[var] = variableDict[var].clone()
        self.rewardCallback = rewardCallback
        self.exploration = exploration
        self.masterMutability = masterMutability
        self.mutabilityMultiplierPerIteration = mutabilityMultiplierPerIteration
        self.lastScore = -1e18
        self.currentScore = -1e18

    def score(self):
        return self.currentScore
    def mutate(self):
        if random.random() < self.exploration:
            self.lastScore = self.currentScore
            for variable in self.variables.keys():
                self.variables[variable].mutate(self.masterMutability)
            self.currentScore = self.rewardCallback(self)
        else:
            for variable in self.variables.keys():
                self.variables[variable].exploit(self.currentScore > self.lastScore, self.masterMutability)
            self.lastScore = self.currentScore
            self.currentScore = self.rewardCallback(self)
        self.masterMutability *= self.mutabilityMultiplierPerIteration
    def clone(self):
        return Agent(self.variables, self.rewardCallback, self.exploration, self.masterMutability, self.mutabilityMultiplierPerIteration)
    def __repr__(self):
        return repr(self.variables)