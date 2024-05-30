from rectangularPath import RectangularPath
from joystick import Joystick
# from mouse import Mouse ???
from kalman_class import Kalman
import numpy as np
import random

class NoiseGenerator():
    def add_noise():
        global dot_x, dot_y
        noise = np.random.randn(2) * random.gauss(1, 15)
        return [dot_x, dot_y] + noise

class Adapter9000():
    
    def __init__(self, canvas_width, canvas_height, step_size, padding):
        self.x_pos = 0 
        self.y_pos = 0
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.step_size = step_size
        self.padding = padding
        pass

    # //TODO: Move Up in init Eventually
    input = RectangularPath()
    kalman = Kalman()
    noise_generator = NoiseGenerator()
    
    def update_input_signal(self, idx):
        if (idx == 1):
            # self.input = Mouse 
            return
        elif (idx == 2):
            self.input = Joystick(self.canvas_width, self.canvas_height)
            return 
        else:
            self.input = RectangularPath(self.canvas_width, self.canvas_height, self.step_size, self.padding)
            return 
    
    def update_values(self):
        self.x_pos, self.y_pos = self.input.update_position()
        return