import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

from src.tombola_manager.tombola_game import TombolaGame
from src.tombola_manager.view_window import ViewWindow
from src.tombola_manager.control_window import ControlWindow


class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tombola Manager")
        self.window.geometry("500x500")
        
        # Set custom icon
        self.window.iconbitmap('src/tombola_manager/icon/icon.ico')
        
        # New game frame
        new_game_frame = ttk.LabelFrame(self.window, text="New Game")
        new_game_frame.pack(padx=10, pady=10, fill="x")
        
        tk.Label(new_game_frame, text="Game Name:").pack(pady=5)
        self.name_entry = tk.Entry(new_game_frame)
        self.name_entry.pack(pady=5)
        tk.Button(new_game_frame, text="Start New Game", 
                 command=self.start_new_game).pack(pady=5)
        
        # Load game frame
        load_game_frame = ttk.LabelFrame(self.window, text="Load Game")
        load_game_frame.pack(padx=10, pady=10, fill="x", expand=True)
        
        self.games_listbox = tk.Listbox(load_game_frame)
        self.games_listbox.pack(padx=10, pady=5, fill="both", expand=True)
        tk.Button(load_game_frame, text="Load Selected Game", 
                 command=self.load_game).pack(pady=5)
        
        self.update_games_list()
        
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
                messagebox.showerror("Error", "A game with this name already exists!")
                return
            
            game = TombolaGame(name)
            game.log_action("Game created")  # Log game creation
            view_window = ViewWindow(game)
            ControlWindow(game, view_window)
        else:
            messagebox.showerror("Error", "Please enter a game name!")
    
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
                game.state = data.get("state", "Ambo")  # Add this line
                game.log_action("Game loaded")
                
                view_window = ViewWindow(game)
                ControlWindow(game, view_window)
            except Exception as e:
                messagebox.showerror("Error", f"Error loading game: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please select a game to load!")
    
    def run(self):
        self.window.mainloop()