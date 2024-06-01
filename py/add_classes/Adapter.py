from rectangularPath import RectangularPath
from joystick import Joystick
# from mouse import Mouse ???
from kalman_class import Kalman
from point import Point
import numpy as np
import random


class NoiseGenerator():

    def __init__(self, sigma):
        self.sigma = sigma

    def add_noise(self, x, y):
        noise = np.random.randn(2) * random.gauss(1, self.sigma)
        return [x, y] + noise

    def set_sigma(self, sigma):
        self.sigma = sigma

    def get_sigma(self):
        return self.sigma


class Adapter9000():

    def __init__(self, canvas_width, canvas_height, step_size, padding, sigma=15):
        self.x_pos = 0
        self.y_pos = 0
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.step_size = step_size
        self.padding = padding
        self.sigma = sigma
        # //TODO: Move Up in init Eventually
        self.input = RectangularPath(
            self.canvas_width, self.canvas_height, self.step_size, self.padding)
        self.kalman = Kalman()
        self.noise_generator = NoiseGenerator(self.sigma)
        self.prev_noise = [0, 0]
        pass

    def update_sigma(self, sigma):
        self.sigma = sigma
        self.kalman.set_sigma(sigma)
        self.noise_generator.set_sigma(sigma)

    def update_input_signal(self, idx):
        if (idx == 1):
            # self.input = Mouse
            self.kalman = Kalman(self.sigma)
            self.noise_generator = NoiseGenerator(self.sigma)
            return
        elif (idx == 2):
            self.input = Joystick(self.canvas_width, self.canvas_height)
            self.kalman = Kalman(self.sigma)
            self.noise_generator = NoiseGenerator(self.sigma)
            return
        else:
            self.input = RectangularPath(
                self.canvas_width, self.canvas_height, self.step_size, self.padding)
            self.kalman = Kalman(self.sigma)
            self.noise_generator = NoiseGenerator(self.sigma)
            return

    def get_prev_noise(self):
        return self.prev_noise[0], self.prev_noise[1]

    def set_prev_noise(self, x, y):
        self.prev_noise = [x, y]

    def update_values(self):
        x_pos, y_pos = self.input.update_position()
        x_n, y_n = self.noise_generator.add_noise(x_pos, y_pos)
        x_n_prev, y_n_prev = self.get_prev_noise()
        self.set_prev_noise(x_n, y_n)
        x_k, y_k = self.kalman.calculate_kalman(x_n, y_n, x_n_prev, y_n_prev)
        pos_point = Point(x_pos, y_pos)
        noise_point = Point(x_n, y_n)
        kalman_point = Point(x_k, y_k)
        return pos_point, noise_point, kalman_point
