import numpy as np

sigma = 15

# State Transition
A = np.array([
    [1,0,0.2,0],
    [0,1,0,0.2],
    [0,0,1,0],
    [0,0,0,1]
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

x = np.array([0, 0, 0, 0])

P = np.array([
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
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
noisyX = 1.0
noisyY = 2.0
x = np.array(x).reshape(-1, 1)  

for i in range(20):
    
    deltaX = noisyX - x[0, 0]
    deltaY = noisyY - x[1, 0]
    measurement = np.array([[noisyX], [noisyY], [deltaX], [deltaY]])
        
    # PREDICTION step
    # x = (A * x) + (B * c)
    x = np.dot(A, x) + np.dot(B, c)
    
    # P = (A * P * AT) + Q
    P = np.dot(np.dot(A, P), A.T) + Q

    # CORRECTION step
    # S = (H * P * HT) + R
    S = np.dot(np.dot(H, P), H.T) + R
    
    # K = P * HT * S^-1
    K = np.dot(np.dot(P, H.T), np.linalg.inv(S))
    
    # y = m - (H * x)
    y = measurement - np.dot(H, x)

    # x = x + (K * y)
    x = x + np.dot(K, y)
    
    print(f"x: {x[0]}")
    print(f"y: {x[1]}")
