import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os

from src.tombola_manager.utils import resource_path


class ControlWindow:
    def __init__(self, game, view_window):
        self.window = tk.Toplevel()
        self.window.title(f"Tombola Control - {game.name}")
        self.game = game
        self.view_window = view_window

        # Set custom icon
        self.window.iconbitmap(resource_path('src/tombola_manager/icon/icon.ico'))

        # Create main frame for better organization
        main_frame = ttk.Frame(self.window)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Left side frame
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side="left", padx=5, fill="both", expand=True)
        
        # Control frame (top left)
        control_frame = ttk.LabelFrame(left_frame, text="Controls")
        control_frame.pack(padx=5, pady=5, fill="x")


        # Add state selection dropdown
        tk.Label(control_frame, text="Select State:", font=("Helvetica", 10)).pack(pady=5)
        self.state_var = tk.StringVar(value="Ambo")
        self.state_dropdown = ttk.Combobox(control_frame, textvariable=self.state_var, state="readonly")
        self.state_dropdown['values'] = ("Ambo", "Terno", "Quaterna", "Cinquina", "Tombola", "SUPERBINGO")
        self.state_dropdown.pack(pady=5)
        self.state_dropdown.bind("<<ComboboxSelected>>", self.update_state)
        
        # Number entry
        tk.Label(control_frame, text="Enter number:", font=("Helvetica", 10)).pack(pady=5)
        self.number_entry = tk.Entry(control_frame, font=("Helvetica", 10))
        self.number_entry.pack(pady=5)
        
        # Buttons
        tk.Button(control_frame, text="Add Number", 
                 command=self.add_number, bg="green", fg="white", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Button(control_frame, text="Remove Number", 
                 command=self.remove_number, bg="red", fg="white", font=("Helvetica", 12, "bold")).pack(pady=5)
        tk.Button(control_frame, text="Save Game", 
                 command=self.save_game, font=("Helvetica", 12)).pack(pady=5)
        
        # Status frame (bottom left)
        status_frame = ttk.LabelFrame(left_frame, text="Status Table")
        status_frame.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Create notebook for different views
        status_notebook = ttk.Notebook(status_frame)
        status_notebook.pack(fill="both", expand=True)
        
        # Grid view tab
        grid_frame = ttk.Frame(status_notebook)
        status_notebook.add(grid_frame, text="Grid View")
        
        # Create grid of numbers
        self.grid_labels = {}
        grid_container = ttk.Frame(grid_frame)
        grid_container.pack(padx=5, pady=5)
        
        for i in range(1, 91):
            row = (i-1) // 10
            col = (i-1) % 10
            label = tk.Label(grid_container, text=str(i), width=3, height=1,
                           relief="raised", borderwidth=1, font=("Helvetica", 10))
            label.grid(row=row, column=col, padx=1, pady=1)
            self.grid_labels[i] = label
        
        # List view tab
        list_frame = ttk.Frame(status_notebook)
        status_notebook.add(list_frame, text="List View")
        
        # Create status table (moved to list view tab)
        self.status_table = ttk.Treeview(list_frame, columns=("Called", "Remaining"),
                                       show="headings", height=5)
        self.status_table.heading("Called", text="Called Numbers")
        self.status_table.heading("Remaining", text="Remaining Numbers")
        self.status_table.column("Called", width=150)
        self.status_table.column("Remaining", width=150)
        self.status_table.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Add statistics
        self.stats_frame = ttk.LabelFrame(status_frame, text="Statistics")
        self.stats_frame.pack(padx=5, pady=5, fill="x")
        
        self.stats_labels = {}
        stats = [
            ("total_numbers", "Total Numbers Called:"),
            ("remaining", "Numbers Remaining:"),
            ("percentage", "Completion Percentage:")
        ]
        
        for key, text in stats:
            frame = ttk.Frame(self.stats_frame)
            frame.pack(fill="x", padx=5, pady=2)
            tk.Label(frame, text=text, font=("Helvetica", 10)).pack(side="left")
            label = tk.Label(frame, text="0", font=("Helvetica", 10))
            label.pack(side="right")
            self.stats_labels[key] = label
        
        # Log frame (right side)
        log_frame = ttk.LabelFrame(main_frame, text="Action Log")
        log_frame.pack(side="right", padx=5, pady=5, fill="both", expand=True)
        
        # Create scrolled text widget for log
        self.log_text = scrolledtext.ScrolledText(log_frame, width=40, height=20, 
                                                wrap=tk.WORD, state='disabled', font=("Helvetica", 10))
        self.log_text.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Load existing log if any
        self.update_log()
        self.update_status_table()
    
    def update_status_table(self):
        # Update grid view
        for num in range(1, 91):
            if num in self.game.numbers:
                self.grid_labels[num].config(bg="green", fg="white")
            else:
                self.grid_labels[num].config(bg="white", fg="black")
        
        # Update list view
        for item in self.status_table.get_children():
            self.status_table.delete(item)
        
        # Get called and remaining numbers
        called_numbers = sorted(list(self.game.numbers))
        remaining_numbers = sorted(list(set(range(1, 91)) - self.game.numbers))
        
        # Split numbers into groups of 10 for better readability
        called_groups = [called_numbers[i:i+10] for i in range(0, len(called_numbers), 10)]
        remaining_groups = [remaining_numbers[i:i+10] for i in range(0, len(remaining_numbers), 10)]
        
        # Add rows to table
        max_rows = max(len(called_groups), len(remaining_groups))
        for i in range(max_rows):
            called = ', '.join(map(str, called_groups[i])) if i < len(called_groups) else ""
            remaining = ', '.join(map(str, remaining_groups[i])) if i < len(remaining_groups) else ""
            self.status_table.insert("", "end", values=(called, remaining))
        
        # Update statistics
        total_called = len(self.game.numbers)
        total_remaining = 90 - total_called
        completion_percentage = (total_called / 90) * 100
        
        self.stats_labels["total_numbers"].config(text=str(total_called))
        self.stats_labels["remaining"].config(text=str(total_remaining))
        self.stats_labels["percentage"].config(text=f"{completion_percentage:.1f}%")
    
    def update_log(self):
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        for log_entry in self.game.log:
            self.log_text.insert(tk.END, log_entry + "\n")
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)  # Auto-scroll to the bottom
    
    def add_number(self):
        try:
            number = int(self.number_entry.get())
            if 1 <= number <= 90:
                if self.game.add_number(number):
                    self.view_window.update_display()
                    self.update_log()
                    self.update_status_table()  # Add this line
                    self.save_game()
                else:
                    messagebox.showwarning("Warning", "Number already exists!")
                    self.game.log_action(f"Failed to add number {number} (already exists)")
                    self.update_log()
            else:
                messagebox.showwarning("Warning", "Number must be between 1 and 90!")
                self.game.log_action(f"Failed to add invalid number {number} (out of range)")
                self.update_log()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
            self.game.log_action("Failed to add invalid input")
            self.update_log()
        self.number_entry.delete(0, tk.END)
    
    def remove_number(self):
        try:
            number = int(self.number_entry.get())
            if self.game.remove_number(number):
                self.view_window.update_display()
                self.update_log()
                self.update_status_table()  # Add this line
                self.save_game()
            else:
                messagebox.showwarning("Warning", "Number not found!")
                self.game.log_action(f"Failed to remove number {number} (not found)")
                self.update_log()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
            self.game.log_action("Failed to remove invalid input")
            self.update_log()
        self.number_entry.delete(0, tk.END)
    
    def update_state(self, event):
        self.game.state = self.state_var.get()
        self.view_window.update_state_display()
        self.game.log_action(f"State changed to {self.game.state}")
        self.update_log()
    
    def save_game(self):
        data = {
            "name": self.game.name,
            "numbers": list(self.game.numbers),
            "date": self.game.date,
            "log": self.game.log,
            "last_number": self.game.last_number,  # Add this line
            "state": self.game.state  # Add this line
        }
        
        if not os.path.exists("games"):
            os.makedirs("games")
            
        with open(f"games/{self.game.name}.json", "w") as f:
            json.dump(data, f)
