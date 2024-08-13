# operation_manager.py
# This class is responsible for executing operations based on the user's selection.
# It uses method names derived from the operation names defined in the XML file.

class OperationManager:
    def __init__(self):
        pass  # The constructor is empty because no initialization is required

    def execute_operation(self, operation_name, params):
        # This method converts the operation name to a method name by replacing spaces with underscores
        # and converting to lowercase. It then checks if the method exists and calls it with the parameters.
        method_name = operation_name.replace(' ', '_').lower()
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            method(**params)  # Call the method with the unpacked dictionary of parameters
        else:
            print(f"Operation '{operation_name}' is not implemented.")  # Handle cases where the method is not found

    # Example operation methods that could be called based on user selection

    def open_file(self, file, mode='r'):
        print(f"Opening file '{file}' in mode '{mode}'")

    def save_file(self, file):
        print(f"Saving file '{file}'")

    def change_resolution(self, resolution):
        print(f"Changing resolution to {resolution}")

    def set_default_file_name(self, filename):
        print(f"Setting default file name to {filename}")
