import tkinter as tk
from Adapter import Adapter9000
from datamodel import DataModel
from point import Point


class CanvasWrapper:

    def __init__(self, w_steps=80, h_steps=60, step_size=10, padding=40):
        self.step_size = step_size
        canvas_width = w_steps * step_size
        self.canvas_width = canvas_width
        canvas_height = h_steps * step_size
        self.canvas_height = canvas_height
        self.isMouseSelected = 1
        self.adapter = Adapter9000(
            canvas_width, canvas_height, step_size, padding)
        self.data = DataModel(padding, padding)
        self.mouse_dot_x, self.mouse_dot_y = 0, 0
        self.root, self.canvas = self.create_canvas()
        pass

    def update_mouse_position(self, event):
        self.mouse_dot_x, self.mouse_dot_y = event.x, event.y

    def update_position(self):
        mouse_x, mouse_y = self.on_move()
        return mouse_x, mouse_y

    def create_canvas(self):
        root = tk.Tk()
        root.geometry(f"{self.canvas_width}x{self.canvas_height}")
        root.title("Kalman Example in 2D - Visualisation")

        # Create a Canvas widget
        canvas = tk.Canvas(root, width=self.canvas_width,
                           height=self.canvas_height, bg='#1F1F31')
        canvas.bind("<Motion>", self.update_mouse_position)
        canvas.pack()
        return root, canvas

    def set_selected(self, var):
        if (var == 0):
            self.isMouseSelected = 1
            self.adapter.update_input_signal(var)
        else:
            self.isMouseSelected = 0
            self.adapter.update_input_signal(var)

    def update_canvas(self):
        position, noise, kalman = self.adapter.update_values()
        self.data.add_new_pos_point(position)
        self.data.add_new_noise_point(noise)
        self.data.add_new_kalman_point(kalman)

        self.canvas.delete("all")
        self.render_canvas()
        # //TODO: Render Cycle Updates
        return

    def create_dot(self, point, color):
        self.canvas.create_oval(point.x-2, point.y-2,
                                point.x+2, point.y+2, fill=color)

    def render_canvas(self):
        position_points = self.data.position_points
        noise_points = self.data.noise_points
        kalman_points = self.data.kalman_points

        if self.isMouseSelected:
            position_point = Point(self.mouse_dot_x, self.mouse_dot_y)
            self.create_dot(position_point, "purple")

        for p in position_points:
            self.create_dot(p, "blue")
        for p in noise_points:
            self.create_dot(p, "green")
        for p in kalman_points:
            self.create_dot(p, "red")

        self.canvas.pack()
        self.canvas.after(40, self.update_canvas)
        return

    def run(self):
        self.canvas.after(40, self.update_canvas)
        self.root.mainloop()


executable = CanvasWrapper()
executable.run()
