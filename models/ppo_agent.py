# models/ppo_agent.py

import torch
from torch.distributions import Normal
from models.networks import ActorCriticNetwork

class PPOAgent(torch.nn.Module):
    def __init__(self, input_dim, action_dim, config):
        super(PPOAgent, self).__init__()
        self.network = ActorCriticNetwork(input_dim, action_dim)
        self.config = config
        self.action_std = torch.ones(action_dim) * 0.5  # Initial standard deviation for exploration
        self.action_var = self.action_std.pow(2)

    def forward(self, x):
        action_mean, state_value = self.network(x)
        action_std = self.action_std.expand_as(action_mean)
        dist = Normal(action_mean, action_std)
        return dist, state_value

    def act(self, x):
        dist, value = self.forward(x)
        action = dist.sample()
        action_logprob = dist.log_prob(action).sum(dim=-1)
        return action, action_logprob, value

    def evaluate_actions(self, x, actions):
        dist, value = self.forward(x)
        action_logprobs = dist.log_prob(actions).sum(dim=-1)
        dist_entropy = dist.entropy().sum(dim=-1)
        return action_logprobs, torch.squeeze(value), dist_entropy
