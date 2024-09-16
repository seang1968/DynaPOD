import tkinter as tk
from leverage_model import LeverageModel
from leverage_controller import LeverageController
from leverage_gui import LeverageGUI

if __name__ == "__main__":
    root = tk.Tk()
    leverage_model = LeverageModel()
    leverage_controller = LeverageController(leverage_model)
    gui = LeverageGUI(root, leverage_controller)
    root.mainloop()
