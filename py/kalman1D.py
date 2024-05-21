import numpy as np
import pandas as pd
import seaborn as sb
from scipy import stats
import serial
import tkinter as tk
import random
import time


def update_position():
    data = ser.readline().decode().strip().split(',')
    if len(data) == 3:
        x_pos, y_pos, is_pressed = map(int, data)

        # Update coordinate system
        x_mapped = int((1023 - x_pos) / 1023 * canvas_width)
        y_mapped = int((y_pos / 1023) * canvas_height)  # Invert the Y-axis
        canvas.coords(joystick_indicator, x_mapped - indicator_radius, y_mapped - indicator_radius,
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                      x_mapped + indicator_radius, y_mapped + indicator_radius)

        # Change color randomly when joystick is pressed
        if is_pressed == 0:
            random_color = random.choice(colors)
            canvas.itemconfig(joystick_indicator, fill=random_color)

    # Schedule the next update
    # Update every 10 milliseconds for real-time updates
    root.after(10, update_position)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


mean0 = 0.0   # e.g. meters or miles
var0  = 20.0

meanMove = 25.0  # e.g. meters, calculated from velocity*dt or step counter or wheel encoder ...
varMove  = 10.0   # Estimated or determined with static measurements

def predict(var, mean, varMove, meanMove):
    new_var = var + varMove
    new_mean= mean+ meanMove
    return new_var, new_mean

new_var, new_mean = predict(var0, mean0, varMove, meanMove)

meanSensor = 25.0
varSensor  = 12.0

def correct(var, mean, varSensor, meanSensor):
    new_mean=(varSensor*mean + var*meanSensor) / (var+varSensor)
    new_var = 1/(1/var +1/varSensor)
    return new_var, new_mean

var, mean = correct(new_var, new_mean, varSensor, meanSensor)

positions = (10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200)+np.random.randn(20)
distances = (10, 10, 10, 10, 10, 10, 10, 10, 10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10)+np.random.randn(20)

print(positions)
print(distances)

mean = mean0
var = var0

for m in range(len(positions)):
    
    # Predict
    var, mean = predict(var, mean, varMove, distances[m])
    print('After prediction:\tmean= %.2f\tvar= %.2f' % (mean, var))
    
    # Correct
    var, mean = correct(var, mean, varSensor, positions[m])
    print('After correction:\tmean= %.2f\tvar=  %.2f\n' % (mean, var))

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Serial port configuration
# Replace 'COM4' with your Arduino's serial port
ser = serial.Serial('/dev/tty.usbmodem101', 9600)

# Create GUI
root = tk.Tk()
root.title("Joystick Position")

# Canvas dimensions
canvas_width = 400
canvas_height = 400

# Create canvas for the coordinate system
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

# Draw coordinate axes
canvas.create_line(0, canvas_height//2, canvas_width,
                   canvas_height//2, width=2)  # X-axis
canvas.create_line(canvas_width//2, 0, canvas_width//2,
                   canvas_height, width=2)    # Y-axis

# Draw gridlines
for i in range(1, 11):
    canvas.create_line(i * (canvas_width//10), 0, i * (canvas_width//10),
                       canvas_height, dash=(2, 2))  # Vertical gridlines
    canvas.create_line(0, i * (canvas_height//10), canvas_width,
                       i * (canvas_height//10), dash=(2, 2))  # Horizontal gridlines

# Indicator radius
indicator_radius = 5

# Create joystick indicator
joystick_indicator = canvas.create_oval(canvas_width//2 - indicator_radius, canvas_height//2 - indicator_radius,
                                        canvas_width//2 + indicator_radius, canvas_height//2 + indicator_radius,
                                        fill="red")

# Colors for random selection
colors = ["red", "green", "blue", "yellow", "orange", "purple"]

# Start updating position
update_position()

root.mainloop()