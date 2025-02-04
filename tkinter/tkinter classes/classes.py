import tkinter as tk
from tkinter import ttk

# this will be the main window...
class App(tk.Tk):
    def __init__(self, title, geo):
        
        # main setup...
        super().__init__()
        w, h = geo  # unpacking a tuple
        self.title = title
        self.geometry = f"{w}x{h}"
        self.minsize(w,h)  

        # widgets
        self.menu = Menu(self)
        self.main = Main(self)

        # run the main loop
        self.mainloop()

class Menu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)   # Frame is the 'parent' of Menu
        self.place(x=0, y=0, relwidth=.3, relheight=1)
        
        self.create_widgets()

    def create_widgets(self):
        # create widgets
        menu_butt01 = ttk.Button(self, text="Button 01")
        menu_butt02 = ttk.Button(self, text="Button 02")
        menu_butt03 = ttk.Button(self, text="Button 03")

        menu_slid01 = ttk.Scale(self, orient="vertical")
        menu_slid02 = ttk.Scale(self, orient="vertical")

        toggle_frame = ttk.Frame(self)
        menu_togg01  = ttk.Checkbutton(toggle_frame, text="Check 01")
        menu_togg02  = ttk.Checkbutton(toggle_frame, text="Check 02")

        entry        = ttk.Entry(self)
        
        # this below was in a separate function, but I moved it here...
        # because could not access the widgets.

        # create the grid
        self.columnconfigure((0,1,2), weight=1, uniform='a')  # 3 columns, same size
        self.rowconfigure((0,1,2,3,4), weight=1, uniform='a')  # 5 rows, same size
        # place widgets on the grid
        menu_butt01.grid(row=0, column=0, sticky='nesw', columnspan=2)
        menu_butt02.grid(row=0, column=2, sticky='nesw')
        menu_butt03.grid(row=1, column=0, sticky='nesw', columnspan=3)

        menu_slid01.grid(row=2, column=0, sticky='nesw', rowspan=2, pady=20)
        menu_slid02.grid(row=2, column=2, sticky='nesw', rowspan=2, pady=20)

        # toggle layout...
        toggle_frame.grid(row=4, column=0, columnspan=3, sticky='nesw')
        menu_togg01.pack(side='left', expand=True)
        menu_togg02.pack(side='left', expand=True)

        entry.place(relx=0.5, rely=0.95, relwidth=0.9, anchor='center')
        #entry.grid(row=5, column=0, sticky='new', columnspan=3)

class Main(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(x=0, y=0, relx=.3, relwidth=.7, relheight=1)
        Main_half(self, "red", "Button 01", "Label 01")
        Main_half(self, "blue", "Button 02", "Label 02")
   
class Main_half(ttk.Frame):
    def __init__(self, parent, color, butt_text, lab_text):
        super().__init__(parent)
        self.place(x=0, y=0, relx=.3, relwidth=.7, relheight=.5)
        
        frame = ttk.Frame(self)
        label = ttk.Label(self, text=lab_text, background=color)   
        button = ttk.Button(self, text=butt_text)
        # place label and button on the frame...
        label.pack(side='top', fill='both', expand=True)
        button.pack(side='bottom', fill='both', expand=True, pady=10)
        # place the frame on the main frame...
        self.pack(side='left', fill='both', expand=True, padx=20, pady=20)


# mainline
App("Class-based app", (600, 600))



