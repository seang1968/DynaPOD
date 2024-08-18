# operation_manager.py
from action_handler import ActionHandler  # Import the ActionHandler class

class OperationManager:
    def __init__(self):
        self.action_handler = ActionHandler()  # Initialize the ActionHandler

   
    
    def execute_operation(self, operation_name, params):
        method_name = operation_name.replace(' ', '_').lower()
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            method(**params)  # Call the method with the unpacked dictionary of parameters        
        elif hasattr(self.action_handler, method_name):
            method = getattr(self.action_handler, method_name)
            method(**params)  # Call the method on the ActionHandler with the parameters
        else:
            print(f"Operation '{operation_name}' is not implemented.")

    def open_file(self, file, mode='r'):
        print(f"Opening file '{file}' in mode '{mode}'")

    def save_file(self, file):
        print(f"Saving file '{file}'")

    def change_resolution(self, resolution):
        print(f"Changing resolution to {resolution}")

    def set_default_file_name(self, filename):
        print(f"Setting default file name to {filename}")

#    def perform_dummy_action(self, param1, param2):
#        ah = ActionHandler().dummy_action(param1, param2)
        
