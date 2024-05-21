import Foundation

// Modellparameter
let F: Float = 1.0  // Zustandsübergangsmatrix (in diesem einfachen Fall)
let H: Float = 1.0  // Messmatrix (in diesem einfachen Fall)
let Q: Float = 1.0  // Prozessgeräusch-Kovarianz (Systemunsicherheit)
let R: Float = 2.0  // Messgeräusch-Kovarianz (Messunsicherheit)

// Initialisierung
var x: Float = 0.0  // Zustandsvektor (geschätzter Zustand)
var P: Float = 1.0  // Kovarianzmatrix (Unsicherheit der Schätzung)

// Funktion zur Kalman-Schätzung
func kalmanFilter(newMeasurement: Float) -> Float {
    // Vorhersage
    let xPredicted = F * x  // Vorhergesagter Zustand
    let PPredicted = F * P * F + Q  // Vorhergesagte Kovarianz

    // Kalman-Gewichtungsfaktor
    let K = PPredicted * H / (H * PPredicted * H + R)

    // Korrektur
    x = xPredicted + K * (newMeasurement - H * xPredicted)
    P = (1 - K * H) * PPredicted

    // Rückgabe der geschätzten Messung
    return x
}

// Array für die Messwerte
var sensorData: [Float] = []

// Simulierte Messungen hinzufügen
let measurements: [Float] = [1,2,3,7,4,5,6/*Data HERE*/]

for measurement in measurements {
    // Kalman-Filter anwenden
    let estimatedValue = kalmanFilter(newMeasurement: measurement)
    
    // Geschätzten Wert ins Array hinzufügen
    sensorData.append(estimatedValue)
}

// Ausgabe der geschätzten Werte
print("Original Werte:   \(measurements)")
print("Geschätzte Werte: \(sensorData)")
