# main.py

import os
os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'

import threading
from utils.config_parser import Config
from interface.gui import SimulationGUI
from environment.world import World
from utils.visualizer import Visualizer
from utils.logger import get_logger
import time
import signal
import traceback
import sys
import torch

# Add this near the top of the file, after the imports
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

def run_simulation(config):
    logger = get_logger("Main")
    logger.info("Starting simulation")
    world = World(config=config, device=device)
    visualizer = None
    if config['visualization']['enable']:
        visualizer = Visualizer(config, world, device)

    # Start visualization in the main thread
    if visualizer:
        update_thread = threading.Thread(target=update_loop, args=(world, visualizer, config), daemon=True)
        update_thread.start()
        visualizer.run()  # This will block until the window is closed
    else:
        update_loop(world, None, config)

def update_loop(world, visualizer, config):
    logger = get_logger("UpdateLoop")
    logger.info("Starting update loop")
    max_steps = config['simulation']['max_steps']
    try:
        for step in range(max_steps):
            try:
                world.update()
                if visualizer:
                    visualizer.update()
                if step % 100 == 0:
                    logger.info(f"Step {step}/{max_steps}")
                time.sleep(config['simulation']['time_step'])
            except Exception as e:
                logger.error(f"Error in step {step}: {e}")
                logger.error(traceback.format_exc())
                break
    except Exception as e:
        logger.error(f"An error occurred in the update loop: {e}")
        logger.error(traceback.format_exc())
    finally:
        if visualizer:
            visualizer.stop()
        logger.info("Simulation completed.")

def start_callback(config):
    # This function will be called after the GUI is closed
    run_simulation(config)

def main():
    config = Config().config
    
    def run_wrapper():
        run_simulation(config)
    
    gui = SimulationGUI(config, on_start_callback=run_wrapper)
    gui.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger = get_logger("Main")
        logger.error(f"Unhandled exception: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)
