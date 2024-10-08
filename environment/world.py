# environment/world.py

import traceback
from environment.container import Container
from environment.food import Food
from agents.predator import Predator
from agents.prey import Prey
from utils.logger import get_logger
import random
from utils.helpers import distance  # Make sure this import is present

class World:
    def __init__(self, config, device):
        self.logger = get_logger(__name__)
        self.config = config
        self.device = device
        self.container = Container(config['simulation']['container_size'])
        self.agents = []
        self.food_items = []
        self.time_step = config['simulation']['time_step']

        # Initialize agents
        self.initialize_agents()

        # Spawn initial food
        self.spawn_food(initial=True)

    def initialize_agents(self):
        num_predators = self.config['simulation']['num_agents']['predators']
        num_prey = self.config['simulation']['num_agents']['prey']

        for _ in range(num_predators):
            predator = Predator(config=self.config, device=self.device)
            self.agents.append(predator)

        for _ in range(num_prey):
            prey = Prey(config=self.config, device=self.device)
            self.agents.append(prey)

    def spawn_food(self, initial=False):
        if initial:
            num_food = self.config['simulation']['num_agents']['prey'] * 2
        else:
            num_food = self.config['simulation']['food_spawn_rate']

        for _ in range(num_food):
            food = Food(position=self.random_position())
            self.food_items.append(food)

    def random_position(self):
        return [random.uniform(0, size) for size in self.config['simulation']['container_size']]

    def get_predators(self):
        return [agent for agent in self.agents if isinstance(agent, Predator) and agent.alive]

    def get_prey(self):
        return [agent for agent in self.agents if isinstance(agent, Prey) and agent.alive]

    def get_food(self):
        return [food for food in self.food_items if not food.consumed]

    def update(self):
        self.logger.debug("Starting world update")
        try:
            # Update all agents
            for agent in list(self.agents):  # Use list to avoid modification during iteration
                if agent.alive:
                    try:
                        agent.update(self)
                    except Exception as e:
                        self.logger.error(f"Error updating {agent.__class__.__name__}: {e}")
                        self.logger.error(traceback.format_exc())
                else:
                    self.agents.remove(agent)
                    self.logger.info(f"{agent.__class__.__name__} removed from the world.")

            # Handle interactions (e.g., eating)
            self.handle_eating()

            # Spawn food periodically
            self.spawn_food()

            # Handle reproduction
            self.handle_reproduction()
        except Exception as e:
            self.logger.error(f"Error in world update: {e}")
            self.logger.error(traceback.format_exc())
            raise
        self.logger.debug("World update completed")

    def handle_eating(self):
        # Predators eat prey
        predators = self.get_predators()
        prey_list = self.get_prey()
        for predator in predators:
            for prey in prey_list:
                if distance(predator.position, prey.position) < (predator.size + prey.size):
                    # Predator eats prey
                    prey.alive = False
                    predator.energy += self.config['agent']['energy']['consumption_gain']
                    self.logger.info(f"Predator at {predator.position} ate prey at {prey.position}.")

        # Prey eat food
        prey_list = self.get_prey()
        food_list = self.get_food()
        for prey in prey_list:
            for food in food_list:
                if distance(prey.position, food.position) < (prey.size + 0.5):  # Assuming food size is 0.5
                    # Prey consumes food
                    food.consumed = True
                    prey.energy += self.config['agent']['energy']['consumption_gain']
                    self.logger.info(f"Prey at {prey.position} consumed food at {food.position}.")

    def handle_reproduction(self):
        # Agents reproduce based on energy thresholds
        for agent in self.agents:
            if agent.energy >= self.config['agent']['energy']['initial'] * 1.5:  # Example threshold
                child = agent.reproduce()
                self.agents.append(child)
                agent.energy /= 2  # Split energy with child
                self.logger.info(f"{agent.__class__.__name__} reproduced. Child at {child.position}.")
