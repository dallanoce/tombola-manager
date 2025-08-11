from datetime import datetime
from .language_manager import LanguageManager


class TombolaGame:
    def __init__(self, name):
        self.name = name
        self.numbers = set()
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log = []
        self.last_number = None
        self.state = "Ambo"
        self.lang = LanguageManager()
    
    def add_number(self, number):
        """Add a number to the game"""
        if 1 <= number <= 90 and number not in self.numbers:
            self.numbers.add(number)
            self.last_number = number
            return True
        return False
    
    def remove_number(self, number):
        """Remove a number from the game"""
        if number in self.numbers:
            self.numbers.remove(number)
            if number == self.last_number:
                self.last_number = None
            return True
        return False
    
    def log_action(self, message):
        """Add an action to the log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log.append(f"[{timestamp}] {message}")
        
    def get_state_text(self):
        """Get the current state text"""
        return self.lang.get_text(self.state.lower())