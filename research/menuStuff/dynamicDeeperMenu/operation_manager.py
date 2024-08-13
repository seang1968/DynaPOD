#operation_manager.py
class OperationManager:
    def __init__(self):
        pass

    def execute_operation(self, operation_name, params):
        method_name = operation_name.replace(' ', '_').lower()
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            method(**params)
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
