import tkinter as tk
import random
import numpy as np
from py.runnable.kalman import Kalman

# -- SETUP
dot_x 
dot_y 

def update_mouse_position(event):
    global dot_x, dot_y
    dot_x, dot_y = event.x, event.y


# Create the main window
root = tk.Tk()
root.title("Responsive Dot")
root.title("Kalman Example in 2D - Visualisation")

# Create a Canvas widget
# canvas = tk.Canvas(root, width=canvas_width,
#                    height=canvas_height, bg='#1F1F31')
canvas.pack()

# Erstelle ein Label, um die Mausposition anzuzeigen
# position_label = tk.Label(root, text="Mouse position: (0, 0)")
# position_label.pack()

# Binde das Motion-Ereignis an die update_mouse_position-Funktion
canvas.bind("<Motion>", update_mouse_position)
# 
