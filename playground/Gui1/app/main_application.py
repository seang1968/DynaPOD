import tkinter as tk

class MainApplication(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.master.title("Simple Windows Application")
        self.master.geometry("400x300")
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        """This method will be used to add widgets to the application."""
        # Example label, you can add more widgets here
        self.label = tk.Label(self, text="Hello, World!")
        self.label.pack(pady=20)

        # Example button, you can add more widgets here
        self.button = tk.Button(self, text="Click Me", command=self.on_button_click)
        self.button.pack(pady=10)

    def on_button_click(self):
        """This method handles button click events."""
        print("Button was clicked!")
