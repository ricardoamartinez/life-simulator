# Reinforcement Learning Predator-Prey Simulation

## Overview

This project simulates a predator-prey ecosystem using reinforcement learning, specifically the Proximal Policy Optimization (PPO) algorithm. Agents (predators and prey) interact within a 3D continuous environment, learning behaviors such as hunting and evasion. Each agent has its own genetic makeup (DNA) that influences its traits and learning parameters.

## Features

- **3D Continuous Environment:** Agents navigate within a confined 3D space.
- **Reinforcement Learning:** Each agent uses the PPO algorithm for decision-making.
- **Genetic Algorithms:** Agents have DNA that governs traits like speed, size, and vision range, with the ability to mutate and evolve over generations.
- **Energy Mechanics:** Agents consume energy through movement and metabolism, requiring them to find food or hunt to survive.
- **Reproduction:** Agents reproduce based on energy thresholds, passing on DNA with potential mutations.
- **Real-time Visualization:** Visualize agent interactions in real-time using VisPy.
- **User Interface:** Configure simulation parameters through a GUI before starting the simulation.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/your_project.git
   cd your_project
