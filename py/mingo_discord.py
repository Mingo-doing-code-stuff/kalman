import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# [Abstract:]
# 
# Der nachfolgende Code zeigt eine vereinfachte Anwendung des Kalman Filters.
# Beim Kalman Filter handelt es sich um einen Zustandsschätzer, welcher mittels eines iterativen 
# Ansatzes dazu beitragen kann, sich dem reellen Zustand eines Systems anzunähren. Dabei wird bei
# jeder Iteration zunächst eine Vorhersage getroffen, mit Hilfe der gemessenen Daten eine Korrektur 
# vorgenommen, und anschließend besagte Korrektur im nächsten Schritt für die nächste Vorhersage 
# verwendet.
# 
# Der Nachfolgende Ablauf im hier Vorhandenen Code ist wie folgt:
#   1. Die Messdaten werden eingelesen, und die ersten benötigten Werte berechnet
#   2. Für den Initialen Setup wird die erste Iteration mit besagten Werten teils Hardgecoded 
#      gesetzt, sodass die weiteren Iterationen ohne weiteres Zutun erfolgen können.
#   3. Beginn der Loop über die Messdaten:
#       3.1 Vorhersage:
#           - Die Fehlerkovarianz wird vorrausberechnet (hier vereinfacht, daher gleich dem Wert der
#             vorherigen Iteration)
#           - Der aktuelle Schätzwert wird auf den in der vorherigen Iteration ermittelten, 
#             bereits korrigierten Wert gesetzt 
#       3.2 Korrektur:
#           - Der Kalman Gain wird neu berechnet
#           - Die Schätzung wird mit der gemessenen Winkelgeschwindigkeit aktualisieren
#           - Die Fehlerkovarianz wird aktualisieren
#       3.3 Die Loop endet und es beginnt die nächste Iteration
# 
#   4. Erstelen eines Plotts
# 
#  

df = pd.read_csv('c_serial_port/data_flugzeug.csv', delimiter=';')
messurement_data_gyro_axis_x = df.iloc[:, 0]
# Anzahl der Messwerte
messurement_sample_size = len(messurement_data_gyro_axis_x)
# Median der Messwerte
median_of_messurement_data = np.median(messurement_data_gyro_axis_x)
# Temperaturbias (Drift) berechnen
messurement_bias = messurement_data_gyro_axis_x - median_of_messurement_data
# Varianz der Messergebnisse (für ein anschauliches Beispiel verwenden wir 0.1)
messurement_bias_varianz = 0.58
# Varianz der Messergebnisse wird durch R dargestellt
varianz_der_messung = messurement_bias_varianz
# Einheitsmatrix, hier numerisch, deshalb = 1
I = 1

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-
# Anwendung der Filteriterationen
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-
# -- Initiale Vorbelegung

filter_collected_values_array = np.zeros(messurement_sample_size)
kalman_collected_values_array = np.zeros(messurement_sample_size)

estimate_previous_iteration = 0
# Vorheriger Messwert unbekannt, deshalb 0 (= `estimate_previous_iteration`)
estimate_current_iteration = estimate_previous_iteration

# Fehlerkovarianz am Anfang 1 und nicht 0, da normalerweise immer ein Messrauschen vorhanden ist
error_covariance_previous_iteration = 1
error_covariance_current_iteration = error_covariance_previous_iteration

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-
# -- Iteration 1: Erste Schätzung

# Messung vornehmen:
messurement_current = messurement_bias[0]
# [3.] Den Kalman Gain berechnen
kalman_gain_current_iteration = error_covariance_current_iteration / (error_covariance_current_iteration + varianz_der_messung)
kalman_collected_values_array[0] = kalman_gain_current_iteration

# [4.] Die Schätzung mit der gemessenen Winkelgeschwindigkeit aktualisieren
estimate_current_iteration = estimate_current_iteration + kalman_gain_current_iteration * (messurement_current - estimate_current_iteration)
filter_collected_values_array[0] = estimate_current_iteration

# [5.] Die Fehlerkovarianz aktualisieren
error_covariance_previous_iteration = (I - kalman_gain_current_iteration) * error_covariance_current_iteration

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-
# -- Iteration 2 bis messurement_sample_size

for iteration in range(1, messurement_sample_size):

    # -- Vorhersage - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    
    # [1.] Die Fehlerkovarianz vorrausberechnen
    # xk = xk-1 
    estimate_current_iteration = estimate_previous_iteration

    # [2.] Den nächsten Zustand darstellen
    # xk = xk-1
    estimate_current_iteration = filter_collected_values_array[iteration - 1]

    # -- Korrektur - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    messurement_current = messurement_bias[iteration]

    # [3.] Den Kalman Gain berechnen
    kalman_gain_current_iteration = error_covariance_current_iteration / (error_covariance_current_iteration + varianz_der_messung)
    kalman_collected_values_array[iteration] = kalman_gain_current_iteration

    # [4.] Die Schätzung mit der gemessenen Winkelgeschwindigkeit aktualisieren
    estimate_current_iteration = estimate_current_iteration + kalman_gain_current_iteration * (messurement_current - estimate_current_iteration)
    filter_collected_values_array[iteration] = estimate_current_iteration

    # [5.] Die Fehlerkovarianz aktualisieren
    error_covariance_previous_iteration = (I - kalman_gain_current_iteration) * error_covariance_current_iteration

    # -- Next Iteration  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-
# Graph plotten
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-

fig, axs = plt.subplots(2)
axs[1].bar(range(messurement_sample_size), kalman_collected_values_array, label='Kk: Kalman Gain', linestyle='-', color=[0, 0.75, 1], edgecolor='b')
axs[0].plot(messurement_bias, '-', label='zk: Messwerte', color='red')
axs[0].plot(filter_collected_values_array, color='green', linewidth=2, label='xk: gefilterte Werte')
axs[0].axhline(0, color='blue', label='reales Signal')

# Legende anzeigen
axs[0].legend()

# Achsenbeschriftung
axs[0].set_xlabel('Zeit in ms')
axs[0].set_ylabel('Winkelgeschwindigkeit in °/s')


# Bereich X-Achse anpassen
axs[0].set_xlim([0, messurement_sample_size])
axs[1].set_xlim([0, messurement_sample_size])

# Plot anzeigen
plt.show()
