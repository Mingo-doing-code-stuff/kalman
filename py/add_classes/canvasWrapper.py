import tkinter as tk
from adapter import Adapter9000
from datamodel import DataModel
from canvasBuilder import CanvasBuilder


class CanvasWrapper:

    def __init__(self, canvas_height=600, canvas_width=800, step_size=10, tail=20):
        canvas_build = CanvasBuilder(canvas_width, canvas_height)
        canvas = canvas_build.canvas
        print(canvas.create_oval(140.0, 150.0, 141.0, 151.0))

        self.adapter = Adapter9000(canvas, step_size, tail)
        pass

    def testing(self):
        for array in self.data:
            temp = array.pop(0)
            # make stuff, update temp
            array.insert(len(array), temp)

    # def set_selected(self, mode):
    #     if (mode == 0):
    #         self.isMouseSelected = True
    #         self.adapter.update_input_signal(mode)
    #     else:
    #         self.isMouseSelected = False
    #         self.adapter.update_input_signal(mode)

    def update_canvas(self):
        x, y = self.adapter.update_values()
        self.render_canvas()
        # //TODO: Render Cycle Updates
        return

    def render_canvas(self):
        return
