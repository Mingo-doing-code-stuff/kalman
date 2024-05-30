from rectangularPath import RectangularPath
from joystick import Joystick
# from mouse import Mouse ???
from kalman_class import Kalman
from datamodel import DataModel
import numpy as np
import random
import sys


class NoiseGenerator():
    def add_noise():
        global dot_x, dot_y
        noise = np.random.randn(2) * random.gauss(1, 15)
        return [dot_x, dot_y] + noise


class Adapter9000():

    def __init__(self, canvas, step_size, tail):
        self.x_pos = 0
        self.y_pos = 0
        self.tail = tail
        self.canvas = canvas
        self.canvas_width = self.canvas.winfo_reqwidth()
        self.canvas_height = canvas.winfo_reqheight()
        self.step_size = step_size
        print("Adapter running")
        self.input = RectangularPath()
        self.kalman = Kalman()
        self.noise_generator = NoiseGenerator()
        self.data = DataModel(3, self.canvas, self.tail,
                              self.step_size, self.canvas_width, self.canvas_height)
        self.canvas = self.data.canvas
        pass

    def update_input_signal(self, idx):
        if (idx == 1):
            # self.input = Mouse
            return
        elif (idx == 2):
            self.input = Joystick(self.canvas_width, self.canvas_height)
            self.kalman = Kalman()
            self.noise_generator = NoiseGenerator()
            self.data = DataModel(
                idx, self.canvas, self.tail, self.step_size, self.canvas_width, self.canvas_height)
            return
        elif (idx == 3):
            self.input = RectangularPath(
                self.canvas_width, self.canvas_height, self.step_size, 60)
            self.kalman = Kalman()
            self.noise_generator = NoiseGenerator()
            self.data = DataModel(
                idx, self.canvas, self.tail, self.step_size, self.canvas_width, self.canvas_height)
            return
        else:
            print("Error: no valid mode selected")
            sys.exit()

    def update_values(self):
        self.x_pos, self.y_pos = self.input.update_position()
        return
