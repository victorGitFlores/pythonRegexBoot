import tkinter as tk

# a label can hold text or an image

# Create the main window
root = tk.Tk()
root.geometry("500x500")

# Create a frame--------------------------------
frame = tk.Frame(root, bg="pink")
frame.grid(row=0, column=0, sticky="nsew")# make frame stretch to fill the window
# Expand the frame to occupy all available space
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
#----------------------------------------------


# Create a label
label = tk.Label(frame, text="Hello, Tkinter!", bg="pink")# to match background color of frame
label.grid(row=0, column=0) # this gives you more control than pack()
# this is an alternative i don't like:
# label.place(x=100, y=100)# place the label at a specific location in the window



# Start the main event loop
root.mainloop()