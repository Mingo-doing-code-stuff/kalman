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

    def __init__(self, canvas):
        self.canvas = canvas
        self.x_pos = 0
        self.y_pos = 0
        self.tail = 20
        self.canvas_width = self.canvas.winfo_reqwidth()
        self.canvas_height = self.canvas.winfo_reqheight()
        self.step_size = 10
        print("Adapter running")
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
                idx, self.tail, self.step_size, self.canvas_width, self.canvas_height)
            return
        elif (idx == 3):
            self.input = RectangularPath(
                self.canvas_width, self.canvas_height, self.step_size, 60)
            self.kalman = Kalman()
            self.noise_generator = NoiseGenerator()
            self.data = DataModel(
                idx, self.tail, self.step_size, self.canvas_width, self.canvas_height)
            return
        else:
            print("Error: no valid mode selected")
            sys.exit()

    def update_values(self):
        self.x_pos, self.y_pos = self.input.update_position()
        self.position_points.pop(0)
        self.position_points.insert(len(self.position_points), self.canvas.coords(
            self.x_pos - 2, self.y_pos - 2, self.x_pos + 2, self.y_pos + 2))
        return

    def get_canvas(self):
        return self.canvas

    def get_canvas_dimensions(self):
        return self.root, self.canvas

    def initial_setup(self):
        self.input = RectangularPath(
            self.canvas_width, self.canvas_height, self.step_size)
        self.kalman = Kalman()
        self.noise_generator = NoiseGenerator()
        self.data = DataModel(self.canvas)
        self.position_points, self.noise_points, self.kalman_points = self.data.prefill()
        print("initial setup complete")
        print(self.data)

# if __name__ == "__main__":
#     adapter = Adapter9000()
#     root, canvas = adapter.get_canvas()
#     root.after(0, adapter.initial_setup)
#     root.mainloop()
