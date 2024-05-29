import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap import ttk  # Use ttk from ttkbootstrap

# [x] Mode: [Square, Joystick, Mousepad]
# [x] Frame Rate: 60 FPS
# TTL: 50 frames
# Noise covariance : 15 [1-116.66]
# prediction Steps : 7
#
# [] Real Path
# [] Noisy
# [] Noisy Path
# [] Filtered
# [] Filtered Path
# [] Prediction

def update_canvas(event=None):
    canvas.delete("all")
    slider1_value = slider1.get()
    slider2_value = slider2.get()
    real_path_value = real_path.get()
    selection_value = dropdown_var.get()
    
    color = "blue" if real_path_value else "green"
    if selection_value == "Option 1":
        canvas.create_rectangle(10, 10, slider1_value, slider2_value, fill=color)
    elif selection_value == "Option 2":
        canvas.create_oval(10, 10, slider1_value, slider2_value, fill=color)

def set_option(value):
    dropdown_var.set(value)
    update_canvas()

# Create the main window
root = tk.Tk()
root.title("Tkinter Canvas Example")

# Create a style object
style = Style(theme='flatly')  # Choose a theme from ttkbootstrap

# Create a frame to hold the canvas and the controls
frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

# Create a canvas widget
canvas = tk.Canvas(frame, bg="grey")
canvas.grid(row=0, column=0, rowspan=4, sticky="nsew")

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Create a dropdown (menubutton) widget with ttkbootstrap styling
dropdown_var = tk.StringVar(value="   Fester Pfad   ")
dropdown = ttk.Menubutton(frame, textvariable=dropdown_var, style='info.TMenubutton')
dropdown.grid(row=0, column=2, padx=10, pady=5)
# Create a menu and associate it with the menubutton
menu = tk.Menu(dropdown, tearoff=0)
dropdown["menu"] = menu
menu.configure()
# Add options to the menu
rec = "   Fester Pfad   "
menu.add_radiobutton(label=rec, variable=dropdown_var, value="rect", command=lambda: set_option(rec))
mouse = "     Mauspad     "
menu.add_radiobutton(label=mouse, variable=dropdown_var, value="mouse", command=lambda: set_option(mouse))
joy = "Externer Joystick"
menu.add_radiobutton(label=joy, variable=dropdown_var, value="joys", command=lambda: set_option(joy))
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Slider
slider1_label = ttk.Label(frame, text="FPS", style='warning.TLabel')
slider1_label.grid(row=1, column=1, padx=10, pady=5, sticky="e")
slider1 = ttk.Scale(frame, from_=10, to=200, orient=tk.HORIZONTAL, style='warning.Horizontal.TScale')
slider1.grid(row=1, column=2, padx=10, pady=5)
slider1.bind("<Motion>", update_canvas)
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Slider
slider2_label = ttk.Label(frame, text="Noise Covariance", style='warning.TLabel')
slider2_label.grid(row=2, column=1, padx=10, pady=5, sticky="e")
slider2 = ttk.Scale(frame, from_=10, to=200, orient=tk.HORIZONTAL, style='warning.Horizontal.TScale')
slider2.grid(row=2, column=2, padx=10, pady=5)
slider2.bind("<Motion>", update_canvas)
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Create a toggle button (checkbox) widget with ttkbootstrap styling
# [] Real Path
real_path = tk.BooleanVar()
real_path_button = ttk.Checkbutton(frame, text="Real Path", variable=real_path, style='success.TCheckbutton', command=update_canvas)
real_path_button.grid(row=3, column=2, columnspan=2, padx=0, pady=0, sticky="w")
# [] Noisy
noisy = tk.BooleanVar()
noisy_button = ttk.Checkbutton(frame, text="Noisy", variable=noisy, style='success.TCheckbutton', command=update_canvas)
noisy_button.grid(row=4, column=2, columnspan=2, padx=0, pady=0, sticky="w")
# [] Noisy Path
noisy_path = tk.BooleanVar()
noisy_path_button = ttk.Checkbutton(frame, text="Noisy Path", variable=noisy_path, style='success.TCheckbutton', command=update_canvas)
noisy_path_button.grid(row=5, column=2, columnspan=2, padx=0, pady=0, sticky="w")
# [] Filtered
filtered = tk.BooleanVar()
filtered_button = ttk.Checkbutton(frame, text="Filtered", variable=filtered, style='success.TCheckbutton', command=update_canvas)
filtered_button.grid(row=6, column=2, columnspan=2, padx=0, pady=0, sticky="w")
# [] Filtered Path
filtered_path = tk.BooleanVar()
filtered_path_button = ttk.Checkbutton(frame, text="Filtered Path", variable=filtered_path, style='success.TCheckbutton', command=update_canvas)
filtered_path_button.grid(row=7, column=2, columnspan=2, padx=0, pady=0, sticky="w")
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Configure the grid layout
frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_rowconfigure(2, weight=1)
frame.grid_rowconfigure(3, weight=1)
frame.grid_rowconfigure(4, weight=1)
frame.grid_rowconfigure(5, weight=1)
frame.grid_rowconfigure(6, weight=1)
frame.grid_rowconfigure(7, weight=1)
frame.grid_rowconfigure(8, weight=1)
frame.grid_rowconfigure(9, weight=1)
frame.grid_rowconfigure(10, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)

# Run the application
root.mainloop()
