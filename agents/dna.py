# agents/dna.py

import random
from utils.helpers import clamp

class DNA:
    def __init__(self, traits=None, mutation_rate=0.01):
        self.traits = traits or {
            'speed': random.uniform(1.0, 5.0),
            'size': random.uniform(0.5, 2.0),
            'vision_range': random.uniform(5.0, 15.0),
        }
        self.mutation_rate = mutation_rate

    def mutate(self):
        for trait in self.traits:
            if random.random() < self.mutation_rate:
                mutation = random.uniform(-0.1, 0.1)  # Mutation magnitude
                self.traits[trait] += mutation
                # Clamp the values within acceptable ranges
                if trait == 'speed':
                    self.traits[trait] = clamp(self.traits[trait], 1.0, 5.0)
                elif trait == 'size':
                    self.traits[trait] = clamp(self.traits[trait], 0.5, 2.0)
                elif trait == 'vision_range':
                    self.traits[trait] = clamp(self.traits[trait], 5.0, 15.0)

    def inherit(self):
        # Create a copy of traits with possible mutations
        child_traits = self.traits.copy()
        child_dna = DNA(traits=child_traits, mutation_rate=self.mutation_rate)
        child_dna.mutate()
        return child_dna
