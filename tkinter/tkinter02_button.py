import tkinter as tk
from tkinter.scrolledtext import ScrolledText

# buttons: you click them, and then they do something

# Create the main window
root = tk.Tk()
root.geometry("500x500")

# Make the grid in the root window stretch
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)


# Create a frame--------------------------------
frame = tk.Frame(root, bg="pink")
frame.grid(row=0, column=0, sticky="nsew")# make frame stretch to fill the window
# Expand the frame to occupy all available space
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
#----------------------------------------------



# the 'command' for the button... this is a callback function
def callback_click01():
    #print("You clicked the button!")
    #better yet, in my opinion:
    # but since its output only, gotta normalize/denormalize the text box
    text_box.config(state="normal")
    text_box.insert(tk.END, "You clicked the button!\n")
    text_box.config(state="disabled")

# Create a button
# pink to match background color of frame
button = tk.Button(frame, text="Click me!", bg="pink", command=callback_click01)
button.grid(row=0, column=0) # this gives you more control than pack()


# text box for output:
text_box = tk.scrolledtext.ScrolledText(
    frame, wrap=tk.WORD, width=40, height=10, state="disabled")
text_box.grid(row=1, column=0, pady=10, sticky="nsew")




# Start the main event loop
root.mainloop()