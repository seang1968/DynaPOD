import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

# Database setup
DB_NAME = "configurations.db"

def initialize_database():
    """Create the database and tables if they do not exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create Coins table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Coins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)
    
    # Create CoinPairs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CoinPairs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pair TEXT UNIQUE NOT NULL
        )
    """)
    
    # Create Channels table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

# Initialize the database
initialize_database()

# GUI Application
class ConfigApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Collection App with Configurations")
        self.root.geometry("800x600")  # Adjust as needed

        # Menu bar
        self.create_menu()

        # Main Frames
        self.create_main_frames()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        
        # File Menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save")
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Configurations Menu
        config_menu = tk.Menu(menu_bar, tearoff=0)
        config_menu.add_command(label="Manage Coins", command=self.manage_coins)
        config_menu.add_command(label="Manage Coin Pairs", command=self.manage_coin_pairs)
        config_menu.add_command(label="Manage Channels", command=self.manage_channels)
        menu_bar.add_cascade(label="Configurations", menu=config_menu)
        
        self.root.config(menu=menu_bar)

    def create_main_frames(self):
        # Dynamic Textbox with Suggestions
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        entry_label = tk.Label(frame, text="Start Typing:")
        entry_label.pack(anchor="w")

        self.entry = tk.Entry(frame)
        self.entry.pack()

        self.listbox = tk.Listbox(frame, height=5)
        self.listbox.pack()

        self.entry.bind("<KeyRelease>", self.update_suggestions)

        # Drop-down menu
        dropdown_label = tk.Label(self.root, text="Choose an option:")
        dropdown_label.pack(anchor="w")

        options = ["Option 1", "Option 2", "Option 3"]
        self.dropdown = ttk.Combobox(self.root, values=options)
        self.dropdown.pack()

        # Button
        submit_button = tk.Button(self.root, text="Submit", command=self.submit_action)
        submit_button.pack(pady=20)

        # Sample data for suggestions
        self.elements = ['BTC', 'BTCC', 'BTCCC', 'ETH', 'XRP', 'LTC', 'BNB']

    def update_suggestions(self, event):
        typed_text = self.entry.get().upper()
        suggestions = [item for item in self.elements if item.startswith(typed_text)]
        self.listbox.delete(0, tk.END)
        for suggestion in suggestions[:5]:
            self.listbox.insert(tk.END, suggestion)

    def submit_action(self):
        selected_option = self.dropdown.get()
        print(f"Submitted: {selected_option}")
        messagebox.showinfo("Submission", f"You selected: {selected_option}")

    # Configuration Management Windows
    def manage_coins(self):
        ConfigManager(self.root, "Coins", "name")

    def manage_coin_pairs(self):
        ConfigManager(self.root, "CoinPairs", "pair")

    def manage_channels(self):
        ConfigManager(self.root, "Channels", "name")

class ConfigManager:
    def __init__(self, parent, table, field):
        self.table = table
        self.field = field
        self.window = tk.Toplevel(parent)
        self.window.title(f"Manage {table}")
        self.window.geometry("400x400")

        # Entry for new item
        self.entry_label = tk.Label(self.window, text=f"Add New {field.capitalize()}:")
        self.entry_label.pack(pady=10)

        self.new_entry = tk.Entry(self.window)
        self.new_entry.pack(pady=5)

        self.add_button = tk.Button(self.window, text="Add", command=self.add_item)
        self.add_button.pack(pady=5)

        # Listbox to display existing items
        self.listbox = tk.Listbox(self.window, height=15)
        self.listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        self.load_items()

    def add_item(self):
        item = self.new_entry.get().strip()
        if not item:
            messagebox.showwarning("Input Error", f"Please enter a {self.field}.")
            return
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute(f"INSERT INTO {self.table} ({self.field}) VALUES (?)", (item,))
            conn.commit()
            messagebox.showinfo("Success", f"{self.field.capitalize()} added successfully.")
            self.new_entry.delete(0, tk.END)
            self.load_items()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", f"{self.field.capitalize()} already exists.")
        finally:
            conn.close()

    def load_items(self):
        self.listbox.delete(0, tk.END)
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(f"SELECT {self.field} FROM {self.table}")
        rows = cursor.fetchall()
        for row in rows:
            self.listbox.insert(tk.END, row[0])
        conn.close()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigApp(root)
    root.mainloop()
