import tkinter as tk


class CanvasWrapper:

    def __init__(self, w_steps=80, h_steps=60, step_size=10):
        self.step_size = step_size
        self.canvas_width = w_steps * self.step_size
        self.canvas_height = h_steps * self.step_size
        self.canvas = self.create_canvas()
        self.selected = 0
        pass

    def create_canvas(self):

        root = tk.Tk()
        root.geometry(f"{self.canvas_width}x{self.canvas_height}")
        root.title("Kalman Example in 2D - Visualisation")

        # Create a Canvas widget
        canvas = tk.Canvas(root, width=self.canvas_width,
                           height=self.canvas_height, bg='#1F1F31')
        canvas.pack()
        return canvas

    def set_selected(self, var):
        self.selected = var
