import os
import json
import keyboard  # Import the keyboard library
from menu.menu_parser import MenuParser
from operations.operation_manager import OperationManager

class MenuManager:
    def __init__(self, xml_file):
        self.menu_parser = MenuParser(xml_file)  # Initialize the parser with the XML file
        self.menu_structure = self.menu_parser.get_menu_structure()  # Get the parsed menu structure
        self.operation_manager = OperationManager()  # Initialize the operation manager
        self.exit_to_main_menu = False  # Flag to track if the user wants to exit to the main menu

        # Set up a global keyboard listener for Ctrl+C to exit to the main menu
        keyboard.add_hotkey('ctrl+c', self.trigger_exit_to_main_menu)

    def trigger_exit_to_main_menu(self):
        print("\nKeyboard shortcut detected. Returning to the main menu...")
        self.exit_to_main_menu = True

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self, current_menu=None, level=1, parent_name="Main Menu", parent_help=None):
        current_menu = current_menu or self.menu_structure

        while True:
            # If exit to main menu is triggered, break out of the loop
            if self.exit_to_main_menu:
                self.exit_to_main_menu = False  # Reset the flag
                return "main_menu"  # Return a signal to go back to the main menu

            if level == 1:
                parent_help = "This is the main menu of the application."
            elif parent_help is None:
                parent_help = current_menu.get('help', '')

            self.clear_terminal()
            self.show_menu(parent_name, parent_help, current_menu, level)

            try:
                choice = int(input("Please choose an option: ")) - 1
                if choice == len(current_menu):
                    if level == 1:
                        return  # Exit the main menu loop
                    else:
                        return
                
                selected_item = list(current_menu.keys())[choice]
                submenu = current_menu[selected_item].get('submenu')
                selected_help = current_menu[selected_item].get('help', '')
                
                if submenu:
                    result = self.display_menu(submenu, level + 1, selected_item, selected_help)
                    if result == "main_menu":
                        return "main_menu"  # Return to the main menu
                else:
                    self.execute_action(selected_item, current_menu[selected_item])

            except KeyboardInterrupt:
                print("\nReturning to the main menu...")
                return "main_menu"  # Signal to return to the main menu

            except (IndexError, ValueError):
                print("Invalid choice. Please try again.")

    def show_menu(self, name, help_text, menu, level):
        print(f"{name}")
        if help_text:
            print(f"Help: {help_text}")

        print("\n" + ">" * (level - 1) + f" {name}:")
        item_keys = [key for key in menu.keys() if isinstance(menu[key], dict)]
        for index, menu_item in enumerate(item_keys):
            details = menu[menu_item]
            help_text = details.get('help', '')
            print(f"{index + 1}. {menu_item} - {help_text}")
        print(f"{len(item_keys) + 1}. Back to Previous Menu" if level > 1 else f"{len(item_keys) + 1}. Exit")

    def execute_action(self, operation_name, subitem):
        params = subitem.get('params', {})
        help_text = subitem.get('help')

        if help_text:
            print(f"\nHelp: {help_text}")

        param_values = {}
        for param_name, param_info in params.items():
            value = input(f"Enter {param_name} (default: {param_info['default']}): ") or param_info['default']
            if param_info['type'] == 'int':
                try:
                    value = int(value)
                except ValueError:
                    print(f"Invalid input for {param_name}. Expected an integer. Using default value {param_info['default']}.")
                    value = int(param_info['default'])
            elif param_info['type'] == 'float':
                try:
                    value = float(value)
                except ValueError:
                    print(f"Invalid input for {param_name}. Expected a float. Using default value {param_info['default']}.")
                    value = float(param_info['default'])
            elif param_info['type'] == 'bool':
                value = value.lower() in ['true', '1', 'yes']
            elif param_info['type'] == 'list':
                try:
                    value = json.loads(value)
                    if not isinstance(value, list):
                        raise ValueError
                except ValueError:
                    print(f"Invalid input for {param_name}. Expected a list. Using default value.")
                    value = json.loads(param_info['default'])
            elif param_info['type'] == 'map':
                try:
                    value = json.loads(value)
                    if not isinstance(value, dict):
                        raise ValueError
                except ValueError:
                    print(f"Invalid input for {param_name}. Expected a map. Using default value.")
                    value = json.loads(param_info['default'])
            param_values[param_name] = value

        self.operation_manager.execute_operation(operation_name, param_values)
