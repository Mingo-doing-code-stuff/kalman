import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('c_serial_port/gyro_verify-2.csv', delimiter=';')
gyroX = df.iloc[0:200, 0]


# Anzahl der Messwerte
gyroXarrSize = len(gyroX)

# Median der Messwerte
gyroXmedian = np.median(gyroX)

# Temperaturbias (Drift) berechnen
gyroXbias = gyroX - gyroXmedian

# Varianz der Messergebnisse (f체r ein anschauliches Beispiel verwenden wir 0.1)
gyroXbiasVarianz = 0.1

# Anwendung der Filteriterationen

# Varianz der Messergebnisse wird durch R dargestellt
R = gyroXbiasVarianz

# Einheitsmatrix, hier numerisch, deshalb = 1
I = 1

# Initiale Vorbelegung
filterVals = np.zeros(gyroXarrSize)
kalmanVals = np.zeros(gyroXarrSize)
xkSub1 = 0
xk = xkSub1  # Vorheriger Messwert unbekannt, deshalb 0

# Fehlerkovarianz am Anfang 1 und nicht 0, da normalerweise immer ein Messrauschen vorhanden ist
PkSub1 = 1
Pk = PkSub1

# Iteration 1: Erste Sch채tzung
zk = gyroXbias[0]
Kk = Pk / (Pk + R)
kalmanVals[0] = Kk
xk = xk + Kk * (zk - xk)
filterVals[0] = xk
Pk = (I - Kk) * Pk

# Iteration 2 bis gyroXarrSize
for j in range(1, gyroXarrSize):
    # Vorhersage
    zk = gyroXbias[j]  # Aktuelle Messung
    xk = filterVals[j - 1]  # xk = xk-1

    # Korrektur
    Kk = Pk / (Pk + R)
    kalmanVals[j] = Kk
    xk = xk + Kk * (zk - xk)
    filterVals[j] = xk
    Pk = (I - Kk) * Pk

# fig, (ax1, ax2) = plt.subplots(1, 2)
# fig.suptitle('Horizontally stacked subplots')
# ax1.plot(x, y)
# ax2.plot(x, -y)


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
