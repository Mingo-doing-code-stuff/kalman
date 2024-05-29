import numpy as np


class Kalman:

    # -- SETUP
    def __init__(self, x_start, y_start):
        self.dot_x = x_start
        self.dot_y = y_start

    sigma = 1

    def set_sigma(self, s):
        self.sigma = s
    
    def get_sigma(self):
        return self.sigma

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

    def calculate_kalman(self, noisy_x, noisy_y, prev_noisy_x, prev_noisy_y):
        self.x[0, 0] = prev_noisy_x
        self.x[1, 0] = prev_noisy_y
        deltaX = noisy_x - self.x[0, 0]
        deltaY = noisy_y - self.x[1, 0]
        measurement = np.array([[noisy_x], [noisy_y], [deltaX], [deltaY]])

        # PREDICTION step
        # [x_k = A * x_k-1 + B * u_k-1]
        self.x = np.dot(self.A, self.x_prev) + np.dot(self.B, self.c)
        # [P_k = A * P_k-1 * A^T + Q ]
        self.P = np.dot(np.dot(self.A, self.P_prev), self.A.T) + self.Q

        # CORRECTION step
        measurement = measurement - np.dot(self.H, self.x)
        # [K_k = P_k * H^T * (H * P_k * H^T + R)^-1]
        self.S = np.dot(np.dot(self.H, self.P), self.H.T) + self.R
        self.K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(self.S))
        # x_k = x_k + K_k(z_k - H * x_k)]
        self.x_prev = self.x + np.dot(self.K, measurement)
        # [ P_k = ( I - K_k * H) * P_k]
        self.P_prev = np.dot(self.I - np.dot(self.K, self.H), self.P)

        return self.x[0, 0], self.x[1, 0]
