import tkinter as tk
from tkinter import ttk

# Main application window
class App(tk.Tk):
    def __init__(self, title, geo):
        super().__init__()
        self.title(title)
        self.geometry(f"{geo[0]}x{geo[1]}")
        self.minsize(geo[0], geo[1])

        # Create and place the menu and main sections
        self.menu = Menu(self)
        self.main = Main(self)

        # Run the main loop
        self.mainloop()

# Menu section
class Menu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(x=0, y=0, relwidth=0.3, relheight=1)
        self.create_widgets()

    def create_widgets(self):
        # Create widgets
        self.menu_butt01 = ttk.Button(self, text="Button 01")
        self.menu_butt02 = ttk.Button(self, text="Button 02")
        self.menu_butt03 = ttk.Button(self, text="Button 03")

        self.menu_slid01 = ttk.Scale(self, orient="vertical")
        self.menu_slid02 = ttk.Scale(self, orient="vertical")

        toggle_frame = ttk.Frame(self)
        self.menu_togg01 = ttk.Checkbutton(toggle_frame, text="Check 01")
        self.menu_togg02 = ttk.Checkbutton(toggle_frame, text="Check 02")

        self.entry = ttk.Entry(self)

        # Configure grid
        self.columnconfigure((0, 1, 2), weight=1, uniform='a')
        self.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

        # Place widgets on the grid
        self.menu_butt01.grid(row=0, column=0, sticky='nesw', columnspan=2)
        self.menu_butt02.grid(row=0, column=2, sticky='nesw')
        self.menu_butt03.grid(row=1, column=0, sticky='nesw', columnspan=3)

        self.menu_slid01.grid(row=2, column=0, sticky='nesw', rowspan=2, pady=20)
        self.menu_slid02.grid(row=2, column=2, sticky='nesw', rowspan=2, pady=20)

        # Toggle layout
        toggle_frame.grid(row=4, column=0, columnspan=3, sticky='nesw')
        self.menu_togg01.pack(side='left', expand=True)
        self.menu_togg02.pack(side='left', expand=True)

        self.entry.place(relx=0.5, rely=0.95, relwidth=0.9, anchor='center')

# Main section
class Main(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0.3, y=0, relwidth=0.7, relheight=1)
        self.create_widgets()

    def create_widgets(self):
        # Create two halves of the main section
        self.main_half1 = MainHalf(self, "red", "Button 01", "Label 01")
        self.main_half2 = MainHalf(self, "blue", "Button 02", "Label 02")

# Half of the main section
class MainHalf(ttk.Frame):
    def __init__(self, parent, color, butt_text, lab_text):
        super().__init__(parent)
        self.pack(side='left', fill='both', expand=True, padx=20, pady=20)

        # Create a frame for the label and button
        frame = ttk.Frame(self)
        frame.pack(fill='both', expand=True)

        # Create and place the label and button
        label = ttk.Label(frame, text=lab_text, background=color)
        button = ttk.Button(frame, text=butt_text)

        label.pack(side='top', fill='both', expand=True)
        button.pack(side='bottom', fill='both', expand=True, pady=10)

# Run the application
if __name__ == "__main__":
    App("Class-based app", (600, 600))