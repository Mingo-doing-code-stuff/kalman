import tkinter as tk
from Adapter import Adapter9000  # Assuming you have this class correctly implemented
from datamodel import DataModel  # Assuming you have this class correctly implemented
from point import Point  # Assuming you have this class correctly implemented
from ttkbootstrap import Style
from ttkbootstrap import ttk


class CanvasWrapper:

    def __init__(self, w_steps=80, h_steps=60, step_size=10, padding=40):
        self.step_size = step_size
        canvas_width = w_steps * step_size
        self.canvas_width = canvas_width
        canvas_height = h_steps * step_size
        self.canvas_height = canvas_height
        self.isMouseSelected = True
        self.adapter = Adapter9000(canvas_width, canvas_height, step_size, padding)
        self.data = DataModel(padding, padding)
        self.mouse_dot_x, self.mouse_dot_y = 0, 0
        self.sidebar_width = 240
        self.fps = 60
        self.root, self.canvas, self.sigma_scale, self.sigma_label, self.fps_scale, self.fps_label, self.input_var = self.create_canvas()
        pass

    def update_mouse_position(self, event):
        self.mouse_dot_x, self.mouse_dot_y = event.x, event.y

    def update_position(self):
        mouse_x, mouse_y = self.on_move()
        return mouse_x, mouse_y

    def create_canvas(self):
        root = tk.Tk()
        root.geometry(f"{self.canvas_width + self.sidebar_width}x{self.canvas_height}")
        root.title("Kalman Example in 2D - Visualisation")

        style = Style(theme='vapor')
        frame = ttk.Frame(root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        # Create a Canvas widget
        canvas = tk.Canvas(frame, width=self.canvas_width, height=self.canvas_height, bg='#1F1F31')
        canvas.grid(row=0, column=0, rowspan=15, sticky="nsew")
        canvas.bind("<Motion>", self.update_mouse_position)

        # Set a fixed width for the column
        frame.grid_columnconfigure(2, minsize=self.sidebar_width)

        sigma_label = ttk.Label(frame, text="Covariance Sigma: 15")
        sigma_label.grid(row=0, column=2, padx=10, pady=5)
        
        sigma_scale = ttk.Scale(frame, from_=1, to=100, orient=tk.HORIZONTAL, style='info.Horizontal.TScale', command=self.update_sigma)
        sigma_scale.set(15)
        sigma_scale.grid(row=1, column=2, padx=10, pady=5)

        fps_label = ttk.Label(frame, text="FPS: 60")
        fps_label.grid(row=2, column=2, padx=10, pady=5)
        
        fps_scale = ttk.Scale(frame, from_=1, to=120, orient=tk.HORIZONTAL, style='info.Horizontal.TScale', command=self.update_fps)
        fps_scale.set(60)
        fps_scale.grid(row=3, column=2, padx=10, pady=5)

        # Dropdown Menu for Input Selection
        input_var = tk.StringVar(value="Maus")
        input_label = ttk.Label(frame, text="Input Source")
        input_label.grid(row=4, column=2, padx=10, pady=5)
        
        input_menu = ttk.Combobox(frame, textvariable=input_var, values=["Maus", "Joystick", "Rechteck"], state="readonly")
        input_menu.grid(row=5, column=2, padx=10, pady=5)
        input_menu.bind("<<ComboboxSelected>>", self.update_input_source)

        return root, canvas, sigma_scale, sigma_label, fps_scale, fps_label, input_var

    def update_sigma(self, value):
        sigma_value = float(value)
        self.sigma_label.config(text=f"Covariance Sigma: {sigma_value:.3f}")
        self.adapter.update_sigma(sigma_value)

    def update_fps(self, value):
        self.fps = int(float(value))
        self.fps_label.config(text=f"FPS: {self.fps}")

    def update_input_source(self, event):
        selection = self.input_var.get()
        print(selection)
        if selection == "Maus":
            self.isMouseSelected = True
            self.adapter.update_input_signal("Maus")
        elif selection == "Joystick":
            self.isMouseSelected = False
            self.adapter.update_input_signal("Joystick")
        elif selection == "Rechteck":
            self.isMouseSelected = False
            self.adapter.update_input_signal("Rechteck")

    def update_canvas(self):
        position, noise, kalman = self.adapter.update_values()
        self.data.add_new_pos_point(position)
        self.data.add_new_noise_point(noise)
        self.data.add_new_kalman_point(kalman)
        self.canvas.delete("all")
        self.render_canvas()
        self.canvas.after(int(1000 / self.fps), self.update_canvas)

    def create_dot(self, point, color):
        self.canvas.create_oval(point.x-2, point.y-2, point.x+2, point.y+2, fill=color, outline='')

    def render_lines(self, points, color):
        for i in range(len(points) - 1):
            self.canvas.create_line(points[i].x, points[i].y, points[i + 1].x, points[i + 1].y, fill=color)

    def render_canvas(self):
        position_points = self.data.position_points
        noise_points = self.data.noise_points
        kalman_points = self.data.kalman_points

        if self.isMouseSelected:
            position_point = Point(self.mouse_dot_x, self.mouse_dot_y)
            self.create_dot(position_point, "purple")
        else :
            for p in position_points:
                self.create_dot(p, "blue")
            for p in noise_points:
                self.create_dot(p, "green")
            for p in kalman_points:
                self.create_dot(p, "red")

        self.render_lines(position_points, "blue")
        self.render_lines(noise_points, "green")
        self.render_lines(kalman_points, "red")

        return

    def run(self):
        self.canvas.after(int(1000 / self.fps), self.update_canvas)
        self.root.mainloop()

executable = CanvasWrapper()
executable.run()
