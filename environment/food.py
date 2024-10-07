# environment/food.py

import numpy as np

class Food:
    def __init__(self, position=None, energy_value=50.0):
        self.position = np.array(position) if position is not None else np.random.uniform(0, 100, size=3)
        self.energy_value = energy_value
        self.consumed = False
