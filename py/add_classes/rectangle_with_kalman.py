import random
import numpy as np
import tkinter as tk
from kalman_class import Kalman


# -- KALMAN PREFERENCES

# -- GUI CONFIGURATION
w_steps = 80
h_steps = 60
step_size = 10
canvas_width = w_steps * step_size
canvas_height = h_steps * step_size
route_padding = 60
line_width = '2'
dot_size = 1
dot_radius = max(int(line_width), dot_size)

fps = 24
tail = 20

kalman_obj = Kalman()
kalman_obj.set_sigma(15)

sigma = kalman_obj.get_sigma()

# -- SETUP
measurement_interval = int(1000/fps)
dot_x = route_padding
dot_y = route_padding


# Create the main window
root = tk.Tk()
root.geometry(f"{canvas_width}x{canvas_height}")
root.title("Kalman Example in 2D - Visualisation")

# Create a Canvas widget
canvas = tk.Canvas(root, width=canvas_width,
                   height=canvas_height, bg='#1F1F31')
canvas.pack()


def exact_oval_create(x, y):
    return canvas.create_oval(x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius, fill='blue', outline='')


def noise_oval_create(x, y):
    return canvas.create_oval(x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius, fill='green', outline='')


def kalman_oval_create(x, y):
    return canvas.create_oval(x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius, fill='red', outline='')


def noise_line_create(x, y, prev_x, prev_y):
    return canvas.create_line(x, y, prev_x, prev_y, fill='green', width=line_width)


def kalman_line_create(x, y, prev_x, prev_y):
    return canvas.create_line(x, y, prev_x, prev_y, fill='red', width=line_width)


exact_dots = []
for i in range(tail):
    exact_dots.append(exact_oval_create(route_padding, route_padding))

noise_dots = []
for i in range(tail):
    noise_dots.append(noise_oval_create(route_padding, route_padding))

noise_lines = []
for i in range(tail):
    noise_lines.append(noise_line_create(
        route_padding, route_padding, route_padding, route_padding))

kalman_dots = []
for i in range(tail):
    kalman_dots.append(kalman_oval_create(route_padding, route_padding))

kalman_lines = []
for i in range(tail):
    kalman_lines.append(kalman_line_create(
        route_padding, route_padding, route_padding, route_padding))

rectangle = canvas.create_rectangle(
    route_padding, route_padding, (canvas_width-route_padding), (canvas_height - route_padding), outline='#292940', width=1)
canvas.tag_lower(rectangle)


def check_position():
    global dot_x, dot_y, route_padding
    if (dot_x < (canvas_width - route_padding) and dot_y == route_padding):
        # TR
        dot_x = dot_x + step_size
    elif (dot_x == (canvas_width - route_padding) and dot_y <= (canvas_height - route_padding)):
        # TL
        dot_y = dot_y + step_size
    elif (dot_x > route_padding and dot_y >= (canvas_height - route_padding)):
        # BR
        dot_x = dot_x - step_size
    else:
        # BL
        dot_y = dot_y - step_size


def add_noise():
    global dot_x, dot_y, sigma
    noise = np.random.randn(2) * random.gauss(1, sigma)
    return [dot_x, dot_y] + noise


def update_canvas(new_x, new_y):

    global dot_x, dot_y
    dot_x = new_x
    dot_y = new_y

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
    exact_oval_temp = exact_dots.pop(0)
    noise_dots_temp = noise_dots.pop(0)
    noise_line_temp = noise_lines.pop(0)
    kalman_dot_temp = kalman_dots.pop(0)
    kalman_lines_temp = kalman_lines.pop(0)

    prev_noise_line = canvas.coords(noise_lines[len(noise_lines)-1])
    prev_kalman_line = canvas.coords(kalman_lines[len(kalman_lines)-1])

    canvas.coords(exact_oval_temp, dot_x - dot_radius, dot_y -
                  dot_radius, dot_x + dot_radius, dot_y + dot_radius)

    canvas.coords(noise_dots_temp, noise_x - dot_radius, noise_y -
                  dot_radius, noise_x + dot_radius, noise_y + dot_radius)

    canvas.coords(noise_line_temp,
                  prev_noise_line[2], prev_noise_line[3], noise_x, noise_y)

    canvas.coords(kalman_dot_temp, kalman_x - dot_radius, kalman_y -
                  dot_radius, kalman_x + dot_radius, kalman_y + dot_radius)

    canvas.coords(kalman_lines_temp, prev_kalman_line[2],
                  prev_kalman_line[3], kalman_x, kalman_y)

    # PUSH ELEMENTS
    exact_dots.insert(len(exact_dots), exact_oval_temp)
    noise_dots.insert(len(noise_dots), noise_dots_temp)
    noise_lines.insert(len(noise_lines), noise_line_temp)
    kalman_dots.insert(len(kalman_dots), kalman_dot_temp)
    kalman_lines.insert(len(kalman_lines), kalman_lines_temp)

    check_position()
    root.after(measurement_interval, update_canvas, dot_x, dot_y)


root.after(measurement_interval, update_canvas, dot_x, dot_y)
root.mainloop()
