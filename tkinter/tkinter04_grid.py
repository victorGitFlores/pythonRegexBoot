import tkinter as tk


root = tk.Tk()
root.geometry("500x500")

# Configure rows and columns
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)



button = tk.Button(root, text="Click Me")
button.grid(row=0, column=0, sticky="nsew")


# keep window alive and listening for events
root.mainloop()
