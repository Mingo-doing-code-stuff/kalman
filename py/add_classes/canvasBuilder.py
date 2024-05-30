import tkinter as tk


class CanvasBuilder:
    def __init__(self, canvas_width, canvas_height):
        self.root = tk.Tk()
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.canvas = self.create_canvas()
        pass

    def create_canvas(self):
        self.root.geometry(f"{self.canvas_width}x{self.canvas_height}")
        self.root.title("Kalman Example in 2D - Visualisation")

        # Create a Canvas widget
        self.canvas = tk.Canvas(self.root, width=self.canvas_width,
                                height=self.canvas_height, bg='#1F1F31')
        self.canvas.pack()
        self.root.mainloop()




class CanvasApp:
    def __init__(self):
        self.root = tk.Tk()
        self.canvas_width = 800
        self.canvas_height = 600
        
        # Create a Canvas widget
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg='#1F1F31')
        self.canvas.pack()
    
    def get_canvas(self):
        return self.canvas
    
    def start(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = CanvasApp()
    app.start()
