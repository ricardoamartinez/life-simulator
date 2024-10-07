# agents/prey.py

import numpy as np
import torch
from agents.base_agent import BaseAgent
from models.ppo_agent import PPOAgent
from utils.helpers import distance
from utils.logger import get_logger

class Prey(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        input_dim = self.get_input_dim()
        action_dim = 3  # Movement in 3D
        self.model = PPOAgent(input_dim=input_dim, action_dim=action_dim, config=self.config).to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.config['model']['learning_rate'])
        self.model.train()

    def get_input_dim(self):
        # Adjust this based on the actual observation space
        num_predators = self.config['simulation']['num_agents']['predators']
        num_food = self.config['simulation']['num_agents']['prey'] * 2  # Assuming max food is twice the number of prey
        return (num_predators + num_food) * 3  # For each entity: x, y, z distance

    def perceive(self, environment):
        observations = []
        # Predators
        for predator in environment.get_predators():
            dist = distance(self.position, predator.position)
            if dist <= self.vision_range:
                direction = (np.array(predator.position) - np.array(self.position)) / dist
                observations.extend(direction * (self.vision_range - dist) / self.vision_range)
            else:
                observations.extend([0.0, 0.0, 0.0])

        # Food
        for food in environment.get_food():
            if food.consumed:
                observations.extend([0.0, 0.0, 0.0])
                continue
            dist = distance(self.position, food.position)
            if dist <= self.vision_range:
                direction = (np.array(food.position) - np.array(self.position)) / dist
                observations.extend(direction * (self.vision_range - dist) / self.vision_range)
            else:
                observations.extend([0.0, 0.0, 0.0])

        # Pad or truncate the observation to match input_dim
        expected_length = self.get_input_dim()
        if len(observations) < expected_length:
            observations += [0.0] * (expected_length - len(observations))
        elif len(observations) > expected_length:
            observations = observations[:expected_length]

        return torch.tensor(observations, dtype=torch.float32).to(self.device)

    def decide(self, observations):
        # Use the PPO model to decide on an action
        with torch.no_grad():
            dist, _ = self.model(observations)
            action = dist.sample()
            action = torch.clamp(action, -1, 1)  # Ensure actions are within bounds
        return action.cpu().numpy()

    def update_model(self, rewards, log_probs, values, dones):
        # Implement PPO update here
        # Placeholder for the update logic
        pass
