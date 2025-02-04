import tkinter as tk
from tkinter import ttk 

# window
window = tk.Tk()   
window.title("Grid Example")
window.geometry("600x400")

# widgets
label01 = tk.Label(window, text="Lable 01", bg="red")
label02 = tk.Label(window, text="Lable 02", bg="blue")
label03 = tk.Label(window, text="Lable 03", bg="green")
label04 = tk.Label(window, text="Lable 04", bg="yellow")

butt01 = tk.Button(window, text="Button 01")
butt02 = tk.Button(window, text="Button 02")

entry = tk.Entry(window)

# define grid
window.columnconfigure(0, weight=1, uniform='a')
window.columnconfigure(1, weight=1, uniform='a')
window.columnconfigure(2, weight=1, uniform='a')
window.rowconfigure(0, weight=1)

# place widgets on the grid
label01.grid(row=0, column=0, sticky='nesw')
label02.grid(row=0, column=2, sticky='nesw')





# keep window alive and listening for events
window.mainloop()
