import numpy as np
import pandas as pd
import seaborn as sb
from scipy import stats
import serial
import tkinter as tk
import random
import time
import functools
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('c_serial_port/gyro.csv', delimiter=';')


# Starting values
mean0 = 0.0   # e.g. meters or miles
var0 = 1

# simulated physics prediction
y_data = df.iloc[:, 0]
meanMove_Array = [0.0] * 10
meanMove = 0.0
varMove = 0.1


def predict(var, mean, varMove, meanMove):
    new_var = var + varMove
    new_mean = mean + meanMove
    return new_var, new_mean


new_var, new_mean = predict(var0, mean0, varMove, meanMove)

meanSensor = -0.0110981098109811
varSensor = 0.535789412157859


def correct(var, mean, varSensor, meanSensor):
    new_mean = (varSensor*mean + var*meanSensor) / (var+varSensor)
    new_var = 1/(1/var + 1/varSensor)
    return new_var, new_mean


var, mean = correct(new_var, new_mean, varSensor, meanSensor)

distances = y_data
positions = []
correction = []
predictions = []
mean = mean0
var = var0

for m in range(len(distances)):
    # varMove = 50

    # Predict
    var, mean = predict(var, mean, varMove, distances[m])

    predictions.append(mean)

    print('After prediction:\tmean= %.2f\tvar= %.2f' % (mean, var))

    # positions.append(y_data[0:m].sum())
    positions.append(y_data[m])
    meanMove_Array.insert(0, y_data[m])
    meanMove_Array.pop()
    meanMove = functools.reduce(lambda a, b: a+b, meanMove_Array) / 10

    # Correct
    var, mean = correct(var, mean, varSensor, meanMove)
    correction.append(mean)
    print('After correction:\tmean= %.2f\tvar=  %.2f' % (mean, var))
    print('Actual value:\t\t\tposi= %.2f\n' % positions[m])


print(correction)
print(positions)
print(predictions)

plt.figure(figsize=(10, 5))
plt.plot(correction[0:200], label='Correction', marker='x')
plt.plot(positions[1:201], label='Sensor data', marker='.', linestyle='')
plt.plot(predictions[0:200], label='Prediction')
plt.legend(loc='best')
plt.xlabel('Count')
plt.show()
