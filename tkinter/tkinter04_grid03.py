import tkinter as tk
from tkinter import ttk

# columnconfigure and rowconfigure... the weight is the priority of the column or row...
# the higher the weight, the more priority it has to expand or fill the window

root = tk.Tk()
root.geometry("500x500")
root.backgroundColor = "pink"

# Create a grid layout with three columns
root.columnconfigure(0, weight=1,) # gets 1 part extra space
root.columnconfigure(1, weight=2) # gets 2 parts extra space
root.columnconfigure(2, weight=1) # gets 1 part extra space

# Add labels to show the column expansion
for i in range(3):  # i = 0, 1, 2 to match columnconfigure
    label = tk.Label(root, text=f"Column {i}")
    if i == 0:
        label.config(bg= "red")
    elif i == 1:
        label.config(bg= "yellow")
    elif i == 2:
        label.config(bg= "blue")
    label.grid(row=0, column=i, sticky="nsew")


# keep window alive and listening for events
root.mainloop()