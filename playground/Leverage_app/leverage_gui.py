import tkinter as tk
from tkinter import ttk

class LeverageGUI:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.title("Leverage Selector")

        # Create the main label
        self.label = ttk.Label(root, text="Leverage:")
        self.label.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        # Create slider and increase size (length=500)
        self.slider = ttk.Scale(
            root, from_=controller.model.min_leverage, to=controller.model.max_leverage,
            orient='horizontal', command=self.slider_changed, length=500
        )
        self.slider.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        # Create entry box
        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(root, textvariable=self.entry_var, width=10)
        self.entry.grid(row=1, column=2, padx=10, pady=10)

        # Add binding for the entry box
        self.entry.bind("<Return>", self.entry_changed)

        # Set default value
        self.entry_var.set(str(controller.model.get_leverage()))
        self.slider.set(controller.model.get_leverage())

        # Add labels for 5, 25, 50, 75, and 100
        self.slider_labels_frame = ttk.Frame(root)
        self.slider_labels_frame.grid(row=2, column=0, columnspan=3)

        self.slider_label_5 = ttk.Label(self.slider_labels_frame, text="5")
        self.slider_label_5.grid(row=0, column=0, padx=(0, 0))

        self.slider_label_25 = ttk.Label(self.slider_labels_frame, text="25")
        self.slider_label_25.grid(row=0, column=1, padx=(90, 0))

        self.slider_label_50 = ttk.Label(self.slider_labels_frame, text="50")
        self.slider_label_50.grid(row=0, column=2, padx=(90, 0))

        self.slider_label_75 = ttk.Label(self.slider_labels_frame, text="75")
        self.slider_label_75.grid(row=0, column=3, padx=(90, 0))

        self.slider_label_100 = ttk.Label(self.slider_labels_frame, text="100")
        self.slider_label_100.grid(row=0, column=4, padx=(75, 0))

    def slider_changed(self, event):
        value = self.slider.get()
        leverage = self.controller.update_leverage(value)
        self.entry_var.set(str(leverage))

    def entry_changed(self, event):
        value = self.entry_var.get()
        try:
            leverage = self.controller.update_leverage(int(value))
            self.slider.set(leverage)
        except ValueError:
            pass
