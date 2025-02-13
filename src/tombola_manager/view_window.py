import tkinter as tk
from tkinter import ttk


class ViewWindow:
    def __init__(self, game):
        self.window = tk.Toplevel()
        self.window.title(f"Tombola View - {game.name}")
        self.game = game
        
        # Create main frame
        main_frame = ttk.Frame(self.window)
        main_frame.grid(padx=10, pady=10, sticky="nsew")
        
        # Add state display
        self.state_display = tk.Text(main_frame, height=1, width=20, state='disabled')
        self.state_display.grid(row=0, column=0, columnspan=10, pady=5)
        self.update_state_display()
        
        # Create grid of numbers with consistent spacing
        self.number_labels = {}
        for i in range(1, 91):
            row = (i-1) // 10 + 1  # Adjust row index to account for state display
            col = (i-1) % 10
            
            # Create a frame for each number to ensure consistent sizing
            frame = ttk.Frame(main_frame, width=50, height=50)
            frame.grid(row=row, column=col, padx=2, pady=2)
            frame.grid_propagate(False)  # Force the frame to stay at specified size
            
            label = tk.Label(frame, text=str(i),
                           font=('TkDefaultFont', 10))
            label.place(relx=0.5, rely=0.5, anchor="center")  # Center in frame
            self.number_labels[i] = label
        
        self.update_display()
    
    def update_display(self):
        called_font = ('TkDefaultFont', 20, 'bold')  # Bold font for called numbers
        uncalled_font = ('TkDefaultFont', 18)  # Normal font for uncalled numbers
        
        for num in range(1, 91):
            label = self.number_labels[num]
            
            if num == self.game.last_number:
                # Last called number - green background, bold
                label.config(
                    bg="green",
                    fg="white",
                    font=called_font
                )
            elif num in self.game.numbers:
                # Called numbers - bold, black on white
                label.config(
                    bg="white",
                    fg="black",
                    font=called_font
                )
            else:
                # Uncalled numbers - light gray, normal font
                label.config(
                    bg="white",
                    fg="lightgray",
                    font=uncalled_font
                )
    
    def update_state_display(self):
        self.state_display.config(state='normal')
        self.state_display.delete(1.0, tk.END)
        self.state_display.insert(tk.END, f"State: {self.game.state}")
        self.state_display.config(state='disabled')