import serial
import tkinter as tk
import random


def update_position():
    data = ser.readline().decode().strip().split(',')
    if len(data) == 3:
        x_pos, y_pos, is_pressed = map(int, data)

        # Update coordinate system
        x_mapped = int((1023 - x_pos) / 1023 * canvas_width)
        y_mapped = int((y_pos / 1023) * canvas_height)  # Invert the Y-axis
        canvas.coords(joystick_indicator, x_mapped - indicator_radius, y_mapped - indicator_radius,
                      x_mapped + indicator_radius, y_mapped + indicator_radius)

        # Change color randomly when joystick is pressed
        if is_pressed == 0:
            random_color = random.choice(colors)
            canvas.itemconfig(joystick_indicator, fill=random_color)

    # Schedule the next update
    # Update every 10 milliseconds for real-time updates
    root.after(10, update_position)


# Serial port configuration
# Replace 'COM4' with your Arduino's serial port
ser = serial.Serial('COM4', 9600)

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
                   canvas_height//2, width=1)  # X-axis
canvas.create_line(canvas_width//2, 0, canvas_width//2,
                   canvas_height, width=1)    # Y-axis

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

# Colors for random selection
colors = ["red", "green", "blue", "yellow", "orange", "purple"]

# Start updating position
update_position()

root.mainloop()
