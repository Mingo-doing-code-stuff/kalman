import tkinter as tk
# from adapter import Adapter9000
from adapter import Adapter9000
from canvasBuilder import CanvasBuilder


class CanvasHandler:

    def __init__(self, canvas_height=600, canvas_width=800, step_size=10, tail=20):
        canvas_build = CanvasBuilder(canvas_width, canvas_height)
        self.root, self.canvas = canvas_build.get_canvas()

        # print(canvas.create_oval(140.0, 150.0, 141.0, 151.0))

        # self.adapter = Adapter9000(canvas, step_size, tail)
        pass

    def testing(self):
        for array in self.data:
            temp = array.pop(0)
            # make stuff, update temp
            array.insert(len(array), temp)

    def pass_canvas_to_adapter(self):
        adapter = Adapter9000(self.canvas)
        adapter.initial_setup()
        adapter.update_values()
        adapter.update_values()
        adapter.update_values()
        adapter.update_values()
        adapter.update_values()
        adapter.update_values()
        adapter.update_values()

    # def set_selected(self, mode):
    #     if (mode == 0):
    #         self.isMouseSelected = True
    #         self.adapter.update_input_signal(mode)
    #     else:
    #         self.isMouseSelected = False
    #         self.adapter.update_input_signal(mode)

    # def update_canvas(self):
    #     x, y = self.adapter.update_values()
    #     self.render_canvas()
    #     # //TODO: Render Cycle Updates
    #     return

    # def render_canvas(self):
    #     return

    def get_canvas(self):
        return self.root, self.canvas


if __name__ == "__main__":
    handler = CanvasHandler()
    root, canvas = handler.get_canvas()
    root.after(0, handler.pass_canvas_to_adapter)
    root.mainloop()
