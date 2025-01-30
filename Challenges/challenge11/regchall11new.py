import tkinter as tk


def setup_gui():
    # Create the main window
    root = tk.Tk()
    root.geometry("500x500")

    # Create a frame--------------------------------
    frame = tk.Frame(root, bg="pink")
    frame.grid(row=0, column=0, sticky="nsew")  # make frame stretch to fill the window
    # Expand the frame to occupy all available space
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    # ----------------------------------------------

def main():
    setup_gui()



    # loop to keep the window open
    tk.mainloop()

if __name__ == "__main__":
    main()

