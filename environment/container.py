# environment/container.py

import numpy as np
from utils.helpers import clamp

class Container:
    def __init__(self, size):
        self.size = np.array(size)  # [Width, Height, Depth]

    def enforce_bounds(self, position):
        # Ensure the position is within the container bounds
        return clamp(position, 0, self.size)
