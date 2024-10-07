# utils/helpers.py

import numpy as np

def distance(a, b):
    return np.linalg.norm(a - b)

def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))
