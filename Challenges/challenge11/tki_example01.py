import tkinter as tk
from tkinter import ttk

def main():
    # Initialize the main window
    root = tk.Tk()
    root.title("Simple Dropdown Example")

    # Label
    label = tk.Label(root, text="Select an option:")
    label.pack(pady=10)

    # Dropdown options
    options = ['abc', 'def', 'ghi', 'jkl', 'mno']

    # StringVar to hold the selected option
    selected_option = tk.StringVar(value=options[0])

    # Dropdown (Combobox)
    dropdown = ttk.Combobox(root, textvariable=selected_option, values=options, state="readonly")
    dropdown.pack(pady=10)

    # Button to show selected option
    def show_selection():
        print(f"Selected option: {selected_option.get()}")

    button = tk.Button(root, text="Show Selection", command=show_selection)
    button.pack(pady=10)

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()