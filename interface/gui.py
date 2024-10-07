# interface/gui.py

import tkinter as tk
from tkinter import ttk
from utils.logger import get_logger

class SimulationGUI:
    def __init__(self, config, on_start_callback):
        self.logger = get_logger(self.__class__.__name__)
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.title("Reinforcement Learning Simulation Setup")
        self.config = config
        self.on_start_callback = on_start_callback
        self.create_widgets()

    def on_closing(self):
        self.root.quit()
        self.root.destroy()

    def create_widgets(self):
        # Number of Predators
        ttk.Label(self.root, text="Number of Predators").grid(column=0, row=0, padx=5, pady=5, sticky='E')
        self.num_predators = tk.IntVar(value=self.config['simulation']['num_agents']['predators'])
        ttk.Entry(self.root, textvariable=self.num_predators).grid(column=1, row=0, padx=5, pady=5)

        # Number of Prey
        ttk.Label(self.root, text="Number of Prey").grid(column=0, row=1, padx=5, pady=5, sticky='E')
        self.num_prey = tk.IntVar(value=self.config['simulation']['num_agents']['prey'])
        ttk.Entry(self.root, textvariable=self.num_prey).grid(column=1, row=1, padx=5, pady=5)

        # Mutation Rate
        ttk.Label(self.root, text="Mutation Rate").grid(column=0, row=2, padx=5, pady=5, sticky='E')
        self.mutation_rate = tk.DoubleVar(value=self.config['dna']['mutation_rate'])
        ttk.Entry(self.root, textvariable=self.mutation_rate).grid(column=1, row=2, padx=5, pady=5)

        # Simulation Steps
        ttk.Label(self.root, text="Max Steps").grid(column=0, row=3, padx=5, pady=5, sticky='E')
        self.max_steps = tk.IntVar(value=self.config['simulation']['max_steps'])
        ttk.Entry(self.root, textvariable=self.max_steps).grid(column=1, row=3, padx=5, pady=5)

        # Container Size
        ttk.Label(self.root, text="Container Size (W, H, D)").grid(column=0, row=4, padx=5, pady=5, sticky='E')
        self.container_size = tk.StringVar(value="100,100,100")
        ttk.Entry(self.root, textvariable=self.container_size).grid(column=1, row=4, padx=5, pady=5)

        # Start Simulation Button
        ttk.Button(self.root, text="Start Simulation", command=self.start_simulation).grid(column=0, row=5, columnspan=2, pady=10)

    def start_simulation(self):
        self.update_config_from_inputs()
        self.logger.info("Configuration updated from GUI inputs.")
        self.root.quit()
        self.on_start_callback()

    def update_config_from_inputs(self):
        try:
            self.config['simulation']['num_agents']['predators'] = self.num_predators.get()
            self.config['simulation']['num_agents']['prey'] = self.num_prey.get()
            self.config['dna']['mutation_rate'] = self.mutation_rate.get()
            self.config['simulation']['max_steps'] = self.max_steps.get()
            container_dims = list(map(float, self.container_size.get().split(',')))
            if len(container_dims) != 3:
                raise ValueError("Container size must have three dimensions separated by commas.")
            self.config['simulation']['container_size'] = container_dims
        except Exception as e:
            self.logger.error(f"Error in configuration inputs: {e}")
            return

    def run(self):
        self.root.mainloop()
