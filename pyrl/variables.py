import random

class Float:
    def __init__(self, value, mutability, _min=None, _max=None):
        self.value = value # Float value of the object, unlimited float
        self.mutability = mutability # How far it can mutate either way if chosen to, unlimited float
        self.lastChangeDirection = 1
        self._min = _min
        self._max = _max

    def clone(self):
        return Float(self.value, self.mutability)
    def mutate(self, masterMutability):
        change = (0.5 - random.random()) * self.mutability * masterMutability
        self.lastChangeDirection = 1 if change > 0 else -1
        self.value += change
        if self._min != None:
            if self.value < self._min:
                self.value = self._min
        if self._max != None:
            if self.value > self._max:
                self.value = self._max
    def exploit(self, lastMoveGood, masterMutability):
        if lastMoveGood:
            self.value += random.random() * self.mutability * masterMutability * self.lastChangeDirection
        else:
            self.value += random.random() * self.mutability * masterMutability * -self.lastChangeDirection
        if self._min != None:
            if self.value < self._min:
                self.value = self._min
        if self._max != None:
            if self.value > self._max:
                self.value = self._max

    def __repr__(self):
        return str(self.value)