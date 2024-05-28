import tkinter as tk

def update_mouse_position(event):
    # Aktualisiere das Label mit den aktuellen Koordinaten des Mauszeigers
    x, y = event.x, event.y
    position_label.config(text=f"Mouse position: ({x}, {y})")

# Erstelle das Hauptfenster
root = tk.Tk()
root.title("Mouse Position Tracker")

# Erstelle eine Canvas
canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack()

# Erstelle ein Label, um die Mausposition anzuzeigen
position_label = tk.Label(root, text="Mouse position: (0, 0)")
position_label.pack()

# Binde das Motion-Ereignis an die update_mouse_position-Funktion
canvas.bind("<Motion>", update_mouse_position)

# Starte die Haupt-Ereignisschleife
root.mainloop()
