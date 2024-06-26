import tkinter as tk
import random
import numpy as np
import serial
from kalman_class import Kalman

ser = serial.Serial('COM4', 9600)

ser.readline().decode().strip().split(',')


# -- KALMAN PREFERENCES
measurement_interval = 20
draw_phase = 0

# -- GUI CONFIGURATION
w_steps = 80
h_steps = 60
step_size = 10
canvas_width = w_steps * step_size
canvas_height = h_steps * step_size
dot_radius = 2

tail = 20

# -- SETUP
dot_x = canvas_width / 2
dot_y = canvas_height / 2

kalman_obj = Kalman()

kalman_obj.set_sigma(15)
sigma = kalman_obj.get_sigma()


# Create the main window
root = tk.Tk()
root.title("Responsive Dot")
root.geometry(f"{canvas_width}x{canvas_height}")
root.title("Kalman Example in 2D - Visualisation")


# Create a Canvas widget
canvas = tk.Canvas(root, width=canvas_width,
                   height=canvas_height, bg='#1F1F31')
canvas.pack()

# Indicator radius
indicator_radius = 3

joystick_indicator = canvas.create_oval(canvas_width//2 - indicator_radius, canvas_height//2 - indicator_radius,
                                        canvas_width//2 + indicator_radius, canvas_height//2 + indicator_radius,
                                        fill="red")


def update_position():
    data = ser.readline().decode().strip().split(',')
    if len(data) == 3:
        x_pos, y_pos, is_pressed = map(int, data)

        # Update coordinate system
        x_mapped = int((1023 - x_pos) / 1023 * canvas_width)
        y_mapped = int((y_pos / 1023) * canvas_height)  # Invert the Y-axis
        canvas.coords(joystick_indicator, x_mapped - indicator_radius, y_mapped - indicator_radius,
                      x_mapped + indicator_radius, y_mapped + indicator_radius)

        return x_mapped, y_mapped
    return update_position()


def oval_create(x, y):
    return canvas.create_oval(x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius, fill='blue', outline='')


def noise_oval_create(x, y):
    return canvas.create_oval(x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius, fill='lightgreen', outline='')


def noise_line_create(x, y, prev_x, prev_y):
    return canvas.create_line(x, y, prev_x, prev_y, fill='lightgreen', width='2')


def kalman_line_create(x, y, prev_x, prev_y):
    return canvas.create_line(x, y, prev_x, prev_y, fill='red', width='2')


last_dots = []
for i in range(tail):
    last_dots.append(oval_create(canvas_width / 2, canvas_height / 2))

noise_dots = []
for i in range(tail):
    noise_dots.append(noise_oval_create(canvas_width / 2, canvas_height / 2))

noise_lines = []
for i in range(tail):
    noise_lines.append(noise_line_create(
        canvas_width / 2, canvas_height / 2, canvas_width / 2, canvas_height / 2))

kalman_lines = []
for i in range(tail):
    kalman_lines.append(kalman_line_create(
        canvas_width / 2, canvas_height / 2, canvas_width / 2, canvas_height / 2))


def add_noise():
    global dot_x, dot_y
    noise = np.random.randn(2) * random.gauss(1, 15)
    return [dot_x, dot_y] + noise


def update_canvas():

    joystick_x, joystick_y = update_position()

    global dot_x, dot_y
    dot_x = joystick_x
    dot_y = joystick_y

    noise_x, noise_y = add_noise()
    prev_noise_temp = noise_dots[len(noise_dots)-1]
    prev_noise_dot = canvas.coords(prev_noise_temp)
    prev_noise_x = prev_noise_dot[0] + dot_radius
    prev_noise_y = prev_noise_dot[1] + dot_radius
    print(f"-- previous Noise point was: {prev_noise_x}, {prev_noise_y}\n")

    kalman_x, kalman_y = kalman_obj.calculate_kalman(
        noise_x, noise_y, prev_noise_x, prev_noise_y)

    print(
        f"Kalman received: {noise_x}, {noise_y}, {prev_noise_x}, {prev_noise_y}\n")
    print(f"kalman x:\t{kalman_x},\nkalman y:\t{kalman_y}\n")

    # POP ELEMENTS
    oval_temp = last_dots.pop(0)
    noise_temp = noise_dots.pop(0)
    line_temp = noise_lines.pop(0)
    kalman_temp = kalman_lines.pop(0)

    prev_line = canvas.coords(noise_lines[len(noise_lines)-1])
    prev_kalman = canvas.coords(kalman_lines[len(kalman_lines)-1])

    canvas.coords(noise_temp, noise_x - dot_radius, noise_y -
                  dot_radius, noise_x + dot_radius, noise_y + dot_radius)
    canvas.coords(oval_temp, dot_x - dot_radius, dot_y -
                  dot_radius, dot_x + dot_radius, dot_y + dot_radius)
    canvas.coords(line_temp, prev_line[2], prev_line[3], noise_x, noise_y)
    canvas.coords(kalman_temp, prev_kalman[2],
                  prev_kalman[3], kalman_x, kalman_y)

    # PUSH ELEMENTS
    last_dots.insert(len(last_dots), oval_temp)
    noise_dots.insert(len(noise_dots), noise_temp)
    noise_lines.insert(len(noise_lines), line_temp)
    kalman_lines.insert(len(kalman_lines), kalman_temp)

    root.after(measurement_interval, update_canvas)


root.after(measurement_interval, update_canvas)
root.mainloop()
