from datetime import datetime


class TombolaGame:
    def __init__(self, name):
        self.name = name
        self.numbers = set()
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log = []
        self.last_number = None  # Add tracking for last number
        self.state = "Ambo"  # Add this line
    
    def add_number(self, number):
        if number not in self.numbers:
            self.numbers.add(number)
            self.last_number = number  # Track last added number
            self.log_action(f"Added number {number}")
            return True
        return False
    
    def remove_number(self, number):
        if number in self.numbers:
            self.numbers.remove(number)
            if self.last_number == number:
                # If we removed the last number, find the new last number
                self.last_number = max(self.numbers) if self.numbers else None
            self.log_action(f"Removed number {number}")
            return True
        return False
    
    def log_action(self, action):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {action}"
        self.log.append(log_entry)