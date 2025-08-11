import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

from src.tombola_manager.tombola_game import TombolaGame
from src.tombola_manager.view_window import ViewWindow
from src.tombola_manager.control_window import ControlWindow
from src.tombola_manager.utils import resource_path
from src.tombola_manager.language_manager import LanguageManager


class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.lang = LanguageManager()
        self.window.title(self.lang.get_text('app_title'))
        self.window.geometry("500x500")
        
        # Set custom icon
        self.window.iconbitmap(resource_path('src/tombola_manager/icon/icon.ico'))

        # Language selection frame
        lang_frame = ttk.Frame(self.window)
        lang_frame.pack(padx=10, pady=5, fill="x")
        
        ttk.Label(lang_frame, text="Language/Lingua:").pack(side="left", padx=5)
        self.lang_var = tk.StringVar(value=self.lang.get_current_language())
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var, values=["en", "it"], state="readonly", width=5)
        lang_combo.pack(side="left")
        lang_combo.bind("<<ComboboxSelected>>", self.change_language)
        
        # New game frame
        new_game_frame = ttk.LabelFrame(self.window, text=self.lang.get_text('new_game'))
        new_game_frame.pack(padx=10, pady=10, fill="x")
        
        ttk.Label(new_game_frame, text=self.lang.get_text('game_name')).pack(pady=5)
        self.name_entry = ttk.Entry(new_game_frame)
        self.name_entry.pack(pady=5)
        ttk.Button(new_game_frame, text=self.lang.get_text('start_new_game'), 
                 command=self.start_new_game).pack(pady=5)
        
        # Load game frame
        load_game_frame = ttk.LabelFrame(self.window, text=self.lang.get_text('load_game'))
        load_game_frame.pack(padx=10, pady=10, fill="x", expand=True)
        
        self.games_listbox = tk.Listbox(load_game_frame)
        self.games_listbox.pack(padx=10, pady=5, fill="both", expand=True)
        ttk.Button(load_game_frame, text=self.lang.get_text('load_selected_game'), 
                 command=self.load_game).pack(pady=5)
        
        self.update_games_list()
    
    def change_language(self, event=None):
        self.lang.set_language(self.lang_var.get())
        # Update all text in the main window
        self.window.title(self.lang.get_text('app_title'))
        for widget in self.window.winfo_children():
            if isinstance(widget, ttk.LabelFrame):
                if 'new_game' in str(widget):
                    widget.configure(text=self.lang.get_text('new_game'))
                elif 'load_game' in str(widget):
                    widget.configure(text=self.lang.get_text('load_game'))
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Button):
                        if 'start_new_game' in str(child):
                            child.configure(text=self.lang.get_text('start_new_game'))
                        elif 'load_selected_game' in str(child):
                            child.configure(text=self.lang.get_text('load_selected_game'))
                    elif isinstance(child, ttk.Label) and 'game_name' in str(child):
                        child.configure(text=self.lang.get_text('game_name'))
        
    def update_games_list(self):
        self.games_listbox.delete(0, tk.END)
        if os.path.exists("games"):
            for file in os.listdir("games"):
                if file.endswith(".json"):
                    self.games_listbox.insert(tk.END, file[:-5])
    
    def start_new_game(self):
        name = self.name_entry.get().strip()
        if name:
            if os.path.exists(f"games/{name}.json"):
                messagebox.showerror(self.lang.get_text('error'), 
                                   self.lang.get_text('game_exists'))
                return
            
            game = TombolaGame(name)
            game.log_action(self.lang.get_text('game_created'))
            view_window = ViewWindow(game)
            ControlWindow(game, view_window)
        else:
            messagebox.showerror(self.lang.get_text('error'), 
                               self.lang.get_text('enter_game_name'))
    
    def load_game(self):
        selection = self.games_listbox.curselection()
        if selection:
            game_name = self.games_listbox.get(selection[0])
            try:
                with open(f"games/{game_name}.json", "r") as f:
                    data = json.load(f)
                
                game = TombolaGame(data["name"])
                game.numbers = set(data["numbers"])
                game.date = data["date"]
                game.log = data.get("log", [])
                game.last_number = data.get("last_number", None)
                game.state = data.get("state", "Ambo")
                game.log_action(self.lang.get_text('game_loaded'))
                
                view_window = ViewWindow(game)
                ControlWindow(game, view_window)
            except Exception as e:
                messagebox.showerror(
                    self.lang.get_text('error'),
                    self.lang.get_text('error_loading').format(str(e))
                )
        else:
            messagebox.showwarning(
                self.lang.get_text('warning'),
                self.lang.get_text('select_game')
            )
    
    def run(self):
        self.window.mainloop()