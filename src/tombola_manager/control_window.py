import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os

from src.tombola_manager.utils import resource_path
from src.tombola_manager.language_manager import LanguageManager


class ControlWindow:
    def __init__(self, game, view_window):
        self.window = tk.Toplevel()
        self.lang = LanguageManager()
        self.window.title(self.lang.get_text('control_title', game.name))
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
        control_frame = ttk.LabelFrame(left_frame, text=self.lang.get_text('controls'))
        control_frame.pack(padx=5, pady=5, fill="x")

        # Add state selection dropdown
        tk.Label(control_frame, text=self.lang.get_text('select_state')).pack(pady=5)
        self.state_var = tk.StringVar(value=self.game.state)
        self.state_dropdown = ttk.Combobox(control_frame, textvariable=self.state_var, state="readonly")
        self.state_dropdown['values'] = (
            self.lang.get_text('ambo'),
            self.lang.get_text('terno'),
            self.lang.get_text('quaterna'),
            self.lang.get_text('cinquina'),
            self.lang.get_text('tombola'),
            self.lang.get_text('superbingo')
        )
        self.state_dropdown.pack(pady=5)
        self.state_dropdown.bind("<<ComboboxSelected>>", self.update_state)
        
        # Number entry
        tk.Label(control_frame, text=self.lang.get_text('enter_number')).pack(pady=5)
        self.number_entry = tk.Entry(control_frame)
        self.number_entry.pack(pady=5)
        
        # Buttons
        tk.Button(control_frame, text=self.lang.get_text('add_number'), 
                 command=self.add_number, bg="green", fg="white").pack(pady=5)
        tk.Button(control_frame, text=self.lang.get_text('remove_number'), 
                 command=self.remove_number, bg="red", fg="white").pack(pady=5)
        tk.Button(control_frame, text=self.lang.get_text('save_game'), 
                 command=self.save_game).pack(pady=5)
        
        # Status frame (bottom left)
        status_frame = ttk.LabelFrame(left_frame, text=self.lang.get_text('status_table'))
        status_frame.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Create notebook for different views
        status_notebook = ttk.Notebook(status_frame)
        status_notebook.pack(fill="both", expand=True)
        
        # Grid view tab
        grid_frame = ttk.Frame(status_notebook)
        status_notebook.add(grid_frame, text=self.lang.get_text('grid_view'))
        
        # Create grid of numbers
        self.grid_labels = {}
        grid_container = ttk.Frame(grid_frame)
        grid_container.pack(padx=5, pady=5)
        
        for i in range(1, 91):
            row = (i-1) // 10
            col = (i-1) % 10
            label = tk.Label(grid_container, text=str(i), width=3, height=1,
                           relief="raised", borderwidth=1)
            label.grid(row=row, column=col, padx=1, pady=1)
            self.grid_labels[i] = label
        
        # List view tab
        list_frame = ttk.Frame(status_notebook)
        status_notebook.add(list_frame, text=self.lang.get_text('list_view'))
        
        # Create status table
        self.status_table = ttk.Treeview(list_frame, columns=("Called", "Remaining"),
                                       show="headings", height=5)
        self.status_table.heading("Called", text=self.lang.get_text('called_numbers'))
        self.status_table.heading("Remaining", text=self.lang.get_text('remaining_numbers'))
        self.status_table.column("Called", width=150)
        self.status_table.column("Remaining", width=150)
        self.status_table.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Add statistics
        self.stats_frame = ttk.LabelFrame(status_frame, text=self.lang.get_text('statistics'))
        self.stats_frame.pack(padx=5, pady=5, fill="x")
        
        self.stats_labels = {}
        stats = [
            ("total_numbers", self.lang.get_text('total_numbers')),
            ("remaining", self.lang.get_text('numbers_remaining')),
            ("percentage", self.lang.get_text('completion'))
        ]
        
        for key, text in stats:
            frame = ttk.Frame(self.stats_frame)
            frame.pack(fill="x", padx=5, pady=2)
            tk.Label(frame, text=text).pack(side="left")
            label = tk.Label(frame, text="0")
            label.pack(side="right")
            self.stats_labels[key] = label
        
        # Log frame (right side)
        log_frame = ttk.LabelFrame(main_frame, text=self.lang.get_text('action_log'))
        log_frame.pack(side="right", padx=5, pady=5, fill="both", expand=True)
        
        # Create scrolled text widget for log
        self.log_text = scrolledtext.ScrolledText(log_frame, width=40, height=20, 
                                                wrap=tk.WORD, state='disabled')
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
                    self.update_status_table()
                    self.save_game()
                else:
                    messagebox.showwarning(self.lang.get_text('warning'), 
                                         self.lang.get_text('number_exists'))
                    self.game.log_action(self.lang.get_text('failed_add').format(number))
                    self.update_log()
            else:
                messagebox.showwarning(self.lang.get_text('warning'), 
                                     self.lang.get_text('invalid_number'))
                self.game.log_action(self.lang.get_text('failed_add_invalid').format(number))
                self.update_log()
        except ValueError:
            messagebox.showerror(self.lang.get_text('error'), 
                               self.lang.get_text('enter_valid'))
            self.game.log_action(self.lang.get_text('failed_add_input'))
            self.update_log()
        self.number_entry.delete(0, tk.END)
    
    def remove_number(self):
        try:
            number = int(self.number_entry.get())
            if self.game.remove_number(number):
                self.view_window.update_display()
                self.update_log()
                self.update_status_table()
                self.save_game()
            else:
                messagebox.showwarning(self.lang.get_text('warning'), 
                                     self.lang.get_text('number_not_found'))
                self.game.log_action(self.lang.get_text('failed_remove').format(number))
                self.update_log()
        except ValueError:
            messagebox.showerror(self.lang.get_text('error'), 
                               self.lang.get_text('enter_valid'))
            self.game.log_action(self.lang.get_text('failed_remove_input'))
            self.update_log()
        self.number_entry.delete(0, tk.END)
    
    def update_state(self, event):
        self.game.state = self.state_var.get()
        self.view_window.update_state_display()
        self.game.log_action(self.lang.get_text('state_changed').format(self.game.state))
        self.update_log()
    
    def save_game(self):
        data = {
            "name": self.game.name,
            "numbers": list(self.game.numbers),
            "date": self.game.date,
            "log": self.game.log,
            "last_number": self.game.last_number,
            "state": self.game.state
        }
        
        if not os.path.exists("games"):
            os.makedirs("games")
            
        with open(f"games/{self.game.name}.json", "w") as f:
            json.dump(data, f)
