# main.py

from utils.config_parser import Config
from interface.gui import SimulationGUI
from environment.world import World
from utils.visualizer import Visualizer
from utils.logger import get_logger
import threading
import time

def run_simulation(config):
    logger = get_logger("Main")
    world = World(config=config)
    visualizer = None
    if config['visualization']['enable']:
        visualizer = Visualizer(config, world)

    # Start visualization in a separate thread
    if visualizer:
        vis_thread = threading.Thread(target=visualizer.run)
        vis_thread.start()

    max_steps = config['simulation']['max_steps']
    for step in range(max_steps):
        world.update()
        if config['visualization']['enable']:
            visualizer.update()
        if step % 100 == 0:
            logger.info(f"Step {step}/{max_steps}")

    logger.info("Simulation completed.")

def start_callback():
    # This function will be called after the GUI is closed
    config = Config().config
    run_simulation(config)

def main():
    # Load configurations
    config = Config().config

    # Initialize GUI
    gui = SimulationGUI(config, on_start_callback=start_callback)
    gui.run()

if __name__ == "__main__":
    main()
