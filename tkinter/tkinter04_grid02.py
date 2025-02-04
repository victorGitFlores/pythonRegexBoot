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
window.columnconfigure((0,1,2,3), weight=1, uniform='a')
# now we know...
window.rowconfigure((0,1,2,3), weight=1, uniform='a')

# place widgets on the grid
label01.grid(row=0, column=0, sticky='nsew')
label02.grid(row=1, column=1, rowspan=3, sticky='nesw')
label03.grid(row=1, column=0, columnspan=3, sticky='nesw' )
label04.grid(row=3, column=3, sticky='se' )
# hw...
butt01.grid(row=0, column=2, columnspan=2, sticky='nesw')
butt02.grid(row=2, column=2, sticky='nesw')
entry.grid(row=3, column=3, rowspan=2)




# keep window alive and listening for events
window.mainloop()
