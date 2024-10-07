# utils/visualizer.py

import vispy.scene
from vispy.scene import visuals
from vispy import scene  # Add this import
import numpy as np
from utils.logger import get_logger
import vispy.app as app

class Visualizer:
    def __init__(self, config, world):
        self.logger = get_logger(__name__)
        self.world = world
        self.container_size = np.array(config['simulation']['container_size'])
        self.display_rate = config['visualization']['display_rate']
        
        self.canvas = vispy.scene.SceneCanvas(keys='interactive', show=True)
        self.view = self.canvas.central_widget.add_view()
        
        # Set up the camera
        self.view.camera = scene.TurntableCamera(
            fov=45,
            elevation=30,
            azimuth=45,
            distance=max(self.container_size) * 1.5,
            center=(0, 0, 0)
        )

        # Draw container boundaries (edges only)
        self.draw_container_edges()

        # Initialize agent visuals
        self.predator_markers = visuals.Markers(parent=self.view.scene)
        self.prey_markers = visuals.Markers(parent=self.view.scene)
        self.food_markers = visuals.Markers(parent=self.view.scene)

        # Set the camera's range
        self.view.camera.set_range(x=[-self.container_size[0]/2, self.container_size[0]/2],
                                   y=[-self.container_size[1]/2, self.container_size[1]/2],
                                   z=[-self.container_size[2]/2, self.container_size[2]/2])

        self.running = False

    def draw_container_edges(self):
        # Define the vertices of the box
        vertices = np.array([
            [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5],
            [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, 0.5], [-0.5, 0.5, 0.5]
        ])
        vertices = vertices * self.container_size

        # Define the connections between vertices
        connections = np.array([
            [0, 1], [1, 2], [2, 3], [3, 0],  # Bottom face
            [4, 5], [5, 6], [6, 7], [7, 4],  # Top face
            [0, 4], [1, 5], [2, 6], [3, 7]   # Vertical edges
        ])

        # Create a LineVisual for the edges
        lines = visuals.Line(pos=vertices, connect=connections, color='white', method='gl', parent=self.view.scene)

    def update(self):
        predators = []
        prey = []
        foods = []

        for agent in self.world.get_predators():
            predators.append(agent.position - self.container_size / 2)

        for agent in self.world.get_prey():
            prey.append(agent.position - self.container_size / 2)

        for food in self.world.get_food():
            foods.append(food.position - self.container_size / 2)

        if predators:
            self.predator_markers.set_data(np.array(predators), face_color='red', size=15)
        else:
            self.predator_markers.set_data(np.empty((0, 3)))

        if prey:
            self.prey_markers.set_data(np.array(prey), face_color='blue', size=10)
        else:
            self.prey_markers.set_data(np.empty((0, 3)))

        if foods:
            self.food_markers.set_data(np.array(foods), face_color='green', size=5)
        else:
            self.food_markers.set_data(np.empty((0, 3)))

        self.canvas.update()

    def run(self):
        self.running = True
        app.run()  # This will block and keep the window open

    def stop(self):
        self.running = False
        app.quit()
