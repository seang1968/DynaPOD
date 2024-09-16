import tkinter as tk
from tkinter import ttk

# Function to update suggestions
def update_suggestions(event):
    typed_text = entry.get().upper()
    suggestions = [item for item in elements if item.startswith(typed_text)]
    listbox.delete(0, tk.END)
    for suggestion in suggestions[:5]:
        listbox.insert(tk.END, suggestion)

# List of possible elements
elements = ['BTC', 'BTCC', 'BTCCC', 'ETH', 'XRP', 'LTC', 'BNB']

# Create the main window
root = tk.Tk()
root.title("Data Collection App")
root.geometry("800x600")  # Adjust the window size to half-screen if needed

# Menu bar
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New")
file_menu.add_command(label="Open")
file_menu.add_command(label="Save")
menu_bar.add_cascade(label="File", menu=file_menu)
root.config(menu=menu_bar)

# Dynamic Textbox with Suggestions
frame = tk.Frame(root)
frame.pack(pady=20)

entry_label = tk.Label(frame, text="Start Typing:")
entry_label.pack(anchor="w")

entry = tk.Entry(frame)
entry.pack()

listbox = tk.Listbox(frame, height=5)
listbox.pack()

entry.bind("<KeyRelease>", update_suggestions)

# Drop-down menu
dropdown_label = tk.Label(root, text="Choose an option:")
dropdown_label.pack(anchor="w")

options = ["Option 1", "Option 2", "Option 3"]
dropdown = ttk.Combobox(root, values=options)
dropdown.pack()

# Button
submit_button = tk.Button(root, text="Submit", command=lambda: print("Submitted!"))
submit_button.pack(pady=20)

root.mainloop()
