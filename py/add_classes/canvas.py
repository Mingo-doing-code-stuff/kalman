import tkinter as tk


class CanvasWrapper:

    def __init__(self, w_steps=80, h_steps=60, step_size=10):
        self.w_steps = w_steps
        self.h_steps = h_steps
        self.step_size = step_size
        self.canvas = self.create_canvas()
        self.selected = 0
        pass

    def create_canvas(self):
        canvas_width = self.w_steps * self.step_size
        canvas_height = self.h_steps * self.step_size

        root = tk.Tk()
        root.geometry(f"{canvas_width}x{canvas_height}")
        root.title("Kalman Example in 2D - Visualisation")

        # Create a Canvas widget
        canvas = tk.Canvas(root, width=canvas_width,
                           height=canvas_height, bg='#1F1F31')
        canvas.pack()
        return canvas
    
    def set_selected(self, var):
        self.selected = var


myCanvasWrapper = CanvasWrapper()
myCanvasWrapper.canvas.create_line(140, 140, 150, 150, fill='red', width=2)
print(myCanvasWrapper)

myCanvasWrapper.canvas.mainloop()
