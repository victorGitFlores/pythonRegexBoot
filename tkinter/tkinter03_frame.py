# frame... a rectangular container to group and hold widgets

from tkinter import *


window = Tk()
window.title("Frame Example")

frame = Frame(window, bg="pink", bd=5, relief=SUNKEN) # bd is border width, relief is border style
# frame.pack(side=BOTTOM) 
frame.place(x=100, y=100)

# within frame, bunch of buttons...
Button(frame, text="W", font="Consolas 25 bold", width=3, bg="#DAF7A6").pack(side=TOP)
Button(frame, text="A", font="Consolas 25 bold", width=3, bg="#DAF7A6").pack(side=LEFT)
Button(frame, text="S", font="Consolas 25 bold", width=3, bg="#DAF7A6").pack(side=LEFT)
Button(frame, text="D", font="Consolas 25 bold", width=3, bg="#DAF7A6").pack(side=LEFT)




# keep window alive and listening for events
window.mainloop()
