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
        self.root = tk.Tk()
        pass


    def create_canvas(self):
        root = tk.Tk()
        root.geometry(f"{self.canvas_width}x{self.canvas_height}")
        root.title("Kalman Example in 2D - Visualisation")

        # Create a Canvas widget
        canvas = tk.Canvas(root, width=self.canvas_width,
                           height=self.canvas_height, bg='#FFFFFF')#'#1F1F31')
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
        position, noise, kalman = self.adapter.update_values()
        self.data.add_new_pos_point(position)
        self.data.add_new_noise_point(noise)
        self.data.add_new_kalman_point(kalman)

        self.canvas.delete("all")
        self.render_canvas()
        # //TODO: Render Cycle Updates
        return
    
    
    def create_dot(self, point):
        self.canvas.create_oval(point.x-2,point.y-2,point.x+40,point.y+40, fill="red")

    def render_canvas(self):
        position_points = self.data.position_points
        noi = self.data.noise_points
        kal = self.data.kalman_points
        
        for p in position_points:
            self.create_dot(p)
        self.canvas.pack()
        self.canvas.after(125,self.update_canvas)
        return
        
    
    def run(self):
        self.canvas.after(125, self.update_canvas)
        self.root.mainloop()

executable = CanvasWrapper()
executable.run()
