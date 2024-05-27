import tkinter as tk
import random
import math
import numpy as np


width = 350
height = 350
sigma = 15
draw_phase = 0
real_point = None
states = []

# Kalman filter variables
A = np.array([[1, 0, 0.2, 0],
                    [0, 1, 0, 0.2],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
B = np.eye(4)
H = np.array([[1, 0, 1, 0],
                    [0, 1, 0, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]])
Q = np.array([[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0.1, 0],
                    [0, 0, 0, 0.1]])
R = np.array([[sigma, 0, 0, 0],
                    [0, sigma, 0, 0],
                    [0, 0, sigma, 0],
                    [0, 0, 0, sigma]])
last_point = np.zeros((4, 1))
last = np.zeros((4, 4))
c = np.zeros((4, 1))



def random_gaussian(mean=0.0, stddev=1.0):
    return random.gauss(mean, stddev)

def create_point(x, y):
    return {'x': x, 'y': y, 'ttl': 50}

def frame():
    global real_point, last_point, draw_phase, last
    draw_phase = draw_phase

    canvas.delete('all')
    step = 4

    if real_point is None:
        real_point = create_point(180, 180)

    if draw_phase == 0:
        real_point['x'] += step
        if real_point['x'] > width - width // 5:
            draw_phase = 1
    elif draw_phase == 1:
        real_point['y'] += step
        if real_point['y'] > height - height // 5:
            draw_phase = 2
    elif draw_phase == 2:
        real_point['x'] -= step
        if real_point['x'] < width // 5:
            draw_phase = 3
    elif draw_phase == 3:
        real_point['y'] -= step
        if real_point['y'] < height // 5:
            draw_phase = 0

    noisy_x = real_point['x'] + random_gaussian(0, sigma)
    noisy_y = real_point['y'] + random_gaussian(0, sigma)

    # Measurement vector
    measurement = np.array([[noisy_x], [noisy_y], [noisy_x - last_point[0, 0]], [noisy_y - last_point[1, 0]]])

    # Prediction step
    x = np.dot(A, last_point) + np.dot(B, c)
    P = np.dot(np.dot(A, last), A.T) + Q

    # Correction step
    S = np.dot(np.dot(H, P), H.T) + R
    K = np.dot(np.dot(P, H.T), np.linalg.inv(S))
    y = measurement - np.dot(H, x)

    last_point = x + np.dot(K, y)
    last = np.dot(np.eye(4) - np.dot(K, H), P)

    canvas.create_oval(real_point['x'] - 2, real_point['y'] - 2, real_point['x'] + 2, real_point['y'] + 2, fill='#0d47a1')
    canvas.create_oval(noisy_x - 2, noisy_y - 2, noisy_x + 2, noisy_y + 2, fill='#388e3c')
    canvas.create_oval(last_point[0, 0] - 2, last_point[1, 0] - 2, last_point[0, 0] + 2, last_point[1, 0] + 2, fill='#dd2c00')

    root.after(125, frame)

root = tk.Tk()
canvas = tk.Canvas(root, width=width, height=height, bg='#37474f')
canvas.pack()

root.after(125 , frame)
root.mainloop()