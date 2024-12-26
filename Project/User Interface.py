import tkinter as tk
import os
from tkinter import messagebox, ttk

try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except ImportError:
    print("The matplotlib library is not installed. Installing it now...")
    os.system("pip install matplotlib")
    print("--------------------------------------------------------------------------")
    print("Installation complete.")
    print("--------------------------------------------------------------------------")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except Exception as e:
    print(f"An error occurred: {e}")

# Import your scheduling algorithms here
from FCFS import fcfs
from nnp import npp 
from pp import pp  # Import the Preemptive Priority function
from rr import rr  # Import the Round Robin function
from sjf import sjf  # Import the Shortest Job First function
from srtf import SRTFScheduler  # Import the SRTF scheduler

class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Scheduler")
        self.root.geometry("800x600")  # Set a default window size
        self.root.configure(bg="#f0f0f0")  # Set a light background color

        self.process_list = []  # List to store processes as dictionaries
        self.selected_algorithm = tk.StringVar(value="First Come First Serve (FCFS)")  # Default selection
        self.gantt_result = None  # Initialize Gantt result

        # Create frames for the scheduler and Gantt chart
        self.scheduler_frame = tk.Frame(root, bg="#f0f0f0")
        self.gantt_frame = tk.Frame(root, bg="#f0f0f0")

        # Initialize the scheduler page
        self.init_scheduler_page()

        # Initialize the Gantt chart page
        self.init_gantt_page()

        # Show the scheduler frame by default
        self.scheduler_frame.pack(fill=tk.BOTH, expand=True)

        # Navigation buttons
        self.nav_frame = tk.Frame(root, bg="#e0e0e0")
        self.nav_frame.pack(fill=tk.X)

        # Create a frame to center the Gantt button
        self.gantt_button_frame = tk.Frame(self.nav_frame, bg="#e0e0e0")
        self.gantt_button_frame.pack(side=tk.TOP, pady=10)

        # Gantt Chart button
        # Enhanced Gantt Chart Button
        self.gantt_button = tk.Button(
            self.gantt_button_frame,
            text="Gantt Chart",
            command=self.show_gantt,
            bg="#2196F3",
            fg="white",
            font=("Arial", 12, "bold"),
            width=20,  # Set a fixed width
            padx=10,   # Internal padding
            pady=5,    # Internal padding
            borderwidth=2,  # Border width
            relief="raised"  # Button relief style
        )
        self.gantt_button.pack(pady=5)

        # Bind hover effects
        self.gantt_button.bind("<Enter>", lambda e: self.on_hover(self.gantt_button, True))
        self.gantt_button.bind("<Leave>", lambda e: self.on_hover(self.gantt_button, False))
        
        

    def init_scheduler_page(self):
        """Initialize the scheduler page."""
        # Frame for algorithm selection
        algorithm_frame = tk.Frame(self.scheduler_frame, padx=10, pady=10, bg="#e0e0e0")
        algorithm_frame.pack(fill=tk.X)

        # Center the algorithm selection label and menu
        tk.Label(algorithm_frame, text="Select Scheduling Algorithm:", bg="#e0e0e0", font=("Arial", 12)).pack(side=tk.TOP, pady=5)
        self.algorithm_menu = ttk.Combobox(algorithm_frame, textvariable=self.selected_algorithm, font=("Arial", 12))
        self.algorithm_menu['values'] = (
            "First Come First Serve (FCFS)", 
            "Non-Preemptive Priority (NPP)", 
            "Preemptive Priority (PP)", 
            "Round Robin (RR)",  
            "Shortest Job First (SJF)",
            "Shortest Remaining Time First (SRTF)"
        )
        self.algorithm_menu.pack(side=tk.TOP, padx=5, pady=5)
        self.algorithm_menu.bind("<<ComboboxSelected>>", self.update_priority_input)

        # Frame for process details input
        input_frame = tk.Frame(self.scheduler_frame, padx=10, pady=10, bg="#e0e0e0")
        input_frame.pack(fill=tk.X)

        # Center the labels and input fields for a single process
        tk.Label(input_frame, text="Process Name:", bg="#e0e0e0", font=("Arial", 12)).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.name_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Arrival Time:", bg="#e0e0e0", font=("Arial", 12)).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.arrival_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.arrival_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Burst Time:", bg="#e0e0e0", font=("Arial", 12)).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.burst_entry = tk.Entry(input_frame, font=("Arial", 12))  # Ensure burst_entry is defined
        self.burst_entry.grid(row=2, column=1, padx=5, pady=5)

        # Button to add a process
        self.add_process_button = tk.Button(
            input_frame,
            text="Add Process",
            command=self.add_process,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            width=15,
            padx=10,
            pady=5
        )
        self.add_process_button.grid(row=4, column=0, pady=10, sticky='ew')  # Center the button in the middle
        self.add_process_button.bind("<Enter>", lambda e: self.on_hover(self.add_process_button, True))
        self.add_process_button.bind("<Leave>", lambda e: self.on_hover(self.add_process_button, False))

        # Button to delete a process
        self.delete_process_button = tk.Button(
            input_frame,
            text="Delete Process",
            command=self.delete_process,
            bg="#f44336",
            fg="white",
            font=("Arial", 12, "bold"),
            width=15,
            padx=10,
            pady=5
        )
        self.delete_process_button.grid(row=4, column=1, pady=10, sticky='ew')  # Center the button in the middle
        self.delete_process_button.bind("<Enter>", lambda e: self.on_hover(self.delete_process_button, True))
        self.delete_process_button.bind("<Leave>", lambda e: self.on_hover(self.delete_process_button, False))

        # Frame for displaying added processes
        self.process_frame = tk.Frame(self.scheduler_frame, bg="#f0f0f0")
        self.process_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview for displaying added processes
        self.process_tree = ttk.Treeview(self.process_frame, columns=("Process Name", "Arrival Time", "Burst Time"), show='headings')
        self.process_tree.heading("Process Name", text="Process Name")
        self.process_tree.heading("Arrival Time", text="Arrival Time")
        self.process_tree.heading("Burst Time", text="Burst Time")

        # Center the numeric columns
        for col in ["Arrival Time", "Burst Time"]:
            self.process_tree.heading(col, anchor="center")
            self.process_tree.column(col, anchor="center")

        # Add a vertical scrollbar
        self.process_scrollbar = ttk.Scrollbar(self.process_frame, orient="vertical", command=self.process_tree.yview)
        self.process_tree.configure(yscrollcommand=self.process_scrollbar.set)

        self.process_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.process_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Button to schedule processes
        # Enhanced Schedule Button
        self.schedule_button = tk.Button(
            self.scheduler_frame,
            text="Schedule",
            command=self.schedule_processes,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            width=20,  # Set a fixed width
            padx=10,   # Internal padding
            pady=5,    # Internal padding
            borderwidth=2,  # Border width
            relief="raised"  # Button relief style
        )
        self.schedule_button.pack(pady=20)  # Add some vertical space around the button

        # Bind hover effects
        self.schedule_button.bind("<Enter>", lambda e: self.on_hover(self.schedule_button, True))
        self.schedule_button.bind("<Leave>", lambda e: self.on_hover(self.schedule_button, False))

                
        # Initially hide the priority and quantum input
        self.priority_label = tk.Label(input_frame, text="Priorities (comma-separated):", bg="#e0e0e0", font=("Arial", 12))
        self.priority_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.quantum_label = tk.Label(input_frame, text="Time Quantum:", bg="#e0e0e0", font=("Arial", 12))
        self.quantum_entry = tk.Entry(input_frame, font=("Arial", 12))

        self.priority_label.grid_forget()
        self.priority_entry.grid_forget()
        self.quantum_label.grid_forget()
        self.quantum_entry.grid_forget()


    def init_gantt_page(self):
        """Initialize the Gantt chart page."""
        self.gantt_label = tk.Label(self.gantt_frame, text="Gantt Chart will be displayed here.", bg="#f0f0f0", font=("Arial", 16))
        self.gantt_label.pack(pady=20)

        # Button to view Gantt chart
        self.view_gantt_button = tk.Button(
            self.gantt_frame,
            text="View Gantt Chart",
            command=self.open_gantt_chart_window,
            bg="#2196F3",
            fg="white",
            font=("Arial", 12, "bold"),
            width=20,  # Set a fixed width
            padx=10,   # Internal padding
            pady=5,    # Internal padding
            borderwidth=2,  # Border width
            relief="raised"  # Button relief style
        )
        self.view_gantt_button.pack(pady=10)

        # Bind hover effects
        self.view_gantt_button.bind("<Enter>", lambda e: self.on_hover(self.view_gantt_button, True))
        self.view_gantt_button.bind("<Leave>", lambda e: self.on_hover(self.view_gantt_button, False))

        # Button to return to the scheduler page
        self.return_button = tk.Button(
            self.gantt_frame,
            text="Back to Scheduler",
            command=self.show_scheduler,
            bg="#f44336",
            fg="white",
            font=("Arial", 12, "bold"),
            width=20,  # Set a fixed width
            padx=10,   # Internal padding
            pady=5,    # Internal padding
            borderwidth=2,  # Border width
            relief="raised"  # Button relief style
        )
        self.return_button.pack(pady=10)

        # Bind hover effects
        self.return_button.bind("<Enter>", lambda e: self.on_hover(self.return_button, True))
        self.return_button.bind("<Leave>", lambda e: self.on_hover(self.return_button, False))


    def on_hover(self, button, hover):
        if hover:
            button.config(bg="#45a049" if button['text'] == "Add Process" else "#d32f2f")  # Darker shade on hover
        else:
            button.config(bg="#4CAF50" if button['text'] == "Add Process" else "#f44336") 

        if hover:
            if button['text'] == "Schedule":
                button.config(bg="#45a049")  # Darker shade on hover
            else:
                button.config(bg="#45a049" if button['text'] == "Add Process" else "#d32f2f")
        else:
            if button['text'] == "Schedule":
                button.config(bg="#4CAF50")  # Original color
            else:
                button.config(bg="#4CAF50" if button['text'] == "Add Process" else "#f44336")

        if hover:
            if button['text'] == "View Gantt Chart":
                button.config(bg="#1E88E5")  # Darker shade on hover
            elif button['text'] == "Back to Scheduler":
                button.config(bg="#d32f2f")  # Darker shade on hover
        else:
            if button['text'] == "View Gantt Chart":
                button.config(bg="#2196F3")  # Original color
            elif button['text'] == "Back to Scheduler":
                button.config(bg="#f44336")  # Original color
        
        if hover:
            if button['text'] == "Gantt Chart":
                button.config(bg="#1E88E5")  # Darker shade on hover
            elif button['text'] == "View Gantt Chart":
                button.config(bg="#1E88E5")  # Darker shade on hover
            elif button['text'] == "Back to Scheduler":
                button.config(bg="#d32f2f")  # Darker shade on hover
        else:
            if button['text'] == "Gantt Chart":
                button.config(bg="#2196F3")  # Original color
            elif button['text'] == "View Gantt Chart":
                button.config(bg="#2196F3")  # Original color
            elif button['text'] == "Back to Scheduler":
                button.config(bg="#f44336")  # Original color

                
                
    def show_scheduler(self):
        """Show the scheduler frame."""
        self.gantt_frame.pack_forget()  # Hide Gantt frame
        self.scheduler_frame.pack(fill=tk.BOTH, expand=True)  # Show scheduler frame

    def show_gantt(self):
        """Show the Gantt chart frame."""
        self.scheduler_frame.pack_forget()  # Hide scheduler frame
        self.gantt_frame.pack(fill=tk.BOTH, expand=True)  # Show Gantt frame

    def update_priority_input(self, event):
        """Show or hide the priority and time quantum input based on the selected algorithm."""
        if self.selected_algorithm.get() in ["Non-Preemptive Priority (NPP)", "Preemptive Priority (PP)"]:
            self.priority_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
            self.priority_entry.grid(row=3, column=1, padx=5, pady=5)
            self.quantum_label.grid_forget()
            self.quantum_entry.grid_forget()
        elif self.selected_algorithm.get() == "Round Robin (RR)":
            self.quantum_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
            self.quantum_entry.grid(row=3, column=1, padx=5, pady=5)
            self.priority_label.grid_forget()
            self.priority_entry.grid_forget()
        else:
            self.priority_entry.grid_forget()
            self.priority_label.grid_forget()
            self.quantum_label.grid_forget()
            self.quantum_entry.grid_forget()

    def open_gantt_chart_window(self):
        """Open a new window to display the Gantt chart."""
        if self.gantt_result is None:
            messagebox.showwarning("Warning", "Please schedule processes first to view the Gantt chart.")
            return

        gantt_window = tk.Toplevel(self.root)
        gantt_window.title("Gantt Chart")
        gantt_window.geometry("800x400")

        # Create a new figure for the Gantt chart
        fig = Figure(figsize=(10, 5))
        ax = fig.add_subplot(111)

        # Prepare data for Gantt chart
        colors = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#FFD700', '#FF69B4', '#8A2BE2', '#FF4500', '#2E8B57', '#D2691E']

        # Check if ganttChartInfo is available in the result
        if 'ganttChartInfo' not in self.gantt_result:
            messagebox.showerror("Error", "Gantt chart data is not available.")
            return

        for i, gantt in enumerate(self.gantt_result['ganttChartInfo']):
            # Create a bar for each job with a different color
            ax.barh(gantt['job'], gantt['stop'] - gantt['start'], left=gantt['start'], color=colors[i % len(colors)])

        ax.set_xlabel('Time')
        ax.set_ylabel('Processes')
        ax.set_title('Gantt Chart')

        # Set x-axis limits dynamically based on the maximum end time
        end_times = [gantt['stop'] for gantt in self.gantt_result['ganttChartInfo']]
        ax.set_xlim(0, max(end_times) + 1)  # Add a little padding to the end time for better visualization

        # Add the figure to the Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=gantt_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def schedule_processes(self):
        """Schedule the processes and display the results in a new window."""
        try:
            # Extract process names, arrival times, and burst times from the process list
            process_names = [p['name'] for p in self.process_list]
            arrival_times = [p['arrival_time'] for p in self.process_list]
            burst_times = [p['burst_time'] for p in self.process_list]

            if len(process_names) == 0:
                raise ValueError("No processes have been added.")

            # Call the appropriate scheduling algorithm
            if self.selected_algorithm.get() == "First Come First Serve (FCFS)":
                result = fcfs(arrival_times, burst_times, process_names)
            elif self.selected_algorithm.get() == "Non-Preemptive Priority (NPP)":
                priorities = list(map(int, self.priority_entry.get().split(',')))
                if len(arrival_times) != len(priorities):
                    raise ValueError("Arrival times and priorities must have the same length.")
                result = npp(arrival_times, burst_times, priorities, process_names)
            elif self.selected_algorithm.get() == "Preemptive Priority (PP)":
                priorities = list(map(int, self.priority_entry.get().split(',')))
                if len(arrival_times) != len(priorities):
                    raise ValueError("Arrival times and priorities must have the same length.")
                result = pp(arrival_times, burst_times, priorities, process_names)
            elif self.selected_algorithm.get() == "Round Robin (RR)":
                time_quantum = int(self.quantum_entry.get())
                result = rr(arrival_times, burst_times, time_quantum, process_names)
            elif self.selected_algorithm.get() == "Shortest Job First (SJF)":
                result = sjf(arrival_times, burst_times, process_names)
            elif self.selected_algorithm.get() == "Shortest Remaining Time First (SRTF)":
                scheduler = SRTFScheduler(arrival_times, burst_times, process_names)
                result = scheduler.schedule()

            # Store the Gantt chart result for later use
            self.gantt_result = result  # Assuming result contains ganttChartInfo

            # Display the results in a new window
            self.show_results_window(result)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show_results_window(self, result):
        """Open a new window to display the scheduling results."""
        results_window = tk.Toplevel(self.root)
        results_window.title("Scheduling Results")
        results_window.geometry("600x400")

        # Create a Treeview to display the results
        result_tree = ttk.Treeview(results_window, columns=("Job", "Arrival Time", "Burst Time", "Finish Time", "Turnaround Time", "Waiting Time"), show='headings')
        result_tree.heading("Job", text="Job")
        result_tree.heading("Arrival Time", text="Arrival Time")
        result_tree.heading("Burst Time", text="Burst Time")
        result_tree.heading("Finish Time", text="Finish Time")
        result_tree.heading("Turnaround Time", text="Turnaround Time")
        result_tree.heading("Waiting Time", text="Waiting Time")

        # Center the numeric columns
        for col in ["Arrival Time", "Burst Time", "Finish Time", "Turnaround Time", "Waiting Time"]:
            result_tree.heading(col, anchor="center")
            result_tree.column(col, anchor="center")

        # Add the results to the Treeview
        for process in result['solvedProcessesInfo']:
            result_tree.insert("", "end", values=(
                process['job'],
                process['at'],
                process['bt'],
                process['ft'],
                process['tat'],
                process['wat']
            ))

        result_tree.pack(fill=tk.BOTH, expand=True)

        # Calculate averages
        total_tat = sum(process['tat'] for process in result['solvedProcessesInfo'])
        total_wt = sum(process['wat'] for process in result['solvedProcessesInfo'])
        num_processes = len(result['solvedProcessesInfo'])

        avg_tat = total_tat / num_processes if num_processes > 0 else 0
        avg_wt = total_wt / num_processes if num_processes > 0 else 0

        # Display average turnaround time and waiting time
        avg_label_frame = tk.Frame(results_window)
        avg_label_frame.pack(pady=10)

        avg_tat_label = tk.Label(avg_label_frame, text=f"Average Turnaround Time: {avg_tat:.2f}", font=("Arial", 12))
        avg_tat_label.pack(side=tk.LEFT, padx=10)

        avg_wt_label = tk.Label(avg_label_frame, text=f"Average Waiting Time: {avg_wt:.2f}", font=("Arial", 12))
        avg_wt_label.pack(side=tk.LEFT, padx=10)

        # Add a button to close
                # Add a button to close the results window
        close_button = tk.Button(results_window, text="Close", command=results_window.destroy, bg="#f44336", fg="white", font=("Arial", 12))
        close_button.pack(pady=10)

    def add_process(self):
        """Add a process to the process list."""
        name = self.name_entry.get()
        arrival_time = self.arrival_entry.get()
        burst_time = self.burst_entry.get()

        # Validate basic inputs
        if not name or not arrival_time.isdigit() or not burst_time.isdigit():
            messagebox.showerror("Error", "Please enter valid process details.")
            return

        arrival_time = int(arrival_time)
        burst_time = int(burst_time)

        # Initialize the process dictionary
        process = {
            'name': name,
            'arrival_time': arrival_time,
            'burst_time': burst_time
        }

        # Check the selected algorithm and add additional details
        if self.selected_algorithm.get() in ["Non-Preemptive Priority (NPP)", "Preemptive Priority (PP)"]:
            priority = self.priority_entry.get()
            if not priority.isdigit():
                messagebox.showerror("Error", "Please enter a valid priority.")
                return
            process['priority'] = int(priority)
            self.process_tree.insert("", "end", values=(process['name'], process['arrival_time'], process['burst_time'], process['priority']))
            self.process_list.append(process)

        elif self.selected_algorithm.get() == "Round Robin (RR)":
            time_quantum = self.quantum_entry.get()
            if not time_quantum.isdigit():
                messagebox.showerror("Error", "Please enter a valid time quantum.")
                return
            process['time_quantum'] = int(time_quantum)
            self.process_tree.insert("", "end", values=(process['name'], process['arrival_time'], process['burst_time'], process['time_quantum']))
            self.process_list.append(process)

        else:  # For FCFS, SJF, SRTF
            self.process_tree.insert("", "end", values=(process['name'], process['arrival_time'], process['burst_time'], "N/A"))
            self.process_list.append(process)

        # Clear the input fields
        self.name_entry.delete(0, tk.END)
        self.arrival_entry.delete(0, tk.END)
        self.burst_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)
        self.quantum_entry.delete(0, tk.END)

    def delete_process(self):
        """Delete the selected process from the process list."""
        selected_item = self.process_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a process to delete.")
            return

        # Get the selected process name
        selected_process = self.process_tree.item(selected_item)['values'][0]

        # Remove the process from the internal list
        self.process_list = [p for p in self.process_list if p['name'] != selected_process]

        # Remove the selected item from the Treeview
        self.process_tree.delete(selected_item)

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()