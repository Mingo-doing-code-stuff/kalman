from canvasBuilder import CanvasApp

# Create an instance of the CanvasApp class
app = CanvasApp()

# Get the canvas from the instance
canvas = app.get_canvas()

# Use the canvas as needed


def get_canvas_height():
    print(canvas.winfo_height())


# Schedule the function to run after the main event loop has started
app.root.after(100, get_canvas_height)

# Start the Tkinter main loop
app.start()
