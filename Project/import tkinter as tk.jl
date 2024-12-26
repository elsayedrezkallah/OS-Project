import tkinter as tk
from tkinter import ttk

def create_gantt_chart(canvas, gantt_data):
    """
    Creates a Gantt chart on the given canvas based on the provided data.

    Args:
        canvas: The Tkinter canvas object to draw the chart on.
        gantt_data: A list of tuples, each containing (job_name, start_time, end_time).
    """
    canvas.delete("all")  # Clear any existing elements on the canvas

    # Calculate chart dimensions
    width = 600
    height = 100
    x_spacing = 50
    y_spacing = 30

    # Draw the chart background
    canvas.create_rectangle(0, 0, width, height, fill="white")

    # Draw the time axis
    canvas.create_line(x_spacing, height - y_spacing, width - x_spacing, height - y_spacing)
    for i in range(0, width - 2 * x_spacing, x_spacing):
        canvas.create_line(x_spacing + i, height - y_spacing, x_spacing + i, height - y_spacing + 10)
        canvas.create_text(x_spacing + i, height - y_spacing + 20, text=str(i), font=("Arial", 8))

    # Draw the job bars
    for job_name, start_time, end_time in gantt_data:
        x1 = x_spacing + start_time * x_spacing
        x2 = x_spacing + end_time * x_spacing
        y1 = height - y_spacing - 20
        y2 = height - y_spacing + 20
        canvas.create_rectangle(x1, y1, x2, y2, fill="lightblue")
        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=job_name, font=("Arial", 10))

def display_results(results):
    """
    Displays the scheduling results in a formatted table.

    Args:
        results: A list of tuples, each containing (job_name, arrival_time, burst_time, finish_time, turnaround_time, waiting_time).
    """
    # Clear the table
    for child in table_frame.winfo_children():
        child.destroy()

    # Create table headers
    headers = ["Job", "Arrival Time", "Burst Time", "Finish Time", "Turnaround Time", "Waiting Time"]
    for i, header in enumerate(headers):
        label = ttk.Label(table_frame, text=header, font=("Arial", 12))
        label.grid(row=0, column=i, padx=5, pady=5)

    # Populate the table with data
    for i, (job_name, arrival_time, burst_time, finish_time, turnaround_time, waiting_time) in enumerate(results):
        for j, value in enumerate([job_name, arrival_time, burst_time, finish_time, turnaround_time, waiting_time]):
            label = ttk.Label(table_frame, text=str(value), font=("Arial", 12))
            label.grid(row=i+1, column=j, padx=5, pady=5)

    # Add an average row
    average_tat = sum(t[4] for t in results) / len(results)
    average_wt = sum(t[5] for t in results) / len(results)
    label = ttk.Label(table_frame, text="Average", font=("Arial", 12))
    label.grid(row=len(results) + 1, column=0, padx=5, pady=5)
    label = ttk.Label(table_frame, text=f"{average_tat:.3f}", font=("Arial", 12))
    label.grid(row=len(results) + 1, column=4, padx=5, pady=5)
    label = ttk.Label(table_frame, text=f"{average_wt:.3f}", font=("Arial", 12))
    label.grid(row=len(results) + 1, column=5, padx=5, pady=5)

# Sample data (replace with your actual scheduling results)
gantt_data = [("A", 0, 1), ("B", 1, 3), ("C", 3, 9)]
results = [("A", 2, 1, 3, 1, 0), ("B", 3, 2, 5, 2, 0), ("C", 4, 4, 9, 5, 1)]

# Create the main window
root = tk.Tk()
root.title("Process Scheduler")

# Create frames for the Gantt chart and table
gantt_frame = tk.Frame(root)
gantt_frame.pack(side=tk.TOP, fill=tk.X)
table_frame = tk.Frame(root)
table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create a canvas for the Gantt chart
canvas = tk.Canvas(gantt_frame, width=600, height=100)
canvas.pack()

# Display the Gantt chart and table
create_gantt_chart(canvas, gantt_data)
display_results(results)

root.mainloop()