import tkinter as tk
from Adapter import Adapter9000
from datamodel import DataModel

class CanvasWrapper:

    def __init__(self, w_steps=80, h_steps=60, step_size=10, padding = 40):
        self.step_size = step_size
        canvas_width = w_steps * step_size
        self.canvas_width = canvas_width 
        canvas_height = h_steps * step_size
        self.canvas_height = canvas_height
        self.isMouseSelected = 0
        self.adapter = Adapter9000(canvas_width, canvas_height, step_size, padding)
        self.data = DataModel(0,0)
        self.adapter.update_input_signal(-1)
        self.canvas = self.create_canvas()
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
        if (var == 0):
            self.isMouseSelected = 1
            self.adapter.update_input_signal(var)
        else:
            self.isMouseSelected = 0
            self.adapter.update_input_signal(var)


    def update_canvas(self):
        x, y = self.adapter.update_values()
        self.render_canvas()
        # //TODO: Render Cycle Updates
        return
    
    
    def render_canvas(self):
        return