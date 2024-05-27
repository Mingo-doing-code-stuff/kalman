import tkinter as tk
import random
import numpy as np

sigma = 2
variance = sigma ** 2

# measurement interval in ms
measurement_interval = 100

delta_t = measurement_interval / 1000

# State Transition
A = np.array([
    [1, 0, 10, 0],
    [0, 1, 0, 10],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])

# Input Control Matrix is ignored
B = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])

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
    [0, 0, 0.01, 0],
    [0, 0, 0, 0.01]
])

# Measurement Noise
R = np.array([
    [variance, 0, 0, 0],
    [0, variance, 0, 0],
    [0, 0, variance, 0],
    [0, 0, 0, variance]
])

x = np.array([0, 0, 0, 0])

P = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])

A = np.array(A)
B = np.array(B)
H = np.array(H)
Q = np.array(Q)
R = np.array(R)
x = np.array(x)
P = np.array(P)
I = np.eye(4)
c = np.zeros((4, 1))  # Assuming control vector is zero
print(x)
x = np.array(x).reshape(-1, 1)
print(x)


def calculate_kalman(noisy_x, noisy_y, prev_noisy_x, prev_noisy_y):
    global x, P  # Declare x and P as global variables
    x[0, 0] = prev_noisy_x
    x[1, 0] = prev_noisy_y
    deltaX = noisy_x - x[0, 0]
    deltaY = noisy_y - x[1, 0]

    measurement = np.array([[noisy_x], [noisy_y], [deltaX], [deltaY]])

    # PREDICTION step
    # [x_k = A * x_k-1 + B * u_k-1]
    print(f"x1: {x}")
    x = np.dot(A, x)
    print(f"x2: {x}")

    # [P_k = A * P_k-1 * A^T + Q ]
    P = np.dot(np.dot(A, P), A.T) + Q

    # CORRECTION step

    S = np.dot(H, np.dot(P, H.T)) + R

    y = measurement - np.dot(H, x)

    # [K_k = P_k * H^T * (H * P_k * H^T + R)^-1]
    K = np.dot(np.dot(P, H.T), np.linalg.inv(S))

    print(f"kalman-gain: \n{K}")

    # x_k = x_k + K_k(z_k - H * x_k)]
    x = x + np.dot(K, y)

    # [ P_k = ( I - K_k * H) * P_k]
    P = np.dot((I - np.dot(K, H)), P)

    print(f"P:\n{P}")

    return x[0, 0], x[1, 0]


# Create the main window
root = tk.Tk()
root.title("Responsive Dot")
root.geometry("400x400")

canvas_width = 400
canvas_height = 400

# Create a Canvas widget
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
canvas.pack()

# Draw the initial dot (circle)
dot_radius = 4
noise_dot_radius = 0
initial_x = 40
initial_y = 40
tail = 20
noise_factor = 4
# Initial position
dot_x = initial_x
dot_y = initial_y


def oval_create(x, y):
    return canvas.create_oval(x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius)


def noise_oval_create(x, y):
    return canvas.create_oval(x - noise_dot_radius, y - noise_dot_radius, x + noise_dot_radius, y + noise_dot_radius, fill='lightgreen')


def noise_line_create(x, y, prev_x, prev_y):
    return canvas.create_line(x, y, prev_x, prev_y, fill='lightgreen', width='2')


def kalman_line_create(x, y, prev_x, prev_y):
    return canvas.create_line(x, y, prev_x, prev_y, fill='black', width='2')


last_dots = []
for i in range(tail):
    last_dots.append(oval_create(40, 40))

noise_dots = []
for i in range(tail):
    noise_dots.append(noise_oval_create(40, 40))

noise_lines = []
for i in range(tail):
    noise_lines.append(noise_line_create(40, 40, 40, 40))

kalman_lines = []
for i in range(tail):
    kalman_lines.append(kalman_line_create(40, 40, 40, 40))

rectangle = canvas.create_rectangle(
    40, 40, 360, 360, outline='lightgrey', width=1)

canvas.tag_lower(rectangle)

print(last_dots)


def check_position():
    global dot_x, dot_y
    if (dot_x < 360 and dot_y == 40):
        dot_x = dot_x + dot_radius * 4
    elif (dot_x == 360 and dot_y < 360):
        dot_y = dot_y + dot_radius * 4
    elif (dot_x > 40 and dot_y == 360):
        dot_x = dot_x - dot_radius * 4
    else:
        dot_y = dot_y - dot_radius * 4


def add_noise():
    global dot_x, dot_y
    noise = np.random.randn(2) * noise_factor
    print(f"noise: {noise}")
    return [dot_x, dot_y] + noise


def move_dot(new_x, new_y):

    global dot_x, dot_y
    dot_x = new_x
    dot_y = new_y
    noise_x, noise_y = add_noise()

    prev_noise_temp = noise_dots[len(noise_dots)-1]

    prev_noise_dot = canvas.coords(prev_noise_temp)
    prev_noise_x = prev_noise_dot[0] + noise_dot_radius
    prev_noise_y = prev_noise_dot[1] + noise_dot_radius

    kalman_x, kalman_y = calculate_kalman(
        noise_x, noise_y, prev_noise_x, prev_noise_y)

    print(prev_noise_x, prev_noise_y)
    print(kalman_x, kalman_y)

    oval_temp = last_dots.pop(0)
    noise_temp = noise_dots.pop(0)
    line_temp = noise_lines.pop(0)
    kalman_temp = kalman_lines.pop(0)

    prev_line = canvas.coords(noise_lines[len(noise_lines)-1])
    prev_kalman = canvas.coords(kalman_lines[len(kalman_lines)-1])

    canvas.coords(noise_temp, noise_x - noise_dot_radius, noise_y -
                  noise_dot_radius, noise_x + noise_dot_radius, noise_y + noise_dot_radius)

    canvas.coords(oval_temp, dot_x - dot_radius, dot_y - dot_radius,
                  dot_x + dot_radius, dot_y + dot_radius)
    canvas.itemconfig(oval_temp, fill='', outline='')

    canvas.coords(line_temp, prev_line[2], prev_line[3], noise_x, noise_y)

    canvas.coords(kalman_temp, prev_kalman[2],
                  prev_kalman[3], kalman_x, kalman_y)

    last_dots.insert(len(last_dots), oval_temp)
    noise_dots.insert(len(noise_dots), noise_temp)
    noise_lines.insert(len(noise_lines), line_temp)
    kalman_lines.insert(len(kalman_lines), kalman_temp)

    canvas.itemconfig(last_dots[0], fill='lightblue')

    print(last_dots)
    check_position()

    print(dot_x, dot_y)
    root.after(measurement_interval, move_dot, dot_x, dot_y)


# Example of updating the dot's position after 2 seconds
# Move dot to (300, 300) after 2 seconds
root.after(measurement_interval, move_dot, dot_x, dot_y)

# Run the Tkinter event loop
root.mainloop()
