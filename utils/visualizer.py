# utils/visualizer.py

import vispy.scene
from vispy.scene import visuals
from vispy import app
import numpy as np
from utils.logger import get_logger

class Visualizer:
    def __init__(self, config, world):
        self.logger = get_logger(__name__)
        self.world = world
        self.container_size = config['simulation']['container_size']
        self.display_rate = config['visualization']['display_rate']
        
        self.canvas = vispy.scene.SceneCanvas(keys='interactive', show=True)
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = 'turntable'
        self.view.camera.fov = 60
        self.view.camera.distance = max(self.container_size) * 2

        # Draw container boundaries
        container = visuals.Box(width=self.container_size[0],
                               height=self.container_size[1],
                               depth=self.container_size[2],
                               edge_color='white',
                               face_color=(0, 0, 0, 0),
                               parent=self.view.scene)

        # Initialize agent visuals
        self.predator_markers = visuals.Markers(parent=self.view.scene)
        self.prey_markers = visuals.Markers(parent=self.view.scene)
        self.food_markers = visuals.Markers(parent=self.view.scene)

    def update(self):
        predators = []
        prey = []
        foods = []

        for agent in self.world.get_predators():
            predators.append(agent.position)

        for agent in self.world.get_prey():
            prey.append(agent.position)

        for food in self.world.get_food():
            foods.append(food.position)

        if predators:
            self.predator_markers.set_data(np.array(predators), face_color='red', size=5)
        else:
            self.predator_markers.set_data(np.empty((0, 3)))

        if prey:
            self.prey_markers.set_data(np.array(prey), face_color='blue', size=5)
        else:
            self.prey_markers.set_data(np.empty((0, 3)))

        if foods:
            self.food_markers.set_data(np.array(foods), face_color='green', size=3)
        else:
            self.food_markers.set_data(np.empty((0, 3)))

        self.canvas.update()

    def run(self):
        app.run()
