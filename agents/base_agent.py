# agents/base_agent.py

import torch
import numpy as np
from agents.dna import DNA
from utils.helpers import distance
from utils.logger import get_logger

class BaseAgent:
    def __init__(self, dna=None, position=None, energy=100.0, config=None):
        self.logger = get_logger(self.__class__.__name__)
        self.dna = dna or DNA()
        self.position = np.array(position) if position is not None else np.random.uniform(0, config['simulation']['container_size'], size=3)
        self.velocity = np.zeros(3)
        self.energy = energy
        self.alive = True
        self.config = config

        # Traits influenced by DNA
        self.speed = self.dna.traits['speed']
        self.size = self.dna.traits['size']
        self.vision_range = self.dna.traits['vision_range']

        # PPO Model
        self.device = torch.device('cuda' if torch.cuda.is_available() and config['hardware']['use_cuda'] else 'cpu')
        self.model = None  # To be defined in subclasses
        self.optimizer = None

        # Initialize model in subclasses

    def perceive(self, environment):
        """Perceive the environment and return observations."""
        raise NotImplementedError

    def decide(self, observations):
        """Decide on an action based on observations."""
        raise NotImplementedError

    def act(self, action):
        """Update agent's state based on the chosen action."""
        # Assuming action is a 3D vector with values between -1 and 1
        self.velocity = action * self.speed
        self.position += self.velocity * self.config['simulation']['time_step']

        # Ensure the agent stays within the container
        self.position = np.clip(self.position, 0, self.config['simulation']['container_size'])

    def consume_energy(self):
        """Consume energy based on movement and metabolism."""
        movement_cost = np.linalg.norm(self.velocity) * self.config['agent']['energy']['movement_cost_factor']
        self.energy -= (movement_cost + self.config['agent']['energy']['metabolism_rate'])

        if self.energy <= 0:
            self.alive = False
            self.logger.info(f"Agent died due to energy depletion.")

    def reproduce(self):
        """Reproduce and create offspring with inherited DNA."""
        child_dna = self.dna.inherit()
        child_position = self.position + np.random.uniform(-1, 1, size=3)  # Slight position offset
        return self.__class__(dna=child_dna, position=child_position, config=self.config)

    def update(self, environment):
        """Update the agent's state."""
        if not self.alive:
            return

        observations = self.perceive(environment)
        action = self.decide(observations)
        self.act(action)
        self.consume_energy()
