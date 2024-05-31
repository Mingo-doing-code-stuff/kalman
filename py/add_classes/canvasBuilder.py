import tkinter as tk


class CanvasBuilder:
    def __init__(self, canvas_width, canvas_height):
        self.root = tk.Tk()
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        # self.root.geometry(f"{self.canvas_width}x{self.canvas_height}")
        # self.root.title("Kalman Example in 2D - Visualisation")

        # Create a Canvas widget
        self.canvas = tk.Canvas(self.root, width=self.canvas_width,
                                height=self.canvas_height, bg='#1F1F31')
        self.canvas.pack()

    def get_canvas(self):
        return self.root, self.canvas


if __name__ == "__main__":
    app = CanvasBuilder()
    root, canvas = app.get_canvas()
    root.mainloop()
