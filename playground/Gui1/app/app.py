import tkinter as tk
from .main_application import MainApplication

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_frame = MainApplication(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
