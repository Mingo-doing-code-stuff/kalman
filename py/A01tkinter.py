import tkinter as tk
import random
import numpy as np

# measurement interval in ms
measurement_interval = 20

delta_t = 0 #1 #measurement_interval / 1000

sigma = 15
draw_phase = 0
real_point = None
states = []
canvas_width = 800
canvas_height = 600
route_padding = 40
# State Transition
A = np.array([[1, 0, 0.2, 0],
                    [0, 1, 0, 0.2],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])

# Input Control Matrix is ignored
B = np.eye(4)

# Observation Matrix
H = np.array([[1, 0, 1, 0],
                    [0, 1, 0, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]])

# Process Noise
Q = np.array([[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0.1, 0],
                    [0, 0, 0, 0.1]])

# Measurement Noise
R = np.array([[sigma, 0, 0, 0],
                    [0, sigma, 0, 0],
                    [0, 0, sigma, 0],
                    [0, 0, 0, sigma]])

x = np.zeros((4, 1))
x_prev = np.zeros((4, 1))

P = np.zeros((4, 4))
P_prev = np.zeros((4, 4))

I = np.eye(4)

c = np.zeros((4, 1))


def calculate_kalman(noisy_x, noisy_y, prev_noisy_x, prev_noisy_y):
    # Declare x, x_prev, P and P_prev as global variables
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

root.title("Responsive Dot")
root.geometry(f"{canvas_width}x{canvas_height}")
root.title("Kalman Example in 2D - Visualisation")

# Create a Canvas widget
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='#1F1F31')
canvas.pack()

# Draw the initial dot (circle)
dot_radius = 2
noise_dot_radius = 2
initial_x = 40
initial_y = 40
tail = 20
noise_factor = 5 #0.5
step_size = 8
# Initial position
dot_x = initial_x
dot_y = initial_y



def oval_create(x, y):
    return canvas.create_oval(x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius, fill='blue', outline='')

def noise_oval_create(x, y):
    return canvas.create_oval(x - noise_dot_radius, y - noise_dot_radius, x + noise_dot_radius, y + noise_dot_radius, fill='lightgreen', outline='')

def noise_line_create(x, y, prev_x, prev_y):
    return canvas.create_line(x, y, prev_x, prev_y, fill='lightgreen', width='2')

def kalman_line_create(x, y, prev_x, prev_y):
    return canvas.create_line(x, y, prev_x, prev_y, fill='red', width='2')


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
    40, 40, 360, 360, outline='#292940', width=1)

canvas.tag_lower(rectangle)

def check_position():
    global dot_x, dot_y
    if (dot_x < 360 and dot_y == 40):
        dot_x = dot_x + step_size
    elif (dot_x == 360 and dot_y < 360):
        dot_y = dot_y + step_size
    elif (dot_x > 40 and dot_y == 360):
        dot_x = dot_x - step_size
    else:
        dot_y = dot_y - step_size


def add_noise():
    global dot_x, dot_y
    noise = np.array([1,1]) + random.gauss(1, 15)
    return [dot_x, dot_y] + noise



def update_canvas(new_x, new_y):

    global dot_x, dot_y
    dot_x = new_x
    dot_y = new_y

    # DEBUG BEGIN
    global render_iteration
    render_iteration += 1 
    # DEBUG END

    noise_x, noise_y = add_noise()
    prev_noise_temp = noise_dots[len(noise_dots)-1]
    prev_noise_dot = canvas.coords(prev_noise_temp)
    prev_noise_x = prev_noise_dot[0] + noise_dot_radius
    prev_noise_y = prev_noise_dot[1] + noise_dot_radius
    print(f"-- previous Noise point was: {prev_noise_x}, {prev_noise_y}\n")

    kalman_x, kalman_y = calculate_kalman(
        noise_x, noise_y, prev_noise_x, prev_noise_y)

    print(f"Kalman received: {noise_x}, {noise_y}, {prev_noise_x}, {prev_noise_y}\n")
    print(f"kalman x:\t{kalman_x},\nkalman y:\t{kalman_y}\n")

    # POP ELEMENTS
    oval_temp = last_dots.pop(0)
    noise_temp = noise_dots.pop(0)
    line_temp = noise_lines.pop(0)
    kalman_temp = kalman_lines.pop(0)

    prev_line   = canvas.coords( noise_lines[len(noise_lines )-1])
    prev_kalman = canvas.coords(kalman_lines[len(kalman_lines)-1])

    canvas.coords(noise_temp, noise_x - noise_dot_radius, noise_y - noise_dot_radius, noise_x + noise_dot_radius, noise_y + noise_dot_radius)
    canvas.coords(oval_temp, dot_x - dot_radius, dot_y - dot_radius, dot_x + dot_radius, dot_y + dot_radius)
    canvas.coords(line_temp, prev_line[2], prev_line[3], noise_x, noise_y)
    canvas.coords(kalman_temp, prev_kalman[2], prev_kalman[3], kalman_x, kalman_y)

    # PUSH ELEMENTS
    last_dots.insert(len(last_dots), oval_temp)
    noise_dots.insert(len(noise_dots), noise_temp)
    noise_lines.insert(len(noise_lines), line_temp)
    kalman_lines.insert(len(kalman_lines), kalman_temp)

    check_position()
    root.after(measurement_interval, update_canvas, dot_x, dot_y)



# Example of updating the dot's position after 2 seconds
# Move dot to (300, 300) after 2 seconds
root.after(measurement_interval, update_canvas, dot_x, dot_y)

# Run the Tkinter event loop
root.mainloop()
