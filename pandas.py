import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Sample data
students = [
    {"name": "Alice", "marks1": 80, "marks2": 90, "marks3": 85},
    {"name": "Bob", "marks1": 70, "marks2": 75, "marks3": 80},
    {"name": "Charlie", "marks1": 90, "marks2": 85, "marks3": 95}
]

# Calculate totals
for student in students:
    student["total"] = student["marks1"] + student["marks2"] + student["marks3"]

# Main app
root = tk.Tk()
root.title("Student Marks Analysis")

# Frame to hold all listboxes side by side
listbox_frame = ttk.Frame(root, padding="10")
listbox_frame.grid(row=0, column=0, sticky="w")

# Listbox for marks selection
ttk.Label(listbox_frame, text="Select Marks Type").grid(row=0, column=0, padx=10)
marks_options = ["marks1", "marks2", "marks3", "total", "all"]
marks_listbox = tk.Listbox(listbox_frame, exportselection=False, height=len(marks_options))
for option in marks_options:
    marks_listbox.insert(tk.END, option)
marks_listbox.select_set(0)
marks_listbox.grid(row=1, column=0, padx=10)

# Listbox for chart type
ttk.Label(listbox_frame, text="Select Chart Type").grid(row=0, column=1, padx=10)
chart_options = ["Bar Chart", "Pie Chart", "Line Chart"]
chart_listbox = tk.Listbox(listbox_frame, exportselection=False, height=len(chart_options))
for option in chart_options:
    chart_listbox.insert(tk.END, option)
chart_listbox.select_set(0)
chart_listbox.grid(row=1, column=1, padx=10)

# Listbox for sorting
ttk.Label(listbox_frame, text="Sort By").grid(row=0, column=2, padx=10)
sort_options = ["marks1", "marks2", "marks3", "total"]
sort_listbox = tk.Listbox(listbox_frame, exportselection=False, height=len(sort_options))
for option in sort_options:
    sort_listbox.insert(tk.END, option)
sort_listbox.select_set(0)
sort_listbox.grid(row=1, column=2, padx=10)

# Sort Button directly under Sort Students list
ttk.Button(listbox_frame, text="Sort Students", command=lambda: sort_students()).grid(row=2, column=2, pady=10)

# Show Chart Button directly below Chart Type
ttk.Button(listbox_frame, text="Show Chart", command=lambda: show_chart()).grid(row=2, column=1, pady=10)

def show_chart():
    selected_mark = marks_listbox.get(marks_listbox.curselection())
    chart_type = chart_listbox.get(chart_listbox.curselection())
    sort_by = sort_listbox.get(sort_listbox.curselection())

    sorted_students = sorted(students, key=lambda x: x[sort_by], reverse=True)
    names = [s["name"] for s in sorted_students]

    # Create a new window for the chart
    new_window = Toplevel(root)
    new_window.title("Chart Window")

    # Create a matplotlib figure
    fig, ax = plt.subplots(figsize=(6, 4))

    if selected_mark == "all":
        for mark in ["marks1", "marks2", "marks3"]:
            ax.plot(names, [s[mark] for s in sorted_students], label=mark)
        ax.set_title("All Marks Comparison")
        ax.legend()
    else:
        values = [s[selected_mark] for s in sorted_students]
        if chart_type == "Bar Chart":
            ax.bar(names, values)
            ax.set_title(f"{selected_mark} - Bar Chart")
        elif chart_type == "Pie Chart":
            ax.pie(values, labels=names, autopct="%1.1f%%")
            ax.set_title(f"{selected_mark} - Pie Chart")
        elif chart_type == "Line Chart":
            ax.plot(names, values, marker='o')
            ax.set_title(f"{selected_mark} - Line Chart")

    # Embed the matplotlib figure in the new window
    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

def sort_students():
    sort_by = sort_listbox.get(sort_listbox.curselection())
    sorted_students = sorted(students, key=lambda x: x[sort_by], reverse=True)
    messagebox.showinfo("Sorting Complete", f"Students sorted by {sort_by}")

root.mainloop()