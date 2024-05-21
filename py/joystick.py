import serial
import tkinter as tk
import random

# Function to update joystick position

mean0 = 0.0   # e.g. meters or miles
var0  = 20.0

meanMove = 25.0  # e.g. meters, calculated from velocity*dt or step counter or wheel encoder ...
varMove  = 10.0   # Estimated or determined with static measurements

def predict(var, mean, varMove, meanMove):
    new_var = var + varMove
    new_mean= mean + meanMove
    return new_var, new_mean

new_var, new_mean = predict(var0, mean0, varMove, meanMove)

meanSensor = 25.0
varSensor  = 12.0

def correct(var, mean, varSensor, meanSensor):
    new_mean=(varSensor*mean + var*meanSensor) / (var+varSensor)
    new_var = 1/(1/var +1/varSensor)
    return new_var, new_mean

var = 0 
mean = 0

def update_position():
    data = ser.readline().decode().strip().split(',')
    if len(data) == 3:
        x_pos, y_pos, is_pressed = map(int, data)

        # Update coordinate system
        x_mapped = int((1023 - x_pos) / 1023 * canvas_width)
        y_mapped = int((y_pos / 1023) * canvas_height)  # Invert the Y-axis
        canvas.coords(joystick_indicator, x_mapped - indicator_radius, y_mapped - indicator_radius,
                      x_mapped + indicator_radius, y_mapped + indicator_radius)
        
        new_var, new_mean = predict(var, mean, varMove, meanMove) 

        var, mean = correct(new_var, new_mean, varSensor, x_mapped)
        x_kalman = mean
        _, y_kalman = y_mapped -10
        canvas.coords(joystick_indicator_kalman, x_kalman - indicator_radius, y_kalman - indicator_radius,
                      x_kalman + indicator_radius, y_kalman + indicator_radius)

        # Change color randomly when joystick is pressed
        if is_pressed == 0:
            random_color = random.choice(colors)
            canvas.itemconfig(joystick_indicator, fill=random_color)

    # Schedule the next update
    # Update every 10 milliseconds for real-time updates
    root.after(10, update_position)


# Serial port configuration
# Replace 'COM4' with your Arduino's serial port
ser = serial.Serial('/dev/tty.usbmodem101', 9600)

# Create GUI
root = tk.Tk()
root.title("Joystick Position")

# Canvas dimensions
canvas_width = 600
canvas_height = 600

# Create canvas for the coordinate system
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

# Draw coordinate axes
canvas.create_line(0, canvas_height//2, canvas_width,
                   canvas_height//2, width=8)  # X-axis
canvas.create_line(canvas_width//2, 0, canvas_width//2,
                   canvas_height, width=8)    # Y-axis

# Draw gridlines
for i in range(1, 11):
    canvas.create_line(i * (canvas_width//10), 0, i * (canvas_width//10),
                       canvas_height, dash=(2, 2))  # Vertical gridlines
    canvas.create_line(0, i * (canvas_height//10), canvas_width,
                       i * (canvas_height//10), dash=(2, 2))  # Horizontal gridlines

# Indicator radius
indicator_radius = 3

# Create joystick indicator
joystick_indicator = canvas.create_oval(canvas_width//2 - indicator_radius, canvas_height//2 - indicator_radius,
                                        canvas_width//2 + indicator_radius, canvas_height//2 + indicator_radius,
                                        fill="red")

joystick_indicator_kalman = canvas.create_oval(canvas_width//2 - indicator_radius, canvas_height//2 - indicator_radius,
                                        canvas_width//2 + indicator_radius, canvas_height//2 + indicator_radius,
                                        fill="blue")
# Colors for random selection
colors = ["red", "green", "blue", "yellow", "orange", "purple"]

# Start updating position
update_position()

root.mainloop()
