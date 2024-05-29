import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap import ttk  # Use ttk from ttkbootstrap

def update_canvas(event=None):
    canvas.delete("all")
    slider1_value = slider1.get()
    slider2_value = slider2.get()
    toggle_value = toggle_var.get()
    selection_value = dropdown_var.get()
    
    color = "blue" if toggle_value else "red"
    if selection_value == "Option 1":
        canvas.create_rectangle(10, 10, slider1_value, slider2_value, fill=color)
    elif selection_value == "Option 2":
        canvas.create_oval(10, 10, slider1_value, slider2_value, fill=color)

def create_slider():
    scale = ttk.Scale()
    scale.configure(frame, from_=1, to=50, orient=tk.HORIZONTAL, style='success.Horizontal.TScale')
    scale.grid(row=0, column=1, padx=10, pady=5)
    scale.bind("<Motion>", update_canvas)

    return scale

# Create the main window
root = tk.Tk()
root.title("Tkinter Canvas Example")

# Create a style object
style = Style(theme='flatly')  # Choose a theme from ttkbootstrap

# Create a frame to hold the canvas and the controls
frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

# Create a canvas widget
canvas = tk.Canvas(frame, bg="white")
canvas.grid(row=0, column=0, rowspan=4, sticky="nsew")

# Create a slider widget with ttkbootstrap styling options
slider1 = ttk.Scale(frame, from_=10, to=200, orient=tk.HORIZONTAL, style='success.Horizontal.TScale')
slider1.grid(row=0, column=1, padx=10, pady=5)
slider1.bind("<Motion>", update_canvas)

slider2 = ttk.Scale(frame, from_=10, to=200, orient=tk.HORIZONTAL, style='info.Horizontal.TScale')
slider2.grid(row=1, column=1, padx=10, pady=5)
slider2.bind("<Motion>", update_canvas)

# Create a toggle button (checkbox) widget with ttkbootstrap styling
toggle_var = tk.BooleanVar()
toggle_button = ttk.Checkbutton(frame, text="Toggle Color", variable=toggle_var, style='success-round-toggle', command=update_canvas)
toggle_button.grid(row=2, column=1, padx=10, pady=5)

# Create a dropdown (combobox) widget with ttkbootstrap styling
dropdown_var = tk.StringVar(value="Option 1")
dropdown = ttk.Combobox(frame, textvariable=dropdown_var, style='info.TCombobox')
dropdown['values'] = ("Option 1", "Option 2")
dropdown.grid(row=3, column=1, padx=10, pady=5)
dropdown.bind("<<ComboboxSelected>>", update_canvas)

# Configure the grid layout
frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_rowconfigure(2, weight=1)
frame.grid_rowconfigure(3, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Run the application
root.mainloop()
