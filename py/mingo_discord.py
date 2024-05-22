import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('c_serial_port/data_flugzeug.csv', delimiter=';')
messurement_data_gyro_axis_x = df.iloc[:, 0]


# Anzahl der Messwerte
messurement_sample_size = len(messurement_data_gyro_axis_x)

# Median der Messwerte
median_of_messurement_data = np.median(messurement_data_gyro_axis_x)

# Temperaturbias (Drift) berechnen
gyroXbias = messurement_data_gyro_axis_x - median_of_messurement_data

# Varianz der Messergebnisse (für ein anschauliches Beispiel verwenden wir 0.1)
gyroXbiasVarianz = 0.1


# Anwendung der Filteriterationen

# Varianz der Messergebnisse wird durch R dargestellt
varianz_der_messung = gyroXbiasVarianz

# Einheitsmatrix, hier numerisch, deshalb = 1
I = 1

# Initiale Vorbelegung
filter_collected_values_array = np.zeros(messurement_sample_size)
kalman_collected_values_array = np.zeros(messurement_sample_size)
estimate_previous_iteration = 0
# Vorheriger Messwert unbekannt, deshalb 0
estimate_current_iteration = estimate_previous_iteration

# Fehlerkovarianz am Anfang 1 und nicht 0, da normalerweise immer ein Messrauschen vorhanden ist
error_covariance_previous_iteration = 1
error_covariance_current_iteration = error_covariance_previous_iteration

# Iteration 1: Erste Schätzung
winkelgeschwindigkeit = gyroXbias[0]
kalman_gain_current_iteration = error_covariance_current_iteration / \
    (error_covariance_current_iteration + varianz_der_messung)
kalman_collected_values_array[0] = kalman_gain_current_iteration
estimate_current_iteration = estimate_current_iteration + \
    kalman_gain_current_iteration * \
    (winkelgeschwindigkeit - estimate_current_iteration)
filter_collected_values_array[0] = estimate_current_iteration
error_covariance_current_iteration = (
    I - kalman_gain_current_iteration) * error_covariance_current_iteration

# Iteration 2 bis gyroXarrSize
for iteration in range(1, messurement_sample_size):

    # Vorhersage
    winkelgeschwindigkeit = gyroXbias[iteration]  # Aktuelle Messung
    # xk = xk-1
    estimate_current_iteration = filter_collected_values_array[iteration - 1]

    # Korrektur
    kalman_gain_current_iteration = error_covariance_current_iteration / \
        (error_covariance_current_iteration + varianz_der_messung)
    kalman_collected_values_array[iteration] = kalman_gain_current_iteration
    estimate_current_iteration = estimate_current_iteration + \
        kalman_gain_current_iteration * \
        (winkelgeschwindigkeit - estimate_current_iteration)
    filter_collected_values_array[iteration] = estimate_current_iteration
    error_covariance_current_iteration = (
        I - kalman_gain_current_iteration) * error_covariance_current_iteration


# Graph plotten
fig, axs = plt.subplots(2)
axs[1].bar(range(gyroXarrSize), kalmanVals, label='Kk: Kalman Gain',
           linestyle='-', color=[0, 0.75, 1], edgecolor='b')
axs[0].plot(gyroXbias, '-', label='zk: Messwerte', color='red')
axs[0].plot(filterVals, color='green', linewidth=2,
            label='xk: gefilterte Werte')
axs[0].axhline(0, color='blue', label='reales Signal')

# Legende anzeigen
axs[0].legend()

# Achsenbeschriftung
axs[0].set_xlabel('Zeit in ms')
axs[0].set_ylabel('Winkelgeschwindigkeit in °/s')


# Bereich X-Achse anpassen
axs[0].set_xlim([0, gyroXarrSize])
axs[1].set_xlim([0, gyroXarrSize])

# Plot anzeigen
plt.show()
