# agents/predator.py

import torch
from agents.base_agent import BaseAgent
from models.ppo_agent import PPOAgent
from utils.helpers import distance
from utils.logger import get_logger

class Predator(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = get_logger(self.__class__.__name__)
        input_dim = self.get_input_dim()
        action_dim = 3  # Movement in 3D
        self.model = PPOAgent(input_dim=input_dim, action_dim=action_dim, config=self.config).to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.config['model']['learning_rate'])
        self.model.train()

    def get_input_dim(self):
        # Define input dimensions based on observations
        # Example: distances and directions to nearest prey and food
        # Here, we'll assume a fixed-size input for simplicity
        num_prey = self.config['simulation']['num_agents']['prey']
        return num_prey * 3  # For each prey: x, y, z distance

    def perceive(self, environment):
        # Detect prey within vision range
        observations = []
        for prey in environment.get_prey():
            dist = distance(self.position, prey.position)
            if dist <= self.vision_range:
                direction = (prey.position - self.position) / dist if dist > 0 else np.zeros(3)
                observations.extend(direction * (self.vision_range - dist) / self.vision_range)  # Weighted direction
            else:
                observations.extend([0.0, 0.0, 0.0])  # No prey detected

        # Pad the observation to match input_dim
        expected_length = self.get_input_dim()
        if len(observations) < expected_length:
            observations += [0.0] * (expected_length - len(observations))

        return torch.tensor(observations, dtype=torch.float32).to(self.device)

    def decide(self, observations):
        # Use the PPO model to decide on an action
        with torch.no_grad():
            dist, _ = self.model(observations)
            action = dist.sample()
            action = torch.clamp(action, -1, 1)  # Ensure actions are within bounds
        return action.cpu().numpy()

    def update_model(self, rewards, log_probs, values, dones):
        # Convert lists to tensors
        rewards = torch.tensor(rewards, dtype=torch.float32).to(self.device)
        old_log_probs = torch.stack(log_probs).detach()
        values = torch.stack(values).detach()
        dones = torch.tensor(dones, dtype=torch.float32).to(self.device)

        # Compute advantages
        returns = []
        G = 0
        for reward, done in zip(reversed(rewards), reversed(dones)):
            if done:
                G = 0
            G = reward + self.config['model']['gamma'] * G
            returns.insert(0, G)
        returns = torch.tensor(returns, dtype=torch.float32).to(self.device)
        advantages = returns - values

        # Normalize advantages
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        # PPO Optimization
        for _ in range(self.config['model']['update_epochs']):
            # Assuming mini-batch processing
            for i in range(0, len(rewards), self.config['model']['mini_batch_size']):
                # Sample mini-batch
                sampled_indices = slice(i, i + self.config['model']['mini_batch_size'])
                sampled_advantages = advantages[sampled_indices]
                sampled_returns = returns[sampled_indices]
                sampled_old_log_probs = old_log_probs[sampled_indices]

                # Forward pass
                dist, state_values = self.model.forward(self.perceive(environment=None))  # Modify as needed
                new_log_probs = dist.log_prob(actions).sum(dim=-1)
                entropy = dist.entropy().sum(dim=-1)

                # Ratio for PPO clipping
                ratios = torch.exp(new_log_probs - sampled_old_log_probs)

                # PPO Loss
                surr1 = ratios * sampled_advantages
                surr2 = torch.clamp(ratios, 1.0 - self.config['model']['clip_epsilon'], 1.0 + self.config['model']['clip_epsilon']) * sampled_advantages
                actor_loss = -torch.min(surr1, surr2).mean()
                critic_loss = torch.nn.functional.mse_loss(state_values.squeeze(), sampled_returns)
                entropy_loss = -entropy.mean()

                loss = actor_loss + 0.5 * critic_loss + 0.01 * entropy_loss

                # Backpropagation
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
