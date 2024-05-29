import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('c_serial_port/data_flugzeug.csv', delimiter=';')
messurement_data_gyro_axis_x= df.iloc[:, 0]


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
estimate_current_iteration = estimate_previous_iteration  # Vorheriger Messwert unbekannt, deshalb 0

# Fehlerkovarianz am Anfang 1 und nicht 0, da normalerweise immer ein Messrauschen vorhanden ist
error_covariance = 1
error_covariance = error_covariance

# Iteration 1: Erste Schätzung
winkelgeschwindigkeit = gyroXbias[0]
kalman_gain_current_iteration = error_covariance / (error_covariance + varianz_der_messung)
kalman_collected_values_array[0] = kalman_gain_current_iteration
estimate_current_iteration = estimate_current_iteration + kalman_gain_current_iteration * (winkelgeschwindigkeit - estimate_current_iteration)
filter_collected_values_array[0] = estimate_current_iteration
error_covariance = (I - kalman_gain_current_iteration) * error_covariance

# Iteration 2 bis gyroXarrSize
for iteration in range(1, messurement_sample_size):
    # Vorhersage
    winkelgeschwindigkeit = gyroXbias[iteration]  # Aktuelle Messung
    estimate_current_iteration = filter_collected_values_array[iteration - 1]  # xk = xk-1

    # Korrektur
    kalman_gain_current_iteration = error_covariance / (error_covariance + varianz_der_messung)
    kalman_collected_values_array[iteration] = kalman_gain_current_iteration
    estimate_current_iteration = estimate_current_iteration + kalman_gain_current_iteration * (winkelgeschwindigkeit - estimate_current_iteration)
    filter_collected_values_array[iteration] = estimate_current_iteration
    error_covariance = (I - kalman_gain_current_iteration) * error_covariance

# Graph plotten
plt.figure()
plt.bar(range(messurement_sample_size), kalman_collected_values_array, label='Kk: Kalman Gain', linestyle='-', color=[0, 0.75, 1], edgecolor='b')
plt.plot(gyroXbias, '-', label='zk: Messwerte', color='red')
plt.plot(filter_collected_values_array, color='green', linewidth=2, label='xk: gefilterte Werte')
plt.axhline(0, color='blue', label='reales Signal')

# Legende anzeigen
plt.legend()

# Achsenbeschriftung
plt.xlabel('Zeit in ms')
plt.ylabel('Winkelgeschwindigkeit in °/s')

# Plot Ränder entfernen
plt.gca().set_loose_inset(plt.gca().get_tight_inset())

# Skalierung Y-Achse anpassen
yticks = plt.gca().get_yticks()
plt.gca().set_yticklabels(np.round(yticks / 131 * 100) / 100)

# Bereich X-Achse anpassen
plt.xlim([0, messurement_sample_size])

# Plot anzeigen
plt.show()