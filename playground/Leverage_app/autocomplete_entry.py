import tkinter as tk
from tkinter import ttk

class AutocompleteEntry(ttk.Entry):
    def __init__(self, suggestions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.suggestions = suggestions
        self.var = self["textvariable"] = tk.StringVar()
        self.var.trace("w", self.update_suggestions)
        self.lb = None

    def update_suggestions(self, *args):
        typed_text = self.var.get().lower()

        # Filter suggestions based on the typed text (case-insensitive)
        matches = [item for item in self.suggestions if typed_text in item.lower()]

        # Limit to top 5 matches
        matches = matches[:5]

        if matches:
            if self.lb:
                self.lb.destroy()
            self.lb = tk.Listbox(self.master, height=len(matches), width=self["width"])
            self.lb.grid(row=self.grid_info()["row"] + 1, column=self.grid_info()["column"], sticky="ew")

            for match in matches:
                self.lb.insert(tk.END, match)

            self.lb.bind("<Button-1>", self.select_suggestion)
        elif self.lb:
            self.lb.destroy()

    def select_suggestion(self, event):
        if self.lb:
            self.var.set(self.lb.get(tk.ACTIVE))
            self.lb.destroy()
