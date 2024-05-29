import random
import numpy as np
import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap import ttk  # Use ttk from ttkbootstrap

# -- KALMAN PREFERENCES

sigma = 1 # //TODO: Fix the adjustability of sigma
draw_phase = 0
real_point = None

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


# -- SETUP
measurement_interval = int(1000/fps)
dot_x = route_padding
dot_y = route_padding

# State Transition
A = np.array([
    [1, 0, 0.2, 0],
    [0, 1, 0, 0.2],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])

# Input Control Matrix is ignored
B = np.eye(4)

# Observation Matrix
H = np.array([
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
])

# Process Noise
Q = np.array([
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0.1, 0],
    [0, 0, 0, 0.1]
])

# Measurement Noise
R = np.array([
    [sigma, 0, 0, 0],
    [0, sigma, 0, 0],
    [0, 0, sigma, 0],
    [0, 0, 0, sigma]
])

x = np.zeros((4, 1))
x_prev = np.zeros((4, 1))

P = np.zeros((4, 4))
P_prev = np.zeros((4, 4))

I = np.eye(4)

c = np.zeros((4, 1))

def calculate_kalman(noisy_x, noisy_y, prev_noisy_x, prev_noisy_y):
    global x, x_prev, P, P_prev
    x[0, 0] = prev_noisy_x
    x[1, 0] = prev_noisy_y
    deltaX = noisy_x - x[0, 0]
    deltaY = noisy_y - x[1, 0]
    measurement = np.array([[noisy_x], [noisy_y], [deltaX], [deltaY]])

    # PREDICTION step
    # [x_k = A * x_k-1 + B * u_k-1]
    x = np.dot(A, x_prev) + np.dot(B, c)
    # [P_k = A * P_k-1 * A^T + Q ]
    P = np.dot(np.dot(A, P_prev), A.T) + Q

    # CORRECTION step
    measurement = measurement - np.dot(H, x)
    # [K_k = P_k * H^T * (H * P_k * H^T + R)^-1]
    S = np.dot(np.dot(H, P), H.T) + R
    K = np.dot(np.dot(P, H.T), np.linalg.inv(S))
    # x_k = x_k + K_k(z_k - H * x_k)]
    x_prev = x + np.dot(K, measurement)
    # [ P_k = ( I - K_k * H) * P_k]
    P_prev = np.dot(np.eye(4) - np.dot(K, H), P)

    return x[0, 0], x[1, 0]


# Create the main window
root = tk.Tk()
root.geometry(f"{canvas_width}x{canvas_height}")
root.title("Kalman Example in 2D - Visualisation")

# Create a Canvas widget
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='#1F1F31')
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
    noise_lines.append(noise_line_create(route_padding, route_padding, route_padding, route_padding))

kalman_dots = []
for i in range(tail):
    kalman_dots.append(kalman_oval_create(route_padding, route_padding))

kalman_lines = []
for i in range(tail):
    kalman_lines.append(kalman_line_create(route_padding, route_padding, route_padding, route_padding))

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
        #BL
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

    kalman_x, kalman_y = calculate_kalman(
        noise_x, noise_y, prev_noise_x, prev_noise_y)

    print(
        f"Kalman received: {noise_x}, {noise_y}, {prev_noise_x}, {prev_noise_y}\n")
    print(f"kalman x:\t{kalman_x},\nkalman y:\t{kalman_y}\n")

    # POP ELEMENTS
    exact_oval_temp = exact_dots.pop(0)
    noise_dots_temp = noise_dots.pop(0)
    noise_line_temp = noise_lines.pop(0)
    kalman_dot_temp =kalman_dots.pop(0)
    kalman_lines_temp = kalman_lines.pop(0)

    prev_noise_line = canvas.coords(noise_lines[len(noise_lines)-1])
    prev_kalman_line = canvas.coords(kalman_lines[len(kalman_lines)-1])

    canvas.coords(exact_oval_temp, dot_x - dot_radius, dot_y -
                  dot_radius, dot_x + dot_radius, dot_y + dot_radius)
    
    canvas.coords(noise_dots_temp, noise_x - dot_radius, noise_y -
                  dot_radius, noise_x + dot_radius, noise_y + dot_radius)
    
    canvas.coords(noise_line_temp, prev_noise_line[2], prev_noise_line[3], noise_x, noise_y)

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


canvas.grid(row=0, column=0, padx=10, pady=10)

# Create a frame for sliders and buttons
control_frame = Frame(root)
control_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

# Create sliders
x_slider = Scale(control_frame, from_=0, to=350, label="X Position", orient="horizontal")
x_slider.grid(row=0, column=0, pady=5)
x_slider.bind("<Motion>", lambda event: update_canvas())  # Update canvas on slider change

y_slider = Scale(control_frame, from_=0, to=350, label="Y Position", orient="horizontal")
y_slider.grid(row=1, column=0, pady=5)
y_slider.bind("<Motion>", lambda event: update_canvas())  # Update canvas on slider change

# Create a toggle button
toggle_var = IntVar()
toggle_button = Checkbutton(control_frame, text="Toggle Color", variable=toggle_var, command=update_canvas)
toggle_button.grid(row=2, column=0, pady=5)

# Create a dropdown (combobox) widget
dropdown_var = tk.StringVar(value="Option 1")
dropdown = ttk.Combobox(control_frame, textvariable=dropdown_var)
dropdown['values'] = ("Option 1", "Option 2")
dropdown.grid(row=3, column=1, padx=10, pady=5)
dropdown.bind("<<ComboboxSelected>>", update_canvas)

root.after(measurement_interval, update_canvas, dot_x, dot_y)
root.mainloop()
