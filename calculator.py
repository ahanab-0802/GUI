import tkinter as tk
from tkinter import messagebox
import math

# Function to update the expression in the entry field
def click_button(value):
    current = entry_var.get()
    entry_var.set(current + str(value))

# Function to clear the entry field
def clear():
    entry_var.set("")

# Function to evaluate the expression
def evaluate():
    try:
        result = eval(entry_var.get())
        entry_var.set(result)
    except:
        messagebox.showerror("Error", "Invalid Expression")

# Function to switch between Standard and Scientific modes
def switch_mode():
    for button in scientific_buttons:
        if mode_var.get() == "Scientific":
            button.grid()
        else:
            button.grid_remove()

# Function for scientific operations
def scientific_operation(op):
    try:
        value = float(entry_var.get())
        if op == "sin":
            result = math.sin(math.radians(value))
        elif op == "cos":
            result = math.cos(math.radians(value))
        elif op == "tan":
            result = math.tan(math.radians(value))
        elif op == "log":
            result = math.log10(value)
        elif op == "sqrt":
            result = math.sqrt(value)
        elif op == "^2":
            result = value ** 2
        elif op == "^3":
            result = value ** 3
        entry_var.set(result)
    except:
        messagebox.showerror("Error", "Invalid Input")

# Creating main window
root = tk.Tk()
root.title("Python Calculator")
root.geometry("400x500")

# Entry field
entry_var = tk.StringVar()
entry = tk.Entry(root, textvariable=entry_var, font=("Arial", 18), bd=10, relief=tk.GROOVE, justify="right")
entry.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=8)

# Radio buttons for mode selection
mode_var = tk.StringVar(value="Standard")
radio_standard = tk.Radiobutton(root, text="Standard", variable=mode_var, value="Standard", command=switch_mode)
radio_scientific = tk.Radiobutton(root, text="Scientific", variable=mode_var, value="Scientific", command=switch_mode)
radio_standard.grid(row=1, column=0, columnspan=2, sticky="w")
radio_scientific.grid(row=1, column=2, columnspan=2, sticky="e")

# Standard buttons
buttons = [
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
    ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
    ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
    ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3),
]

for (text, row, col) in buttons:
    action = lambda x=text: click_button(x) if x != "=" else evaluate()
    tk.Button(root, text=text, width=5, height=2, font=("Arial", 14), command=action).grid(row=row, column=col, padx=5, pady=5)

# Clear Button
tk.Button(root, text="C", width=5, height=2, font=("Arial", 14), command=clear).grid(row=5, column=3, padx=5, pady=5)

# Scientific buttons
scientific_buttons = []
scientific_operations = [
    ('sin', 6, 0), ('cos', 6, 1), ('tan', 6, 2), ('log', 6, 3),
    ('sqrt', 7, 0), ('^2', 7, 1), ('^3', 7, 2)
]

for (text, row, col) in scientific_operations:
    button = tk.Button(root, text=text, width=5, height=2, font=("Arial", 14),
                       command=lambda x=text: scientific_operation(x))
    button.grid(row=row, column=col, padx=5, pady=5)
    scientific_buttons.append(button)

# Hide scientific buttons initially
switch_mode()

# Run the application
root.mainloop()