# operation_manager.py
# This class is responsible for executing operations based on the user's selection.
# It uses method names derived from the operation names defined in the XML file.
# It also delegates specific actions to the ActionHandler class when appropriate.

from action_handler import ActionHandler  # Import the ActionHandler class

class OperationManager:
    def __init__(self):
        self.action_handler = ActionHandler()  # Initialize the ActionHandler

    def execute_operation(self, operation_name, params):
        # This method converts the operation name to a method name by replacing spaces with underscores
        # and converting to lowercase. It then checks if the method exists in ActionHandler or in itself
        # and calls it with the parameters.
        method_name = operation_name.replace(' ', '_').lower()
        if hasattr(self.action_handler, method_name):
            method = getattr(self.action_handler, method_name)
            method(**params)  # Call the method on the ActionHandler with the parameters
        elif hasattr(self, method_name):
            method = getattr(self, method_name)
            method(**params)  # Call the method in OperationManager with the parameters
        else:
            print(f"Operation '{operation_name}' is not implemented.")  # Handle cases where the method is not found

    # Example operation methods that could be called based on user selection

    def open_file(self, file, mode='r'):
        print(f"Opening file '{file}' in mode '{mode}'")
        # Here you can add the actual logic to open the file

    def save_file(self, file):
        print(f"Saving file '{file}'")
        # Here you can add the actual logic to save the file

    def change_resolution(self, resolution):
        print(f"Changing resolution to {resolution}")
        # Here you can add the actual logic to change the resolution

    def set_default_file_name(self, filename):
        print(f"Setting default file name to {filename}")
        # Here you can add the actual logic to set the default file name
