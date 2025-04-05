import tkinter as tk
from tkinter import ttk

maze = [
    [1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 0, 1, 0, 1, 0, 1, 1, 1],
    [0, 2, 0, 3, 4, 4, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [3, 3, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 0, 0, 0, 0, 4, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

solution=[(2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (3, 9), (4, 9), (4, 8), (4, 7), (4, 6), (4, 5), (4, 4), (5, 4), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (7, 9), (8, 9), (8, 8), (8, 7), (8, 6)]





# Create the main window
root = tk.Tk()
root.title("Left Text / Right Options")
root.geometry("500x300")

# Create the main frame
main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill=tk.BOTH, expand=True)

# Create left and right sections inside the main frame
left_frame = ttk.Frame(main_frame)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

right_frame = ttk.Frame(main_frame)
right_frame.pack(side=tk.RIGHT, fill=tk.Y)

# Add a text field in the left frame
text_area = tk.Text(left_frame, wrap=tk.WORD, height=15, width=40)
text_area.pack(fill=tk.BOTH, expand=True)

# Add radio buttons in the right frame
radio_label = ttk.Label(right_frame, text="Choose an option:")
radio_label.pack(anchor=tk.NW, pady=(0, 5))

# Variable to store selected option
selected_option = tk.StringVar(value="Option 1")

# List of radio button options
options = ["Option 1", "Option 2", "Option 3"]

# Create radio buttons
for option in options:
    rb = ttk.Radiobutton(
        right_frame,
        text=option,
        value=option,
        variable=selected_option
    )
    rb.pack(anchor=tk.NW)

# Run the application
root.mainloop()