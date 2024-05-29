Um zu verstehen, wie aus der Bewegung der Maus die Transitionsmatrix und die notwendigen Berechnungen für die Prediction im Kalman-Filter ermittelt werden, ist es wichtig, die Grundlagen des Kalman-Filters und dessen Anwendung auf das Problem der Mausbewegung zu betrachten. 

### Grundlagen des Kalman-Filters

Der Kalman-Filter ist ein rekursiver Algorithmus, der den Zustand eines Systems basierend auf einer Serie von fehlerbehafteten Messungen schätzt. Er besteht aus zwei Hauptschritten: **Prediction** und **Correction**.

1. **Prediction (Vorhersage)**:
   - **Vorhersage des nächsten Zustands**: Der aktuelle Zustand des Systems wird verwendet, um den nächsten Zustand vorherzusagen.
   - **Vorhersage der Fehlerkovarianz**: Die Unsicherheit der Vorhersage wird ebenfalls aktualisiert.

2. **Correction (Korrektur)**:
   - **Kalman Gain**: Berechnung des Kalman-Gains, der das Gewicht angibt, das den Messungen im Vergleich zu den Vorhersagen zugeordnet wird.
   - **Zustandsaktualisierung**: Der vorhergesagte Zustand wird basierend auf den aktuellen Messungen angepasst.
   - **Fehlerkovarianzaktualisierung**: Die Unsicherheit der Schätzung wird angepasst.

### Mathematische Formeln

#### Notationen

- $\( \mathbf{x}_k \)$: Zustand des Systems zur Zeit \( k \).
- $\( \mathbf{P}_k \)$: Fehlerkovarianzmatrix zur Zeit \( k \).
- $\( \mathbf{A} \)$: Zustandsübergangsmatrix.
- $\( \mathbf{B} \)$: Steuerungsmatrix.
- $\( \mathbf{u}_k \)$: Steuervektor zur Zeit \( k \).
- $\( \mathbf{Q} \)$: Prozessrauschkovarianz.
- $\( \mathbf{H} \)$: Messmatrix.
- $\( \mathbf{R} \)$: Messrauschkovarianz.
- $\( \mathbf{z}_k \)$: Messung zur Zeit \( k \).

#### Vorhersageschritt

1. **Zustandsvorhersage**:
   
   $\( \mathbf{x}_{k|k-1} = \mathbf{A} \mathbf{x}_{k-1} + \mathbf{B} \mathbf{u}_k \)$
  
1. **Fehlerkovarianzvorhersage**:
   
   $\( \mathbf{P}_{k|k-1} = \mathbf{A} \mathbf{P}_{k-1} \mathbf{A}^\top + \mathbf{Q} \)$

#### Korrekturschritt

1. **Kalman Gain**:
   
   $\( \mathbf{K}_k = \mathbf{P}_{k|k-1} \mathbf{H}^\top (\mathbf{H} \mathbf{P}_{k|k-1} \mathbf{H}^\top + \mathbf{R})^{-1} \)$

2. **Zustandsaktualisierung**:
   
   $\( \mathbf{x}_k = \mathbf{x}_{k|k-1} + \mathbf{K}_k (\mathbf{z}_k - \mathbf{H} \mathbf{x}_{k|k-1}) \)$

3. **Fehlerkovarianzaktualisierung**:
   
   $\( \mathbf{P}_k = (\mathbf{I} - \mathbf{K}_k \mathbf{H}) \mathbf{P}_{k|k-1} \)$

### Anwendung auf die Mausbewegung

In der Implementierung wird die Bewegung der Maus modelliert. Die Zustandsvektoren und Matrizen sind wie folgt definiert:

- **Zustandsvektor** $\( \mathbf{x} \)$:
  
  $\( \mathbf{x} = \begin{bmatrix} x \\ y \\ \dot{x} \\ \dot{y} \end{bmatrix} \)$
  
  Hierbei sind $\( x \)$ und $\( y \)$ die Positionen, und $\( \dot{x} \)$ und $\( \dot{y} \)$ die Geschwindigkeiten in den jeweiligen Richtungen.

- **Zustandsübergangsmatrix** $\( \mathbf{A} \)$:
  
  $\( \mathbf{A} = \begin{bmatrix}
  1 & 0 & \Delta t & 0 \\
  0 & 1 & 0 & \Delta t \\
  0 & 0 & 1 & 0 \\
  0 & 0 & 0 & 1 \\
  \end{bmatrix} \)$

  Diese Matrix beschreibt, wie der Zustand von einem Zeitpunkt zum nächsten übergeht. Hierbei ist $\( \Delta t \)$ die Zeit zwischen den Messungen.

- **Steuerungsmatrix** 
  
  $\( \mathbf{B} \)$ und Steuervektor $\( \mathbf{u} \)$ werden in diesem Fall ignoriert.

- **Messmatrix** $\( \mathbf{H} \)$:
  
  $\( \mathbf{H} = \begin{bmatrix}
  1 & 0 & 0 & 0 \\
  0 & 1 & 0 & 0
  \end{bmatrix} \)$
  Diese Matrix beschreibt, wie der Zustandsvektor in den Messvektor umgewandelt wird.

- **Prozessrauschkovarianz** $\( \mathbf{Q} \)$:
  
  $\( \mathbf{Q} = \begin{bmatrix}
  0 & 0 & 0 & 0 \\
  0 & 0 & 0 & 0 \\
  0 & 0 & q & 0 \\
  0 & 0 & 0 & q
  \end{bmatrix} \)$
  Hierbei ist \( q \) ein Parameter, der das Ausmaß des Prozessrauschens bestimmt.

- **Messrauschkovarianz** $\( \mathbf{R} \)$:
  
  $\( \mathbf{R} = \begin{bmatrix}
  \sigma^2 & 0 \\
  0 & \sigma^2
  \end{bmatrix} \)$

  Hierbei ist $\( \sigma \)$ die Standardabweichung des Messrauschens.

### Implementierung des Kalman-Filters im Code

Der gegebene Code nutzt die oben beschriebenen Matrizen und Vektoren, um die Bewegung der Maus zu glätten:

1. **Initialisierung der Kalman-Filter-Matrizen** in der `init` Methode:

```javascript
this.A = m([
    [1, 0, 0.2, 0],
    [0, 1, 0, 0.2],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]);

this.B = m([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]);

this.H = m([
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]);

this.Q = m([
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0.1, 0],
    [0, 0, 0, 0.1]
]);

this.R = m([
    [this.sigma, 0, 0, 0],
    [0, this.sigma, 0, 0],
    [0, 0, this.sigma, 0],
    [0, 0, 0, this.sigma]
]);
```

2. **Vorhersageschritt** in der `frame` Methode:

```javascript
let deltaX = noisyX - this.lastPoint.elements[0];
let deltaY = noisyY - this.lastPoint.elements[1];
let measurement = v([noisyX, noisyY, deltaX, deltaY]);

// PREDICTION step
var x = this.A.multiply(this.lastPoint).add(this.B.multiply(this.c));
var P = this.A.multiply(this.last).multiply(this.A.transpose()).add(this.Q);
```

3. **Korrekturschritt** in der `frame` Methode:

```javascript
var S = this.H.multiply(P).multiply(this.H.transpose()).add(this.R);
var K = P.multiply(this.H.transpose()).multiply(S.inverse());
var y = measurement.subtract(this.H.multiply(x));

this.lastPoint = x.add(K.multiply(y));
this.last = window.Matrix.I(4).subtract(K.multiply(this.H)).multiply(P);
```

Dieser Code glättet die Mausbewegung durch die Kombination der gemessenen Positionen und den geschätzten Zuständen. Dies führt zu einer robusteren Schätzung der tatsächlichen Mausposition, indem der Rauscheffekt reduziert wird.

