import tkinter as tk
from tkinter import ttk

from src.tombola_manager.utils import resource_path
from src.tombola_manager.language_manager import LanguageManager


class ViewWindow:
    def __init__(self, game):
        # Configure styles for dark mode
        style = ttk.Style()
        style.configure("Dark.TFrame", background="#2e2e2e")

        self.window = tk.Toplevel()
        self.lang = LanguageManager()
        self.window.title(self.lang.get_text('view_title', game.name))
        self.window.attributes('-fullscreen', True)  # Make the window full screen
        self.window.resizable(False, False)  # Make the window not resizable
        self.game = game
    
        # Set custom icon
        self.window.iconbitmap(resource_path('src/tombola_manager/icon/icon.ico'))
        
        # Set dark mode colors
        self.bg_color = "#2e2e2e"
        self.fg_color = "#ffffff"
        self.highlight_color = "#4e4e4e"
        self.called_font = 20
        self.uncalled_font = 18
        
        self.window.configure(bg=self.bg_color)
        
        # Create main frame
        main_frame = ttk.Frame(self.window)
        main_frame.grid(padx=20, pady=20, sticky="nsew")
        main_frame.configure(style="Dark.TFrame")
        
        # Configure grid to expand with window
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Add state display
        self.state_display = tk.Text(main_frame, height=1, width=30, state='disabled', bg=self.bg_color, fg=self.fg_color, font=('TkDefaultFont', 14))
        self.state_display.grid(row=0, column=0, columnspan=10, pady=5, sticky="ew")
        self.state_display.tag_configure("center", justify='center')
        self.update_state_display()
        
        # Create grid of numbers with consistent spacing
        self.number_labels = {}
        for i in range(1, 91):
            row = (i-1) // 10 + 1  # Adjust row index to account for state display
            col = (i-1) % 10
            
            # Create a frame for each number to ensure consistent sizing
            frame = ttk.Frame(main_frame, width=50, height=50)
            frame.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            frame.grid_propagate(False)  # Force the frame to stay at specified size
            frame.configure(style="Dark.TFrame")
            
            label = tk.Label(frame, text=str(i), width=2,
                           font=('TkDefaultFont', 10), bg=self.bg_color, fg=self.fg_color)
            label.place(relx=0.5, rely=0.5, anchor="center")  # Center in frame
            self.number_labels[i] = label
        
        # Configure grid to expand with window
        for i in range(1, 10):
            main_frame.grid_rowconfigure(i, weight=1)
            main_frame.grid_columnconfigure(i, weight=1)
        
        self.update_display()
        
        # Bind the configure event to adjust font size only once
        self.window.bind('<Configure>', self.adjust_font_size_once)
        self.font_adjusted = False
    
    def adjust_font_size_once(self, event):
        if not self.font_adjusted:
            self.adjust_font_size(event)
            self.font_adjusted = True
    
    def adjust_font_size(self, event):
        # Calculate font size based on window size
        new_font_size = max(10, int(event.width / 40))
        self.called_font = new_font_size
        self.uncalled_font = new_font_size - 2
        
        for num in range(1, 91):
            label = self.number_labels[num]
            if num == self.game.last_number:
                label.config(font=('TkDefaultFont', self.called_font, 'bold'))
            elif num in self.game.numbers:
                label.config(font=('TkDefaultFont', self.called_font, 'bold'))
            else:
                label.config(font=('TkDefaultFont', self.uncalled_font))
        
        self.state_display.config(font=('TkDefaultFont', new_font_size))
    
    def update_display(self):
        called_font = ('TkDefaultFont', self.called_font, 'bold')  # Bold font for called numbers
        uncalled_font = ('TkDefaultFont', self.uncalled_font)  # Normal font for uncalled numbers
        
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
                    bg=self.highlight_color,
                    fg="#ffffff",
                    font=called_font
                )
            else:
                # Uncalled numbers - light gray, normal font
                label.config(
                    bg=self.bg_color,
                    fg="#4e4e4e",
                    font=uncalled_font
                )
    
    def update_state_display(self):
        self.state_display.config(state='normal')
        self.state_display.delete(1.0, tk.END)
        self.state_display.insert(tk.END, self.game.state, "center")
        self.state_display.config(state='disabled')